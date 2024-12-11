"""
This Module offers the possibility to build up a PreDoCS coordinate system and transform loads on beam nodes.
TODO write this module
codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import numpy as np
import pytest

from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
    from PreDoCS.SolverInterface.SolverInterfacePreDoCS import PreDoCS_SolverPreDoCS
except ImportError:
    log.warning('cpacs_interface not installed')

try:
    from lightworks.opti.gradients.gradients_config import GradientsControl
    from lightworks.opti.gradients.gradients_solver import _read_panel_loads, SolverGradients
    from lightworks.opti.optimisation_model import OptimisationModel
    from lightworks.mechana.constraints.constraint_processor import ConstraintProcessor
    from lightworks.opti.config import OptimisationControl
    from lightworks.opti.gradients.utils import reshape_abd_matrix
    from test.tests.SolverInterface.test_SolverInterfaceLightworks import create_model_lightworks, stiffness_step
except ImportError:
    log.warning('Lightworks not installed')


pytestmark = pytest.mark.cpacs_interface_required


def test_external_loads(data_dir):
    input_cpacs_file = "Rect_Beam_external_load.xml"
    input_cpacs_path = os.path.join(data_dir, 'CPACS')

    # Solver and structural model
    predocs_ctrl = PreDoCS_SolverControl(cpacs_file=input_cpacs_file,
                                         cpacs_path=input_cpacs_path,
                                         wing_idx=0,
                                         orientation='load_reference_points',
                                         loads_are_internal_loads=False,
                                         node_placement=6,
                                         processor_type='Hybrid',
                                         element_length=None,
                                         segment_deflection=5e-3,
                                         parallel_process=False,
                                         engineering_constants_method='with_poisson_effect',
                                         hybrid_processor='Jung',
                                         front_spar_uid=None,
                                         rear_spar_uid=None)

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # Test loads
    loads_proc = solver.load_processor
    lc_name = list(loads_proc.load_cases_interpolated_nodes.keys())[0]
    assert loads_proc.load_cases_interpolated_nodes[lc_name].length == 6
    # assert loads_proc.load_cases_nodal[lc_name].length == 6
    assert len(loads_proc.load_cases_elements) == 0


def test_internal_loads(data_dir):
    input_cpacs_file = "Rect_Beam_internal_load.xml"
    input_cpacs_path = os.path.join(data_dir, 'CPACS')


    # Solver and structural model
    predocs_ctrl = PreDoCS_SolverControl(cpacs_file=input_cpacs_file,
                                         cpacs_path=input_cpacs_path,
                                         wing_idx=0,
                                         orientation='load_reference_points',
                                         loads_are_internal_loads=True,
                                         node_placement=6,
                                         processor_type='Hybrid',
                                         element_length=None,
                                         segment_deflection=5e-3,
                                         parallel_process=False,
                                         engineering_constants_method='with_poisson_effect',
                                         hybrid_processor='Jung',
                                         front_spar_uid=None,
                                         rear_spar_uid=None)

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # Test loads
    loads_proc = solver.load_processor
    lc_name = list(loads_proc.load_cases_interpolated_nodes.keys())[0]

    nodal_loads = loads_proc.load_cases_interpolated_nodes[lc_name]
    assert nodal_loads.length == 6
    # assert loads_proc.load_cases_nodal[lc_name].length == 6

    element_loads = loads_proc.load_cases_elements[lc_name]
    assert element_loads.length == 5

    force = 5e4
    assert np.allclose(nodal_loads.fx, 0)
    assert np.allclose(nodal_loads.fy, force)
    assert np.allclose(nodal_loads.fz, 0)

    assert np.allclose(element_loads.fx, 0)
    assert np.allclose(element_loads.fy, force)
    assert np.allclose(element_loads.fz, 0)

    lever_nodes = 10/5 * np.array([5, 4, 3, 2, 1, 0])
    assert np.allclose(nodal_loads.mx, -force * lever_nodes, atol=3e2)
    assert np.allclose(nodal_loads.my, 0, atol=1e2)
    assert np.allclose(nodal_loads.mz, 0, atol=1e2)

    lever_elements = np.array([9, 7, 5, 3, 1])
    assert np.allclose(element_loads.mx, -force * lever_elements, rtol=5e-3)
    assert np.allclose(element_loads.my, 0, atol=1e2)
    assert np.allclose(element_loads.mz, 0, atol=1e2)


def test_external_loads2(data_dir):
    # CPACS file with internal loads but external loads SolverControl
    input_cpacs_file = "Rect_Beam_internal_load.xml"
    input_cpacs_path = os.path.join(data_dir, 'CPACS')

    # Solver and structural model
    predocs_ctrl = PreDoCS_SolverControl(cpacs_file=input_cpacs_file,
                                         cpacs_path=input_cpacs_path,
                                         wing_idx=0,
                                         orientation='load_reference_points',
                                         loads_are_internal_loads=False,
                                         node_placement=6,
                                         processor_type='Hybrid',
                                         element_length=None,
                                         segment_deflection=5e-3,
                                         parallel_process=False,
                                         engineering_constants_method='with_poisson_effect',
                                         hybrid_processor='Jung',
                                         front_spar_uid=None,
                                         rear_spar_uid=None)

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    with pytest.raises(AssertionError):
        solver.build_model()


def test_internal_loads2(data_dir):
    # CPACS file with external loads but internal loads SolverControl
    input_cpacs_file = "Rect_Beam_external_load.xml"
    input_cpacs_path = os.path.join(data_dir, 'CPACS')

    # Solver and structural model
    predocs_ctrl = PreDoCS_SolverControl(cpacs_file=input_cpacs_file,
                                         cpacs_path=input_cpacs_path,
                                         wing_idx=0,
                                         orientation='load_reference_points',
                                         loads_are_internal_loads=True,
                                         node_placement=6,
                                         processor_type='Hybrid',
                                         element_length=None,
                                         segment_deflection=5e-3,
                                         parallel_process=False,
                                         engineering_constants_method='with_poisson_effect',
                                         hybrid_processor='Jung',
                                         front_spar_uid=None,
                                         rear_spar_uid=None)

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    with pytest.raises(AssertionError):
        solver.build_model()


def test_plot_load_envelopes(data_dir, tmp_dir):
    input_cpacs_file = "analytical_example_circ_beam_loads_CPACS.xml"
    input_cpacs_path = os.path.join(data_dir, 'CPACS')

    # Solver and structural model
    predocs_ctrl = PreDoCS_SolverControl(cpacs_file=input_cpacs_file,
                                         cpacs_path=input_cpacs_path,
                                         wing_idx=0,
                                         orientation='load_reference_points',
                                         loads_are_internal_loads=True,
                                         node_placement=6,
                                         processor_type='Hybrid',
                                         element_length=None,
                                         segment_deflection=5e-3,
                                         parallel_process=False,
                                         engineering_constants_method='with_poisson_effect',
                                         hybrid_processor='Jung',
                                         front_spar_uid=None,
                                         rear_spar_uid=None)

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # Load Processor
    loads_proc = solver.load_processor

    # loads_proc.plot_load_envelopes(
    #     loads_type='forces',
    #     one_plot=False,
    #     file_format_str=os.path.join(tmp_dir, 'envelope_forces_{}.png'),
    # )
    # loads_proc.plot_load_envelopes(
    #     loads_type='moments',
    #     one_plot=False,
    #     file_format_str=os.path.join(tmp_dir, 'envelope_moments_{}.png'),
    # )

    loads_proc.plot_load_envelopes(
        loads_type='forces',
        one_plot=True,
        file_format_str=os.path.join(tmp_dir, 'envelope_forces.png'),
    )
    loads_proc.plot_load_envelopes(
        loads_type='moments',
        one_plot=True,
        file_format_str=os.path.join(tmp_dir, 'envelope_moments.png'),
    )


@pytest.mark.lightworks_required
def test_loads_complexstep(data_dir):
    """
    Test for complex stiffness to complex loads
    """
    grad_ctrl = GradientsControl(gradient_estimation_mode='modular_default', solver_gradient_mode='modular_cs')
    OptimisationControl(
        parameter_selection={'individual_thickness': True},
        parallel=False,
        strength_criteria=['max_strain'],
        gradient_options=grad_ctrl.get_config(),
    )

    structural_model, solver = create_model_lightworks(
        data_dir, "Beam_Composite_bending_opti.xml", num_beam_nodes=6, use_lp=True,
    )

    constraint_processor = ConstraintProcessor.from_assembly(structural_model, solver)
    opt_model = OptimisationModel(
        structural_model=structural_model,
        solver=solver,
        constraint_processor=constraint_processor,
    )
    solver_gradients_processor = SolverGradients(opt_model, parallel=False)

    # complex stiffness
    panel_stiffness = reshape_abd_matrix(opt_model.structural_model.base_parts[0].abd) + 0j
    # Add a step to one stiffness
    panel_stiffness[0] = panel_stiffness[0] + 2 ** -100j
    stiffness = stiffness_step(panel_stiffness, opt_model)
    complex_number = 0
    for i in range(len(stiffness)):
        if stiffness[i].imag != 0:
            complex_number += 1
    assert complex_number != 0
