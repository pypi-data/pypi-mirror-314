"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
import numpy as np
from _pytest.python_api import approx
import pytest


def load_ABD_from_file(file):
    ABD = np.loadtxt(file)
    A = ABD[0:3, 0:3]
    D = ABD[3:6, 3:6]
    B1 = ABD[0:3, 3:6]
    B2 = ABD[3:6, 0:3]
    assert np.array_equal(B1, B2)
    return A, B1, D


@pytest.mark.unit_tests
def test_ABD(data_dir, laminate1, laminate2):
    laminate_list = [
        (laminate2, None, os.path.join(data_dir, 'elamx2', 'laminate2.txt')),
        (laminate1, None, os.path.join(data_dir, 'elamx2', 'laminate1.txt')),
        (laminate1, 0.0, os.path.join(data_dir, 'elamx2', 'laminate1_reference_plane.txt')),
    ]
    for laminate, reference_surface, laminate_file in laminate_list:
        # ELAMX starts at the positive end of the laminate (+n), PreDoCS at the negative (-n)
        laminate.layup.reverse()
        
        # PreDoCS calculation
        A, B, D, A_s = laminate.get_ABD_matrices(reference_surface)
        # TODO: test A_s
        
        # ELAMX data
        A_ref, B_ref, D_ref = load_ABD_from_file(laminate_file)
        
        # ELAMX: mm -> PreDoCS: m
        A_ref *= 1e3
        #B_ref *= 1e3
        D_ref /= 1e3
        
        # Test
        assert approx(A.flatten(), abs=1e-3, rel=1e-6) == A_ref.flatten()
        assert approx(B.flatten(), abs=1e-3, rel=1e-6) == B_ref.flatten()
        assert approx(D.flatten(), abs=1e-3, rel=1e-6) == D_ref.flatten()


@pytest.mark.unit_tests
def test_engineering_constants(laminate1, laminate2):
    laminate_list = [(laminate1, None,
                      {'E_x': 78854.6, 'E_y': 38324.6, 'G_xy': 14282.2, 't': 2.208},
                      {'E_x': 83010.8, 'E_y': 40344.6, 'G_xy': 14282.2, 't': 2.208}),
                     (laminate1, 0.0,
                      {'E_x': 25068.1, 'E_y': 3860.2, 'G_xy': 2487.1, 't': 2.208},
                      {'E_x': 83010.8, 'E_y': 40344.6, 'G_xy': 14282.2, 't': 2.208}),
                     (laminate2, None,
                      {'E_x': 10040.1, 'E_y': 33403.5, 'G_xy': 6713.6, 't': 2},
                      {'E_x': 24636.9, 'E_y': 88636.2, 'G_xy': 19323.2, 't': 2})]
    # Tests
    for laminate, reference_surface, engineering_constants_with_poisson_effect, engineering_constants_without_poisson_effect in laminate_list:
        # With poisson effect
        E_1, E_2, G = laminate.get_engineering_constants(method='with_poisson_effect', reference_surface=reference_surface)
        assert approx(E_1 / 1e6, abs=1, rel=1e-4) == engineering_constants_with_poisson_effect['E_x']
        assert approx(E_2 / 1e6, abs=1, rel=1e-4) == engineering_constants_with_poisson_effect['E_y']
        assert approx(G / 1e6, abs=1, rel=1e-4) == engineering_constants_with_poisson_effect['G_xy']
        assert approx(laminate.thickness * 1e3) == engineering_constants_with_poisson_effect['t']
         
        # Without poisson effect
        E_1, E_2, G = laminate.get_engineering_constants(method='without_poisson_effect', reference_surface=reference_surface)
        assert approx(E_1 / 1e6, abs=1, rel=1e-4) == engineering_constants_without_poisson_effect['E_x']
        assert approx(E_2 / 1e6, abs=1, rel=1e-4) == engineering_constants_without_poisson_effect['E_y']
        assert approx(G / 1e6, abs=1, rel=1e-4) == engineering_constants_without_poisson_effect['G_xy']
        assert approx(laminate.thickness * 1e3) == engineering_constants_without_poisson_effect['t']
    