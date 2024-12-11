"""
Created on 26.06.2018

@author: Daniel
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import numpy as np

from PreDoCS.util.util import line_line_intersection, line_plane_intersection, \
    pt_is_in_plane_dir
from PreDoCS.util.vector import Vector


def test_line_line_intersection():
    # line definitions
    l0 = Vector([1, 1, 0])
    l0_dir = Vector([1, 0, 0])

    l1 = Vector([0, 0, 0])
    l1_dir1 = Vector([0, 0, 1])
    l1_dir2 = Vector([0, 1, 0])

    intersection1 = line_line_intersection(l0, l0_dir, l1, l1_dir1)
    intersection2 = line_line_intersection(l0, l0_dir, l1, l1_dir2)

    assert intersection1 is None
    assert np.allclose(intersection2, [0, 1, 0])


def test_line_plane_intersection():

    # line definitions
    l0 = Vector([1, 1, 1])
    l_dir1 = Vector([1, 0, 0])
    l_dir2 = Vector([0, 0, 1])

    # plane definitions
    p0 = Vector([0, 0, 0])
    p_normal = Vector([1, 0, 0])

    intersection1 = line_plane_intersection(l0, l_dir1, p0, p_normal)
    intersection2 = line_plane_intersection(l0, l_dir2, p0, p_normal)

    assert np.allclose(intersection1, Vector([0, 1, 1]))
    assert intersection2 is None


def test_pt_is_in_plane_dir():

    # plane definition
    p0 = Vector([0, 0, 0])
    p_normal = Vector([0, 0, 1])

    # points
    pts = [(Vector([0, 0, 0]), True),
           (Vector([0, 0, 1]), True),
           (Vector([0, 0, 2]), True),
           (Vector([1, 1, 2]), True),
           (Vector([1, 1, -2]), False)]

    for pt, res in pts:
        pt_is_in_plane_dir(p0, p_normal, pt)
        assert pt_is_in_plane_dir(p0, p_normal, pt) == res

