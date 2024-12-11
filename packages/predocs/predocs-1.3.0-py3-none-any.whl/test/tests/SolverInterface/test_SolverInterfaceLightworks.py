"""
Project description:
Maintainer:

.. codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
.. created:: 08.03.2019
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
import pickle
import time
from copy import deepcopy
from time import time

import h5py
import numpy as np
import pytest

from PreDoCS.WingAnalysis.Display import plot_beam_displacements, plot_beam_internal_loads, \
    plot_beam_cross_section_displacements
from PreDoCS.util.data import save_divide
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.geometry import transform_location_m
from PreDoCS.util.inout import write_json, read_json, read_cloudpickle, write_cloudpickle
from PreDoCS.util.filters import modified_kwargs
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)

try:
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
except ImportError:
    log.warning('cpacs_interface not installed')

try:
    from lightworks.mechana import criteria
    from lightworks.mechana.loads.loadstate_processor import get_design_load_cases
    from lightworks.mechana.constraints.constraint_processor import ConstraintProcessor
    from lightworks.opti.config import OptimisationControl
    from lightworks.opti.gradients.gradients_config import GradientsControl
    from lightworks.opti.optimisation_model import OptimisationModel
    from lightworks.opti.optimisation_interface import OptimisationInterface
    from lightworks.opti.result_postprocessors.spanwise_plots import plot_and_save_graphs
    from lightworks.structural_model_generator.structural_model_writer import write_structural_model
    from lightworks.opti.gradients.gradients_solver import _read_panel_loads, SolverGradients
    from lightworks.opti.gradients.utils import reshape_abd_matrix, complex_step_derivative
    from PreDoCS.SolverInterface.SolverInterfaceLightworks import PreDoCS_SolverLightworks
except ImportError:
    log.warning('Lightworks not installed')


pytestmark = pytest.mark.lightworks_required


testdata = [
    ('Beam', True, False, False, 'thickness_skin', 'Hybrid', 'Song', False),
    ('Beam', True, False, False, 'thickness_skin', 'Hybrid', 'Jung', False),
    ('Beam', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('Beam', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', True),
    ('Beam', True, False, False, 'individual_thickness', 'Hybrid', 'JungWithoutWarping', False),
    pytest.param('Beam', True, False, False, 'lp', 'Hybrid', 'JungWithoutWarping', False,
                 marks=pytest.mark.xfail(reason="No LP back transformation", raises=NotImplementedError)),
    # ('Beam', True, False, False, 'lp', 'Hybrid', 'JungWithoutWarping', True),
    ('IEA-LA', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('IEA-3D', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('simple', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('Beam_kink', False, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('Beam_kink_loadaxis', False, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
    ('Beam_node', True, False, False, 'thickness_skin', 'Hybrid', 'JungWithoutWarping', False),
]
@pytest.mark.parametrize('case_name, optimise, set_initial, reload_file, optimization_param, processor_type,'
                         ' hybrid_processor, converged_results', testdata)
def test_solver_interface(data_dir, tmp_path, case_name, optimise, set_initial,
                          reload_file, optimization_param,
                          processor_type, hybrid_processor, converged_results):
    cpacs_path = os.path.join(data_dir, 'CPACS')
    opt_ctrl_path = os.path.join(data_dir, 'optimization_control')
    initial_thickness = 0.025
    plot_cs_idx = 1
    plot_lc_name = 'bending'
    parallel_process_optimisation = converged_results
    deflection_constraint = False

    # General settings
    predocs_solver_control_defaults = dict(
        cpacs_path=cpacs_path,
        wing_idx=0,
        processor_type=processor_type,
        loads_are_internal_loads=False,
        element_length=None,
        segment_deflection=1e-3,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        hybrid_processor=hybrid_processor,
        front_spar_uid=None,
        rear_spar_uid=None,
        calc_element_load_state_functions=True,
        calc_element_load_state_min_max=False,
    )

    # Control section
    if case_name == 'Beam_kink':
        output_file = "Beam_Composite_bending_kink_cell_without_spar_internal_loads_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'base_config.conf')
        plot_lc_name = 'bending'
        predocs_solver_control_dict = dict(
            cpacs_file="Beam_Composite_bending_kink_cell_without_spar_internal_loads.xml",
            orientation='3d-beam',
            node_placement=7,
            loads_are_internal_loads=True,
        )

    elif case_name == 'Beam_kink_loadaxis':
        output_file = "Beam_Composite_bending_kink_cell_without_spar_external_loads_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'base_config.conf')
        plot_lc_name = 'bending'
        predocs_solver_control_dict = dict(
            cpacs_file="Beam_Composite_bending_kink_cell_without_spar_external_loads.xml",
            orientation='load_reference_points',
            node_placement=7,
        )

    elif case_name == 'Beam_node':
        output_file = "Beam_Composite_bending_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'base_config.conf')
        plot_lc_name = 'bending'
        predocs_solver_control_dict = dict(
            cpacs_file="Beam_Composite_bending_opti.xml",
            orientation='load_reference_points',
            node_placement=np.linspace(0, 9.98, 6).tolist(),
        )

    elif case_name == 'simple':
        output_file = "simple_beam_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'base_config.conf')
        plot_lc_name = 'fx_max'
        predocs_solver_control_dict = dict(
            cpacs_file="simple_beam.xml",
            orientation='load_reference_points',
            node_placement=7,
            loads_are_internal_loads=True,
        )

    elif case_name == 'IEA-LA':
        output_file = "IEA-15-240-RWT_CPACS_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'IEA_config.conf')
        plot_lc_name = 'fz_max'
        predocs_solver_control_dict = dict(
            cpacs_file="IEA-15-240-RWT_CPACS.xml",
            orientation='load_reference_points',
            node_placement=6,
            loads_are_internal_loads=True,
        )

    elif case_name == 'IEA-3D':
        output_file = "IEA-15-240-RWT_CPACS_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'IEA_config.conf')
        plot_lc_name = 'fz_max'
        predocs_solver_control_dict = dict(
            cpacs_file="IEA-15-240-RWT_CPACS.xml",
            orientation='3d-beam',
            node_placement=6,
            loads_are_internal_loads=True,
        )

    elif case_name == 'Beam':
        output_file = "Beam_Composite_bending_out.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'base_config.conf')
        predocs_solver_control_dict = dict(
            cpacs_file="Beam_Composite_bending_opti.xml",
            orientation='load_reference_points',
            node_placement=6,
            element_length=0.1,
            segment_deflection=None,
            front_spar_uid='MidSpar' if converged_results else None,
            rear_spar_uid='MidSpar' if converged_results else None
        )
        deflection_constraint = False if converged_results else True

    elif case_name == 'Atlas':
        output_file = "cpacs_atlas_v01_cpacs3_mod_sparPos_preprocessed.xml"
        opt_ctrl_file = os.path.join(opt_ctrl_path, 'Atlas_config.conf')
        initial_thickness = 0.06
        plot_lc_name = 'MHPC1MT1'
        predocs_solver_control_dict = dict(
            cpacs_file="cpacs_atlas_v01_cpacs3_mod_sparPos.xml",
            orientation='load_reference_points',
            node_placement=16,
            element_length=0.25,
            segment_deflection=None,
            front_spar_uid='wing_Spar_FS',
            rear_spar_uid='wing_Spar_RS',
        )
    else:
        raise RuntimeError()

    # PreDoCS config
    predocs_ctrl = PreDoCS_SolverControl(
        **modified_kwargs(predocs_solver_control_defaults, **predocs_solver_control_dict)
    )

    # Lightworks config
    opt_ctrl = OptimisationControl(force_run_dir=True)
    opt_ctrl.read_config(path=opt_ctrl_file)
    opt_ctrl.run_dir = tmp_path
    opt_ctrl.lp_space_path = os.path.join(data_dir, 'LP_Space')
    opt_ctrl.parallel = parallel_process_optimisation

    if optimization_param == 'thickness_skin':
        opt_ctrl.parameter_selection['thickness_skin'] = True
        opt_ctrl.parameter_selection['lamination_parameter_skin'] = False
        opt_ctrl.parameter_selection['individual_thickness'] = False
        opt_ctrl.strength_criteria[0] = 'max_stress'
    elif optimization_param == 'individual_thickness':
        opt_ctrl.parameter_selection['thickness_skin'] = True
        opt_ctrl.parameter_selection['lamination_parameter_skin'] = False
        opt_ctrl.parameter_selection['individual_thickness'] = True
        opt_ctrl.strength_criteria[0] = 'max_stress'
    elif optimization_param == 'lp':
        predocs_ctrl.use_lp = True
        opt_ctrl.parameter_selection['thickness_skin'] = True
        opt_ctrl.parameter_selection['lamination_parameter_skin'] = True
        opt_ctrl.parameter_selection['individual_thickness'] = False
        opt_ctrl.strength_criteria[0] = 'strength_lamination_parameter'
    else:
        raise NameError('Invalid parameter to be optimized')

    if converged_results:
        opt_ctrl.algorithm_options['NLOPT']['max_eval'] = 3
        opt_ctrl.algorithm_options['NLOPT']['max_time'] = 10*60

    ## tests for deflection constraints
    if deflection_constraint:
        #### Input for deflection constraints ###
        # these input are for depretiated load cases and in the current xml file. In the current xml file there is only
        #bending load case, thus only flapwise bending restrictions can be at place .
        deflection_constraints_input = {
            'constraints': {
                'bending': {'flap': {'spanwise_positions': [1], 'max_deflection': [8]}},
            },
            'coordinate_system': {'flap': 'global', 'edge': 'global', 'twist': 'global'}
        }
        # deflection_constraints_input = {'constraints': {'bending': {'flap':
        #                                                                 {'spanwise_positions': [1],
        #                                                                  'max_deflection': [8]}},
        #                                                 'torsion': {'flap':
        #                                                                 {'spanwise_positions': [0.5, 1],
        #                                                                  'max_deflection': [2, 8]},
        #                                                             'edge':
        #                                                                 {'spanwise_positions': [1],
        #                                                                  'max_deflection': [2]},
        #                                                             'twist':
        #                                                                 {'spanwise_positions': [0, 0.2, 0.4, 0.6,
        #                                                                                         0.8,
        #                                                                                         1],
        #                                                                  'max_deflection': [0.01, 1, 2, 3, 4, 5]}}},
        #                                 'coordinate_system': {'flap': 'global', 'edge': 'global',
        #                                                       'twist': 'global'}}

        opt_ctrl.deflection_constraint = deflection_constraints_input

    t = time()
    # Initialise Model
    solver = PreDoCS_SolverLightworks(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # # A set of lamination parameter
    # lp_instance = solver.c2p._materials_dict['SymmetricBalanced'].get_lamination_parameter()
    #
    # # Basic material
    # material = solver.c2p._raw_materials_dict['T300_15k_976']
    #
    # # Get model method for optimisation interface / if skin and material is given only skin is used.
    # structural_model = solver.get_structural_model(lp=True, rib_spacing=1.0, stringer_spacing=0.3,
    #                                                skin=lp_instance, material=material)

    # Get structural model for optimisation
    structural_model = solver.structural_model

    if os.path.exists(opt_ctrl.run_dir):
        for file in os.scandir(opt_ctrl.run_dir):
            os.remove(file.path)
    else:
        os.makedirs(opt_ctrl.run_dir)

    optimiser = OptimisationInterface(structural_model, solver)

    if set_initial:
        optimiser.set_initial_thickness([initial_thickness, initial_thickness], linear=True)
        optimiser.set_labeled_thickness(label='not_cwb', thickness=0.002)
        log.info('Initial thickness values set')

    if reload_file:
        optimiser.read_file(file_name='intermediateResults', iteration=-1)
        optimiser.opt_ctrl = opt_ctrl
        parameters = optimiser.optimisation_processor.optimisation_model.parameters
        log.info('Loaded parameters from file')

    log.info('Optimisation interface set up')

    if optimise:
        log.info('Starting optimisation')
        opti_return = optimiser.optimise()
        log.info(opti_return)

        ## tests for deflection constraints
        if deflection_constraint:
            ### write tests for constraint processor ###
            deflection_constraint_object = optimiser.constraint_processor.deflection_constraint[0]
            panels_identified = ConstraintProcessor.get_constraint_panels_dict(
               deflection_constraint_object.deflection_constraints_input, structural_model)
            constraints_input = deflection_constraint_object.deflection_constraints_input
            for load_case in constraints_input['constraints'].keys():
                for constraint_type in constraints_input['constraints'][load_case].keys():
                    assert len(constraints_input['constraints'][load_case][constraint_type]['spanwise_positions']) == \
                           len(constraints_input['constraints'][load_case][constraint_type]['max_deflection'])

            assert len(panels_identified['bending']['flap']['1.0']) == 1
            le_te_dict = ConstraintProcessor.get_le_te_for_tiwst_constraint(constraint_panels_dict=panels_identified)
            # assert len(le_te_dict['torsion']['twist']['0']['te']) == 4
            assert len(deflection_constraint_object.constraints) == 1
            assert len(deflection_constraint_object.constraints) == len(deflection_constraint_object.element_ids)
            ##### End of tests for constraint processor ####

        # if converged_results:
    #     assert return_string in [1, 2, 3, 4]
        # Export csv
        # optimiser.export_csv()

        # Save Protocols
        predocs_ctrl.write_to_protocol(path=opt_ctrl.run_dir, name='predocs_protocol.xlsx')
        opt_ctrl.write_config(path=os.path.join(opt_ctrl.run_dir, 'config_out.conf'))
        log.info('Protocols saved to file')

    log.info('optimization run took {} s'.format(time() - t))

    write_structural_model(solver.cpacs_interface, structural_model)
    solver.cpacs_interface.save_file(output_file)
    # optimiser.dump('H:/opt.bin')

    # Get all node positions
    node_positions = solver.get_nodes()

    # Get all node displacements
    all_node_displacements = solver.read_displacements()

    # Plot stuff
    if opt_ctrl.parameter_selection['individual_thickness']:
        plot_and_save_graphs(
            file_location=opt_ctrl.run_dir + '/intermediate_results.hd5',
            save_location=opt_ctrl.run_dir,
            show=False
        )
    solver.plot_material(plot_cs_idx)
    solver.plot_all_materials()
    solver.plot_beam_stiffness_and_inertia(50)
    solver.plot_loads(plot_lc_name, ['shift', 'import', 'interpolate', 'transform'])
    solver.plot_load_redistribution(selected_load_case=plot_lc_name, load_key='fx', export=True, path=opt_ctrl.run_dir)
    solver.plot_load_redistribution(selected_load_case=plot_lc_name, load_key='fy', export=True, path=opt_ctrl.run_dir)
    if not predocs_ctrl.loads_are_internal_loads:
        solver.plot_beam_displacements(plot_lc_name)
    solver.plot_cut_loads(plot_lc_name)
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='N_zz', plot_value_numbers=False, save_location= None)
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='N_zz', plot_value_numbers=True, save_location= opt_ctrl.run_dir)
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='sigma_zz', plot_value_numbers=False, save_location=None)
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='sigma_zs', plot_value_numbers=False, save_location=None)

    #solver.plot3D(plot_lc_name) # TODO: auto close
    log.info('Plotted created successfully')


def create_model_lightworks(data_dir, cpacs_file, num_beam_nodes=10, use_lp=False, **kwargs):
    # Control section
    ctrl = PreDoCS_SolverControl(
        cpacs_file=cpacs_file,
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        wing_idx=0,
        orientation='root-tip',
        node_placement=num_beam_nodes,
        processor_type='Hybrid',
        hybrid_processor='JungWithoutWarping',
        element_length=0.1,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        use_lp=use_lp,
        **kwargs
    )

    # Initialise Model
    model = PreDoCS_SolverLightworks(ctrl)

    # Create Model
    model.build_model()

    return model.structural_model, model


def test_update_structural_model(data_dir):
    """
    In this test, a PreDoCS model is created and a structural model as defined in the optimisation framework is derived.

    Subsequently the material thickness and lamination parameter are altered and the structural model is updated.

    Now the PreDoCS model is updated with the method update_structural_model(structural_model, panel2segment).

    Since the material thickness was increased and the aluminium alloy was replaced by carbon fiber, a reduction in

    bending is expected. This reduction is assured by an assert statement.

    """
    structural_model, model_VCP = create_model_lightworks(data_dir, "Beam_Composite.xml", num_beam_nodes=6, dtype=np.float64)

    abd_old = deepcopy(structural_model.skins[0].abd)

    model_VCP.get_panel_loads(structural_model.base_parts[0])

    tip_bending_old_x = model_VCP.beam_displacement_function_dict['bending'](model_VCP.predocs_coord.beam_length)[1]
    #tip_bending_old_y = model_VCP.beam_displacements_dict['bending'][54]

    # Measure start time
    start_time = time()

    # Change structural model
    for skin in structural_model.skins:
        lp = skin.get_lamination_parameter(material=model_VCP.cpacs_interface.get_material('T300_15k_976'))
        #lp.v_a = lp.v_a * -0.9
        #lp.v_b = lp.v_b * -0.9
        #lp.v_d = lp.v_d * -0.9
        lp.thickness = lp.thickness*1.5
        skin.abd = lp.abd

    assert not np.allclose(structural_model.skins[0].abd, abd_old)

    # Update structural model
    model_VCP.update_structural_model()

    tip_bending_new_x = model_VCP.beam_displacement_function_dict['bending'](model_VCP.predocs_coord.beam_length)[1]
    #tip_bending_new_y = model_VCP.beam_displacements_dict['bending'][54]

    # Measure duration
    end_time = time()
    duration = end_time - start_time

    # Assert duration
    log.info("Duration of the update: {0:.3} seconds".format(duration))

    bending_reduction_percent_x = (tip_bending_old_x - tip_bending_new_x)/tip_bending_old_x
    #bending_reduction_percent_y = (tip_bending_old_y - tip_bending_new_y)/tip_bending_old_y

    assert tip_bending_new_x < tip_bending_old_x
    #assert tip_bending_new_y < tip_bending_old_y


def test_get_panel_loads(data_dir):
    structural_model, model = create_model_lightworks(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    upper_panel = structural_model.parts[0].parts[0]
    upper_panel_loadcases = model.get_panel_loads(upper_panel)

    lower_panel = structural_model.parts[1].parts[0]
    lower_panel_loadcases = model.get_panel_loads(lower_panel)

    assert upper_panel_loadcases[0] not in lower_panel_loadcases

    upper_anal_cases = {}

    for idx, panel_loadcase in enumerate(upper_panel_loadcases):

        upper_anal_cases[idx] = {'lc': panel_loadcase,
                                 'sc': [criteria.stability.compression_buckling_orthotropic_hsb,
                                        criteria.strength.von_mises_strength_rf]}

    lower_anal_cases = {}

    for idx, panel_loadcase in enumerate(lower_panel_loadcases):
        lower_anal_cases[idx] = {'lc': panel_loadcase,
                          'sc': [criteria.stability.compression_buckling_orthotropic_hsb,
                                 criteria.strength.von_mises_strength_rf]}

    upper_result = upper_panel.evaluate(upper_anal_cases)
    lower_result = lower_panel.evaluate(lower_anal_cases)

    # Additionally get element id's and lengths
    web_panel = structural_model.parts[2].parts[0]
    web_panel_loadcases, web_element_names, web_element_lengths = model.get_panel_loads(web_panel, element_flag=True)

    design_load_cases_hypsiz = get_design_load_cases(web_panel_loadcases,
                                                     strength_method='hypersizer', stability_method='hypersizer',
                                                     element_ids=web_element_names, element_weights=web_element_lengths)


def test_instantiate_constraint_processor(data_dir):
    structural_model, model = create_model_lightworks(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    opt_ctrl = OptimisationControl()
    opt_ctrl.strength_criteria = ['max_strain']
    opt_ctrl.stability_criteria = [
        'compression_buckling_orthotropic_hsb',
        'shear_buckling_orthotropic_hsb'
    ]
    constraint_processor = ConstraintProcessor.from_assembly(structural_model, model)
    constraints = constraint_processor.constraints


def test_get_structural_model_lp_constraints(data_dir):
    # Import Lamination Parameter Model
    structural_model, model = create_model_lightworks(data_dir, "Beam_Composite.xml", num_beam_nodes=6, use_lp=True)

    opt_ctrl = OptimisationControl()
    opt_ctrl.strength_criteria = ['strength_lamination_parameter']
    opt_ctrl.stability_criteria = ['compression_buckling_orthotropic_hsb', 'shear_buckling_orthotropic_hsb']

    with h5py.File(os.path.join(data_dir, 'LP_Space', 'lp_design_space_merged.hd5'), 'r') as f:
        lp_design_space = f['lp_space'][()]

    constraint_processor_1 = ConstraintProcessor.from_assembly(
        structural_model, model, lp_design_space=lp_design_space)

    constraint_processor_2 = ConstraintProcessor.from_assembly(
        structural_model, model, lp_design_space=lp_design_space)

    assert np.allclose(constraint_processor_1.constraints, constraint_processor_2.constraints),\
        'Two constraint processor made from the same structural model and solver should return identical constraints.'

    # Change structural model
    for skin in structural_model.skins:
        lp = skin
        lp.v_a = lp.v_a * -0.9
        lp.v_b = lp.v_b * -0.9
        lp.v_d = lp.v_d * 0.9
        lp.thickness = lp.thickness*1.5

    # Update structural model
    model.update_structural_model()

    # Only update constraint_processor_1
    constraint_processor_1.update_loads(model)

    if len(constraint_processor_1.constraints) == len(constraint_processor_2.constraints):
        assert not np.allclose(constraint_processor_1.constraints, constraint_processor_2.constraints)
    else:
        constraint_processor_1.constraints
        constraint_processor_2.constraints


def test_instantiate_optimisation_model(data_dir):
    structural_model, solver = create_model_lightworks(data_dir, "Beam_Composite.xml", num_beam_nodes=6, use_lp=True)

    opt_ctrl = OptimisationControl()
    opt_ctrl.strength_criteria = ['strength_lamination_parameter']
    opt_ctrl.stability_criteria = [
        'compression_buckling_orthotropic_hsb',
        'shear_buckling_orthotropic_hsb'
    ]
    constraint_processor = ConstraintProcessor.from_assembly(structural_model, solver)

    optimisation_model = OptimisationModel(structural_model=structural_model,
                                           solver=solver,
                                           constraint_processor=constraint_processor)

    # check main functionality is still provided.
    optimisation_model.parameters = optimisation_model.parameters*0.99
    constraints = optimisation_model.constraints

    # Check object is now cloud-picklable
    # A negative protocol number always selects the highest protocol. At least protocol 3 for python 3 should be chosen.
    write_cloudpickle('optimisation_model.bin', optimisation_model)

    # Load an check pickled model
    unpickled_opt_model = read_cloudpickle('optimisation_model.bin')

    unpickled_opt_model.parameters = optimisation_model.parameters*0.99


def test_get_displacements(data_dir, save_data=False):
    structural_model, solver = create_model_lightworks(data_dir, "Beam_Composite.xml", num_beam_nodes=6, dtype=np.float64)

    def replace_vectors(input_dict: dict):
        """Replace vectors with list."""
        return {
            lc_name:
                {node_id: node_displacements.tolist() for node_id, node_displacements in nodal_displacements.items()}
            for lc_name, nodal_displacements in input_dict.items()
        }

    displacements_cell = replace_vectors(solver.get_displacements(panel=structural_model.base_parts[0]))
    displacements_spar_cell = replace_vectors(solver.get_displacements(panel=structural_model.base_parts[1]))

    # "_old.json" for the old versions of the shape functions in BeamFEM
    displacements_cell_ref_filename = os.path.join(data_dir, 'test_get_displacements', 'displacements_cell_ref.json')
    displacements_spar_cell_ref_filename = os.path.join(data_dir, 'test_get_displacements', 'displacements_spar_cell_ref.json')
    if save_data:
        # Save reference data
        write_json(displacements_cell_ref_filename, displacements_cell)
        write_json(displacements_spar_cell_ref_filename, displacements_spar_cell)

    # Load reference data
    displacements_cell_ref = read_json(displacements_cell_ref_filename)
    displacements_spar_cell_ref = read_json(displacements_spar_cell_ref_filename)

    # Compare data
    for lc_name, nodal_displacements in displacements_cell.items():
        for node_id, node_displacements in nodal_displacements.items():
            assert np.allclose(node_displacements, displacements_cell_ref[lc_name][node_id])

    for lc_name, nodal_displacements in displacements_spar_cell.items():
        for node_id, node_displacements in nodal_displacements.items():
            assert np.allclose(node_displacements, displacements_spar_cell_ref[lc_name][node_id])


def test_pickle_lightworks(data_dir, tmp_dir):
    structural_model, solver = create_model_lightworks(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    # Post process Model
    log.info('Stresses created successfully')

    # Test pickle
    file_name = os.path.join(tmp_dir, 'solver.p')
    write_cloudpickle(os.path.join(tmp_dir, 'solver.p'), solver)
    solver2 = read_cloudpickle(file_name)


def test_material_world_VCP(data_dir):
    # Import structural model VCP
    structural_model, model = create_model_lightworks(data_dir, "Beam_Test.xml", num_beam_nodes=6)

    E_VCP1, E_VCP1, G_VCP1 = model.cs_processors[0].discreet_geometry.components[0].shell.get_engineering_constants()
    E_VCP, E_VCP, E_VCP, nu_VCP, nu_VCP, nu_VCP, G_VCP, G_VCP, G_VCP = model.cs_processors[0].discreet_geometry.components[0].shell.material.get_engineering()

    assert np.isclose(E_VCP, E_VCP1)
    assert np.isclose(G_VCP, G_VCP1)


def test_solver_interface_results_with_given_data(data_dir, save_data=False):
    # Control section
    ref_data_filename = os.path.join(data_dir, 'reference_solver_interface_data.json')
    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'analysis_config.conf')
    predocs_ctrl = PreDoCS_SolverControl(
        cpacs_file="Rect_Beam_external_load.xml",
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        wing_idx=0,
        orientation='load_reference_points',
        node_placement=6,
        processor_type='Hybrid',
        hybrid_processor='JungWithoutWarping',
        element_length=None,
        segment_deflection=5e-3,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        front_spar_uid=None,
        rear_spar_uid=None,
        calc_element_load_state_functions=False,
        calc_element_load_state_min_max=True,
        dtype=np.float64,
    )

    opt_ctrl = OptimisationControl(force_run_dir=True)
    opt_ctrl.read_config(path=opt_ctrl_file)

    # Initialise Model
    t = time()
    solver = PreDoCS_SolverLightworks(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # Get structural model for optimisation
    structural_model = solver.structural_model

    if os.path.exists(opt_ctrl.run_dir):
        for file in os.scandir(opt_ctrl.run_dir):
            os.remove(file.path)
    else:
        os.makedirs(opt_ctrl.run_dir)

    optimiser = OptimisationInterface(structural_model, solver)

    log.info('Optimisation interface set up')

    log.info('Starting optimisation')
    opti_return = optimiser.optimise()
    log.info(opti_return)

    # Save Protocols
    # predocs_ctrl.write_to_protocol(path=opt_ctrl.run_dir, name='predocs_protocol.xlsx')
    # opt_ctrl.write_config(path=os.path.join(opt_ctrl.run_dir, 'config_out.conf'))
    # log.info('Protocols saved to file')

    log.info('Analysis run took {} s'.format(time() - t))

    # solver.write_structural_model(structural_model)
    # solver.save_results_file(output_file)

    def load_state_to_dict(ls):
        return {
            'strain_state': ls.strain_state,
            'stress_state': ls.stress_state
        }

    data = {
        'beam_displacements': {lc: beam_displacements_dict.tolist() for lc, beam_displacements_dict in solver._internal_solver._beam_displacements_dict.items()},
        'min_max_load_states_dict': {
            lc: [{str(element.id): (load_state_to_dict(min_load_state), load_state_to_dict(max_load_state))
                  for element, (min_load_state, max_load_state) in cs_min_max_load_states.items()}
                 for cs_min_max_load_states in min_max_load_states]
            for lc, min_max_load_states in solver.min_max_load_states_dict.items()}
    }

    # Save reference data
    if save_data:
        write_json(ref_data_filename, data, indent=1)
        return

    # Load reference data
    ref_data = read_json(ref_data_filename)

    # Compare beam displacements
    for lc in data['beam_displacements'].keys():
        assert np.allclose(data['beam_displacements'][lc],
                         ref_data['beam_displacements'][lc],
                         rtol=1e-5, atol=1e-10)

    # Compare element load states
    for lc in data['min_max_load_states_dict'].keys():
        for cs_idx in range(len(data['min_max_load_states_dict'][lc])):

            for element_id in data['min_max_load_states_dict'][lc][cs_idx].keys():
                for ls_idx in [0, 1]:
                    this_load_state = data['min_max_load_states_dict'][lc][cs_idx][element_id][ls_idx]
                    ref_load_state = ref_data['min_max_load_states_dict'][lc][cs_idx][element_id][ls_idx]

                    # Element load states
                    for k in this_load_state['strain_state'].keys():
                        if k != 'kappa_ss':  # TODO: include in tests
                            assert np.allclose(
                                this_load_state['strain_state'][k],
                                ref_load_state['strain_state'][k],
                                rtol=1e-2, atol=1e-13), \
                                f"load case {lc} - cross section {cs_idx} - element {element_id} - min/max {ls_idx} - {k}:\n{this_load_state['strain_state'][k]}"
                    for k in this_load_state['stress_state'].keys():
                        assert np.allclose(
                            this_load_state['stress_state'][k],
                            ref_load_state['stress_state'][k],
                            rtol=1e-2, atol=1e-3), \
                            f"load case {lc} - cross section {cs_idx} - element {element_id} - min/max {ls_idx} - {k}:\n{this_load_state['stress_state'][k]}"


@pytest.mark.parametrize('use_case', [
    # 'CTNT',  # disabled because too slow
    # 'CTNT_no_solver_gradients',  # disabled because too slow
    'CTNT_modular_gradients',
    'no_solver_gradients',
    'with_solver_gradients'
])
@pytest.mark.parametrize('optimisation', [
    False,
    # True,  # disabled because too slow
])
def test_solver_interface_seriell_parallel(
        data_dir,
        tmp_path,
        use_case: str,
        optimisation: bool,
        reload_data=False,
        debug: bool = False,
):
    configurations = [
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ]
    use_case_suffix = f'uc_{use_case}_opti_{optimisation}'
    results_filename = os.path.join(data_dir, f'results_{use_case_suffix}.p')
    if reload_data:
        with open(results_filename, 'rb') as f:
            results = pickle.load(f)
    else:
        results = []
        run_times = []
        for i, (parallel_predocs, parallel_lightworks) in enumerate(configurations):
            log.info(f'parallel_predocs: {parallel_predocs}, parallel_lightworks: {parallel_lightworks}')

            # Control section
            solver_details_path = os.path.abspath(os.path.join(data_dir, f'{parallel_predocs}_{parallel_lightworks}'))
            if os.path.exists(solver_details_path):
                for file in os.scandir(solver_details_path):
                    os.remove(file.path)
            else:
                os.makedirs(solver_details_path)
            os.environ['solver_details_path'] = solver_details_path

            run_dir = tmp_path / str(i)
            if use_case == 'CTNT' or use_case == 'CTNT_no_solver_gradients' or use_case == 'CTNT_modular_gradients':
                # CTNT use case
                if use_case == 'CTNT_no_solver_gradients':
                    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'base_config_CTNT_no_solver_gradients_config.conf')
                elif use_case == 'CTNT_modular_gradients':
                    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'base_config_CTNT_modular_gradients.conf')
                else:
                    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'base_config_CTNT.conf')
                num_beam_nodes = 6
                front_spar_uid = 'inner_FrontSpar'
                rear_spar_uid = 'inner_RearSpar'
                predocs_ctrl = PreDoCS_SolverControl(
                    cpacs_file='CTNT_center_wing_tubes_6ribs_manual.xml',
                    cpacs_path=os.path.join(data_dir, 'CPACS'),
                    wing_uid='wing',
                    # orientation='wingspan',
                    orientation='load_reference_points',
                    # orientation='root-tip',
                    loads_are_internal_loads=True,
                    node_placement=num_beam_nodes,
                    processor_type='Hybrid',
                    element_length=0.05,
                    # segment_deflection=5e-3,
                    parallel_process=parallel_predocs,
                    engineering_constants_method='with_poisson_effect',
                    hybrid_processor='JungWithoutWarping',
                    front_spar_uid=front_spar_uid,
                    rear_spar_uid=rear_spar_uid,
                    calc_element_load_state_functions=True,
                    calc_element_load_state_min_max=True,
                    mold_angle=0
                )
            else:
                # PreDoCS test use case
                if use_case == 'no_solver_gradients':
                    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'seriell_parallel_no_solver_gradients_config.conf')
                else:
                    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'seriell_parallel_config.conf')
                predocs_ctrl = PreDoCS_SolverControl(
                    cpacs_file='Beam_Composite_bending_opti.xml',
                    cpacs_path=os.path.join(data_dir, 'CPACS'),
                    wing_idx=0,
                    orientation='load_reference_points',
                    node_placement=6,
                    processor_type='Hybrid',
                    hybrid_processor='JungWithoutWarping',
                    element_length=0.1,
                    segment_deflection=None,
                    parallel_process=parallel_predocs,
                    engineering_constants_method='with_poisson_effect',
                    front_spar_uid=None,
                    rear_spar_uid=None,
                    calc_element_load_state_functions=False,
                    calc_element_load_state_min_max=True
                )

            OptimisationControl().reset()
            opt_ctrl = OptimisationControl(force_run_dir=True)
            opt_ctrl.read_config(path=opt_ctrl_file)

            # opt_ctrl.scheduler_address = cluster.client.scheduler.address if parallel_lightworks else None
            opt_ctrl.run_dir = run_dir
            opt_ctrl.parallel = parallel_lightworks
            opt_ctrl.algorithm_options['NLOPT']['max_eval'] = 3
            opt_ctrl.algorithm_options['NLOPT']['max_time'] = 10*60
            if optimisation:
                opt_ctrl.algorithm = 'mma'
            else:
                opt_ctrl.algorithm = 'external'

            # Initialise Model
            t = time()
            solver = PreDoCS_SolverLightworks(predocs_ctrl)

            # Create PreDoCS Model
            solver.build_model()
            log.info('Model created successfully')

            if os.path.exists(opt_ctrl.run_dir):
                for file in os.scandir(opt_ctrl.run_dir):
                    os.remove(file.path)
            else:
                os.makedirs(opt_ctrl.run_dir)

            optimiser = OptimisationInterface(solver.structural_model, solver)

            log.info('Optimisation interface set up')

            log.info('Starting optimisation')
            opti_return = optimiser.optimise()
            log.info(opti_return)

            # Save Protocols
            # predocs_ctrl.write_to_protocol(path=opt_ctrl.run_dir, name='predocs_protocol.xlsx')
            # opt_ctrl.write_config(path=os.path.join(opt_ctrl.run_dir, 'config_out.conf'))
            # log.info('Protocols saved to file')

            run_time = time() - t
            run_times.append(f'(pd {parallel_predocs}, lw {parallel_lightworks}): {run_time} s')
            log.info('Optimisation took {} s'.format(run_time))

            # Read intermediate results
            hdf_data = {}
            with h5py.File(os.path.join(run_dir, 'intermediate_results.hd5'), 'r') as f:
                keys = []
                f.visit(keys.append)
                for key in keys:
                    if isinstance(f[key], h5py.Dataset):
                        hdf_data[key] = f[key][()]
            results.append(hdf_data)
            del os.environ['solver_details_path']

            if debug:
                with open(results_filename, 'wb') as f:
                    pickle.dump(results, f)

                with open(os.path.join(data_dir, f'run_times_{use_case_suffix}.txt'), 'w') as f:
                    f.write('\n'.join(run_times))

    # Compare data
    assert len(results) > 1
    differences = {}
    ref_idx = 0
    ref = results[ref_idx]

    def get_diff_desc(idx):
        return f'(pd {configurations[ref_idx][0]}, lw {configurations[ref_idx][1]}) to '\
               f'(pd {configurations[idx][0]}, lw {configurations[idx][1]})'

    for i, res in enumerate(results):
        if i != ref_idx:
            log.info(f'Compare to {i}')
            assert ref.keys() == res.keys()
            for k in ref.keys():
                log.info(f'Compare key {k}')
                if isinstance(ref[k], np.ndarray):
                    # Numpy array
                    if np.issubdtype(ref[k].dtype, np.number):
                        if not np.allclose(ref[k], res[k], rtol=1e-3, atol=1e-3):
                            differences[f'{get_diff_desc(i)}: ({k})'] = (ref[k], res[k], (res[k] - ref[k]))
                    else:
                        if not np.all(ref[k] == res[k]):
                            differences[f'{get_diff_desc(i)}: ({k})'] = (ref[k], res[k])
                else:
                    # Plain type
                    if not ref[k] == res[k]:
                        differences[f'{get_diff_desc(i)}: ({k})'] = (ref[k], res[k])

    if debug:
        with open(os.path.join(data_dir, f'differences_{use_case_suffix}.txt'), 'w') as f:
            f.write('\n'.join(differences.keys()))

        with open(os.path.join(data_dir, f'differences_{use_case_suffix}.p'), 'wb') as f:
            pickle.dump(differences, f)

    # def ids_to_df(ids):
    #     if len(ids[0]) > 9:
    #         # Nodes
    #         return pd.DataFrame([(int(i[0:3]), int(i[3:6]), int(i[6:9]), int(i[8:11])) for i in ids],
    #                             columns=['cs_id', 'segment_id', 'element_id', 'node_id'])
    #     else:
    #         # Elements
    #         return pd.DataFrame([(int(i[0:3]), int(i[3:6]), int(i[6:9])) for i in ids], columns=['cs_id', 'segment_id', 'element_id'])
    #
    # ref_ids_df = ids_to_df(differences['(pd False, lw False) to (pd False, lw True): (model_geometry/element_ids)'][0])
    # res_ids_df = ids_to_df(differences['(pd False, lw False) to (pd False, lw True): (model_geometry/element_ids)'][1])
    #
    #
    # ref_ids_df[ref_ids_df['cs_id'] == 1]
    # res_ids_df[res_ids_df['cs_id'] == 1]

    assert len(differences) == 0


def stiffness_step(stiff_step: np.ndarray, optimisation_model) -> np.ndarray:
    """
    Evaluates parameter step and sets global parameters or panel abd entries
    depending on which gradients are calculated.

    Parameters
    ----------
    stiff_step
        parameter vector with stiffness

    Returns
    -------
    ndarray
        panel loads of all panels as array
    """
    optimisation_model.structural_model.base_parts[0].abd = reshape_abd_matrix(stiff_step)
    optimisation_model.solver.update_structural_model()

    panel_loads, i = _read_panel_loads(optimisation_model)
    return np.array(panel_loads).flatten()


def test_solver_with_complexstep(data_dir):
    """
    :param data_dir:
    :return: assert if the method complexstep gets gradients as floats.
             With a conf-file for the Optimization.
    """
    cpacs_path = os.path.join(data_dir, 'CPACS')
    opt_ctrl_path = os.path.join(data_dir, 'optimization_control')
    opt_ctrl_file = os.path.join(opt_ctrl_path, 'test_solver_with_complexstep.conf')
    predocs_ctrl = PreDoCS_SolverControl(
        cpacs_file="Beam_Composite_bending_opti.xml",
        cpacs_path=cpacs_path,
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
        rear_spar_uid='MidSpar'
    )

    opt_ctrl = OptimisationControl(force_run_dir=True)
    opt_ctrl.read_config(path=opt_ctrl_file)
    opt_ctrl.lp_space_path = os.path.join(data_dir, 'LP_Space')
    opt_ctrl.parallel = True

    solver = PreDoCS_SolverLightworks(predocs_ctrl)
    solver.build_model()
    opti_model = OptimisationModel(
        solver.structural_model,
        solver,
        ConstraintProcessor().from_assembly(solver.structural_model, solver),
    )
    opti_model.solve()
    panel_stiffness = reshape_abd_matrix(opti_model.structural_model.base_parts[0].abd)

    gradients = complex_step_derivative(stiffness_step, panel_stiffness, None, None, False, None, None, opti_model)
    complex_number = 0

    # After complex_step the complex numbers are floats and !=0.
    for i in range(len(gradients)):
        if gradients.any() != 0:
            complex_number += 1
    assert complex_number != 0


def test_b2000_comparison(data_dir, tmp_path):
    cpacs_file = 'Rectangular_wing_box_b2000.xml'
    opt_ctrl_file = os.path.join(data_dir, 'optimization_control', 'base_config_b2000_comparison.conf')
    parallel_process_optimisation = True
    num_beam_nodes = 5  # 5 nodes = 4 cells
    optimise = False
    output_file = "b2000_comparison.xml"
    front_spar_uid = 'inner_FrontSpar'
    rear_spar_uid = 'inner_RearSpar'
    plot_cs_idx = 0
    plot_lc_name = 'bending'
    predocs_ctrl = PreDoCS_SolverControl(
        cpacs_file=cpacs_file,
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        wing_uid='wing',
        # orientation='wingspan',
        orientation='load_reference_points',
        # orientation='root-tip',
        loads_are_internal_loads=False,
        node_placement=num_beam_nodes,
        processor_type='Hybrid',
        # element_length=0.05,
        segment_deflection=5e-3,
        parallel_process=False,
        engineering_constants_method='with_poisson_effect',
        hybrid_processor='JungWithoutWarping',
        front_spar_uid='FrontSpar',
        rear_spar_uid='RearSpar',
        calc_element_load_state_functions=True,
        calc_element_load_state_min_max=True,
        mold_angle=0
    )

    # Optimisation control
    opt_ctrl = OptimisationControl(force_run_dir=True)
    opt_ctrl.read_config(path=opt_ctrl_file)
    opt_ctrl.run_dir = tmp_path
    opt_ctrl.lp_space_path = os.path.join(data_dir, 'LP_Space')
    opt_ctrl.parallel = parallel_process_optimisation
    opt_ctrl.scheduler_address = None

    # Initialise Model
    solver = PreDoCS_SolverLightworks(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    # Get structural model for optimisation
    structural_model = solver.structural_model

    if os.path.exists(opt_ctrl.run_dir):
        for file in os.scandir(opt_ctrl.run_dir):
            os.remove(file.path)
    else:
        os.makedirs(opt_ctrl.run_dir)

    optimiser = OptimisationInterface(structural_model, solver)

    log.info('Optimisation interface set up')

    if optimise:
        log.info('Starting optimisation')
        x, f, return_string = optimiser.optimise()
        log.info(return_string)

        # Save Protocols
        predocs_ctrl.write_to_protocol(path=opt_ctrl.run_dir, name='predocs_protocol.xlsx')
        opt_ctrl.write_config(path=os.path.join(opt_ctrl.run_dir, 'config_out.conf'))
        log.info('Protocols saved to file')

    write_structural_model(solver.cpacs_interface, structural_model)
    solver.cpacs_interface.save_file(output_file)

    # Plot stuff
    plot_dir = opt_ctrl.run_dir
    solver.plot_material(plot_cs_idx, file=os.path.join(plot_dir, 'materials.png'))
    solver.plot_all_materials(file=os.path.join(plot_dir, 'all_materials.png'))
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='N_zz', plot_value_numbers=False,
                            file=os.path.join(plot_dir, 'N_zz.png'))
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='N_zz', plot_value_numbers=True,
                            file=os.path.join(plot_dir, 'N_zz2.png'))
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='sigma_zz', plot_value_numbers=False,
                            file=os.path.join(plot_dir, 'sigma_zz.png'))
    solver.plot_load_states(plot_cs_idx, plot_lc_name, selected_stress_state='sigma_zs', plot_value_numbers=False,
                            file=os.path.join(plot_dir, 'sigma_zs.png'))

    log.info('Plotted created successfully')


def get_test_kinked_beam_predocs_coord(data_dir, x_axis_definition):
    predocs_ctrl = PreDoCS_SolverControl(
        cpacs_file='Beam_Composite_bending_kink_simple_internal_loads.xml',
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        loads_are_internal_loads=True,
        wing_idx=0,
        orientation='load_reference_points',
        node_placement=11,
        segment_deflection=5e-3,
        x_axis_definition=x_axis_definition,
    )

    # Initialise Model
    t = time()
    solver = PreDoCS_SolverLightworks(predocs_ctrl)
    solver.build_model()
    log.info('Analysis run took {} s'.format(time() - t))

    return solver.predocs_coord


def test_predocscoord_transformation(data_dir):
    predocs_coord_old = get_test_kinked_beam_predocs_coord(data_dir, 'old')
    predocs_coord_new = get_test_kinked_beam_predocs_coord(data_dir, 'new')
    predocs_coord_beam_cosy = get_test_kinked_beam_predocs_coord(data_dir, 'beam_cosy')

    points = [Vector([2, 3, 1]), Vector([4, 7, 5])]
    z2_list = [3, 7]

    # Old x-axis definition
    point_transformed_wing_old = [
        transform_location_m(predocs_coord_old.transformation_aircraft_2_wing, point)
        for z2, point in zip(z2_list, points)
    ]
    point_transformed_predocs_old = [
        transform_location_m(predocs_coord_old.transformation_aircraft_2_predocs(z2), point)
        for z2, point in zip(z2_list, points)
    ]
    trafo1_wing = [-1.5, 1, 3]
    trafo2_wing = [-3.5, 5, 7]
    trafo1_predocs = [-1.5, 1, 0]
    trafo2_predocs = [-3.03980009, 5., 0.64756782]
    assert np.allclose(trafo1_wing, point_transformed_wing_old[0])
    assert np.allclose(trafo2_wing, point_transformed_wing_old[1])
    assert np.allclose(trafo1_predocs, point_transformed_predocs_old[0])
    assert np.allclose(trafo2_predocs, point_transformed_predocs_old[1])

    # New x-axis definition
    point_transformed_wing_new = [
        transform_location_m(predocs_coord_new.transformation_aircraft_2_wing, point)
        for z2, point in zip(z2_list, points)
    ]
    point_transformed_predocs_new = [
        transform_location_m(predocs_coord_new.transformation_aircraft_2_predocs(z2), point)
        for z2, point in zip(z2_list, points)
    ]
    assert np.allclose(trafo1_wing, point_transformed_wing_new[0])
    assert np.allclose(trafo2_wing, point_transformed_wing_new[1])
    assert np.allclose(trafo1_predocs, point_transformed_predocs_new[0])
    assert np.allclose(trafo2_predocs, point_transformed_predocs_new[1])

    # beam_cosy definition
    point_transformed_wing_beam_cosy = [
        transform_location_m(predocs_coord_beam_cosy.transformation_aircraft_2_wing, point)
        for z2, point in zip(z2_list, points)
    ]
    point_transformed_predocs_beam_cosy = [
        transform_location_m(predocs_coord_beam_cosy.transformation_aircraft_2_predocs(z2), point)
        for z2, point in zip(z2_list, points)
    ]
    trafo1_wing_beam_cosy = [1.5, -1, 3]
    trafo2_wing_beam_cosy = [3.5, -5, 7]
    trafo1_predocs_beam_cosy = [1.5, -1, 0]
    trafo2_predocs_beam_cosy = [3.03980009, -5., 0.64756782]
    assert np.allclose(trafo1_wing_beam_cosy, point_transformed_wing_beam_cosy[0])
    assert np.allclose(trafo2_wing_beam_cosy, point_transformed_wing_beam_cosy[1])
    assert np.allclose(trafo1_predocs_beam_cosy, point_transformed_predocs_beam_cosy[0])
    assert np.allclose(trafo2_predocs_beam_cosy, point_transformed_predocs_beam_cosy[1])


internal_external_loads_input = [
    # (
    #         'Beam_Composite_bending_mixed', False,
    #         [('Beam_Composite_bending_internal_loads.xml', True), ('Beam_Composite_bending_without_spar_internal_loads.xml', True)],
    # ),
    (
            'Rect_Beam', False,
            [('Rect_Beam_internal_load.xml', True), ('Rect_Beam_external_load.xml', False)],
    ),
    (
            'Beam_Composite_bending', False,
            [('Beam_Composite_bending_internal_loads.xml', True), ('Beam_Composite_bending_external_loads.xml', False)],
    ),
    (
            'Beam_Composite_bending_without_spar', False,
            [('Beam_Composite_bending_without_spar_internal_loads.xml', True), ('Beam_Composite_bending_without_spar_external_loads.xml', False)],
    ),
    pytest.param(
            'Beam_Composite_bending_kink_simple', True,
            [('Beam_Composite_bending_kink_simple_internal_loads.xml', True), ('Beam_Composite_bending_kink_simple_external_loads.xml', False)],
            marks=pytest.mark.xfail(reason="Load Definition to coarse (load reference points)", raises=AssertionError)
    ),
    (
            'Beam_Composite_bending_kink_simple_fine', True,
            [('Beam_Composite_bending_kink_simple_internal_loads.xml', True), ('Beam_Composite_bending_kink_simple_external_loads_fine.xml', False)],
    ),
    (
            'Beam_Composite_bending_kink_spar_fine', True,
            [('Beam_Composite_bending_kink_spar_internal_loads.xml', True), ('Beam_Composite_bending_kink_spar_external_loads_fine.xml', False)],
    ),
]


@pytest.mark.parametrize('input_name, kinked, input_list', internal_external_loads_input)
def test_kinked_beam_external_internal_loads(data_dir, tmp_dir, input_name, kinked, input_list):
    output_dir = os.path.join(tmp_dir, input_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if kinked:
        node_placement = list(np.linspace(0, 5, 6)) + list(np.linspace(5, 5 + np.sqrt(5**2+1**2), 6))[1:]
    else:
        node_placement = 11

    results = {True: {}, False: {}}
    for cpacs_file, internal_loads in input_list:
        internal_name = 'internal' if internal_loads else 'external'
        predocs_ctrl = PreDoCS_SolverControl(
            cpacs_file=cpacs_file,
            cpacs_path=os.path.join(data_dir, 'CPACS'),
            loads_are_internal_loads=internal_loads,
            wing_idx=0,
            orientation='load_reference_points',
            node_placement=node_placement,
            processor_type='Hybrid',
            hybrid_processor='JungWithoutWarping',
            segment_deflection=5e-3,
            parallel_process=True,
            engineering_constants_method='with_poisson_effect',
            calc_element_load_state_functions=True,
            calc_element_load_state_min_max=False,
            dtype=np.float64,
        )

        # Initialise Model
        t = time()
        solver = PreDoCS_SolverLightworks(predocs_ctrl)
        solver.build_model()
        log.info('Analysis run took {} s'.format(time() - t))

        results[internal_loads]['beam_displacements'] = solver.beam_displacement_function_dict
        results[internal_loads]['cs_displacements'] = solver.cross_section_displacement_dict

        solver.plot_loads(solver.load_case_names[0], base_file_name=os.path.join(output_dir, f'{input_name}_{internal_name}_loads_{{}}.png'))

    # Compare
    beam_length = solver.predocs_coord.beam_length
    z2_compare = np.linspace(0, beam_length, 100)

    plot_data_beam_displ = {}
    plot_data_cs_displ = {}
    plot_data_loads = {}
    load_cases = results[True]['beam_displacements'].keys()
    for load_case in load_cases:
        for internal_loads in [True, False]:
            internal_name = 'internal' if internal_loads else 'external'

            beam_displacements_function = results[internal_loads]['beam_displacements'][load_case]
            beam_displacements = []
            for z2 in z2_compare:
                u = beam_displacements_function(z2)
                beam_displacements.append(np.concatenate((((z2,), u))))
            plot_data_beam_displ[internal_name] = np.array(beam_displacements)

            cs_displacements_list = results[internal_loads]['cs_displacements'][load_case]

            cross_section_displacements = [
                [z] + d.tolist()
                for z, d in zip(solver.predocs_coord.z2_cs, cs_displacements_list)
            ]
            plot_data_cs_displ[internal_name] = np.array(cross_section_displacements)

            cross_section_loads = [
                [z] + list(cs_proc.stiffness.stiffness_matrix @ np.array(d.tolist()))
                for z, cs_proc, d in zip(solver.predocs_coord.z2_cs, solver.cs_processors, cs_displacements_list)
            ]
            plot_data_loads[internal_name] = np.array(cross_section_loads)

        plot_beam_displacements(
            plot_data_beam_displ,
            num_plots=6,
            file=os.path.join(output_dir, f'{input_name}_beam_displ_beam_{load_case}.png'),
        )
        plot_beam_cross_section_displacements(
            plot_data_cs_displ,
            num_plots=6,
            file=os.path.join(output_dir, f'{input_name}_beam_displ_cs_{load_case}.png'),
        )
        plot_beam_internal_loads(
            plot_data_loads,
            num_plots=6,
            file=os.path.join(output_dir, f'{input_name}_beam_loads_{load_case}.png'),
        )

        abs_diff = plot_data_beam_displ['external'] - plot_data_beam_displ['internal']
        rel_diff = save_divide(abs_diff, plot_data_beam_displ['internal'])

        abs_diff_plot = abs_diff.copy()
        abs_diff_plot[:, 0] = plot_data_beam_displ['internal'][:, 0]
        rel_diff_plot = rel_diff.copy()
        rel_diff_plot[:, 0] = plot_data_beam_displ['internal'][:, 0]

        plot_beam_displacements(
            {'abs_diff': abs_diff_plot},
            num_plots=6,
            file=os.path.join(output_dir, f'{input_name}_beam_displ_{load_case}_abs_diff.png'),
        )
        plot_beam_displacements(
            {'rel_diff': rel_diff_plot},
            num_plots=6,
            file=os.path.join(output_dir, f'{input_name}_beam_displ_{load_case}_rel_diff.png'),
        )

        assert np.allclose(plot_data_beam_displ['internal'], plot_data_beam_displ['external'], atol=1e-2, rtol=1e-2)  # Tolerance: 1 cm or 1 %


@pytest.mark.parametrize('input_name, kinked, input_list', internal_external_loads_input)
def test_kinked_beam_external_internal_loads_recovery_from_strains(data_dir, tmp_dir, input_name, kinked, input_list):
    strain_label_list = ['epsilon_zz', 'gamma_zs']
    load_case = 'test_load_case1' if input_name == 'Rect_Beam' else 'bending'

    if kinked:
        node_placement = list(np.linspace(0, 5, 3)) + list(np.linspace(5, 5 + np.sqrt(5**2+1**2), 3))[1:]
    else:
        node_placement = 5

    n = 10
    a = 0
    b = 0
    r = 0.5
    positions_circle_predocs = [Vector([r * np.cos(t) + a, r * np.sin(t) + b, 0]) for t in np.linspace(0, (2*np.pi) / (n+1) * n, n)]

    # Generate strains from external loads
    predocs_ctrl_external = PreDoCS_SolverControl(
        cpacs_file=input_list[1][0],
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        loads_are_internal_loads=False,
        wing_idx=0,
        orientation='load_reference_points',
        node_placement=node_placement,
        processor_type='Hybrid',
        hybrid_processor='JungWithoutWarping',
        segment_deflection=5e-3,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        calc_element_load_state_functions=True,
        calc_element_load_state_min_max=False,
        dtype=np.float64,
    )

    # Initialise Model
    t = time()
    solver_external = PreDoCS_SolverLightworks(predocs_ctrl_external)
    solver_external.build_model()
    log.info('Analysis run took {} s'.format(time() - t))

    # Generate sensor positions
    sensor_positions = []
    for z2 in solver_external.predocs_coord.z2_cs:
    # for y in [2.5, 7.5]:
        transformation = solver_external.predocs_coord.transformation_predocs_2_aircraft(z2)
        sensor_positions.extend([transform_location_m(transformation, pc) for pc in positions_circle_predocs])

    # Generate strains
    displacement_recovery_setup_external = solver_external.get_cross_section_displacement_from_sensor_strains_setup(
        sensor_positions, strain_label_list,
    )
    sensor_strains_external = solver_external.get_sensor_load_states(
        load_case,
        displacement_recovery_setup_external[1],
        strain_label_list,
    )

    cs_loads_external = {
        i_cs: solver_external.cs_processors[i_cs].stiffness.stiffness_matrix @ np.array(displ.tolist())
        for i_cs, displ in enumerate(solver_external.cross_section_displacement_dict[load_case])
    }

    # Load internal loads reference
    predocs_ctrl_internal = PreDoCS_SolverControl(
        cpacs_file=input_list[0][0],
        cpacs_path=os.path.join(data_dir, 'CPACS'),
        loads_are_internal_loads=True,
        wing_idx=0,
        orientation='load_reference_points',
        node_placement=node_placement,
        processor_type='Hybrid',
        hybrid_processor='JungWithoutWarping',
        segment_deflection=5e-3,
        parallel_process=True,
        engineering_constants_method='with_poisson_effect',
        calc_element_load_state_functions=True,
        calc_element_load_state_min_max=False,
        dtype=np.float64,
    )

    # Initialise Model
    t = time()
    solver_internal = PreDoCS_SolverLightworks(predocs_ctrl_internal)
    solver_internal.build_model()
    log.info('Analysis run took {} s'.format(time() - t))

    cs_loads_internal = {
        i_cs: solver_internal.cs_processors[i_cs].stiffness.stiffness_matrix @ np.array(displ.tolist())
        for i_cs, displ in enumerate(solver_internal.cross_section_displacement_dict[load_case])
    }

    # Recover loads from strains
    displacement_recovery_setup_internal = solver_internal.get_cross_section_displacement_from_sensor_strains_setup(
        sensor_positions, strain_label_list,
    )
    cs_displacement_dict = solver_internal.get_cross_section_displacement_from_sensor_strains(
        sensor_strains_external,
        *displacement_recovery_setup_internal,
    )
    cs_loads_recovered = {
        i_cs: solver_internal.cs_processors[i_cs].stiffness.stiffness_matrix @ np.array(displ.tolist())
        for i_cs, displ in cs_displacement_dict.items()
    }

    # # Displacements
    # cs_displ_external = {
    #     i_cs: np.array(displ.tolist())
    #     for i_cs, displ in enumerate(solver_external.cross_section_displacement_dict[load_case])
    # }
    # cs_displ_internal = {
    #     i_cs: np.array(displ.tolist())
    #     for i_cs, displ in enumerate(solver_internal.cross_section_displacement_dict[load_case])
    # }
    #
    # cs_displ_external2 = {
    #     z2: np.array(
    #         solver_external._internal_solver._beam.post_processing(
    #             solver_external._internal_solver._beam_displacements_dict[load_case], z2
    #         )[1].tolist()
    #     )
    #     for z2 in np.linspace(0, 10, 200)
    # }
    # plot_beam_cross_section_displacements(
    #     {'ext': np.array([[z2] + list(displ) for z2, displ in cs_displ_external2.items()])},
    #     num_plots=6,
    #     file=os.path.join(tmp_dir, 'cs_displ_external2.png'),
    # )

    # Comparison of loads
    for loads_external, loads_internal, loads_recovered in zip(cs_loads_external.values(), cs_loads_internal.values(), cs_loads_recovered.values()):
        assert np.allclose(loads_internal, loads_external, atol=1, rtol=1e-2)
        assert np.allclose(loads_internal, loads_recovered, atol=1, rtol=1e-2)
        assert np.allclose(loads_external, loads_recovered, atol=1, rtol=1e-2)


def test_plot_3d(data_dir, tmp_path):
    structural_model, solver = create_model_lightworks(data_dir, "Beam_Composite.xml", num_beam_nodes=6, dtype=np.float64)
    solver.plot_3d(selected_load_case='bending', file=tmp_path / 'plot-3d.png')
