"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os.path
import sys
from random import random
from time import perf_counter

import pytest

from PreDoCS.CrossSectionAnalysis.Display import plot_cross_section_element_values, plot_discreet_geometry
from PreDoCS.CrossSectionAnalysis.Interfaces import ClassicCrossSectionLoads, ClassicCrossSectionLoadsWithBimoment
from PreDoCS.CrossSectionAnalysis.Processors import IsotropicCrossSectionProcessor, \
    HybridCrossSectionProcessor, SongCrossSectionProcessor, JungCrossSectionProcessor, CrossSectionProcessor, \
    JungWithoutWarpingCrossSectionProcessor
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElement, \
    CompositeElement
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.vector import Vector
from PreDoCS.notebook_utils.comparison import *
from PreDoCS.util.inout import write_json, read_json, read_cloudpickle, write_cloudpickle
from test.CrossSections import get_wing_cross_section_geometry_definition_dict


def random_vector3():
    return Vector([random(), random(), random()])


def test_cross_section_processor_performance(data_dir, tmp_dir):
    num_cs_calcs = 10
    num_lc_calcs_per_cs = 10

    geometry_id = 11
    test_load_case = ClassicCrossSectionLoadsWithBimoment(Vector([1, 0, 0]), Vector([0, 0, 0]), 0)

    perf_dict = {
        'cs_geometry': [],
        'cs_stiffness': [],
        'cs_calc': [],
        'lc': [],
    }

    wing_cs_definition_dict = get_wing_cross_section_geometry_definition_dict(os.path.join(data_dir, 'profiles'))

    for i_cs in range(num_cs_calcs):
        # Create geometry
        t = perf_counter()
        geometry_definition = wing_cs_definition_dict[geometry_id]
        discreet_geometry = geometry_definition.get_discreet_geometry(
            CompositeElement, element_length=0.05,
        )
        perf_dict['cs_geometry'].append(perf_counter() - t)
        # log.warning(f'Create geometry took {(perf_counter() - t) * 1000:.1f} ms')
        # plot_discreet_geometry(
        #     discreet_geometry,
        #     file=os.path.join(tmp_dir, 'tests', '{}_geometry_{}.png'.format(geometry_id, processor_type.__name__)),
        # )

        # Calc stiffness
        t = perf_counter()
        materials = {s.shell for s in discreet_geometry.components}
        for material in materials:
            material.stiffness = get_stiffness_for_shell(material, CompositeElement, engineering_constants_method='song')
        perf_dict['cs_stiffness'].append(perf_counter() - t)
        # log.warning(f'Calc stiffness took {(perf_counter() - t) * 1000:.1f} ms')

        t = perf_counter()
        # Create cross section processor
        cs_processor = HybridCrossSectionProcessor(2, 11.1, hybrid_processor='Jung')
        cs_processor.discreet_geometry = discreet_geometry
        cs_processor._update_if_required()
        perf_dict['cs_calc'].append(perf_counter() - t)
        # log.warning(f'Create CS took {(perf_counter() - t) * 1000:.1f} ms')

        for i_lc in range(num_lc_calcs_per_cs):
            t = perf_counter()
            displacements2, load_states2 = cs_processor.calc_load_case(test_load_case)
            perf_dict['lc'].append(perf_counter() - t)
            # log.warning(f'LC calc took {(perf_counter() - t) * 1000:.1f} ms')

    log.warning(f'num_cs_calcs={num_cs_calcs}, num_lc_calcs_per_cs={num_lc_calcs_per_cs}')
    for k, l in perf_dict.items():
        log.warning(f'{k}: median: {np.median(l) * 1000:.0f} ms, mean: {np.mean(l) * 1000:.0f} ms, std: {np.std(l) * 1000:.0f} ms')


