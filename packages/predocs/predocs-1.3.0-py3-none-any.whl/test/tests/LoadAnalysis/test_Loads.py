""" This module tests the Load class

.. codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.vector import Vector
from PreDoCS.WingAnalysis.PreDoCSCoord import PreDoCSCoord
from PreDoCS.LoadAnalysis.Load import DynamicReferencePoints, LoadCase

log = get_module_logger(__name__)

try:
    from PreDoCS.WingAnalysis.CPACS2PreDoCS import CPACS2PreDoCS
    from PreDoCS.WingAnalysis.cpacs_interface_predocs import CPACSInterfacePreDoCS
    from test.tests.WingAnalysis.test_PreDoCSCoord import get_test_PreDoCSCoord, get_test_PreDoCSCoord_simple, \
    get_test_PreDoCSCoord_simple2
except ImportError:
    log.warning('cpacs_interface not installed')

pytestmark = pytest.mark.cpacs_interface_required


def load_cpacs_file(cpacs_dir, cpacs_file, loads_are_internal_loads) -> 'CPACS2PreDoCS':
    cpacs_interface = CPACSInterfacePreDoCS(cpacs_dir, cpacs_file)
    c2p = CPACS2PreDoCS(
        cpacs_interface,
        loads_are_internal_loads=loads_are_internal_loads,
        get_element_stiffness_func=get_stiffness_for_shell,
        wing_index=0,
    )
    return c2p


def load_case_example(data_dir):
    # Create test load case from load case dict
    # Import cpacs load case dictionary
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'analytical_example_circ_beam_loads_CPACS.xml',
        loads_are_internal_loads=True,
    )

    # Extract test load case and test reference points
    loadcase = c2p.loadcase_dict['fx_max']
    reference_points = loadcase.load_reference_points

    return loadcase, reference_points


def test_import_load_case(tmp_dir, data_dir):
    """
    Test the load import method of CPACS2PreDoCS

    :param tmp_dir: str
    :param data_dir: str
    :return: load_case_dict: DynamicReferencePoints
    """
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_kink_simple_internal_loads.xml',
        loads_are_internal_loads=True,
    )

    for loadcase in c2p.loadcase_dict.values():
        assert hasattr(loadcase, 'name'), 'No load cases imported!'
        assert hasattr(loadcase, '_load_reference_points'), 'No load reference points imported'
        assert loadcase.length > 0, 'No loads found in load case!'


# def test_plot_load_case3D(tmp_dir, data_dir, show=False):
#     """
#     Test the 3D load plot environment. Figures are saved in tmp and optionally shown.
#
#     :param tmp_dir: str
#     :param data_dir: str
#     :param show: bool
#     :return:
#     """
#
#     result_path = os.path.join(tmp_dir, 'LoadsTests')
#
#     if not os.path.exists(result_path):
#         os.makedirs(result_path)
#
#     load_case_dict = test_import_load_case(tmp_dir, data_dir)
#
#     for load_case in load_case_dict.values():
#         fig = load_case.plot_load_case3D()
#         fig.savefig(os.path.join(result_path,  load_case.name + '3D.png' ))
#
#         if show:
#             manager = plt.get_current_fig_manager()
#             manager.window.showMaximized()


def test_plot_load_case2D(tmp_dir, data_dir, show=False):
    """
    Test the 2D load plot environment. Figures are saved in tmp and optionally shown.

    :param tmp_dir:
    :param data_dir:
    :param show:
    :return:
    """
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_kink_simple_internal_loads.xml',
        loads_are_internal_loads=True,
    )

    result_path = os.path.join(tmp_dir, 'LoadsTests')
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    for load_case in c2p.loadcase_dict.values():
        fig = load_case.plot_load_case2D()
        fig.savefig(os.path.join(result_path, load_case.name + '_2D.png'))

        if show:
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()


def test_calc_cross_sections(tmp_dir, data_dir):
    """
    Test the calculation of eta with arbitrary points in space, such as a kinked axis

    :param tmp_dir:
    :param data_dir:
    :return:
    """
    x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    y = [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5]
    z = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5]

    eta = np.linspace(0, 10, 11)
    cs_eta = np.linspace(0.5, 9.5, 10)
    points = DynamicReferencePoints(x, y, z)
    # cs, cs_eta_calc = points.calc_cross_sections()

    assert np.allclose(eta, points.eta), \
        'Eta is not calculated correctly'
    # assert np.allclose(cs_eta, cs_eta_calc), \
    #     'Eta of the cross sections is not calculated correctly'


