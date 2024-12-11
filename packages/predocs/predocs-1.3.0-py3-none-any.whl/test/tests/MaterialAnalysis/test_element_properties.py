"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
import os

import pytest
import numpy as np

from PreDoCS.CrossSectionAnalysis.Processors import SongCrossSectionProcessor
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElementStiffness,\
    CompositeElementStiffness, CompositeElement
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.data import save_divide
from PreDoCS.util.vector import Vector
from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry

log = get_module_logger(__name__)

try:
    from lightworks.opti.config import OptimisationControl
    from lightworks.opti.gradients.gradients_config import GradientsControl
    from lightworks.opti.gradients.utils import complex_step_derivative, finite_difference, reshape_abd_matrix
    from lightworks.opti.optimisation_model import OptimisationModel
    from lightworks.mechana.constraints.constraint_processor import ConstraintProcessor
    from PreDoCS.SolverInterface.SolverInterfaceLightworks import PreDoCS_SolverLightworks
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
except ImportError:
    log.warning('Lightworks not installed')


@pytest.mark.unit_tests
def test_element_stiffness_calculation(alu, laminate1):
    # Isotropic Element
    IsotropicElementStiffness.from_isotropic_shell(alu)
    IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='with_poisson_effect')
    IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='without_poisson_effect')
    IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='wiedemann')
    IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='song')
    with pytest.raises(RuntimeError):
        IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='unknown')
        
    # Composite Element
    CompositeElementStiffness.from_isotropic_shell(alu)
    CompositeElementStiffness.from_composite_shell(laminate1)


@pytest.mark.unit_tests
def test_element_stiffness_compare(alu, laminate1):
    # Isotropic Element
    i1 = IsotropicElementStiffness.from_isotropic_shell(alu)
    i2 = IsotropicElementStiffness.from_composite_shell(laminate1, engineering_constants_method='with_poisson_effect')
        
    # Composite Element
    c1 = CompositeElementStiffness.from_isotropic_shell(alu)
    c2 = CompositeElementStiffness.from_composite_shell(laminate1)
    
    # Tests
    assert i1 == i1
    assert i1 != i2
    assert c1 == c1
    assert c1 != c2
    with pytest.raises(TypeError):
        i1 == c1
    with pytest.raises(TypeError):
        c1 == i1


@pytest.mark.unit_tests
def test_stress_states_from_strain_state_functions(alu, laminate1):
    # Isotropic Element
    element_stiffness = IsotropicElementStiffness.from_isotropic_shell(alu)
    stress_state = element_stiffness.stress_state_from_strain_state_function(
        {'normal_strain': lambda s: 1e-5, 'shear_strain': lambda s: 1e-5})
    assert 'normal_flow' in stress_state
    assert 'shear_flow' in stress_state
    
    # Composite Element
    element_stiffness = CompositeElementStiffness.from_composite_shell(laminate1)
    stress_state_functions = SongCrossSectionProcessor.stress_state_from_strain_state_function(
        element_stiffness.K_Song,
        element_stiffness.A_s,
        {'epsilon_zz_0': lambda s: 1e-5,
         'gamma_zs': lambda s: 1e-5,
         'kappa_zz': lambda s: 1e-5,
         'gamma_zn': lambda s: 1e-5})
    assert 'N_zz' in stress_state_functions
    assert 'N_zs' in stress_state_functions
    assert 'N_zn' in stress_state_functions
    assert 'N_sn' in stress_state_functions
    assert 'M_zz' in stress_state_functions
    assert 'M_zs' in stress_state_functions


@pytest.mark.unit_tests
def test_composite_element_stiffness_calculations(laminate1):
    element_stiffness = CompositeElementStiffness.from_composite_shell(laminate1)
    element_stiffness.torsion_compliance


@pytest.mark.unit_tests
def test_composite_element_calculations(laminate1):
    component1 = DiscreetCrossSectionGeometry.Component(1, laminate1)

    n1 = DiscreetCrossSectionGeometry.Node(1, Vector([1.1, 1.3]))
    n2 = DiscreetCrossSectionGeometry.Node(2, Vector([4.5, 6.8]))
    n3 = DiscreetCrossSectionGeometry.Node(3, Vector([2, 1]))

    e1 = CompositeElement(1, n1, n2, component1)
    e2 = CompositeElement(2, n2, n3, component1)
    e3 = CompositeElement(3, n3, n1, component1)
    elements = [e3, e1, e2]

    discreet_geometry = DiscreetCrossSectionGeometry()
    discreet_geometry.add_elements(elements)
    assert e1.r_midsurface(discreet_geometry, Vector([5.4, 2.7]))
    # element.r_nodes(Vector([5.4, 2.7]))
    assert e1.q_midsurface(discreet_geometry, e1.length / 2., Vector([5.4, 2.7]))