@pytest.mark.slow
@pytest.mark.parametrize('geometry_id', [
        50, 51, 52, 53, 54, 55,
        70, 71, 72, 73, 74, 75, 76,
    ] + list(range(100, 107)),
)
def test_cross_section_processors(data_dir, tmp_dir, geometry_id):
    # TODO: list(range(100,107)) + list(range(200,207)) + [210,211,220,221,222] + [500,501] + list(range(700,707)) + [710,711]
    open_cs_list = [
        50, 51, 52, 53, 54, 55,
        70, 71, 72, 73, 74, 75, 76,
    ]
    test_load_case_1 = ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([0, 1, 0]))
    test_load_case_21 = ClassicCrossSectionLoadsWithBimoment(Vector([1, 0, 0]), Vector([0, 0, 0]), 0)
    test_load_case_22 = ClassicCrossSectionLoads(Vector([0, 1, 0]), Vector([0, 0, 0]))
    test_load_case_23 = ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([0, 0, 1]))

    # ClassicCrossSectionLoads(random_vector3(), random_vector3())
    # ClassicCrossSectionLoadsWithBimoment(random_vector3(), random_vector3() , random())

    processor_types = [
        (JungCrossSectionProcessor, CompositeElement, [test_load_case_21], ['N_zz', 'N_zs']),
        (JungWithoutWarpingCrossSectionProcessor, CompositeElement, [test_load_case_1], ['N_zz', 'N_zs']),
        (IsotropicCrossSectionProcessor, IsotropicElement, [test_load_case_1], ['normal_flow', 'shear_flow']),
        (HybridCrossSectionProcessor, CompositeElement, [test_load_case_22, test_load_case_23], ['N_zz', 'N_zs', 'M_zs']),
        (SongCrossSectionProcessor, CompositeElement, [test_load_case_21], ['N_zz', 'N_zs']),
    ]

    wing_cs_definition_dict = get_wing_cross_section_geometry_definition_dict(os.path.join(data_dir, 'profiles'))
    # for geometry_id in geometry_ids:
    for processor_type, element_type, internal_loads, plot_keys in processor_types:
        #processor_label = 'P{}'.format(processor_types.index((processor_type, element_type)))
        if geometry_id in open_cs_list and (processor_type == SongCrossSectionProcessor):
            # Skip open cross-section for Song processor
            continue

        # Create geometry
        geometry_definition = wing_cs_definition_dict[geometry_id]
        discreet_geometry = geometry_definition.get_discreet_geometry(
            element_type, element_length=0.05,
        )
        plot_discreet_geometry(
            discreet_geometry,
            file=os.path.join(tmp_dir, 'tests', '{}_geometry_{}.png'.format(geometry_id, processor_type.__name__)),
        )

        # Calc stiffness
        materials = {s.shell for s in discreet_geometry.components}
        for material in materials:
            material.stiffness = get_stiffness_for_shell(material, element_type, engineering_constants_method='song')

        # Create cross section processor
        cs_processor = processor_type(2, 11.1, open_cs=not geometry_definition.close_open_ends)
        if isinstance(cs_processor, JungCrossSectionProcessor) or isinstance(cs_processor, SongCrossSectionProcessor):
            cs_processor._shear_center = Vector([0, 0])

        cs_processor.discreet_geometry = discreet_geometry

        # if geometry_id in open_cs_list and (processor_type == SongCrossSectionProcessor):
        #     with pytest.raises(RuntimeError):
        #         cs_processor._update_if_required()
        #     continue

        assert discreet_geometry == cs_processor.discreet_geometry

        assert cs_processor.id == 2
        assert cs_processor.z_beam == 11.1

        cs_processor.stiffness
        cs_processor.inertia

        cs_processor.elastic_center
        cs_processor.principal_axis_angle
        cs_processor.shear_center

        cs_processor.transform_cross_section_to_elastic_atm
        cs_processor.transform_elastic_to_cross_section_atm
        cs_processor.transform_elastic_to_principal_axis_atm
        cs_processor.transform_principal_axis_to_elastic_atm
        cs_processor.transform_cross_section_to_principal_axis_atm
        cs_processor.transform_principal_axis_to_cross_section_atm

        displacements1 = cs_processor.calc_displacements(internal_loads[0])
        load_states1 = {e: cs_processor.calc_element_load_state(e, displacements1) for e in cs_processor.discreet_geometry.elements}

        # save_persist_data_cloudpickle(
        #     os.path.join(tmp_dir, 'tests', '{}_processor_{}.p'.format(geometry_id, processor_type.__name__)),
        #     cs_processor,
        # )

        # element_data = {e: (e.integral_values_0['omega'] + e.integral_values_l['omega']) / 2 for e in discreet_geometry.elements}
        # plot_cross_section_element_values(
        #     cs_processor,
        #     element_data,
        #     values_are_functions=False,
        #     max_display_value=0.5,
        #     plot_value_numbers=False,
        #     plot_value_scale=True,
        #     plot_direction_as_arrow=False,
        #     cross_section_size=(15, 8),
        #     title='omega',
        #     file=os.path.join(tmp_dir, 'tests', f'{geometry_id}_{processor_type.__name__}_omega.png'),
        # )
        # element_data = {e: e.torsional_function_value for e in discreet_geometry.elements}
        # plot_cross_section_element_values(
        #     cs_processor,
        #     element_data,
        #     values_are_functions=False,
        #     max_display_value=0.5,
        #     plot_value_numbers=False,
        #     plot_value_scale=True,
        #     plot_direction_as_arrow=False,
        #     cross_section_size=(15, 8),
        #     title='torsional_function_value',
        #     file=os.path.join(tmp_dir, 'tests', f'{geometry_id}_{processor_type.__name__}_torsional_function_value.png'),
        # )

        for i, loads in enumerate(internal_loads):
            displacements2, load_states2 = cs_processor.calc_load_case(loads)

            # Plot the normal flow for all cross section elements
            for plot_key in plot_keys:
                element_data = {element: load_state.stress_state[plot_key] for element, load_state in load_states2.items()}
                plot_cross_section_element_values(
                    cs_processor,
                    element_data,
                    values_are_functions=True,
                    max_display_value=0.5,
                    plot_value_numbers=False,
                    plot_value_scale=True,
                    plot_direction_as_arrow=plot_key=='N_zs',
                    cross_section_size=(15, 8),
                    title=plot_key,
                    file=os.path.join(tmp_dir, 'tests', f'{geometry_id}_{processor_type.__name__}_lc-{i}_{plot_key}.png'),
                )


