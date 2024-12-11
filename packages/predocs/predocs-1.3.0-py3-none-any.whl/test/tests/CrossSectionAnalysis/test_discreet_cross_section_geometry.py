"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
import pickle

import pytest
from _pytest.python_api import approx
import numpy as np

from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement
from PreDoCS.util.vector import Vector
from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from copy import copy


@pytest.fixture
def component1(alu):
    return DiscreetCrossSectionGeometry.Component(6, alu, 0.0)


@pytest.fixture
def component2(alu):
    return DiscreetCrossSectionGeometry.Component(7, alu, 0.0)


@pytest.mark.unit_tests
def test_node():
    pos = Vector([2, 3])
    node = DiscreetCrossSectionGeometry.Node(5, pos)
    node2 = copy(node)
    assert node.id == 5
    assert hash(node) == hash(node2)
    assert node.id == node2.id
    assert node.position == pos
    
    assert node == node
    assert node !=  DiscreetCrossSectionGeometry.Node(4, pos)
    with pytest.raises(TypeError):
        node == pos


@pytest.mark.unit_tests
def test_component(component1, component2, alu):
    assert component1.id == 6
    assert component1.shell == alu
    assert component1._midsurface_offset == 0.0
    
    assert component1 == component1
    assert component1 !=  component2
    with pytest.raises(TypeError):
        component1 == alu


@pytest.mark.unit_tests
def test_segment(component1):
    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([0, 0]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([0, 1]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([1, 1]))
    
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component1)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n3, component1)
    elements = [e1, e2]
    segment = DiscreetCrossSectionGeometry.Segment(2, elements)

    assert segment.id == 2
    assert segment.node1 == n1
    assert segment.node2 == n3
    assert segment.elements == elements
    # assert segment.length == 2
    assert segment.shell == component1.shell


@pytest.mark.unit_tests
def test_cell(component1, component2):
    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([0, 0]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([0, 1]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([1, 1]))
    n4 = DiscreetCrossSectionGeometry.Node(4, Vector([1, 0]))
    nodes = [n1, n2, n3, n4]
    
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component1)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n3, component1)
    e3 = DiscreetCrossSectionGeometry.Element(3, n3, n4, component2)
    e4 = DiscreetCrossSectionGeometry.Element(4, n4, n1, component2)
    elements = [e4, e1, e2, e3]
    
    discreet_geometry = DiscreetCrossSectionGeometry()
    discreet_geometry.add_elements(elements)
    
    cell = DiscreetCrossSectionGeometry.Cell(nodes, discreet_geometry)
    assert cell.nodes == nodes
    assert cell.elements == elements
    assert cell.area == 1  # TODO: für unterschiedliche Mittelebenen
    
    assert cell.is_cutted == False
    cell.cut_node = n1
    assert cell.is_cutted == True


@pytest.mark.unit_tests
def test_element(alu):
    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([0, 0]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([1, 0]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([1, 1]))
    
    t = 2e-2  # Thickness material

    component1 = DiscreetCrossSectionGeometry.Component(10, alu, 0.0)
    component2 = DiscreetCrossSectionGeometry.Component(11, alu, -0.5)
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component1)
    e2 = DiscreetCrossSectionGeometry.Element(2, n1, n2, component2)
    e3 = DiscreetCrossSectionGeometry.Element(3, n1, n3, component1)

    # e1.dx_ds
    # e1.dy_ds
    
    assert e1.id == 1
    assert hash(e1) == 1
    assert e1 == e1
    assert e1.node1 == n1
    assert e1.node2 == n2

    assert e1.position == Vector([0.5, 0])

    assert e2.position == Vector([0.5, 0])

    assert e1.angle_in_cross_section == 0
    assert e2.angle_in_cross_section == 0
    assert approx(e3.angle_in_cross_section) == np.deg2rad(45)
    
    assert e1.length_vector == Vector([1, 0])
    assert e3.length_vector == Vector([1, 1])
    
    assert e1.length == 1
    assert e3.length == np.sqrt(2)
    
    assert e1.thickness_vector == Vector([0, -t])
    assert e3.thickness_vector == Vector([1, -1]) * t / np.sqrt(2)
    
    assert e1.thickness == t
    assert e3.thickness == t
    
    assert e1.area == t
    assert e3.area == t*np.sqrt(2)
    
    assert e1.component == component1
    assert e2.component == component2
    
    assert e1.shell == alu
    assert e2.shell == alu