def init_elementproperties(param, optimisation_model):
    """
    init of ElementProperties/CompositeElementStiffness

    Parameters
    ----------
    param: np.ndarray
                vector of dimension 9 with A-Matrix of in-plane stiffness (3x3)

    optimisation_model:
                Optimisation_model

    Returns
    ----------
    diff of C[0,0], ..., C[0,4] to A_11, ..., A_66
    """
    dtype = param.dtype
    skin = optimisation_model.structural_model.base_parts[0].skin
    abd = np.array(optimisation_model.structural_model.base_parts[0].abd, dtype=dtype)

    # Update the optimisation_model
    abd[:3, :3] = reshape_abd_matrix(param)
    optimisation_model.structural_model.base_parts[0].abd = abd
    optimisation_model.solver.update_structural_model()

    # Calc element stiffness
    A = abd[:3, :3]
    B = abd[:3, 3:]
    D = abd[3:, 3:]
    A_s = skin.a_s
    t = skin.thickness
    density = skin.density

    A_dict = {11: A[0, 0], 22: A[1, 1], 66: A[2, 2], 12: A[0, 1], 16: A[0, 2], 26: A[1, 2]}
    B_dict = {11: B[0, 0], 22: B[1, 1], 66: B[2, 2], 12: B[0, 1], 16: B[0, 2], 26: B[1, 2]}
    D_dict = {11: D[0, 0], 22: D[1, 1], 66: D[2, 2], 12: D[0, 1], 16: D[0, 2], 26: D[1, 2]}
    A_s_dict = {44: A_s[0, 0], 55: A_s[1, 1], 45: A_s[0, 1]}

    return CompositeElementStiffness(t, density, A_dict, B_dict, D_dict, A_s_dict, dtype=dtype).K_Jung


@pytest.mark.lightworks_required
def test_element_stiffness_matrix_differentiate(data_dir):
    """
    Comparison FD and CS
    """
    # FD
    grad_ctrl_1 = GradientsControl(gradient_estimation_mode='modular_default', solver_gradient_mode='modular_fd')
    OptimisationControl(
        parameter_selection={'thickness_skin': True},
        parallel=False,
        strength_criteria=['max_strain'],
        gradient_options=grad_ctrl_1.get_config(),
    )
    input_cpacs = 'Beam_Composite_bending_opti.xml'
    input_cpacs_path = os.path.join(data_dir, 'CPACS')
    predocs_ctrl = PreDoCS_SolverControl(
        cpacs_file=input_cpacs,
        cpacs_path=input_cpacs_path,
        wing_idx=0,
        orientation='load_reference_points',
        node_placement=6,
        processor_type='Hybrid',
        hybrid_processor='Jung',
        element_length=0.1,
        segment_deflection=None,
        parallel_process=False,
        engineering_constants_method='with_poisson_effect',
        front_spar_uid='MidSpar',
        rear_spar_uid='MidSpar',
    )

    solver = PreDoCS_SolverLightworks(predocs_ctrl)
    solver.build_model()
    opti_model_1 = OptimisationModel(
        solver.structural_model,
        solver,
        ConstraintProcessor().from_assembly(solver.structural_model, solver),
    )
    opti_model_1.solve()
    panel_stiffness_a_fd = reshape_abd_matrix(opti_model_1.structural_model.base_parts[0].abd[:3,:3])
    gradients_1 = finite_difference(init_elementproperties, panel_stiffness_a_fd, None, None, False, None, 'f', opti_model_1)

    # CS
    grad_ctrl_2 = GradientsControl(gradient_estimation_mode='modular_default', solver_gradient_mode='modular_cs')
    OptimisationControl(
        parameter_selection={'thickness_skin': True},
        parallel=False,
        strength_criteria=['max_strain'],
        gradient_options=grad_ctrl_2.get_config(),
    )
    opti_model_2 = OptimisationModel(
        solver.structural_model,
        solver,
        ConstraintProcessor().from_assembly(solver.structural_model, solver),
    )
    opti_model_2.solve()
    panel_stiffness_a_cs = reshape_abd_matrix(opti_model_2.structural_model.base_parts[0].abd[:3,:3])
    gradients_2 = complex_step_derivative(init_elementproperties, panel_stiffness_a_cs, None, None, False, None, None, opti_model_1)

    # Compare
    grad_diff_abs = gradients_2 - gradients_1
    grad_diff_rel = save_divide(grad_diff_abs, gradients_1)
    # log.info(f'Gradient FD: {gradients_1}')
    # log.info(f'Gradient CS: {gradients_2}')
    # log.info(f'Abs diff: {grad_diff_abs}')
    # log.info(f'Rel diff: {grad_diff_rel}')
    assert np.all(grad_diff_abs.all() <= 1e-8)