@pytest.mark.slow
def test_processor_results_with_given_cross_section_data_and_stress_distributions(
        predocs_root_dir, data_dir, tmp_dir, save_data=False
):
    # Import Comparison module
    sys.path.append(os.path.join(predocs_root_dir, 'test'))
    from Comparison import process_comparison_sets
    becas_dir = os.path.join(data_dir, '..', 'BECAS')

    # Setup
    with_becas = True if os.environ.get('BECAS_PATH') is not None else False
    comparison_sets = [50, 70, 100, 200, 700]  # [100, 200, 300, 400, 500, 600, 700, 900, 1000, 1100, 1200, 1300, 1400]
    data_output_path = os.path.join(tmp_dir, 'comparison_tests')

    processors = ['hybrid_jung',
                  # 'hybrid_song',
                  'isotropic_song']  # , 'isotropic_no_stress', 'jung', 'song']
    if with_becas:
        processors = ['becas'] + processors

    load_cases = ['transverse_y', 'bending_x', 'torsion'] #  ['transverse_x', 'transverse_y', 'extension', 'bending_x', 'bending_y', 'torsion']

    profiles_dict = {
        50:  [50, 51, 52, 53, 54, 55],
        70: [70, 71, 72, 73, 74, 75, 76],
        100: [105, 106, 110, 111], #list(range(100, 112)),
        200: [205, 206, 210, 211, 222], #list(range(200, 207)) + [210, 211, 220, 221, 222],
        300: list(range(300, 373)),
        400: list(range(400, 440)),
        500: [500, 501],
        600: list(range(600, 673)),
        700: [705, 706, 710, 711, 712], #list(range(700, 707)) + [710, 711, 712],
        900: list(range(900, 904)) + [910, 911],
        1000: list(range(1000, 1073)),
        1100: [1100],
        1200: list(range(1200, 1204)) + [1210, 1211],
        1300: list(range(1300, 1337)),
        1400: list(range(1400, 1404)),
        20000: [20000, 20001, 20002, 20003],
    }

    principle_axis_loads = []
    #     'bending_X_PA',
    #     'bending_Y_PA',
    #     'transverse_X_PA',
    #     'transverse_Y_PA'
    # ]

    # plots = {'load_cases': ['transverse_x',
    #                         # 'transverse_y', 'extension', 'bending_x',
    #                         'bending_y',
    #                         # 'torsion',
    #                         ]}
    plot_kwargs = {
        'plot_value_scale': True,
        'scale_length': 0.5,
        'max_display_value': 0.3,
        'plot_value_numbers': False,
        'plot_title': False,
        'arrow_scale_factor': 2,
        'file_format': '.png',
        'dpi': 300,
        'cross_section_size': (10,7)
    }

    comparison_dict = {k: {'processors': processors, 'profiles': profiles,
                           'load_cases': load_cases, 'plots': None, 'full_plots': False}
                       for k, profiles in profiles_dict.items()}

    # Calculate Results
    process_comparison_sets(
        {k: v for k, v in comparison_dict.items() if k in comparison_sets},
        becas_dir=becas_dir,
        profiles_path=os.path.join(data_dir, 'profiles'),
        output_path=data_output_path,
        shear_center_as_origin=True,
        parallel_processing=False,
        element_length=0.1,
        plot_kwargs=plot_kwargs,
    )

    # Prepare data for comparison
    data_dicts = {}
    for comparison_set in comparison_sets:
        # Load the data from the files
        cs_processors = comparison_dict[comparison_set]['processors']
        profiles = comparison_dict[comparison_set]['profiles']
        processor_dirs = {processor: os.path.join(data_output_path, os.path.join(processor, 'output')
                                     if processor == 'becas' else processor)
                          for processor in cs_processors}

        # Read data
        data_dict = read_input_files(profiles, processor_dirs)

        # Remove unused attributes and update data dicts
        for processor in cs_processors:
            for profile in profiles:
                data_dict[processor][profile].pop('calculation_time', None)
                data_dict[processor][profile].pop('cs_processor', None)
                data_dict[processor][profile].pop('discreet_geometry', None)
            if processor not in data_dicts:
                data_dicts[processor] = {}
            data_dicts[processor].update(data_dict[processor])

        # Save reference data
        ref_data_filename = os.path.join(data_dir, f'reference_processor_data_{comparison_set}.p')
        if save_data:
            write_cloudpickle(ref_data_filename, data_dicts)
            continue

        # Load reference data
        ref_data_dicts = read_cloudpickle(ref_data_filename)

        # Compare the data
        cs_processors = comparison_dict[comparison_set]['processors']
        profiles = comparison_dict[comparison_set]['profiles']
        for processor in cs_processors:
            log.info(f'processor: {processor}')
            for profile in profiles:
                log.info(f'profile: {profile}')
                this = data_dicts[processor][profile]
                ref = ref_data_dicts[processor][profile]

                # Assert cross section properties
                cs_properties = [
                    ('elastic_center', 1e-5, 1e-2),
                    ('shear_center', 1e-5, 1e-2),
                    ('principal_axis_angle', 1e-5, 1e-2),
                    ('stiffness_matrix', 1e-3, 1e4),
                    ('compliance_matrix', 1e-3, 1e-11),
                    ('mass_matrix', 1e-5, 1e-5),
                    ('elastic_center', 1e-5, 1e-8),
                ]
                for key, rel_tol, abs_tol in cs_properties:
                    if key in ref:
                        assert np.allclose(this[key], ref[key], rtol=rel_tol, atol=abs_tol), \
                               f"{processor} - {profile} - {key}:\n{this[key]}"

                # Assert displacement reactions
                if 'displacement_reactions' in ref:
                    for displacement_reaction in this['displacement_reactions'].keys():
                        # Exclude principle axis displacement reactions
                        if displacement_reaction not in principle_axis_loads:
                            this_displacement_reaction = this['displacement_reactions'][displacement_reaction]
                            ref_displacement_reaction = ref['displacement_reactions'][displacement_reaction]

                            # Displacements
                            for k in this_displacement_reaction['displacements'].keys():
                                assert np.allclose(this_displacement_reaction['displacements'][k],
                                                 ref_displacement_reaction['displacements'][k],
                                                  rtol=1e-5, atol=1e-13), \
                                    f"{processor} - {profile} - displacement reaction {displacement_reaction} - {k}:\n{this_displacement_reaction['displacements'][k]}"

                            # Element load states
                            for element_id in this_displacement_reaction['element_load_states'].keys():
                                for k in this_displacement_reaction['element_load_states'][element_id]['strain_state'].keys():
                                    if k != 'kappa_ss':  # TODO: include in tests
                                        assert np.allclose(this_displacement_reaction['element_load_states'][element_id]['strain_state'][k],
                                                          ref_displacement_reaction['element_load_states'][element_id]['strain_state'][k],
                                                          rtol=1e-2, atol=1e-10), \
                                            f"{processor} - {profile} - displacement reaction {displacement_reaction} - {element_id} - {k}:\n{this_displacement_reaction['element_load_states'][element_id]['strain_state'][k]}"
                                for k in this_displacement_reaction['element_load_states'][element_id]['stress_state'].keys():
                                    assert np.allclose(this_displacement_reaction['element_load_states'][element_id]['stress_state'][k],
                                                      ref_displacement_reaction['element_load_states'][element_id]['stress_state'][k],
                                                      rtol=1e-2, atol=1e-3), \
                                        f"{processor} - {profile} - displacement reaction {displacement_reaction} - {element_id} - {k}:\n{this_displacement_reaction['element_load_states'][element_id]['stress_state'][k]}"

                # Assert load cases
                if 'load_cases' in ref:
                    for load_case in this['load_cases'].keys():
                        # Exclude principle axis displacement reactions
                        if load_case not in principle_axis_loads:
                            this_load_case = this['load_cases'][load_case]
                            ref_load_case = ref['load_cases'][load_case]

                            # Internal Load
                            for k in this_load_case['internal_load'].keys():
                                assert np.allclose(this_load_case['internal_load'][k],
                                                 ref_load_case['internal_load'][k],
                                                  rtol=1e-5, atol=1e-10), \
                                    f"{processor} - {profile} - load case {load_case} - {k}:\n{this_load_case['internal_load'][k]}"

                            for k in this_load_case['displacements'].keys():
                                assert np.allclose(this_load_case['displacements'][k],
                                                  this_load_case['displacements'][k],
                                                  rtol=1e-5, atol=1e-10), \
                                                  f"{processor} - {profile} - load case {load_case} - {k}:\n{this_load_case['displacements'][k]}"

                            # Element load states
                            for element_id in this_load_case['element_load_states'].keys():
                                for k in this_load_case['element_load_states'][element_id]['strain_state'].keys():
                                    if k != 'kappa_ss':  # TODO: include in tests
                                        assert np.allclose(
                                            this_load_case['element_load_states'][element_id]['strain_state'][k],
                                            ref_load_case['element_load_states'][element_id]['strain_state'][k],
                                            rtol=1e-2, atol=1e-13), \
                                            f"{processor} - {profile} - load case {load_case} - {element_id} - {k}:\n{this_load_case['element_load_states'][element_id]['strain_state'][k]}"
                                for k in this_load_case['element_load_states'][element_id]['stress_state'].keys():
                                    assert np.allclose(
                                        this_load_case['element_load_states'][element_id]['stress_state'][k],
                                        ref_load_case['element_load_states'][element_id]['stress_state'][k],
                                        rtol=1e-2, atol=1e-3), \
                                        f"{processor} - {profile} - load case {load_case} - {element_id} - {k}:\n{this_load_case['element_load_states'][element_id]['stress_state'][k]}"


