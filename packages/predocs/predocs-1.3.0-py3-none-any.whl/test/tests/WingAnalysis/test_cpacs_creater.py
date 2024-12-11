"""
This module contains tests with regard to CPACS_WingCreater

@date: 15.01.2021
@author: Swapan, Madabhushi Venkata <>
@author: Edgar, Werthen <>
@Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center)
<www.dlr.de>. All rights reserved.
"""

#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import numpy as np
import pandas as pd
import pytest

from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from lightworks.cpacs_interface.cpacs_interface_lightworks import CPACSInterfaceLightworks
    from lightworks.mechana.materials.materiallaws import Orthotropic
except ImportError:
    log.warning('Lightworks not installed')

pytestmark = pytest.mark.lightworks_required


def test_write_materials_cpacs(data_dir):
    """
    Tests if the materials in the csv are consistent with material properties by checking if all the eigen values
    of compliance matrix are positive.

    TODO: Use more reliable material data for testing in future
    Assumptions made in this materials.csv:
    E3 = E2
    G23 = G13
    nu13 = nu12 except for biax nu23 = nu13 = 0.28 (due to lack of information)
    Xt_2(uniax) = Xt_3(uniax) = Xt_3(biax) = Xt_3(triax)
    Xc_2(uniax) = Xc_3(uniax) = Xc_3(biax) = Xc_3(triax)
    epsilon_t_2(uniax) = epsilon_t_3(uniax) = epsilon_t_3(biax) = epsilon_t_3(triax)
    epsilon_c_2(uniax) = epsilon_c_3(uniax) = epsilon_c_3(biax) = epsilon_c_3(triax)

    """
    materials = pd.read_csv(os.path.join(data_dir, 'CPACS/materials_test.csv'), sep=';', skiprows=1,
                            names=['material_name', 'Reference', 'density', 'fiber_volume_fraction',
                                   'E1', 'E2', 'E3', 'G12', 'G23', 'G13', 'nu12', 'nu23', 'nu13',
                                   'Xt1', 'Xt2', 'Xt3', 'Xc1', 'Xc2', 'Xc3', 'tau_12', 'epsilon_t_1',
                                   'epsilon_t_2', 'epsilon_t_3', 'epsilon_c_1', 'epsilon_c_2', 'epsilon_c_3'])
    cpacs_interface = CPACSInterfaceLightworks(directory=os.path.join(data_dir, 'CPACS'), filename='Beam_Test.xml')
    cpacs_interface.add_materials_from_table(materials)

    for i, row in materials.iterrows():
        material = Orthotropic(E_11=float(row['E1']) * 1e09, E_22=float(row['E2']) * 1e09,
                               E_33=float(row['E3']) * 1e09, G_23=float(row['G23']) * 1e09,
                               G_12=float(row['G12']) * 1e09, G_13=float(row['G13']) * 1e09,
                               nu_13=float(row['nu13']), nu_12=float(row['nu12']),
                               nu_23=float(row['nu23']), name=row['material_name'],
                               density=float(row['density']))
        cpacs_material = cpacs_interface.get_material(row['material_name'])
        assert np.allclose(cpacs_material.compliance_matrix, material.compliance_matrix)
