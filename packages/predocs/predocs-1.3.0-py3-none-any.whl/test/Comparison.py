"""
This module provides function to process a large number of cross sections at once.
For this purpose "comparison sets" are used. A comparison set is a list of profiles which are processed in a similar way.
With the `process_comparison_sets` function, multiple comparison sets can be processed at once.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import concurrent.futures as cf
import os
import subprocess
from typing import Any

import numpy as np
import pandas as pd

from CrossSections import get_wing_cross_section_geometry_definition_dict
from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import WingCrossSectionGeometryDefinition
from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Display import plot_cross_section_element_values
from PreDoCS.CrossSectionAnalysis.Export import generate_BECAS_input
from PreDoCS.CrossSectionAnalysis.Interfaces import IElement
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement, \
    IsotropicElement
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.inout import write_json, read_json, read_cloudpickle, write_cloudpickle
from PreDoCS.util.vector import Vector
from Testing import IsotropicTestCrossSection, SongTestCrossSection, JungTestCrossSection, \
    HybridSongTestCrossSection, HybridJungTestCrossSection, CrossSectionTesting

log = get_module_logger(__name__)


def _create_cross_section_plots(
        cross_section_id: int,
        cross_section: CrossSectionTesting,
        cross_section_data: dict[str, Any],
        plots: dict[str, list[str]],
        full_plots: bool,
        path: str,
        plot_kwargs: dict[str, Any],
) -> None:
    """
    Create all plots for one cross section of a comparison set.

    Parameters
    ----------
    cross_section_id
        The id of the cross section.
    cross_section
        The testing cross section.
    cross_section_data
        The cross section data of the testing cross section.
    plots
        Selection of plots to generate: dict['load_cases'/'displacement_reactions', list[load case names]]
    full_plots
        True of all plots, False for a reduced number of plots.
    path
        The path where to save the plot.
    plot_kwargs
        Additional kwargs for the plot functions.
    """
    if plots is not None and len(plots) > 0:
        log.info('\t\t\tSTART Plot cross section {}'.format(cross_section_id))
        directory = os.path.join(path, str(cross_section_id))
        if not os.path.exists(directory):
            os.makedirs(directory)
        displacement_reactions_to_plot = plots[
            'displacement_reactions'] if 'displacement_reactions' in plots.keys() else []
        load_cases_to_plot = plots['load_cases'] if 'load_cases' in plots.keys() else []
        cross_section.create_cross_section_plots(
            cross_section_data,
            directory,
            displacement_reactions_to_plot=displacement_reactions_to_plot,
            load_cases_to_plot=load_cases_to_plot,
            full_plots=full_plots,
            **plot_kwargs,
        )
        log.info('\t\t\tFINISHED Plot cross section {}'.format(cross_section_id))


def _get_discreet_geometry(
        geometry_definition: WingCrossSectionGeometryDefinition,
        **kwargs,
) -> DiscreetCrossSectionGeometry:
    """
    Returns a `DiscreetCrossSectionGeometry` from a `WingCrossSectionGeometryDefinition`.
    Furthermore, the element stiffness is calculated from the element materials.
    """
    # Arguments
    assert 'element_type' in kwargs
    element_type = kwargs['element_type']
    new_kwargs = kwargs.copy()
    new_kwargs.pop('element_type')

    # Create geometry
    discreet_geometry = geometry_definition.get_discreet_geometry(element_type, **new_kwargs)

    # Calc stiffness
    materials = {s.shell for s in discreet_geometry.components}
    for material in materials:
        material.stiffness = get_stiffness_for_shell(material, **kwargs)

    return discreet_geometry


def _process_cross_section(cross_section_id, **kwargs) -> None:
    """
    Process one cross section of one comparison set.

    Parameters
    ----------
    cross_section_id
        The id of the cross section to process.
    """
    # Arguments
    assert 'output_path' in kwargs.keys()
    output_path = kwargs['output_path']
    assert 'processor_types_dict' in kwargs
    processor_types_dict = kwargs['processor_types_dict']
    assert 'geometry_definition_dict' in kwargs
    geometry_definition_dict = kwargs['geometry_definition_dict']
    geometry_definition = geometry_definition_dict[cross_section_id]
    plot_kwargs = kwargs.get('plot_kwargs', dict())
    cs_plot_kwargs = kwargs.get('cs_plot_kwargs', None)
    shear_center_as_origin = kwargs.get('shear_center_as_origin', False)

    log.info('\tSTART Process cross section {}'.format(cross_section_id))

    if shear_center_as_origin:
        # New origin
        discreet_geometry = _get_discreet_geometry(
            geometry_definition,
            **dict(processor_types_dict['isotropic_song'], **kwargs),
        )
        cross_section = IsotropicTestCrossSection(discreet_geometry)
        data = cross_section.get_cross_section_data()
        new_origin = data['shear_center']
        log.info('\t\tnew_origin: {}, {}'.format(new_origin.x, new_origin.y))

    # Process cross sections
    for processor, processor_dict in processor_types_dict.items():
        log.info('\t\tSTART Process {}'.format(processor))

        discreet_geometry = _get_discreet_geometry(geometry_definition, **dict(processor_dict, **kwargs))
        if shear_center_as_origin:
            for n in discreet_geometry.nodes:
                n.position -= new_origin
            discreet_geometry._update_required = True

        processor_path = os.path.join(output_path, processor)
        if processor == 'becas':
            becas_input_path = os.path.join(processor_path, 'input', str(cross_section_id))
            if not os.path.exists(becas_input_path):
                os.makedirs(becas_input_path)

            # Write BECAS input files
            generate_BECAS_input(
                discreet_geometry, becas_input_path, temp_input_file=os.path.join(becas_input_path, 'temp.inp')
            )

            # Save geometry
            write_cloudpickle(os.path.join(becas_input_path, 'discreet_geometry.p'), discreet_geometry)
        else:
            if not os.path.exists(processor_path):
                os.makedirs(processor_path)
            cross_section = processor_dict['processor_type'](discreet_geometry)

            # Save geometry
            write_cloudpickle(
                os.path.join(processor_path, f'{cross_section_id}_discreet_geometry.p'),
                cross_section.discreet_geometry,
            )

            # Save processor
            write_cloudpickle(os.path.join(processor_path, f'{cross_section_id}_processor.p'),
                                          cross_section)

            data = cross_section.get_cross_section_data()
            persist_data = cross_section.get_cross_section_persist_data(data)
            write_json(os.path.join(processor_path, '{}.json'.format(cross_section_id)), persist_data)

            # Make plots
            if cs_plot_kwargs is not None and cross_section_id in cs_plot_kwargs:
                plot_kwargs_ = cs_plot_kwargs[cross_section_id]
            else:
                plot_kwargs_ = plot_kwargs
            _create_cross_section_plots(
                cross_section_id,
                cross_section,
                data,
                processor_dict['plots'],
                processor_dict['full_plots'],
                processor_path,
                plot_kwargs_,
            )

        log.info('\t\tFINISHED Process {}'.format(processor))

    log.info('\tFINISHED Process cross section {}'.format(cross_section_id))


"""stress_label: (plot_direction_as_arrow, unit, title_format, file_name)"""
_becas_stresses_plot_dict = {
    'stress_zz': (False, '$N/m^2$', r'$\sigma_{{zz}}$ [$N/m^2 = Pa$] through {}', '41-sigma_zz'),
    'stress_zs': (True, '$N/m^2$', r'$\sigma_{{zs}}$ [$N/m^2 = Pa$] through {}', '42-sigma_zs')
}


def _process_cross_sections(
        cross_section_ids: list[int],
        processor_types_dict: dict[str, dict[str, Any]],
        **kwargs,
) -> None:
    """
    Process the cross sections of one comparison set.

    Parameters
    ----------
    cross_section_ids
        The cross section ids to process.
    processor_types_dict
        Settings for the different processors: dict[processor string, settings dict]
            - 'load_cases': bool
                True for creating load case plots.
            - 'plots': dict[str, list[str]]
                Selection of plots to generate: dict['load_cases'/'displacement_reactions', list[load case names]]
            - 'full_plots': bool
                True, if generate all stress plots, False for a reduced number.
            - 'processor_type': ICrossSectionProcessor
                The processor class.
            - 'element_type': IElement
                The element class used by the processor.
            - 'engineering_constants_method': str
                The engineering constants method used in the processor.
                See CLT.Laminate.get_engineering_constants for available options.
    """
    # Arguments
    use_octave = kwargs.get('use_octave', True)
    parallel_processing = kwargs['parallel_processing'] if 'parallel_processing' in kwargs else False
    stride_paraview = kwargs['stride_paraview'] if 'stride_paraview' in kwargs else 5
    assert 'output_path' in kwargs.keys()
    output_path = kwargs['output_path']
    assert 'profiles_path' in kwargs.keys()
    profiles_path = kwargs['profiles_path']
    plot_kwargs = kwargs.get('plot_kwargs', dict())
    cs_plot_kwargs = kwargs.get('cs_plot_kwargs', None)

    log.info('START Cross section creation')

    kwargs['processor_types_dict'] = processor_types_dict
    kwargs['geometry_definition_dict'] = get_wing_cross_section_geometry_definition_dict(profiles_path)

    log.info('FINISHED Cross section creation')

    log.info('START Cross section processing')

    if parallel_processing:
        # Process cross sections parallel
        executor = cf.ThreadPoolExecutor()
        executor.map(lambda cross_section_id: _process_cross_section(cross_section_id, **kwargs), cross_section_ids)
    else:
        for cross_section_id in cross_section_ids:
            _process_cross_section(cross_section_id, **kwargs)

    log.info('FINISHED Cross section processing')

    # Do the BECAS calculation for all profiles
    if 'becas' in processor_types_dict.keys():
        log.info('START run BECAS')

        # Setup
        calc_load_cases = processor_types_dict['becas']['load_cases'] or processor_types_dict['becas']['plots']
        if processor_types_dict['becas']['plots'] and processor_types_dict['becas']['plots']['load_cases']:
            becas_load_cases = processor_types_dict['becas']['plots']['load_cases']
        else:
            becas_load_cases = []
        becas_input_path = os.path.join(output_path, 'becas', 'input')
        becas_output_path = os.path.join(output_path, 'becas', 'output')
        if not os.path.exists(becas_output_path):
            os.makedirs(becas_output_path)

        # Run
        becas_dir = kwargs['becas_dir']
        if use_octave:
            cmd = "diary '{}'; BECAS_calc_profiles({}, {}, '{}', '{}')".format(
                os.path.join(becas_dir, 'BECAS_run.log'),
                str(cross_section_ids),
                'true' if calc_load_cases else 'false',
                becas_input_path + '/', becas_output_path + '/'
            )
            run_args = [
                'octave',
                '--path', becas_dir,
                '--eval', cmd,
                '--no-gui',
            ]
        else:
            cmd = "BECAS_calc_profiles({}, {}, '{}', '{}')".format(
                str(cross_section_ids),
                'true' if calc_load_cases else 'false',
                becas_input_path + '/', becas_output_path + '/'
            )
            run_args = [
                'matlab',
                '-sd', becas_dir,
                '-logfile', os.path.join(becas_dir, 'BECAS_run.log'),
                '-batch', cmd,
                '-wait'
            ]
        log.info('BECAS run_args: ' + str(run_args))
        log.info('BECAS cmd: ' + str(cmd))

        process = subprocess.Popen(run_args)
        if process.wait():
            log.error('ERROR run BECAS')
        else:
            log.info('FINISHED run BECAS')

        # Load element load states and create stress plots
        log.info('START make BECAS stress plots')
        if calc_load_cases:
            for cross_section_id in cross_section_ids:
                log.info(f'cross_section_id: {cross_section_id}')
                # Read BECAS results file
                beacs_results = read_json(os.path.join(becas_output_path, f'{cross_section_id}.json'))

                becas_stresses_dict = {}
                cell_data_df_dict = {}
                rows_dict = None
                for lc_name in becas_load_cases:
                    log.info(f'lc_name: {lc_name}')
                    # Load geometry
                    discreet_geometry = read_cloudpickle(
                        os.path.join(becas_input_path, str(cross_section_id), 'discreet_geometry.p'),
                    )

                    # Element: ID-element mapping
                    id_element_mapping = {e.id: e for e in discreet_geometry.elements}

                    # Load stresses
                    results_path = os.path.join(becas_output_path, str(cross_section_id), 'load_cases', lc_name)
                    becas_case_filename = os.path.join(results_path, 'becas_results.case')
                    becas_stresses_dict[lc_name], cell_data_df_dict[lc_name], rows_dict = _get_becas_stress_distribution(
                        becas_case_filename,
                        discreet_geometry.elements,
                        rows_dict,
                    )

                    # Create stress plots
                    if cs_plot_kwargs is not None and cross_section_id in cs_plot_kwargs:
                        plot_kwargs_ = cs_plot_kwargs[cross_section_id]
                    else:
                        plot_kwargs_ = plot_kwargs
                    for stress_name, (
                            plot_direction_as_arrow, unit, title_format, file_name) in _becas_stresses_plot_dict.items():
                        element_stress_dict = becas_stresses_dict[lc_name][stress_name]
                        results_dict = {id_element_mapping[e_id]: e_value
                                        for e_id, e_value in element_stress_dict.items()}

                        plot_kwargs_.pop('plot_direction_as_arrow', None)
                        plot_kwargs_.pop('values_are_functions', None)
                        plot_kwargs_.pop('scale_unit', None)
                        plot_kwargs_.pop('title', None)
                        plot_kwargs_.pop('file', None)
                        file_format = plot_kwargs_.get('file_format', 'png')
                        plot_title = plot_kwargs_.get('plot_title', None)

                        mass_matrix = np.array(beacs_results['mass_matrix'])
                        cog = Vector([
                            -mass_matrix[2, 4] / mass_matrix[2, 2],
                            mass_matrix[2, 3] / mass_matrix[2, 2]
                        ])
                        plot_cross_section_element_values(
                            discreet_geometry,
                            results_dict,
                            plot_direction_as_arrow=plot_direction_as_arrow,
                            values_are_functions=False,
                            scale_unit=unit,
                            title=title_format.format(lc_name) if plot_title else None,
                            file=os.path.join(results_path, '{}.{}'.format(file_name, file_format)),
                            cog=cog,
                            **plot_kwargs_,
                        )

                # Update BECAS results
                beacs_results['load_cases'] = {k: {
                    'element_load_states': becas_stresses_dict[k],
                    'cell_data_df': cell_data_df_dict[k].to_json(),
                } for k in becas_stresses_dict.keys()}

                # Write BECAS results file
                write_json(os.path.join(becas_output_path, f'{cross_section_id}.json'), beacs_results)

        log.info('FINISHED make BECAS stress plots')

        # Generate the PARAVIEW output
        if processor_types_dict['becas']['plots'] is not None:
            log.info('START make BECAS plots')

            # Setup
            becas_results_case_format_string = os.path.join(
                becas_output_path, '{0}', 'load_cases', '{1}', 'becas_results.case'
            )
            output_format_string = os.path.join(becas_output_path, '{0}', 'load_cases', '{1}', '{2}.png')
            args = ['pvpython',
                    os.path.join(becas_dir, 'make_plots.py'),
                    '-r', becas_results_case_format_string,
                    '-o', output_format_string]
            if processor_types_dict['becas']['full_plots']:
                args.append('-f')
            args += ['-g 0.02',
                     '-b -0.2',
                     '-l'] + ['{}'.format(l) for l in becas_load_cases] + \
                    ['-c'] + ['{}'.format(p) for p in cross_section_ids] + \
                    ['-s'] + ['{}'.format(stride_paraview) for p in cross_section_ids]

            # Run
            with open(os.path.join(becas_dir, 'PARAVIEW_make_plots.log'), 'w+') as log_file:
                process = subprocess.Popen(args, stdout=log_file, stderr=log_file)
                if process.wait():
                    log.error('ERROR make BECAS plots')
                else:
                    log.info('FINISHED make BECAS plots')


def process_comparison_sets(comparison_dict: dict[int, dict[str, Any]], **kwargs) -> None:
    """
    Process all comparison set given in `comparison_dict`.

    Parameters
    ----------
    comparison_dict
        Settings for the different comparison sets:
            - 'processors': list[str]
                List of all cross section processors to use. Options:
                    - 'becas': BECAS calculation.
                    - 'isotropic_no_stress': IsotropicTestCrossSection with engineering_constants_method = 'with_poisson_effect'
                    - 'isotropic_song': IsotropicTestCrossSection with engineering_constants_method = 'song'
                    - 'hybrid_song': HybridSongTestCrossSection with main processor SongTestCrossSection
                    - 'hybrid_jung': HybridJungTestCrossSection with main processor JungTestCrossSection
                    - 'song': SongTestCrossSection
                    - 'jung': JungTestCrossSection
            - 'profiles': list[int]
                List of all profile ids.
            - 'load_cases': bool
                True for creating load case plots.
            - 'plots': dict[str, list[str]]
                Selection of plots to generate: dict['load_cases'/'displacement_reactions', list[load case names]]
            - 'full_plots': bool
                True, if generate all stress plots, False for a reduced number.
    """
    processor_types = {
        'isotropic_no_stress': IsotropicTestCrossSection,
        'isotropic_song': IsotropicTestCrossSection,
        'hybrid_song': HybridSongTestCrossSection,
        'hybrid_jung': HybridJungTestCrossSection,
        'song': SongTestCrossSection,
        'jung': JungTestCrossSection,
    }
    element_types = {
        'isotropic_no_stress': IsotropicElement,
        'isotropic_song': IsotropicElement,
        'hybrid_song': CompositeElement,
        'hybrid_jung': CompositeElement,
        'song': CompositeElement,
        'jung': CompositeElement,
        'becas': CompositeElement,
    }
    engineering_constants_methods = {
        'isotropic_no_stress': 'with_poisson_effect',
        'isotropic_song': 'song',
    }
    for comparison_set, comparison_props in comparison_dict.items():
        # Setup
        processor_types_dict = {}
        for p in comparison_props['processors']:
            processor_dict = {
                'load_cases': comparison_props['load_cases'],
                'plots': comparison_props['plots'],
                'full_plots': comparison_props['full_plots'],
            }
            if p in processor_types:
                processor_dict['processor_type'] = processor_types[p]
            if p in element_types:
                processor_dict['element_type'] = element_types[p]
            if p in engineering_constants_methods:
                processor_dict['engineering_constants_method'] = engineering_constants_methods[p]
            processor_types_dict[p] = processor_dict

        # Process cross sections
        _process_cross_sections(comparison_props['profiles'], processor_types_dict, **kwargs)


def _find_closest_element(position: Vector, elements_list: list[IElement], max_dist: float = 1e-2) -> IElement:
    """Returns the element with the shortest distance to the given position."""
    elements_list = np.array(elements_list)
    dist = np.array([(element.position - position).length for element in elements_list])
    min_dist = np.min(dist)
    assert min_dist <= max_dist
    selected_elements = elements_list[dist == min_dist]
    assert len(selected_elements) == 1
    return selected_elements[0]


def _get_becas_stress_distribution(
        becas_case_filename: str,
        ref_elements: list[IElement],
        rows_dict: dict = None,
) -> (dict[str, dict[str, float]], pd.DataFrame, dict):
    """
    Reads the BECAS stress distribution from the EnSight Gold output files.

    Parameters
    ----------
    becas_case_filename
        The BECAS case file to read.
    ref_elements
        List of the PreDoCS cross section elements for the mapping.

    Returns
    -------
    dict[stress label, dict[element id, value]]
    """
    from paraview.simple import EnSightReader, servermanager
    from BECAS.paraview_utils import apply_tensor_calculation_filter

    # Read data
    log.info('START read BECAS results')
    log.info(f'becas_case_filename: {becas_case_filename}')
    resultscase = EnSightReader(
        CaseFileName=becas_case_filename,
        CellArrays=[
            'material_id', 'material_ori_1', 'material_ori_2', 'material_ori_3',
            'elementnumbers', 'strain11', 'strain22', 'strain12', 'strain13',
            'strain23', 'strain33', 'stress11', 'stress22', 'stress12', 'stress13',
            'stress23', 'stress33', 'failure11', 'failure22', 'failure12', 'failure13',
            'failure23', 'failure33'
        ],
        PointArrays=['nodenumbers', 'elastic_axis_1', 'elastic_axis_2', 'warping']
    )
    if not resultscase:
        raise RuntimeError('Error while loading files')
    log.info('read BECAS results from file finished')

    # Tensor calculation
    input_filter = apply_tensor_calculation_filter(resultscase, 1)
    log.info('tensor calculation finished')

    # Fetch element data
    becas_data = servermanager.Fetch(input_filter)
    block = becas_data.GetBlock(0)
    number_of_cells = becas_data.GetNumberOfCells()
    cell_data = block.GetCellData()

    # Get cell data arrays
    cell_data_keys = ['stress_zz', 'stress_zs']
    cell_data_dict = {k: cell_data.GetArray(k) for k in cell_data_keys + ['elementnumbers']}

    log.info('get cell data finished')

    # Create cell values data frame
    cell_data_list = []
    for i_cell in range(number_of_cells):
        cell = block.GetCell(i_cell)
        points = cell.GetPoints()
        num_points = points.GetNumberOfPoints()
        #log.debug([points.GetPoint(i_point) for i_point in range(num_points)])
        position = np.mean([points.GetPoint(i_point) for i_point in range(num_points)], axis=0)
        cell_data = {
            k: (-1 if k == 'stress_zs' else 1) * v.GetValue(i_cell)  # TODO: workaround, take element direction into account
            for k, v in cell_data_dict.items()
        }
        cell_data['position'] = Vector(position)
        cell_data['thickness'] = Vector(points.GetPoint(2)).dist(Vector(points.GetPoint(1)))
        cell_data_list.append(cell_data)
    cell_data_df = pd.DataFrame(cell_data_list)
    log.info('cell data df finished')

    # Find BECAS-PreDoCS cell-element mapping
    if rows_dict is None:
        rows_dict = {}
        for i, row in cell_data_df.iterrows():
            ref_element = _find_closest_element(row.position[0:2], ref_elements)
            becas_element_id = row['elementnumbers']
            if ref_element in rows_dict:
                rows_dict[ref_element].append(becas_element_id)
            else:
                rows_dict[ref_element] = [becas_element_id]
        assert len(cell_data_df) == np.sum([len(rows) for rows in rows_dict.values()])
        log.info('BECAS-PreDoCS-mapping finished')

    # Calculate mean stresses
    mean_stresses_dict = {k: {} for k in cell_data_keys}
    for ref_element, becas_element_ids in rows_dict.items():
        rows = cell_data_df[cell_data_df['elementnumbers'].isin(becas_element_ids)]
        for stress_label in cell_data_keys:
            mean_stresses_dict[stress_label][ref_element.id] = np.sum(rows.loc[:, stress_label] * rows.loc[:, 'thickness']) / ref_element.thickness  # Ply stress * ply thickness / laminate thickness
    log.info('calc mean stresses finished')

    log.info('FINISHED read BECAS results')
    return mean_stresses_dict, cell_data_df, rows_dict