def test_create_dynamic_reference_points(tmp_dir, data_dir):
    """
    Test the creation of DynamicReferencePoints between two given points.

    :param tmp_dir:
    :param data_dir:
    :return:
    """
    wing_length = 87

    # create beam axis as dynamic aircraft reference points
    p1 = Vector([0.0, 0.0, 0.0])
    p2 = Vector([0, 0, wing_length])

    beam_reference_points = DynamicReferencePoints.create_from_2points(p1, p2, 11)

    assert abs(wing_length - beam_reference_points.wing_length) < 0.001,\
        'The created DynamicReferencePoints have not the right length'
    assert beam_reference_points.size == 11,\
        'The number of DynamicReferencePoints does not match the required number'


def test_get_reference_axis(tmp_dir, data_dir):
    """
    Test the calculation of a reference_point and a reference_axis from a set of DynamicReferencePoints
    :param tmp_dir:
    :param data_dir:
    :return:
    """
    # Example load case, Example load reference points
    loadcase, test_reference_points = load_case_example(data_dir)

    # Build reference point and axis manually as vectors
    trp = test_reference_points
    point1 = Vector([trp.x[0], trp.y[0], trp.z[0]])
    point2 = Vector([trp.x[-1], trp.y[-1], trp.z[-1]])
    axis = point2-point1
    axis = axis.normalised

    # return PreDoCS coordinate system definition
    reference_point, reference_axis = test_reference_points.get_reference_axis()

    assert np.allclose([point1], reference_point, rtol=1e-4), 'The reference_point is not the defined starting point.'
    assert np.allclose([axis], reference_axis, rtol=1e-4), 'The reference_axis is pointing towards the wrong direction.'


def test_transformation_cpacs_predocs(tmp_dir, data_dir):
    # create PreDoCS coordinate system
    predocs_coord = get_test_PreDoCSCoord_simple()

    # create transformation matrix: transforms (rotation and translation) from CPACS into PreDoCS coordinate system
    transformation_matrix_cp = predocs_coord.transformation_aircraft_2_wing
    transformation_matrix_cp_cs = predocs_coord.transformation_aircraft_2_predocs(0)
    transformation_matrix_cp_ref = np.array([
        [-1, 0, 0, 1],
        [0, 0, 1, -2],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ])
    assert np.allclose(transformation_matrix_cp, transformation_matrix_cp_ref)
    assert np.allclose(transformation_matrix_cp, transformation_matrix_cp_cs)

    # create transformation matrix: transforms (rotation and translation) from PreDoCS into CPACS coordinate system
    transformation_matrix_pc = predocs_coord.transformation_wing_2_aircraft
    transformation_matrix_pc_cs = predocs_coord.transformation_predocs_2_aircraft(0)
    transformation_matrix_pc_ref = np.array([
        [-1, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 2],
        [0, 0, 0, 1],
    ])
    assert np.allclose(transformation_matrix_pc, transformation_matrix_pc_ref)
    assert np.allclose(transformation_matrix_pc, transformation_matrix_pc_cs)

    # Example load case, Example load reference points
    loadcase, test_reference_points = load_case_example(data_dir)

    # transform set of test reference points from CPACS into PreDoCS coordinate system
    transformed_test_reference_points = test_reference_points.transform_reference_points(transformation_matrix_cp)
    assert np.allclose(transformed_test_reference_points.x, [1] * 11)
    assert np.allclose(transformed_test_reference_points.y, [-2] * 11)
    assert np.allclose(transformed_test_reference_points.z, np.linspace(0, 10, 11))

    # Create transformed load case
    transformed_load_case = loadcase.transformed_load_case(transformation_matrix_cp)
    zero_list = [0] * 11
    assert np.allclose(transformed_load_case.fx, [15000] * 10 + [0])
    assert np.allclose(transformed_load_case.fy, zero_list)
    assert np.allclose(transformed_load_case.fz, zero_list)
    assert np.allclose(transformed_load_case.mx, zero_list)
    assert np.allclose(transformed_load_case.my, zero_list)
    assert np.allclose(transformed_load_case.mz, zero_list)


def test_interpolate_loadcase(tmp_dir, data_dir):
    # Import transformed load case
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_external_loads.xml',
        loads_are_internal_loads=False,
    )

    # Extract test load case
    loadcase = c2p.loadcase_dict['bending']

    # Import PreDoCS coordinate System
    predocs_coord = get_test_PreDoCSCoord_simple2()

    # transform set of test reference points from CPACS into PreDoCS coordinate system
    transformed_load_case = loadcase.transformed_load_case(predocs_coord.transformation_aircraft_2_wing)

    # Interpolate loads given in PreDoCS coordinate system
    # WARNING is expected here since beam node axis is not parallel to load reference axis
    interpolated_load_case = transformed_load_case.interpolated_loadcase_external(predocs_coord)

    assert np.isclose(sum(transformed_load_case.fx), sum(interpolated_load_case.fx), rtol=1e-5), \
        'The sum of interpolated loads is not equal to the sum of the original loads!'


