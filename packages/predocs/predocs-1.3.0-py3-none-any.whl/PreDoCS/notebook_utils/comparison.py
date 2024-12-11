"""
This module contains helping function for the comparison of the different cross section processors.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""

#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import csv
import math
import os

import cloudpickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from PreDoCS.CrossSectionAnalysis.Display import savefig_args
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.data import interp1d
from PreDoCS.util.inout import read_json

log = get_module_logger(__name__)


## Funktionen

def read_input_files(profiles, processor_dirs):
    ## Read the output data files of the tools.
    data_dicts = {}
    for processor, processor_dir in processor_dirs.items():
        print(processor)
        d = {}
        for profile in profiles:
            print(profile)
            d[profile] = read_json(os.path.join(processor_dir, '{}.json'.format(profile)))
            if processor == 'becas':
                with open(os.path.join(processor_dir, '..', 'input', str(profile), 'discreet_geometry.p'), 'rb') as file:
                    d[profile]['discreet_geometry'] = cloudpickle.load(file)
            else:
                with open(os.path.join(processor_dir, '{}_processor.p'.format(profile)), 'rb') as file:
                    d[profile]['cs_processor'] = cloudpickle.load(file)
        data_dicts[processor] = d#{ profile: json.load(open('{}{}.json'.format(processor_dir, profile))) for profile in profiles }
    return data_dicts

def get_stiffness_matrices(profile, data_dicts, tol=10.0):
    ## Returns the stiffness matrices from the output data of the tools.
    stiffness_matrices_dict = {}
    for k, d in data_dicts.items():
        stiffness = np.array(d[profile]['stiffness_matrix'])
        stiffness[abs(stiffness) < tol] = 0.0
        stiffness_matrices_dict[k] = stiffness
    return stiffness_matrices_dict

def get_mass_dicts(profile, data_dicts, tol=10.0):
    ## Returns the mass_matrix matrices from the output data of the tools.
    mass_dicts_dict = {}
    for k, d in data_dicts.items():
        mass_matrix = np.array(d[profile]['mass_matrix'])
        mass_matrix[abs(mass_matrix) < tol] = 0.0
        mass_matrix = matrix_to_dict(mass_matrix)
        mass_dicts_dict[k] = mass_matrix
    return mass_dicts_dict

def get_stiffness_dicts(profile, data_dicts, tol=10.0):
    ## Returns the stiffness matrices from the output data of the tools.
    stiffness_dicts_dict = {}
    for k, d in data_dicts.items():
        stiffness = np.array(d[profile]['stiffness_matrix'])
        stiffness[abs(stiffness) < tol] = 0.0
        stiffness = matrix_to_dict(stiffness)
        if 'GI_t' in d[profile].keys():
            stiffness[44] = d[profile]['GI_t']
        stiffness_dicts_dict[k] = stiffness
    return stiffness_dicts_dict

def create_3D_stifness_dicts(profiles, data_dicts, tol=10.0):
    ## Returns the 3D-arrays of the stiffness arrays. The third dimension is the profile index.
    stiffness_dicts_3d_dict = {}
    for profile in profiles:
        stiffness_dicts_dict = get_stiffness_dicts(profile, data_dicts, tol)
        for processor in data_dicts.keys():
            if processor not in stiffness_dicts_3d_dict.keys():
                stiffness_dicts_3d_dict[processor] = {}
            stiffness_dicts_3d_dict[processor][profile] = stiffness_dicts_dict[processor]
    return stiffness_dicts_3d_dict

def matrix_to_dict(m):
    ## Converts a symmetric matrix to a dict.
    shape = m.shape
    assert shape[0] == shape[1]
    size = shape[0]
    d = {}
    for r in range(size):
        for c in range(r, size):
            d[(r+1)*10+c+1] = m[r, c]
    return d

def matrix_string(m):
    ## Converts a matrix to a string.
    s = ''
    for row in range(m.shape[0]):
        for col in range(m.shape[1]):
            val = m[row, col]
            if np.isnan(val):
                val = 0
            s += '{:5e}\t'.format(val)
        s += '\n'
    return s

# def zero_range_siffness_dicts(stiffness_dicts, zero_range=1):
#     ## Returns the stiffness dict with all values set to zero that are around zero in a range of zero_range.
#     for p in stiffness_dicts.keys():
#         for k, v in stiffness_dicts[p].items():
#             if abs(v) < zero_range:
#                 stiffness_dicts[p][k] = 0
#     return stiffness_dicts
    
def zero_range(value, zero_range=1e-3):
    ## Returns the value, if it is not around zero in a range of zero_range.
    if abs(value) < zero_range:
        return 0
    else:
        return value

def compare_data(data, true_value='first_value', reference_value=None, multiples=None):
    ## Returns a list of compared data.
    if true_value == 'none':
        res = [None]
    else:
        res = [data[0]]
    
    if true_value == 'first_value' or true_value == 'first_value_other_reference':
        for i in range(1, len(data)):
            res += [data[i], difference(data[i], data[0], reference_value=reference_value
                                        if true_value == 'first_value_other_reference'
                                        else None, multiples=multiples)]
    elif true_value == 'no_comparison':
        for i in range(1, len(data)):
            res += [data[i], None]
    elif true_value == 'none':
        for i in range(len(data)):
            res += [data[i], None]
    return res


def difference(value, true_value, reference_value=None, multiples=None):
    ## Calcs the relative error of value to true_value.
    if value is None or true_value is None:
        return None
    else:
        if multiples is not None:
            value = value % multiples
            true_value = multiples % multiples
        if reference_value is None:
            reference_value = true_value
        
        if value == true_value:
            return 0
        elif true_value == 0 and reference_value is None:
            return np.inf
        elif reference_value == 0:
            return np.inf
        else:
            return (value-true_value)/reference_value*100


def comapre_matrix_coefficients(dicts, processors, indices, index_offsets, matrix_prefix):
    ## Returns a list of table rows where the stiffness coefficients are compared.
    rows = []
    for r, c in indices:
        indices = {processor: r*10 + c + 11 + (index_offsets[processor] if index_offsets is not None else 0)
                   for processor in processors}
        rows.append(['${}_{{{}{}}}$'.format(matrix_prefix, r+1, c+1)] +\
                    compare_data([dicts[processor][indices[processor]] if (indices[processor] in dicts[processor].keys()) else None
                                  for processor in processors]
                                )
                   )
    return rows


def comapre_coupling_coefficients(stiffness_dicts, processors, stiffness_indices, index_offsets):
    ## Returns a list of table rows where the coupling coefficients are compared.
    rows = []
    for r, c in stiffness_indices:
        indices_couplig = {processor: r*10 + c + 11 + (index_offsets[processor] if processor in index_offsets.keys() else 0)
                           for processor in processors}
        indices1 = {processor: (r+1)*11 + (index_offsets[processor] if processor in index_offsets.keys() else 0)
                   for processor in processors}
        indices2 = {processor: (c+1)*11 + (index_offsets[processor] if processor in index_offsets.keys() else 0)
                   for processor in processors}
        rows.append(['$\eta_{{{}{}}}$'.format(r+1, c+1)] +\
                    compare_data([stiffness_dicts[processor][indices_couplig[processor]] /
                                  np.sqrt(stiffness_dicts[processor][indices1[processor]] * stiffness_dicts[processor][indices2[processor]])
                                  if (indices_couplig[processor] in stiffness_dicts[processor].keys()) else None
                                  for processor in processors]))
    return rows


def comapre_shear_correction_factors(stiffness_dicts, processors, index_offsets):
    ## Returns a list of table rows of the shear correction factors.
    rows = []
    true_processor = processors[0]
    other_processor = processors[1:]

    indices = {processor: (11 + index_offsets[processor]) if processor in index_offsets.keys() else 11
               for processor in other_processor}
    true_stiffness = stiffness_dicts[true_processor][11]
    rows.append(['K_x'] + \
                compare_data([true_stiffness / stiffness_dicts[processor][indices[processor]]
                              if (indices[processor] in stiffness_dicts[processor].keys()) else None
                              for processor in other_processor],
                             true_value='none')
                )

    indices = {processor: (22 + index_offsets[processor]) if processor in index_offsets.keys() else 22
               for processor in other_processor}
    true_stiffness = stiffness_dicts[true_processor][22]
    rows.append(['K_y'] + \
                compare_data([true_stiffness / stiffness_dicts[processor][indices[processor]]
                              if (indices[processor] in stiffness_dicts[processor].keys()) else None
                              for processor in other_processor],
                             true_value='none')
                )

    return rows


def value_string(value, number_format):
    ## Returns a string for a given value. '-' for None.
    if value is None:
        return '-'
    elif value == np.inf:
        return '?'
    else:
        return ('\\num{{{'+number_format+'}}}').format(value)


def create_comaparison_tables(profiles, processors, data_dicts, index_offsets, profile_size, hlines=True):
    ## Creates a table, where the calculations of the different processors are compared.
    hline = '\\addlinespace\n'
    table_dict = {}
    main_mass_indices = []
    coupling_mass_indices = []
    main_stiffness_indices = []
    coupling_stiffness_indices = []
    for i in range(6):
        main_mass_indices.append((i, i))
    for i in range(7):
        main_stiffness_indices.append((i, i))
    for r in range(6):
        for c in range(r + 1, 6):
            coupling_mass_indices.append((r, c))
    for r in range(7):
        for c in range(r + 1, 7):
            coupling_stiffness_indices.append((r, c))
    for profile in profiles:
        rows = []

        # EC
        rows += [['elastic_center_x'] + \
                 compare_data([zero_range(data_dicts[processor][profile]['elastic_center'][0])
                               for processor in processors],
                              true_value='first_value_other_reference',
                              reference_value=profile_size)
                 ]
        rows += [['elastic_center_y'] + \
                 compare_data([zero_range(data_dicts[processor][profile]['elastic_center'][1])
                               for processor in processors],
                              true_value='first_value_other_reference',
                              reference_value=profile_size)
                 ]
        if hlines:
            rows.append(hline)

        # SC
        rows += [['shear_center_x'] + \
                 compare_data([zero_range(data_dicts[processor][profile]['shear_center'][0])
                               for processor in processors],
                              true_value='first_value_other_reference',
                              reference_value=profile_size)
                 ]
        rows += [['shear_center_y'] + \
                 compare_data([zero_range(data_dicts[processor][profile]['shear_center'][1])
                               for processor in processors],
                              true_value='first_value_other_reference',
                              reference_value=profile_size)
                 ]

        if hlines:
            rows.append(hline)

        # PAA
        rows += [['principal_axis_angle'] + \
                 compare_data([zero_range(np.rad2deg(data_dicts[processor][profile]['principal_axis_angle']), 1e-1)
                               for processor in processors],
                              true_value='no_comparison')
                 ]
        if hlines:
            rows.append(hline)

        mass_dicts = get_mass_dicts(profile, data_dicts, 1e-3)

        stiffness_dicts = get_stiffness_dicts(profile, data_dicts, 1e1)

        # Shear correction factors
        rows += comapre_shear_correction_factors(stiffness_dicts, processors, index_offsets)

        if hlines:
            rows.append(hline)

        # Mass matrix
        rows += comapre_matrix_coefficients(mass_dicts, processors, main_mass_indices, None, 'I')
        if hlines:
            rows.append(hline)

        rows += comapre_matrix_coefficients(mass_dicts, processors, coupling_mass_indices, None, 'I')
        if hlines:
            rows.append(hline)

        # Stiffness matrix
        rows += comapre_matrix_coefficients(stiffness_dicts, processors, main_stiffness_indices, index_offsets, 'S')
        if hlines:
            rows.append(hline)

        rows += comapre_matrix_coefficients(stiffness_dicts, processors, coupling_stiffness_indices, index_offsets, 'S')
        if hlines:
            rows.append(hline)

        # Coupling coefficients
        rows += comapre_coupling_coefficients(stiffness_dicts, processors, coupling_stiffness_indices, index_offsets)

        table_dict[profile] = rows
    return table_dict


def plot_value_over_profiles(profiles_x_labels, stiffness_dicts, processors, indizes, index_offsets, x_label,
                             y_label_format_string, file_format_string=None, polar_plot=False, xlog=False, line_format='-o',
                             legend_strings=None, legend_location='center left', legend_bbox_to_anchor=(1.1, 0.5),
                             figsize=(15,10), plot_title=True, **kwargs):
    ## Plots a matrix element over the number of profiles.
    for index in indizes:
        plt.figure(figsize=figsize)
        ax = plt.subplot(111, polar=polar_plot)
        if plot_title:
            ax.set_title('{} über {}'.format(y_label_format_string.format(index), x_label))
        for processor in processors:
            profiles = sorted(profiles_x_labels.keys())
            value_index = index + index_offsets[processor] if processor in index_offsets.keys() else index
            y = [(stiffness_dicts[processor][profile][value_index]
                  if value_index in stiffness_dicts[processor][profile]
                  else None)
                 for profile in profiles]
            ax.plot([profiles_x_labels[profile] for profile in profiles], y, line_format)
        if not polar_plot:
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label_format_string.format(index))
        if xlog:
            ax.set_xscale('log')
        ax.grid()
        lgd = None
        if legend_strings is not None:
            lgd = ax.legend(legend_strings, loc=legend_location, bbox_to_anchor=legend_bbox_to_anchor)
        if file_format_string is None:
            plt.show()
        else:
            plt.savefig(file_format_string.format(index), bbox_extra_artists=(lgd,), **{k: v for k, v in kwargs.items() if k in savefig_args})
            plt.close()

def save_value_over_profiles(profiles_x_labels, stiffness_dicts, processors, indizes, index_offsets, first_column_label,
                             column_label_format_string, file_format_string=None):
    ## Plots a matrix element over the number of profiles.
    cols = [[first_column_label] + list(profiles_x_labels.values())]
    for index in indizes:
        for processor in processors:
            value_index = index + index_offsets[processor] if processor in index_offsets.keys() else index
            y = [stiffness_dicts[processor][profile][value_index] for profile in profiles_x_labels.keys()]
            cols.append([column_label_format_string.format(index, processor)] + y)
        with open(file_format_string.format(index), 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"')
            for i in range(len(profiles_x_labels.keys())):
                writer.writerow([c[i] for c in cols])
# def plot_quotient_over_profiles(profiles_x_labels, dividend, divisor, indizes, title, x_label, y_label_format_string, file_format_string=None):
#     ## Plots a matrix element over the number of profiles.
#     assert len(dividend) == len(divisor)
#     for index in indizes:
#         plt.figure()
#         plt.title(title)
#         value_index = index
#         y = [dividend[profile][value_index] / divisor[profile][value_index] for profile in profiles_x_labels.keys()]
#         plt.plot(profiles_x_labels.values(), y, '-o')
#         plt.xlabel(x_label)
#         plt.ylabel(y_label_format_string.format(index))
#         if file_format_string is None:
#             plt.show()
#         else:
#             plt.savefig(file_format_string.format(index))
#             plt.close()


def make_performance_plot(calculation_time_dict, title=None, file=None, figsize=(15,10),
                          y_label='computation time [s]', logy=True, processor_labels=None, **kwargs):
    ## Creates a boxplot for the prerfomance comparison
    plt.figure(figsize=figsize)
    ax = plt.subplot(111)
    if title:
        ax.set_title(title)
    #ax.set_xlabel('Berechnungsmethode')
    ax.set_ylabel(y_label)
    if logy:
        ax.set_yscale('log')
    if processor_labels:
        labels = [processor_labels[k] for k in calculation_time_dict.keys()]
    else:
        labels = calculation_time_dict.keys()
    ax.boxplot(list(calculation_time_dict.values()), labels=labels)
    ax.grid(axis='y')
    if file is None:
        plt.show()
    else:
        plt.savefig(file, **{k: v for k, v in kwargs.items() if k in savefig_args})#, bbox_inches='tight'
        plt.close()


def images_vstack(images_list, mode='RGB'):
    ## Vertical stack of images.
    max_width = max([ i.size[0] for i in images_list])
    i_stack = []
    for img in images_list:
        img = img.convert(mode)
        new_size = (max_width, int(img.size[1]*max_width/img.size[0]))
        res = img.resize(new_size, Image.BILINEAR)
        i_stack.append(np.asarray(res))
    return Image.fromarray(np.vstack(i_stack))

def images_hstack(images_list, mode='RGB'):
    ## Horizontal stack of images.
    max_height = max([ i.size[1] for i in images_list])
    i_stack = []
    for img in images_list:
        img = img.convert(mode)
        new_size = (int(img.size[0]*max_height/img.size[1]), max_height)
        res = img.resize(new_size, Image.BILINEAR)
        i_stack.append(np.asarray(res))
    return Image.fromarray(np.hstack(i_stack))

def images_grid_stack(images_list, mode='RGB', tile_size=(1000,750)):
    ## Horizontal stack of images.
    num_imgs = len(images_list)
    cols = math.ceil(math.sqrt(num_imgs))
    rows = math.ceil(num_imgs / cols)
    #tile_size = images_list[0].size
    tile_aspect_ratio = tile_size[0]/tile_size[1]
    result = Image.new("RGB", (tile_size[0]*cols, tile_size[1]*rows), "white")
    for i in range(num_imgs):
        row = i // cols
        col = i % cols
        img = images_list[i]
        img = img.convert(mode)
        aspect_ratio = img.size[0]/img.size[1]
        if aspect_ratio < tile_aspect_ratio:
            # Width critical
            new_size = (int(img.size[0]*tile_size[1]/img.size[1]), tile_size[1])
        else:
            # Height critical
            new_size = (tile_size[0], int(img.size[1]*tile_size[0]/img.size[0]))
        new_img = img.resize(new_size, Image.BILINEAR)
        result.paste(new_img, (tile_size[0]*col, tile_size[1]*row))
    return result


def make_comparison_plots(processors, profiles, load_cases, load_states, processor_dirs,
                          load_states_file_names, plots_path, stack_method='grid'):
    ## Fügt die Kraft- unf Momentenflussverläufe der einzelnen Methoden zusammen in ein Bild.
    for profile in profiles:
        for lc in load_cases:
            for ls in load_states:
                images = []
                for processor in processors:
                    plot_file = os.path.join(processor_dirs[processor], str(profile), 'load_cases', lc, load_states_file_names[ls][processor])
                    images.append(Image.open(plot_file))
                output_path = os.path.join(plots_path, str(profile))
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                output_file = os.path.join(output_path, '{}_{}.png'.format(lc, ls))
                if stack_method == 'vertical':
                    images_vstack(images).save(output_file)
                elif stack_method == 'horizontal':
                    images_vstack(images).save(output_file)
                elif stack_method == 'grid':
                    images_grid_stack(images).save(output_file)


def save_stiffness_matrices(file, profiles, processors, data_dicts):
    ## Steifigkeitsmatrizen speichern.
    with open(file, 'w', encoding='utf-8') as f:
        for profile in profiles:
            f.write('Profil {}\n'.format(profile))
            stiffness_matrices_dict = get_stiffness_matrices(profile, data_dicts, tol=10.0)
            for processor in processors:
                f.write('\n{}:\n'.format(processor))
                f.write(matrix_string(stiffness_matrices_dict[processor]))

            # f.write('\nPreDoCS Composite Abweichung [%]:\n')
            # diff_comp = (predocs_comp_stiffness_6-becas_stiffness)/becas_stiffness*100
            # f.write(matrix_string(diff_comp))

            # f.write('\nPreDoCS Isotrop Abweichung [%]:\n')
            # diff_iso = (predocs_iso_stiffness-becas_stiffness_3)/becas_stiffness_3*100
            # f.write(matrix_string(diff_iso))
            f.write('\n\n')


def get_comparison_tables(profiles, processors, table_dict):
    ## LATEX Tabellen erstellen, in denen die Größen direkt verglichen werden.
    labels = {'elastic_center_x': (r'$x_{ESP}$ [\si{\meter}]', ':.3f', ':.2f'),
              'elastic_center_y': (r'$y_{ESP}$ [\si{\meter}]', ':.3f', ':.2f'),
              'shear_center_x': (r'$x_{SMP}$ [\si{\meter}]', ':.3f', ':.2f'),
              'shear_center_y': (r'$y_{SMP}$ [\si{\meter}]', ':.3f', ':.2f'),
              'principal_axis_angle': (r'HAW [\si{\degree}]', ':.1f', ':.2f'),
              'K_x': (r'$K_x$ [-]', ':.3f', '-'),
              'K_y': (r'$K_y$ [-]', ':.3f', '-')}
    none_set = {0.0, None}
    # num_processors = len(data_dicts.keys())
    processors_to_compare = processors[1:]
    first_processor = processors[0]
    first_col_width = 0.09
    col_width1 = 0.11  # (0.8-first_col_width)/(1+2*len(processors_to_compare))
    col_width2 = 0.1
    tables = {}
    for profile in profiles:
        # Head rule
        # profile_id = profile % 100
        profile_string = '{0:03d}'.format(profile)
        # profile_id_string = '{0:02d}'.format(profile_id)
        s1 = '\\begin{table}[ht]\n\\scriptsize\n\\centering\n\\caption{Testfall ' + profile_string + '}\n'  # \\label{tab:profil-'+profile_string+'}\n'
        s2 = '\\begin{tabular}{p{' + str(first_col_width) + '\\textwidth}p{' + str(col_width1) + '\\textwidth}'
        s3 = ' & \\parbox{' + str(col_width1) + '\\textwidth}{\\textbf{' + first_processor + '}}'
        s4 = '& '
        for p in processors_to_compare:
            s2 += 'p{' + str(col_width1) + '\\textwidth}p{' + str(col_width2) + '\\textwidth}'
            s3 += ' & \\multicolumn{2}{l}{\\parbox{' + str(
                col_width1 + col_width2) + '\\textwidth}{\\textbf{' + p + '}}}'
            s4 += ' & Wert & Abw. [\\si{\\percent}]'
        s3 += ' \\\\ '
        for i in range(len(processors_to_compare)):
            s3 += '\\cmidrule(lr){{{}-{}}} '.format(i * 2 + 3, i * 2 + 4)
        s2 += '}\n\\toprule\n'
        s3 += '\n'
        s4 += ' \\\\ \\midrule\n'
        table = s1 + s2 + s3 + s4

        # Write rows
        for row in table_dict[profile]:
            if isinstance(row, list):
                # Get labels and number formats
                row_label = row[0]
                if row_label in labels.keys():
                    label = labels[row_label][0]
                    value_format = labels[row_label][1]
                    diff_format = labels[row_label][2]
                    if len(labels[row_label]) > 3:
                        true_value = labels[row_label][3]
                    else:
                        true_value = row[1]
                else:
                    label = row_label
                    value_format = ':.3E'
                    diff_format = ':.2f'
                    true_value = row[1]

                # Check if diffferent values exists
                different_values = set(row[1:-1]) - none_set
                if len(different_values) > 0 or row_label in labels.keys():

                    # If different values exists or row has label data write row
                    row_string = '{} & {}'.format(label, value_string(true_value, value_format))
                    for i in range(len(processors_to_compare)):
                        row_string += ' & {} & {}'.format(value_string(row[i * 2 + 2], value_format),
                                                          value_string(row[i * 2 + 3], diff_format))
                    row_string += ' \\\\\n'
                    table += row_string
            else:
                table += row

        # Bottom rule
        table += '\\bottomrule\n\\end{tabular}\n\\end{table}\n\n'
        tables[profile] = table
    return tables


def plot_rel_error(ax, x_ref, y_ref, x, y, span_label='span [$m$]', y_label='rel. error [%]', interpolation_method='linear'):
    ref = interp1d(x_ref,
                   y_ref,
                   kind=interpolation_method)
    val = interp1d(x,
                   y,
                   kind=interpolation_method)

    x_plot = x
    ax.plot(x_plot, (val(x_plot) - ref(x_plot)) / ref(x_plot) * 100, '-x')
    ax.set_xlabel(span_label)
    ax.set_ylabel(y_label)
