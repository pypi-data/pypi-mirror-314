"""
For further details, see notebook 'docs/Validation/1D FEM/index'.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import math
import os
import subprocess

import numpy as np
import pandas as pd
import pytest

from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import WingCrossSectionGeometryDefinition, \
    load_profile_points
from PreDoCS.CrossSectionAnalysis.Display import plot_discreet_geometry
from PreDoCS.CrossSectionAnalysis.Processors import HybridCrossSectionProcessor
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement
from PreDoCS.MaterialAnalysis.Materials import Orthotropic
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell, CompositeShell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.vector import Vector
from PreDoCS.WingAnalysis.Display import plot_beam_displacements, plot_beam_internal_loads, \
    plot_beam_cross_section_displacements

log = get_module_logger(__name__)

try:
    from PreDoCS.WingAnalysis.BeamFEM import Beam, BeamElement3NodeWithWarping, get_element_type_from_str
except ImportError:
    log.warning('cpacs_interface not installed')


pytestmark = pytest.mark.cpacs_interface_required


def get_cross_section_data(cs_definitions, hybrid_processors, plot_cs=False):
    cs_data = []
    for cs_definition, hybrid_processor in zip(cs_definitions, hybrid_processors):
        # Create discreet cross section geometry
        discreet_geometry = cs_definition.get_discreet_geometry(CompositeElement, element_length=0.1)
        if plot_cs:
            plot_discreet_geometry(discreet_geometry)

        # Calc material stiffness for cross section processing
        materials = {s.shell for s in discreet_geometry.components}
        for material in materials:
            material.stiffness = get_stiffness_for_shell(material, CompositeElement)

        # Create cross section processor and do the calculation
        cs_processor = HybridCrossSectionProcessor(hybrid_processor=hybrid_processor)
        cs_processor.discreet_geometry = discreet_geometry
        cs_data.append((cs_processor.stiffness.stiffness_matrix, cs_processor.inertia.inertia_matrix))
    return cs_data


def write_ansys_stiffness_input(cs_data, file_format_string='stiffness_{}.inp'):
    # Write stiffness matrices to file for the import in ANSYS
    # Due to ofther coordinate sytems of ANSYS and PreDoCS, a permutation of rows and columns with the matrix V must performed
    V = np.zeros((6, 6))
    new_indices = [2, 3, 4, 5, 1, 0]
    for i in range(len(new_indices)):
        V[i, new_indices[i]] = 1

    for i in range(len(cs_data)):
        stiffness = V @ cs_data[i][0][0:6, 0:6] @ V.T
        rows = stiffness.shape[0]
        cols = stiffness.shape[1]
        with open(file_format_string.format(i + 1), 'w') as f:
            for row in range(rows):
                s = ''
                for col in range(row, cols):
                    s += '{: 1.15e}, '.format(stiffness[row, col])
                f.write('cbmx,{}, {}\n'.format(row + 1, s))


def write_ansys_inertia_input(cs_data, file_format_string='inertia_{}.inp'):
    # Write inertia matrices to file for the import in ANSYS
    for i in range(len(cs_data)):
        inertia = cs_data[i][1]
        rows = inertia.shape[0]
        cols = inertia.shape[1]
        with open(file_format_string.format(i + 1), 'w') as f:
            for row in range(rows):
                s = ''
                for col in range(row, cols):
                    s += ', {: 1.15e}'.format(inertia[row, col])
                f.write('cbmd,{}{}\n'.format(row + 1, s))


def write_ansys_node_input(beam_data, file_format_string='beam_nodes_{}.inp'):
    # write node data for each beam to import geometry in ANSYS
    for i, beam in enumerate(beam_data):
        with open(file_format_string.format(i + 1), 'w') as f:
            for i, node in enumerate(beam[0].nodes):
                f.write('n,{},{},{},{}\n'.format(i + 1, node.pos.x, node.pos.y, node.pos.z))


def read_ansys_static_results(folder_path, num_beams, num_boundary_conditions, num_load_cases):
    # reads the ansys results written by a ANSYS analysis
    ansys_analysis = []
    for i_beam in range(num_beams):
        load_case_data = []
        for i_bc in range(num_boundary_conditions):
            for i_lc in range(num_load_cases):
                file_name = 'beam_{}_bc_{}_l_{}.txt'.format(i_beam + 1, i_bc + 1, i_lc + 1)
                if os.path.exists(os.path.join(folder_path, file_name)):
                    load_case_data.append(get_ansys_node_displacements(os.path.join(folder_path, file_name)))
                else:
                    raise RuntimeError('No file for the load case and beam found for: '+ file_name)
        ansys_analysis.append(load_case_data)

    return ansys_analysis


def read_ansys_modal_results(folder_path, num_beams, num_boundary_conditions, num_eigenmodes):
    ansys_modal_analysis = []
    for i_beam in range(num_beams):
        eigenmodes_bc = []
        for i_bc in range(num_boundary_conditions):
            result = {}

            filename = 'eigenfreq_beam_{}_bc_{}.txt'.format(i_beam + 1, i_bc + 1)

            freq_df = pd.read_table(os.path.join(folder_path, filename),
                                    sep='\s+', dtype=np.float64, skiprows=4, nrows=num_eigenmodes)
            freq_df.columns = freq_df.columns.str.strip()

            for i_m in range(num_eigenmodes):
                filename = 'beam_{}_bc_{}_m_{}.txt'.format(i_beam + 1, i_bc + 1, i_m + 1)
                eigenmode = get_ansys_node_displacements(os.path.join(folder_path, filename))
                result[freq_df.at[i_m, 'TIME/FREQ']] = eigenmode
            eigenmodes_bc.append(result)
        ansys_modal_analysis.append(eigenmodes_bc)

    return ansys_modal_analysis


# Function for creation of a FE beam and the corresponding load cases
def create_test_beam(length, num_nodes, cs_function, kink_data=None, element_type_name='4node-no-warping'):
    """
    Creates a beam with given length, number of nodes and cross section data as a function of z2. The shape function
    can be chosen and a kink can be introduces to the beam.

    Parameters
    ----------
    length: float
        Length of the beam
    num_nodes: int
        Number of Nodes for the beam
    cs_function: function(z2)
        Function for cross section data at z2
    kink_data: (z2_kink, angle)
        z2_kink contains the position of the kink and angle is the angle between the z-axis and the beam of the kinked
        section.

        - The beam is always kinked in the y-direction for a positive angle.

        - If kink_data=None no kink is implemented

        - Ignored if z2_kink>length

    old_version: boolean
        Decides if old shape functions are used. These are not compatible with a kinked beam!

    Returns
    -------
    beam: Beam
        Contains the test  beam of PreDoCS
    boundary_conditions: list(tuple(3))
        Contains Dirichlet bc for a clamped end and for a two point support case
    load_cases_bc: list(tuple(bc, load))
        Contains load cases for this beam and extra dirichlet boundary conditions for each load case
    """
    # Node positions
    z2_nodes = np.linspace(0, length, num_nodes)
    if kink_data is None:
        pos_nodes = [Vector([0, 0, z2_nodes_i]) for z2_nodes_i in z2_nodes]
    else:  # kink the beam at half the length by 90 degrees

        # calculate the direction of the kinked section
        kink_dir = Vector([0, math.sin(math.radians(kink_data[1])), math.cos(math.radians(kink_data[1]))])

        pos_nodes = []
        for i in range(num_nodes):
            if z2_nodes[i] <= kink_data[0]:
                pos_nodes.append(Vector([0, 0, z2_nodes[i]]))
            else:
                pos_nodes.append(Vector([0,
                                         (z2_nodes[i] - kink_data[0]) * kink_dir.y,
                                         (z2_nodes[i] - kink_data[0]) * kink_dir.z + kink_data[0]]))

    # Element data
    element_stiffness = []
    element_inertia = []
    for i in range(num_nodes - 1):
        z2_mean = (z2_nodes[i] + z2_nodes[i + 1]) / 2.
        stiffness, inertia = cs_function(z2_mean)
        element_stiffness.append(stiffness)
        element_inertia.append(inertia)
    beam = Beam(z2_nodes, pos_nodes, element_stiffness, element_inertia, get_element_type_from_str(element_type_name))

    # Boundary conditions
    clamped_end = [(0, i, 0) for i in range(6)]
    middle_node_idx = int((num_nodes - 1) / 2)
    two_point_support = [(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 5, 0),
                         (middle_node_idx, 0, 0), (middle_node_idx, 1, 0), (middle_node_idx, 2, 0)]

    boundary_conditions = [clamped_end, two_point_support]

    # Load cases
    load_cases = []

    # Point loads
    for i in range(6):
        R = beam.get_load_vector(node_loads=[(num_nodes - 1, i, 1)])
        load_cases.append(([], R))

    # Line loads
    for i in range(3):
        R = beam.get_load_vector(line_load_function=lambda j, z: 1 if j == i else 0)
        load_cases.append(([], R))

    # Displacement controlled
    for i in range(6):
        R = beam.get_load_vector()
        load_cases.append(([(num_nodes - 1, i, 1)], R))

    return beam, boundary_conditions, load_cases


def get_displacement_difference_area(matrix_predocs, matrix_ansys):
    cols = [1, 2, 3, 4, 5, 6]
    z2_predocs = matrix_predocs[:, 0].flatten()
    z2_ansys = matrix_ansys[:, 0].flatten()
    assert np.allclose(z2_predocs, z2_ansys)
    z2 = z2_predocs
    area_ansys_all = 0
    area_predocs_all = 0
    for i_dis in range(6):
        dis_ansys = matrix_ansys[:, cols[i_dis]].flatten()
        dis_predocs = matrix_predocs[:, cols[i_dis]].flatten()
        area_predocs = np.trapz(dis_predocs, z2)
        area_ansys = np.trapz(dis_ansys, z2)
        area_predocs_all += area_predocs
        area_ansys_all += area_ansys
    return area_predocs_all, area_ansys_all


ansys_data_cols = ['X', 'Y', 'Z',  # Node z position
                   'UX', 'UY', 'UZ',  # Spatial displacement
                   'ROTX', 'ROTY', 'ROTZ']  # Rotational displacement


# Loads the beam displacements from a file
def get_ansys_node_displacements(filename):
    df = pd.read_table(filename, sep='\s+', names=ansys_data_cols, dtype=np.float64)
    z2 = [0]
    for i, [x, y, z] in enumerate(df.values[1:, 0:3]):
        z2.append(
            z2[-1] + math.sqrt((df.values[i, 0] - x) ** 2 + (df.values[i, 1] - y) ** 2 + (df.values[i, 2] - z) ** 2))

    displacements = np.zeros([len(z2), 7])
    displacements[:, 0] = z2
    displacements[:, 1:] = df.values[:, 3:]
    return displacements


def run_ansys(ansys_path, feFilename, runDir, jobName='job'):
    """This method opens an ansys run in an specified directory with the specified 
    input filename. It can also switch between local and remote(fa institute cluster) calculations. 

    The remote jobs are performed by copying the files of the local input directory to the 
    cluster on "\\\\cluster.fa.bs.dlr.de\\<username>\\delis\\<runDirName>".
    Then the program creates an ssh connection to the cluster. More information about
    the ssh connection can be found in serviceflb.utilities.callSSH.
    After the completion of the job the result is copied back to the local runDir.

    Ansys return Codes can be found in the documentation at(important for local calculations)::

        // Programmer's Manual // II. Guide to User-Programmable Features // 2. UPF Subroutines and Functions // 2.6. Running Mechanical APDL as a Subroutine

    :param feFilename: name of fe input file optionally with relative or absolute path
    :param runDir: absolute or relative path to the folder where the fe run should be executed(see also subRunDir)
    :param subRunDir: optional path that may be added to runDir like runDir+subRunDir 
    :param doRemoteCall: flag if the calculation should be done on a remote computer
    :param copyCreatedFiles: flag if all files in the directory runDir+subRunDir should be copied to the
                      local machine
    :param jobName: name of the fe job
    :returns: Ansys return value

    """
    ansysPath = os.path.normpath(ansys_path)
    os.environ['ANS_CONSEC'] = 'YES'
    feFilename = os.path.abspath(feFilename)
    ansArr = [ansysPath,
              '-dir', os.path.abspath(runDir),
              '-o', os.path.abspath(runDir + '\\ansys.log'),
              '-i', feFilename,
              '-b',
              '-j', jobName,
              '-np', '1']
    # print(ansArr)
    if not os.path.exists(ansysPath):
        raise RuntimeError('Wrong ANSYS path')
    retval = subprocess.call(ansArr)
    log.info('Return value of ansys call: ' + str(retval))
    if retval:
        raise RuntimeError('The ansys return code "' + str(retval) +
                           '" indicates errors within ansys. Please check the logfile.')
    return retval


def test_beam_fem(alu, ply, ply_thickness, data_dir, tmp_dir, ansys_working_path, do_plots=False):
    length = 10
    num_nodes = 21
    num_eigenmodes = 20
    ansys_input_file = os.path.join(ansys_working_path, 'validation_static_modal.cmd')

    ply = Orthotropic(
        E_11=133068810100.32,
        E_22=9238974380.03,
        E_33=9238974380.03,
        nu_12=0.3179,
        nu_13=0.3179,
        nu_23=0.3179,
        G_12=3504921995.5,
        G_13=6274228870.0,
        G_23=6274228870.0,
        name='glass_triax',
        density=1600,
    )

    # Material
    laminate_1 = CompositeShell(name='Laminate 1', layup=[(ply, 0.1, 30.0)])
    laminate_2 = CompositeShell(name='Laminate 2', layup=[(ply, 0.1, -30.0)])

    # Profile points of the box cross sections
    profile_points_box1 = np.array(load_profile_points(os.path.join(data_dir, 'profiles', 'rectangle_center.txt'),
                                                       False))
    profile_points_box2 = profile_points_box1 * (2. / 3.)
    profile_points_box3 = profile_points_box1 / 2.

    profile_points_box1 = [Vector(v) for v in profile_points_box1]
    profile_points_box2 = [Vector(v) for v in profile_points_box2]
    profile_points_box3 = [Vector(v) for v in profile_points_box3]

    # The definitions of the cross sections
    cs_definitions = [
        WingCrossSectionGeometryDefinition(profile_points_box1, alu),
        WingCrossSectionGeometryDefinition(profile_points_box2, alu),
        WingCrossSectionGeometryDefinition(profile_points_box3, alu),
        WingCrossSectionGeometryDefinition(profile_points_box1, laminate_1),
        WingCrossSectionGeometryDefinition(
            profile_points_box1,
            laminate_1,
            material_regions=[((Vector([0.5, 0.25]), Vector([-0.5, -0.249])), laminate_2)],
        ),
        WingCrossSectionGeometryDefinition(profile_points_box1, alu),
    ]
    hybrid_processors = ['JungWithoutWarping'] * 5 + ['Jung']

    cs_data = get_cross_section_data(cs_definitions, hybrid_processors, False)

    # Wing Input    
    def beam4_cs_distribution(z2):
        if 0 <= z2 < .3 * length:
            return cs_data[0]
        elif .3 * length <= z2 < .7 * length:
            return cs_data[1]
        else:
            return cs_data[2]

    beam_data = [
        create_test_beam(length, num_nodes, lambda z2: cs_data[5], element_type_name='jung'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[5], element_type_name='3node-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[0], element_type_name='3node-no-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[5], element_type_name='4node-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[0], element_type_name='4node-no-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[3], element_type_name='4node-no-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[4], element_type_name='4node-no-warping'),
        create_test_beam(length, num_nodes, beam4_cs_distribution, element_type_name='4node-no-warping'),
        create_test_beam(length, num_nodes, lambda z2: cs_data[0], kink_data=(5, 45), element_type_name='4node-no-warping'),
    ]

    # Do the PreDoCS calculations
    predocs_static_analysis_displacements = []
    predocs_static_analysis_cross_section_displacements = []
    predocs_static_analysis_internal_loads = []
    predocs_modal_analysis = []
    points_to_plot = num_nodes  # because the ANSYS displacements are given only for the nodes, can be more for better plots
    z2_to_plot = np.linspace(0, length, points_to_plot)
    # For each beam
    for i, (beam, boundary_conditions, load_cases) in enumerate(beam_data):
        log.info(f'Process beam data #{i}')
        # Static analysis
        result_displacements = []
        result_cross_section_displacements = []
        result_internal_loads = []
        for boundary_condition in boundary_conditions:
            for given_displacements, load_vector in load_cases:
                # For each load case
                beam_displacements_list, node_reactions_vector_list = beam.static_analysis(boundary_condition + given_displacements, [load_vector])
                post_processing_results = {z2: beam.post_processing(beam_displacements_list[0], z2) for z2 in z2_to_plot}
                result_displacements.append(np.array([[z2] + values[0] for z2, values in post_processing_results.items()]))
                result_cross_section_displacements.append(np.array([[z2] + values[1].tolist() for z2, values in post_processing_results.items()]))
                result_internal_loads.append(np.array([[z2] + values[2].tolist() for z2, values in post_processing_results.items()]))
        predocs_static_analysis_displacements.append(result_displacements)
        predocs_static_analysis_cross_section_displacements.append(result_cross_section_displacements)
        predocs_static_analysis_internal_loads.append(result_internal_loads)

        # TODO compare reaction forces

        # Modal analysis
        result_data = []
        for boundary_condition in boundary_conditions:
            beam_bc_data = {}
            eigenmodes = beam.modal_analysis(boundary_condition, num_eigenmodes)
            for freq, displacement_vector in eigenmodes.items():
                post_processing_results = {z2: beam.post_processing(displacement_vector, z2) for z2 in z2_to_plot}
                beam_bc_data[freq] = np.array([[z2] + values[0] for z2, values in post_processing_results.items()])
            result_data.append(beam_bc_data)
        predocs_modal_analysis.append(result_data)

    # ANSYS solution
    num_boundary_conditions = len(boundary_conditions)
    num_load_cases = len(load_cases)
    num_beams = 8#len(beam_data)

    # Create dirs
    if not os.path.exists(os.path.join(ansys_working_path, 'section_data')):
        os.makedirs(os.path.join(ansys_working_path, 'section_data'))

    if not os.path.exists(os.path.join(ansys_working_path, 'static_analysis')):
        os.makedirs(os.path.join(ansys_working_path, 'static_analysis'))

    if not os.path.exists(os.path.join(ansys_working_path, 'modal_analysis')):
        os.makedirs(os.path.join(ansys_working_path, 'modal_analysis'))

    if not os.path.exists(os.path.join(ansys_working_path, 'node_data')):
        os.makedirs(os.path.join(ansys_working_path, 'node_data'))

    # Write stiffness matrices to file for the import in ANSYS
    write_ansys_stiffness_input(cs_data, os.path.join(ansys_working_path, 'section_data', 'stiffness_{}.inp'))

    # Write inertia matrices to file for the import in ANSYS
    write_ansys_inertia_input(cs_data, os.path.join(ansys_working_path, 'section_data', 'inertia_{}.inp'))

    # Write Node data to file for the import in ANSYS
    write_ansys_node_input(beam_data, os.path.join(ansys_working_path, 'node_data', 'beam_nodes_{}.inp'))

    # Run the ANSYS calculation
    if 'ANSYS_EXE' in os.environ:# otherwise precalculated data is used
        run_ansys(os.environ['ANSYS_EXE'], ansys_input_file, ansys_working_path)

    # Load the ANSYS data
    ansys_static_analysis = read_ansys_static_results(os.path.join(ansys_working_path, 'static_analysis'),
                                                      num_beams, num_boundary_conditions, num_load_cases)

    ansys_modal_analysis = read_ansys_modal_results(os.path.join(ansys_working_path, 'modal_analysis'),
                                                    num_beams, num_boundary_conditions, num_eigenmodes)

    # Display the results
    if do_plots:
        for i_beam_data in range(num_beams):
            for i_bc in range(num_boundary_conditions):
                for i_lc in range(num_load_cases):
                    plot_beam_displacements(
                        {
                            'PreDoCS': predocs_static_analysis_displacements[i_beam_data][i_lc + i_bc * num_load_cases],
                            'ANSYS': ansys_static_analysis[i_beam_data][i_lc + i_bc * num_load_cases]
                        },
                        num_plots=6,
                        plot_size=(5, 3),
                        title='Beam displacements, beam data {}, load case {}'.format(i_beam_data,
                                                                                     i_lc + i_bc * num_load_cases),
                        file=os.path.join(tmp_dir, 'tests',
                                          '{:03d}_{:03d}_1_displacements.png'.format(i_beam_data,
                                                                                     i_lc + i_bc * num_load_cases)))
                    # plot_beam_cross_section_displacements(
                    #     {'PreDoCS': predocs_static_analysis_cross_section_displacements[i_beam_data][i_lc + i_bc * num_load_cases]},
                    #     num_plots=7,
                    #     plot_size=(5, 3),
                    #     title='Beam cross section displacements, beam data {}, load case {}'.format(i_beam_data,
                    #                                                                                 i_lc + i_bc * num_load_cases),
                    #     file=os.path.join(tmp_dir, 'tests',
                    #                       '{:03d}_{:03d}_2_cross_section_displacements.png'.format(i_beam_data,
                    #                                                                                i_lc + i_bc * num_load_cases)))
                    #
                    # plot_beam_internal_loads(
                    #     {'PreDoCS': predocs_static_analysis_internal_loads[i_beam_data][i_lc + i_bc * num_load_cases]},
                    #     num_plots=7,
                    #     plot_size=(5, 3),
                    #     title='Beam internal loads, beam data {}, load case {}'.format(i_beam_data,
                    #                                                                     i_lc + i_bc * num_load_cases),
                    #     file=os.path.join(tmp_dir, 'tests',
                    #                        '{:03d}_{:03d}_3_internal_loads.png'.format(i_beam_data,
                    #                                                                    i_lc + i_bc * num_load_cases)))

    # Do the tests
    # area_predocs_all = np.zeros([num_beams, num_load_cases * num_boundary_conditions])
    # area_ansys_all = np.zeros([num_beams, num_load_cases * num_boundary_conditions])
    for i_beam in range(num_beams):
        log.info(f'Compare beam data #{i_beam}')
        for i_bc in range(num_boundary_conditions):
            for i_lc in range(num_load_cases):
                matrix_predocs = predocs_static_analysis_displacements[i_beam][i_lc + i_bc * num_load_cases]
                matrix_ansys = ansys_static_analysis[i_beam][i_lc + i_bc * num_load_cases]
                atol = np.max(matrix_ansys) * 1e-2
                # All rel. differences less than 1 % and abs diff less than 1 % of the max displacement value
                assert np.allclose(matrix_predocs, matrix_ansys, rtol=1e-2, atol=atol)
                # area_predocs_all_, area_ansys_all_ = get_displacement_difference_area(
                #     matrix_predocs, matrix_ansys
                # )
                # area_predocs_all[i_beam, i_lc + i_bc * num_load_cases] = area_predocs_all_
                # area_ansys_all[i_beam, i_lc + i_bc * num_load_cases] = area_ansys_all_

    # assert np.allclose(area_predocs_all, area_ansys_all, rtol=1e-4, atol=1e-15)  # All rel. differences less than 0.01 %

    # TODO test for modal analysis


def test_beam_kink(alu, data_dir):
    """
    Compare kinked beam calculations to analytical solution.
    The analytical calculation path can be found in the `analytical_calculations` subdirectory.
    """
    length = 10
    num_nodes = 101

    # Profile points of the box cross sections
    profile_points_box1 = np.array(load_profile_points(os.path.join(data_dir, 'profiles', 'rectangle_center.txt'),
                                                       False))
    profile_points_box1 = [Vector(v) for v in profile_points_box1]

    # The definitions of the cross sections
    cs_definition = WingCrossSectionGeometryDefinition(profile_points_box1, alu)

    # Do the PreDoCS calculations
    cs_data = get_cross_section_data([cs_definition], ['Jung'], False)
    beam, boundary_conditions, load_cases = create_test_beam(
        length, num_nodes, lambda z2: cs_data[0], kink_data=(5, 45), element_type_name='4node-warping',
    )
    boundary_condition = boundary_conditions[0]  # Clamped end
    given_displacements, load_vector = load_cases[0]  # Tip load in x-direction
    beam_displacements_list, node_reactions_vector_list = beam.static_analysis(
        boundary_condition + given_displacements, [load_vector])
    beam_tip_displacement = beam.post_processing(beam_displacements_list[0], length)[0]

    # Analytical displacements (Tip load in x-direction)
    cs_stiffness_matrix = cs_data[0][0]
    F = 1
    E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = alu.material.engineering_constants
    E = E11
    G = G12
    b = 1
    h = 0.5
    t = alu.thickness
    I_by = 1/12 * (h**3 * b - (h-2*t)**3 * (b-2*t))
    I_bx = 1/12 * (h * b**3 - (h-2*t) * (b-2*t)**3)
    I_t = (2 * ((b-t)*(h-t))**2) / (((b-t)+(h-t)) / t)

    assert np.isclose(cs_stiffness_matrix[4, 4], E * I_bx, rtol=3e-2)
    assert np.isclose(cs_stiffness_matrix[3, 3], E * I_by, rtol=3e-2)
    assert np.isclose(cs_stiffness_matrix[5, 5], G * I_t, rtol=1e-2)

    I_b = I_by
    a = d = length/2
    b = c = math.sqrt(2)/4 * length
    w_B = -F/E/I_b * (1/6*a**3 - 1/2*c*a**2)
    w_diff_B = -F/E/I_b * (1/2*a**2 - c*a)
    w_tip_bending = w_B + w_diff_B * b + 1/3 * F*d**3/(E*I_b)
    w_tip_torsion = math.tan(F*c / (G * I_t) * a) * c
    w_tip = w_tip_bending + w_tip_torsion

    assert np.isclose(w_tip, beam_tip_displacement[0], rtol=2e-2)