def test_interpolate_loadcase_error(tmp_dir, data_dir):
    # Import transformed load case
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_kink_simple_external_loads.xml',
        loads_are_internal_loads=False,
    )

    # Extract test load case
    loadcase = c2p.loadcase_dict['bending']

    # Import PreDoCS coordinate System
    predocs_coord = get_test_PreDoCSCoord_simple()

    # transform set of test reference points from CPACS into PreDoCS coordinate system
    transformed_load_case = loadcase.transformed_load_case(predocs_coord.transformation_aircraft_2_wing)

    # Interpolate loads given in PreDoCS coordinate system
    # WARNING is expected here since beam node axis is not parallel to load reference axis
    with pytest.raises(AssertionError):
        interpolated_load_case = transformed_load_case.interpolated_loadcase_external(predocs_coord)


def test_interpolate_curved_loadcase(tmp_dir, data_dir):
    # Import transformed load case
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_kink_simple_external_loads.xml',
        loads_are_internal_loads=False,
    )

    # Extract test load case
    loadcase = c2p.loadcase_dict['bending']

    # Test PreDoCS coordinate system instantiation through class initialisation
    reference_points = [Vector([0.5, 0, 0]), Vector([0.5, 5, 0])]
    reference_axes = [Vector([0, 1, 0]), Vector([1, 5, 0])]
    section_lengths = [5, np.sqrt(5**2 + 1**2)]

    num_beam_nodes = 11
    beam_nodes_z2 = np.linspace(0, np.sum(section_lengths), num_beam_nodes)
    predocs_coord = PreDoCSCoord(reference_points, reference_axes, section_lengths, beam_nodes_z2)

    # transform set of test reference points from CPACS into PreDoCS coordinate system
    transformed_load_case = loadcase.transformed_load_case(predocs_coord.transformation_aircraft_2_wing)

    # Interpolate loads given in PreDoCS coordinate system
    interpolated_load_case = transformed_load_case.interpolated_loadcase_external(predocs_coord)

    assert np.isclose(sum(transformed_load_case.fx), sum(interpolated_load_case.fx), rtol=1e-5), \
        'The sum of interpolated loads is not equal to the sum of the original loads!'


def test_plot_load_redistribution(tmp_dir, data_dir, show=False):
    # Import transformed load case
    c2p = load_cpacs_file(
        os.path.join(data_dir, 'CPACS'),
        'Beam_Composite_bending_external_loads.xml',
        loads_are_internal_loads=False,
    )

    # Extract test load case
    loadcase = c2p.loadcase_dict['bending']

    # Import PreDoCS coordinate System
    predocs_coord = get_test_PreDoCSCoord_simple2()

    # transform set of test reference points from CPACS into PreDoCS coordinate system
    transformed_load_case = loadcase.transformed_load_case(predocs_coord.transformation_aircraft_2_wing)

    # Interpolate loads given in PreDoCS coordinate system
    # WARNING is expected here since beam node axis is not parallel to load reference axis
    interpolated_load_case = transformed_load_case.interpolated_loadcase_external(predocs_coord)

    result_path = os.path.join(tmp_dir, 'LoadsTests')
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    fig = LoadCase.plot_load_redistribution(transformed_load_case, interpolated_load_case)
    fig.savefig(os.path.join(result_path, loadcase.name + '_redistribution.png'))

    if show:
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()


def test_move_loads(tmp_dir, data_dir):

    # import load case in PreDoCS coordinates and interpolated load case
    predocs_coord = get_test_PreDoCSCoord()
    interpolated_load_case = test_interpolate_loadcase(tmp_dir, data_dir)

    # create load application axis in global coordinates
    wingroot = Vector([23.58454965, 0., -1.33886196])
    wingtip = Vector([35.99258137, 26.00961361, 0.41231221])
    beam_nodes = predocs_coord.create_drps_wing(predocs_coord.z2_bn)
    load_application_points_global = DynamicReferencePoints.create_from_2points(wingroot, wingtip, beam_nodes.z.size)

    # points have in fact not the same z-coordinates as interpolated loads. Doesn't matter for this test however
    load_application_points = load_application_points_global.transform_reference_points(predocs_coord.transformation_aircraft_2_predocs(0))

    # beam_node_loads = interpolated_load_case.moved_loads_to_load_application_points(load_application_points)

    # TODO assert statement

    # return beam_node_loads