@pytest.mark.unit_tests
def test_discreet_cross_section_geometry(component1, component2):
    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([0, 0]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([1, 0]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([1, 1]))
    n4 = DiscreetCrossSectionGeometry.Node(4, Vector([0, 1]))
    n5 = DiscreetCrossSectionGeometry.Node(5, Vector([1.5, 0.5]))
    nodes = [n1, n2, n3, n4, n5]

    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component1)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n5, component1)
    e3 = DiscreetCrossSectionGeometry.Element(3, n5, n3, component1)
    e4 = DiscreetCrossSectionGeometry.Element(4, n3, n4, component1)
    e5 = DiscreetCrossSectionGeometry.Element(5, n4, n1, component1)
    e6 = DiscreetCrossSectionGeometry.Element(6, n2, n3, component2)
    elements = [e1, e2, e3, e4, e5]

    discreet_geometry = DiscreetCrossSectionGeometry()
    discreet_geometry.add_elements(elements)
    discreet_geometry.add_element(e6)

    assert discreet_geometry.elements == elements + [e6]
    assert discreet_geometry.nodes == nodes
    assert discreet_geometry.components == [component1, component2]
    assert discreet_geometry.get_element_from_nodes(n1, n2) == e1
    assert discreet_geometry.get_element_from_nodes(n1, n3) is None
    assert discreet_geometry.get_neighbor_nodes(n2) == [n1, n3, n5]
    assert discreet_geometry.get_adjacent_elements(n3) == [e3, e4, e6]
    assert DiscreetCrossSectionGeometry.get_common_node_from_elements(e4, e5) == n4
    assert DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(e4, [e4]) == True
    assert DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(e4, [e3, e4, e5]) == True
    assert DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(e4, [e5, e4, e3]) == False

    segments = discreet_geometry.segments
    assert len(segments) == 3
    
    cells = discreet_geometry.cells
    assert len(cells) == 2
    
    assert discreet_geometry.segment_border_nodes == [n2, n3]
    # TODO: more segment testing; in direction of cell; element in direction of segment
    # discreet_geometry.get_common_node_from_segments(segments[0], segments[1])
    # discreet_geometry.is_element_in_direction_of_segment(e1, segments[1])
    # discreet_geometry.is_segment_in_direction_of_cell(segments[0], cells[0])

    assert discreet_geometry.get_shortest_path(n1, n5) == [n1, n2, n5]

    cut_geometry = discreet_geometry.copy()
    cut_geometry.cut_discreet_geometry(n3, n4)
    assert len(cut_geometry.cells) == 1


@pytest.mark.unit_tests
def test_midsurface_offset(alu):
    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([0, 0]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([0, 0.5]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([1, 0.5]))
    n4 = DiscreetCrossSectionGeometry.Node(4, Vector([1, 0]))

    delta_t = alu.thickness / 4  # TODO: should be / 2
    # delta_t2 = alu.thickness / 2

    component1 = DiscreetCrossSectionGeometry.Component(6, alu, 0.0)
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component1)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n3, component1)
    e3 = DiscreetCrossSectionGeometry.Element(3, n3, n4, component1)
    e4 = DiscreetCrossSectionGeometry.Element(4, n4, n1, component1)
    discreet_geometry1 = DiscreetCrossSectionGeometry()
    discreet_geometry1.add_elements([e1, e2, e3, e4])

    node_midsurface_positions = discreet_geometry1.node_midsurface_positions
    assert node_midsurface_positions[e1.node1] == Vector([0, 0])
    assert node_midsurface_positions[e1.node2] == Vector([0, 0.5])
    assert node_midsurface_positions[e2.node1] == Vector([0, 0.5])
    assert node_midsurface_positions[e2.node2] == Vector([1, 0.5])
    # assert e1.reference_position == Vector([0, 0.25])
    # assert e2.reference_position == Vector([0.5, 0.5])

    component2 = DiscreetCrossSectionGeometry.Component(6, alu, 0.5)
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component2)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n3, component2)
    e3 = DiscreetCrossSectionGeometry.Element(3, n3, n4, component2)
    e4 = DiscreetCrossSectionGeometry.Element(4, n4, n1, component2)
    discreet_geometry2 = DiscreetCrossSectionGeometry()
    discreet_geometry2.add_elements([e1, e2, e3, e4])

    node_midsurface_positions = discreet_geometry2.node_midsurface_positions
    assert node_midsurface_positions[e1.node1] == Vector([0 + delta_t, 0 + delta_t])
    assert node_midsurface_positions[e1.node2] == Vector([0 + delta_t, 0.5 - delta_t])
    assert node_midsurface_positions[e2.node1] == Vector([0 + delta_t, 0.5 - delta_t])
    assert node_midsurface_positions[e2.node2] == Vector([1 - delta_t, 0.5 - delta_t])
    # assert e1.reference_position == Vector([0 + delta_t2, 0.25])
    # assert e2.reference_position == Vector([0.5, 0.5 - delta_t2])

    component3 = DiscreetCrossSectionGeometry.Component(6, alu, -0.5)
    e1 = DiscreetCrossSectionGeometry.Element(1, n1, n2, component3)
    e2 = DiscreetCrossSectionGeometry.Element(2, n2, n3, component3)
    e3 = DiscreetCrossSectionGeometry.Element(3, n3, n4, component3)
    e4 = DiscreetCrossSectionGeometry.Element(4, n4, n1, component3)
    discreet_geometry3 = DiscreetCrossSectionGeometry()
    discreet_geometry3.add_elements([e1, e2, e3, e4])

    node_midsurface_positions = discreet_geometry3.node_midsurface_positions
    assert node_midsurface_positions[e1.node1] == Vector([0 - delta_t, 0 - delta_t])
    assert node_midsurface_positions[e1.node2] == Vector([0 - delta_t, 0.5 + delta_t])
    assert node_midsurface_positions[e2.node1] == Vector([0 - delta_t, 0.5 + delta_t])
    assert node_midsurface_positions[e2.node2] == Vector([1 + delta_t, 0.5 + delta_t])
    # assert e1.reference_position == Vector([0 - delta_t2, 0.25])
    # assert e2.reference_position == Vector([0.5, 0.5 + delta_t2])


@pytest.mark.unit_tests
def test_discreet_geometry_pickle(tmp_dir, cs_definition):
    discreet_geometry = cs_definition.get_discreet_geometry(element_type=CompositeElement, element_length=0.1)

    # Save
    pickle.dump(discreet_geometry, open(os.path.join(tmp_dir, 'discreet_geometry.p'), 'wb'))

    # Load
    discreet_geometry_load = pickle.load(open(os.path.join(tmp_dir, 'discreet_geometry.p'), 'rb'))
