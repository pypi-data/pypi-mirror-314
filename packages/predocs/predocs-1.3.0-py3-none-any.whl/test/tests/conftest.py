"""
Created on 20.07.2018

@author: Daniel
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import matplotlib
import numpy as np
import pytest
import logging

from PreDoCS.MaterialAnalysis.Materials import Transverse_Isotropic, Isotropic
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell, CompositeShell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.globals import core_init

matplotlib.use('agg')

# Configure NumPy to treat warnings as exceptions
np.seterr(all='raise')

# Init logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
core_init('.')
log = get_module_logger(__name__)


try:
    from lightworks.opti.config import OptimisationControl

    @pytest.fixture(autouse=True)
    def reset_optimisation_control():
        OptimisationControl().reset()
        yield
except ImportError:
    log.warning('Lightworks not installed')


@pytest.fixture(scope='session')
def predocs_root_dir():
    return os.path.abspath(os.path.join(__file__, '..',  '..',  '..'))


@pytest.fixture(scope='session')
def data_dir(predocs_root_dir):
    return os.path.abspath(os.path.join(predocs_root_dir, 'test',  'data'))


@pytest.fixture(scope='session')
def profiles_path(data_dir):
    return os.path.join(data_dir, 'profiles')


@pytest.fixture(scope='session')
def tmp_dir(predocs_root_dir):
    return os.path.abspath(os.path.join(predocs_root_dir, 'tmp'))


@ pytest.fixture(scope='session')
def ansys_working_path(predocs_root_dir):
    return os.path.abspath(os.path.join(predocs_root_dir, 'test',  'ANSYS'))


@pytest.fixture
def alu_material():
    return Isotropic(71e9, 0.32, name='Alu', density=2820)


@pytest.fixture
def alu(alu_material):
    return IsotropicShell(alu_material, 2e-2, name='Alu2')


@pytest.fixture
def alu_thick(alu_material):
    return IsotropicShell(alu_material, 5e-2, name='Alu5')


@pytest.fixture
def ply():
    return Transverse_Isotropic(
        134.7e9, 7.7e9, 0.369, 0.5, 4.2e9, name='Hexcel T800/M21', density=1590,
    )


@pytest.fixture
def ply_thickness():
    return 0.184e-3


@pytest.fixture
def laminate1(ply, ply_thickness, orientation=0):
    return CompositeShell(
        name='Laminate 1',
        layup=[
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation+45.0),
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation-45.0),
            (ply, ply_thickness, orientation+90.0),
            (ply, ply_thickness, orientation+90.0),
            (ply, ply_thickness, orientation-45.0),
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation+45.0),
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation),
        ],
    )


@pytest.fixture
def laminate2(ply, ply_thickness, orientation=0):
    return CompositeShell(
        name='Laminate 2',
        layup=[
            (ply, 1e-3, orientation-45.0),
            (ply, 1e-3, orientation+90.0),
        ],
    )


@pytest.fixture
def laminate3(ply, ply_thickness, orientation=0):
    return CompositeShell(
        name='Laminate3',
        layup=[
            (ply, ply_thickness, orientation),
            (ply, ply_thickness, orientation),
            (ply, 2*ply_thickness, orientation+45.0),
        ],
    )


@pytest.fixture
def cs_definition(data_dir, alu, alu_thick):
    from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import load_profile_points, \
        WingCrossSectionGeometryDefinition
    from PreDoCS.util.vector import Vector

    geometry_points = load_profile_points(os.path.join(data_dir, 'profiles', 'NACA-2412-cos-50.txt'), True)
    cs_definition = WingCrossSectionGeometryDefinition(
        geometry_points,
        alu,
        material_regions=[
            ((Vector([0.819834, 0.034369]), Vector([0.594684, 0.064054])), alu_thick),
        ],
        webs=[
            ((Vector([0.3, -1]), Vector([0.3, 2])), alu_thick),
            ((Vector([0.5, -1]), Vector([0.5, 2])), alu),
        ],
        material_region_lines=[
            ((Vector([0.3, -1]), Vector([0.3, 2])), alu_thick),
        ],
    )
    return cs_definition
