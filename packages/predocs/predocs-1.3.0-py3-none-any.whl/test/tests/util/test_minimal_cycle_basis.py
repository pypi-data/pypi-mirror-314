"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import pytest
import networkx as nx
from PreDoCS.util.MinimalCycleBasis import MinimalCycleBasis
from PreDoCS.util.vector import Vector


@pytest.fixture
def example_graph():
    # Testdata from paper
    vertices = [ MinimalCycleBasis.Vertex(Vector([1,3])), MinimalCycleBasis.Vertex(Vector([0,2])),
                MinimalCycleBasis.Vertex(Vector([3,2])), MinimalCycleBasis.Vertex(Vector([2,2.5])),
                MinimalCycleBasis.Vertex(Vector([1,2.5])), MinimalCycleBasis.Vertex(Vector([3,3])),
                MinimalCycleBasis.Vertex(Vector([4,4])), MinimalCycleBasis.Vertex(Vector([5,2])),
                MinimalCycleBasis.Vertex(Vector([5,4])), MinimalCycleBasis.Vertex(Vector([8,4])),
                MinimalCycleBasis.Vertex(Vector([3.5,1])), MinimalCycleBasis.Vertex(Vector([4.5,1])),
                MinimalCycleBasis.Vertex(Vector([4,3])), MinimalCycleBasis.Vertex(Vector([7,0])),
                MinimalCycleBasis.Vertex(Vector([8,1])), MinimalCycleBasis.Vertex(Vector([10,0])),
                MinimalCycleBasis.Vertex(Vector([9.5,3])), MinimalCycleBasis.Vertex(Vector([11,4])),
                MinimalCycleBasis.Vertex(Vector([11,2])), MinimalCycleBasis.Vertex(Vector([12,4.5])),
                MinimalCycleBasis.Vertex(Vector([11,0])), MinimalCycleBasis.Vertex(Vector([14,0])),
                MinimalCycleBasis.Vertex(Vector([14,2])), MinimalCycleBasis.Vertex(Vector([12,0.5])),
                MinimalCycleBasis.Vertex(Vector([13,0.5])), MinimalCycleBasis.Vertex(Vector([12.5,1.8])),
                MinimalCycleBasis.Vertex(Vector([10.5,2.5])), MinimalCycleBasis.Vertex(Vector([9,2.5])),
                MinimalCycleBasis.Vertex(Vector([8,3])), MinimalCycleBasis.Vertex(Vector([8,2.3])),
                MinimalCycleBasis.Vertex(Vector([7,2.5])) ]
    elements = [ (vertices[1], vertices[0]),
                 (vertices[0], vertices[5]),
                 (vertices[2], vertices[5]),
                 (vertices[1], vertices[2]),
                 (vertices[4], vertices[3]),
                 (vertices[3], vertices[2]),
                 (vertices[5], vertices[6]),
                 (vertices[6], vertices[8]),
                 (vertices[8], vertices[9]),
                 (vertices[8], vertices[7]),
                 (vertices[7], vertices[9]),
                 (vertices[7], vertices[18]),
                 (vertices[9], vertices[16]),
                 (vertices[16], vertices[17]),
                 (vertices[17], vertices[18]),
                 (vertices[17], vertices[19]),
                 (vertices[19], vertices[18]),
                 (vertices[18], vertices[22]),
                 (vertices[22], vertices[21]),
                 (vertices[21], vertices[20]),
                 (vertices[20], vertices[18]),
                 (vertices[20], vertices[23]),
                 (vertices[23], vertices[25]),
                 (vertices[25], vertices[24]),
                 (vertices[24], vertices[23]),
                 (vertices[15], vertices[14]),
                 (vertices[14], vertices[13]),
                 (vertices[10], vertices[12]),
                 (vertices[12], vertices[11]),
                 (vertices[11], vertices[10]),
                 (vertices[16], vertices[26]),
                 (vertices[26], vertices[27]),
                 (vertices[27], vertices[16]),
                 (vertices[30], vertices[28]),
                 (vertices[28], vertices[29]),
                 (vertices[29], vertices[30]) ]

    g = nx.Graph()
    for node1, node2 in elements:
        g.add_edge(node1, node2)
    
    return MinimalCycleBasis(g)
    
# TODO: weitere Tests
@pytest.mark.unit_tests
def test_find_all_faces(example_graph):
    assert len(example_graph.get_faces()) == 7
        