@pytest.mark.cpacs_interface_required
def test_6_cell_cs_cutting(data_dir, tmp_path, load_results=False):
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
    from PreDoCS.SolverInterface.SolverInterfacePreDoCS import PreDoCS_SolverPreDoCS

    filename = os.path.join(data_dir, '6_cell_discreet_geometry.p')
    if load_results:
        cs_processor = read_cloudpickle(filename)
    else:
        predocs_ctrl = PreDoCS_SolverControl(
            cpacs_file='Rectangular_wing_box_extended.xml',
            cpacs_path=os.path.join(data_dir, 'CPACS'),
            wing_idx=0,
            orientation='load_reference_points',
            node_placement=6,
            processor_type='Hybrid',
            hybrid_processor='Jung',
            element_length=None,
            segment_deflection=1e-3,
            parallel_process=True,
            engineering_constants_method='with_poisson_effect',
            front_spar_uid='MidSpar',
            rear_spar_uid='MidSpar',
        )
        solver = PreDoCS_SolverPreDoCS(predocs_ctrl)
        solver.build_model()
        cs_processor = solver.cs_processors[2]

        write_cloudpickle(filename, cs_processor)

    cutted_dg = CrossSectionProcessor.get_cutted_discreet_geometry_from_discreet_geometry(cs_processor.discreet_geometry)
