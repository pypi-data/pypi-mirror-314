#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import numpy as np
import pytest

from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.inout import write_cloudpickle, read_cloudpickle

log = get_module_logger(__name__)

try:
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
    from PreDoCS.SolverInterface.SolverInterfacePreDoCS import PreDoCS_SolverPreDoCS
except ImportError:
    log.warning('cpacs_interface not installed')


pytestmark = pytest.mark.cpacs_interface_required


def create_model(data_dir, cpacs_file, num_beam_nodes=10, use_lp=False, **kwargs):
    # Control section
    ctrl = PreDoCS_SolverControl(
        cpacs_file=cpacs_file,
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        wing_idx=0,
        orientation='root-tip',
        node_placement=num_beam_nodes,
        processor_type='Hybrid',
        hybrid_processor='Jung',
        element_length=0.1,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        use_lp=use_lp,
        **kwargs
    )

    # Initialise Model
    model = PreDoCS_SolverPreDoCS(ctrl)

    # Create Model
    model.build_model()

    return model


def test_solver_internal_loads_beam_displacements(data_dir):
    # Import structural model
    model_ext = create_model(
        data_dir, "Rect_Beam_external_load.xml", num_beam_nodes=6)
    model_int = create_model(
        data_dir, "Rect_Beam_internal_load.xml", num_beam_nodes=6, loads_are_internal_loads=True)

    # Calculate bending with PreDoCS in PreDoCS coordinates
    selected_load_case = 'test_load_case1'
    beam_displacement_function_ext = model_ext.beam_displacement_function_dict[selected_load_case]
    beam_displacement_function_int = model_int.beam_displacement_function_dict[selected_load_case]

    z_comp = np.linspace(0, model_ext.predocs_coord.beam_length, 50)
    beam_displacements_ext = np.array([beam_displacement_function_ext(z) for z in z_comp])
    beam_displacements_int = np.array([beam_displacement_function_int(z) for z in z_comp])

    # # DEBUG
    # model_ext.plot_beam_displacements(selected_load_case, file=r'H:\ext.png')
    # model_int.plot_beam_displacements(selected_load_case, file=r'H:\int.png')
    # beam_displacements_diff = beam_displacements_int - beam_displacements_ext
    # beam_displacements_diff_rel = beam_displacements_diff / beam_displacements_ext

    assert np.allclose(beam_displacements_int, beam_displacements_ext, atol=1e-2, rtol=1e-2)


def test_beam_bending(data_dir):
    # Import structural model
    model = create_model(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    # Beam data
    pi = np.pi
    thickness = 0.001
    diameter_outside = 1
    diameter_inside = diameter_outside - 2 * thickness
    length = 10
    E = 71008206015.79999

    # Moment of inertia in CPACS Coordinates
    I_pipe = (pi * (diameter_outside**4 - diameter_inside**4)) / (32 * diameter_outside)
    Ix = I_pipe + (thickness * diameter_inside**3)/12  # Ix = I_pipe + I_spar (vertically)
    Iz = I_pipe + (thickness**3 * diameter_inside)/12  # Ix = I_pipe + I_spar (horizontally)

    # Force in CPACS Coordinates
    Fx = -15000
    Fz = 15000

    # Bending in CPACS Coordinates
    u_bernoulli = (Fx * length**3) / (3 * E * Iz)
    w_bernoulli = (Fz * length**3) / (3 * E * Ix)

    # Calculate bending with PreDoCS in PreDoCS coordinates
    displacement_vector = model.beam_displacement_function_dict['bending'](length)
    u_PreDoCS = displacement_vector[0]
    v_PreDoCS = displacement_vector[1]

    u_discrepancy = (u_PreDoCS + u_bernoulli)/u_PreDoCS
    v_discrepancy = (v_PreDoCS - w_bernoulli)/v_PreDoCS

    assert u_discrepancy < 0.5, 'PreDoCS calculation is too far away from the Euler beam Theory'
    assert v_discrepancy < 0.5, 'PreDoCS calculation is too far away from the Euler beam Theory'


def test_opt_ctrl_protocol(data_dir, tmp_path):
    ctrl = PreDoCS_SolverControl(
        cpacs_file="Beam_Composite.xml",
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        wing_idx=1,
        orientation='load_reference_points',
        node_placement=6,
        processor_type='Hybrid',
        hybrid_processor='Song',
        element_length=0.05,
        segment_deflection=None,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect'
    )

    ctrl.write_to_protocol(path=tmp_path, name='test_protocol.xlsx')

    ctrl.element_length = 0.1

    ctrl.write_to_protocol(path=tmp_path, name='test_protocol.xlsx')

    ctrl.read_from_protocol(path=tmp_path, name='test_protocol.xlsx', nr=1)

    assert ctrl.element_length == 0.05

    ctrl.read_from_protocol(path=tmp_path, name='test_protocol.xlsx', nr=2)

    assert ctrl.element_length == 0.1


def test_pickle(data_dir, tmp_dir):
    solver = create_model(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    # Post process Model
    log.info('Stresses created successfully')

    # Test pickle
    file_name = os.path.join(tmp_dir, 'solver.p')
    write_cloudpickle(os.path.join(tmp_dir, 'solver.p'), solver)
    solver2 = read_cloudpickle(file_name)
