""" This Module tests the load class

.. codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from collections import namedtuple

import numpy as np
import pytest

from PreDoCS.LoadAnalysis.Load import DynamicReferencePoints
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.geometry import transform_location_m, create_transformation_matrix_aircraft_2_predocs_old, \
    create_transformation_aircraft_2_predocs_new
from PreDoCS.util.occ import transformation_occ_2_matrix
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)

try:
    from PreDoCS.WingAnalysis.PreDoCSCoord import PreDoCSCoord
except ImportError:
    log.warning('cpacs_interface not installed')


pytestmark = pytest.mark.cpacs_interface_required


def get_test_PreDoCSCoord():
    wingroot = Vector([23.58454965, 0., -1.33886196])
    wingtip = Vector([35.99258137, 26.00961361, 0.41231221])

    # Test PreDoCS coordinate system instantiation through class initialisation
    reference_point = [Vector([20.3611, 0.3218, -0.624])]
    reference_axis = [Vector([0.48770725, 0.87300724, 0.])]
    wing_length = wingtip.dist(wingroot)
    section_lengths = [wing_length]

    num_beam_nodes = 11
    beam_nodes_z2 = np.linspace(0, wing_length, num_beam_nodes)
    predocs_coord = PreDoCSCoord(reference_point, reference_axis, section_lengths, beam_nodes_z2)

    return predocs_coord


def get_test_PreDoCSCoord_simple():
    wing_length = 25
    wingroot = Vector([1, 0, 2])
    wingtip = Vector([1, wing_length, 2])

    # Test PreDoCS coordinate system instantiation through class initialisation
    reference_point = [wingroot]
    reference_axis = [Vector([0, 1, 0])]
    section_lengths = [wing_length]

    num_beam_nodes = 11
    beam_nodes_z2 = np.linspace(0, wing_length, num_beam_nodes)
    predocs_coord = PreDoCSCoord(reference_point, reference_axis, section_lengths, beam_nodes_z2)

    return predocs_coord


def get_test_PreDoCSCoord_simple2():
    wing_length = 10
    wingroot = Vector([0.5, 0, 0])
    wingtip = Vector([0, wing_length, 0])

    # Test PreDoCS coordinate system instantiation through class initialisation
    reference_point = [wingroot]
    reference_axis = [Vector([0, 1, 0])]
    section_lengths = [wing_length]

    num_beam_nodes = 11
    beam_nodes_z2 = np.linspace(0, wing_length, num_beam_nodes)
    predocs_coord = PreDoCSCoord(reference_point, reference_axis, section_lengths, beam_nodes_z2)

    return predocs_coord


def test_PreDoCSCoord(tmp_dir, data_dir):
    """
    Create a predocs_coord instance for the cpacs 016_016.xml aircraft and check it.
    """
    # 016_016.xml cpacs geometry data
    c2p = namedtuple('c2p', ['wingtip_leading_point', 'wingbox_trailing_point', 'wingroot', 'wingtip', 'load_reference_points', 'component_segment', 'cpacs_interface'])
    c2p.wingtip_leading_point = Vector([35.36328005, 26.00961361, 0.40682038])
    c2p.wingbox_trailing_point = Vector([27.77222609, 2.59, -1.59499122])
    c2p.wingroot = Vector([23.58454965, 0., -1.33886196])
    c2p.wingtip = Vector([35.99258137, 26.00961361, 0.41231221])
    #loadcase, c2p.load_reference_points = load_case_example(tmp_dir, data_dir)
    c2p.load_reference_points = DynamicReferencePoints.create_from_2points(c2p.wingroot, c2p.wingtip, 40)
    c2p.cpacs_interface = namedtuple('cpacs_interface', ['tixi_handle'])
    c2p.cpacs_interface.tixi_handle = namedtuple('tixi_handle', ['checkElement'])
    c2p.cpacs_interface.tixi_handle.checkElement = lambda x: False
    c2p.component_segment = namedtuple('component_segment', ['xpath'])
    c2p.component_segment.xpath = '/path'

    # Test PreDoCS coordinate system instantiation through class initialisation
    num_beam_nodes = 11
    predocs_coord = get_test_PreDoCSCoord()
    predocs_coord.transformation_aircraft_2_wing  # noqa
    predocs_coord.transformation_wing_2_aircraft  # noqa
    predocs_coord.transformation_aircraft_2_predocs(10)
    predocs_coord.transformation_predocs_2_aircraft(10)

    # Test PreDoCS coordinate system instantiation by from_c2p method
    predocs_coord = PreDoCSCoord.from_c2p(c2p, num_beam_nodes, orientation='load_reference_points', ensure_cross_sections_in_shell=False)
    predocs_coord.transformation_aircraft_2_wing  # noqa
    predocs_coord.transformation_wing_2_aircraft  # noqa
    predocs_coord.transformation_aircraft_2_predocs(10)
    predocs_coord.transformation_predocs_2_aircraft(10)


def test_predocscoord_section_transformation():
    reference_points = [Vector([0, 0, 0]), Vector([0, 1, 0])]
    reference_axes = [Vector([0, 1, 0]), Vector([1, 1, 0])]
    section_lengths = [1, np.sqrt(2)]
    num_beam_nodes = 3

    beam_nodes_z2 = np.linspace(0, sum(section_lengths), num_beam_nodes)

    points = [Vector([0.1, 0.2, 0.5]), Vector([0.8, 0.2, 1.5])]
    z2_list = [0.2, 1.5]

    # Old x-axis definition
    predocs_coord = PreDoCSCoord(reference_points, reference_axes, section_lengths, beam_nodes_z2, x_axis_definition='old')
    point_transformed_wing = [
        transform_location_m(predocs_coord.transformation_aircraft_2_wing, point)
        for z2, point in zip(z2_list, points)
    ]
    point_transformed_predocs = [
        transform_location_m(predocs_coord.transformation_aircraft_2_predocs(z2), point)
        for z2, point in zip(z2_list, points)
    ]
    trafo1_wing = [-0.1, 0.5, 0.2]
    trafo2_wing = [-0.8, 1.5, 0.2]
    trafo1_predocs = [-0.1, 0.5, 0]
    trafo2_predocs = [-1.13137085, 1.5, -0.5]
    assert np.allclose(trafo1_wing, point_transformed_wing[0])
    assert np.allclose(trafo2_wing, point_transformed_wing[1])
    assert np.allclose(trafo1_predocs, point_transformed_predocs[0])
    assert np.allclose(trafo2_predocs, point_transformed_predocs[1])

    # New x-axis definition
    predocs_coord = PreDoCSCoord(reference_points, reference_axes, section_lengths, beam_nodes_z2, x_axis_definition='new')
    point_transformed_wing = [
        transform_location_m(predocs_coord.transformation_aircraft_2_wing, point)
        for z2, point in zip(z2_list, points)
    ]
    point_transformed_predocs = [
        transform_location_m(predocs_coord.transformation_aircraft_2_predocs(z2), point)
        for z2, point in zip(z2_list, points)
    ]
    assert np.allclose(trafo1_wing, point_transformed_wing[0])
    assert np.allclose(trafo2_wing, point_transformed_wing[1])
    assert np.allclose(trafo1_predocs, point_transformed_predocs[0])
    assert np.allclose(trafo2_predocs, point_transformed_predocs[1])


def test_is_point_on_axis():
    reference_points = [Vector([0, 0, 0]), Vector([0, 1, 0])]
    reference_axes = [Vector([0, 1, 0]), Vector([1, 1, 0])]
    section_lengths = [1, np.sqrt(2)]
    num_beam_nodes = 3

    beam_nodes_z2 = np.linspace(0, sum(section_lengths), num_beam_nodes)

    predocs_coord = PreDoCSCoord(reference_points, reference_axes, section_lengths, beam_nodes_z2)

    # Tests in CPACS coordinates
    points_on_axis_aircraft = [
        (Vector([0, 0.5, 0]), True),
        (Vector([0.5, 1.5, 0]), True),
        (Vector([0, -1e-6, 0]), True),
        (Vector([1, 2 + 1e-6, 0]), True),
        (Vector([2, 1, 0]), False),
        (Vector([1, 0, 0]), False),
    ]
    for point, point_on_axis in points_on_axis_aircraft:
        assert point_on_axis == predocs_coord.is_point_on_beam_axis_aircraft(point), f'Point: {point} should be on axis: {point_on_axis}'

    # Tests in PreDoCS beam coordinates
    points_on_axis_predocs = [
        (Vector([0, 0, 0.5]), True),
        (Vector([-0.5, 0, 1.5]), True),
        (Vector([0, 0, -1e-6]), True),
        (Vector([-1, 0, 2 + 1e-6]), True),
        (Vector([-2, 0, 1]), False),
        (Vector([-1, 0, 0]), False),
    ]
    for point, point_on_axis in points_on_axis_predocs:
        assert point_on_axis == predocs_coord.is_point_on_beam_axis_predocs(point), f'Point: {point} should be on axis: {point_on_axis}'


def test_transformations():
    ref_point_wing_cpacs = Vector([4.5, 0, 3])
    ref_dir_wing_capcs = Vector([0, 1, 0])

    trsf_old = create_transformation_matrix_aircraft_2_predocs_old(ref_point_wing_cpacs, ref_dir_wing_capcs)
    trsf_global = transformation_occ_2_matrix(create_transformation_aircraft_2_predocs_new(
        ref_point_wing_cpacs, ref_dir_wing_capcs,
    ))

    assert np.allclose(trsf_old, trsf_global)

    p_tip_cpacs = Vector([4.5, 10, 3])
    p_tip_predocs_old = transform_location_m(trsf_old, p_tip_cpacs)
    p_tip_predocs_global = transform_location_m(trsf_global, p_tip_cpacs)

    p_le_cpacs = Vector([3.5, 10, 3])
    p_le_predocs_old = transform_location_m(trsf_old, p_le_cpacs)
    p_le_predocs_global = transform_location_m(trsf_global, p_le_cpacs)

    p_ss_cpacs = Vector([4.5, 10, 4])
    p_ss_predocs_old = transform_location_m(trsf_old, p_ss_cpacs)
    p_ss_predocs_global = transform_location_m(trsf_global, p_ss_cpacs)

    assert np.allclose(p_tip_predocs_old, Vector([0, 0, 10]))
    assert np.allclose(p_tip_predocs_global, Vector([0, 0, 10]))

    assert np.allclose(p_le_predocs_old, Vector([1, 0, 10]))
    assert np.allclose(p_le_predocs_global, Vector([1, 0, 10]))

    assert np.allclose(p_ss_predocs_old, Vector([0, 1, 10]))
    assert np.allclose(p_ss_predocs_global, Vector([0, 1, 10]))


# def test_transformations2():
#     ref_point_wing_cpacs = Vector([4.5, 0, 3])
#     ref_dir_wing_capcs = Vector([0, 1, 0])
#
#     trsf_old = transformation_occ_2_matrix(create_transformation_c2p(ref_point_wing_cpacs, ref_dir_wing_capcs))
#     trsf_global = create_transformation_matrix_aircraft_2_predocs_new(ref_point_wing_cpacs, ref_dir_wing_capcs, Vector([1, 0, 0]))
#
#     assert np.allclose(trsf_old, trsf_global)
#
#     p_tip_cpacs = Vector([4.5, 10, 3])
#     p_tip_predocs_old = transform_location_m(trsf_old, p_tip_cpacs)
#     p_tip_predocs_global = transform_location_m(trsf_global, p_tip_cpacs)
#
#     p_le_cpacs = Vector([3.5, 10, 3])
#     p_le_predocs_old = transform_location_m(trsf_old, p_le_cpacs)
#     p_le_predocs_global = transform_location_m(trsf_global, p_le_cpacs)
#
#     p_ss_cpacs = Vector([4.5, 10, 4])
#     p_ss_predocs_old = transform_location_m(trsf_old, p_ss_cpacs)
#     p_ss_predocs_global = transform_location_m(trsf_global, p_ss_cpacs)
#
#     assert np.allclose(p_tip_predocs_old, Vector([0, 0, 10]))
#     assert np.allclose(p_tip_predocs_global, Vector([0, 0, 10]))
#
#     assert np.allclose(p_le_predocs_old, Vector([1, 0, 10]))
#     assert np.allclose(p_le_predocs_global, Vector([1, 0, 10]))
#
#     assert np.allclose(p_ss_predocs_old, Vector([0, 1, 10]))
#     assert np.allclose(p_ss_predocs_global, Vector([0, 1, 10]))
#
