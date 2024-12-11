"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os.path

import numpy as np
import pytest

from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import load_profile_points, \
    WingCrossSectionGeometryDefinition
from PreDoCS.CrossSectionAnalysis.Interfaces import ClassicCrossSectionLoadsWithBimoment
from PreDoCS.CrossSectionAnalysis.Processors import HybridCrossSectionProcessor
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement
from PreDoCS.MaterialAnalysis.Materials import Transverse_Isotropic as Transverse_Isotropic_PreDoCS
from PreDoCS.MaterialAnalysis.Materials import Isotropic as Isotropic_PreDoCS
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell, CompositeShell, get_stiffness_for_shell, \
    get_stiffness_for_shell_VCP
from PreDoCS.notebook_utils.comparison import *
from PreDoCS.util.vector import Vector

try:
    from lightworks.mechana.materials.materiallaws import Transverse_Isotropic as Transverse_Isotropic_lightworks
    from lightworks.mechana.materials.materiallaws import Isotropic as Isotropic_lightworks
    from lightworks.mechana.skins.composite import Laminate
    from lightworks.mechana.skins.metal import Sheet
except ImportError:
    log.warning('Lightworks not installed')


def get_shell_layup(ply, ply_thickness, orientation):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
    ]


def get_web_layup(ply, ply_thickness, orientation=0.):
    return [
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation + 90.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation - 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation + 45.0),
        (ply, ply_thickness, orientation),
    ]


def get_test_ply_data_predocs(thickness_step, stiffness_step, dtype):
    p1 = Transverse_Isotropic_PreDoCS(
        134.7e9 + stiffness_step, 7.7e9 + stiffness_step, 0.369, 0.5, 4.2e9 + stiffness_step, name='Hexcel T800/M21', density=1590, dtype=dtype,
    )
    p1_thickness = 0.184e-3 + thickness_step
    return p1, p1_thickness


def get_shells_isotropic_predocs(dtype, thickness_step, stiffness_step):
    alu_density = 2820
    alu_E = 71e9 + stiffness_step
    alu_nu = 0.32

    p1, p1_thickness = get_test_ply_data_predocs(thickness_step, stiffness_step, dtype)

    alu_material = Isotropic_PreDoCS(alu_E, alu_nu, name='Alu', density=alu_density, dtype=dtype)
    alu = IsotropicShell(alu_material, 24*p1_thickness, name='Alu')

    return alu, alu


def get_shells_laminate_predocs(dtype, thickness_step, stiffness_step, orientation_step):
    p1, p1_thickness = get_test_ply_data_predocs(thickness_step, stiffness_step, dtype)

    l_shell = CompositeShell(name='Laminat Shell', layup=get_shell_layup(p1, p1_thickness, orientation_step), dtype=dtype)
    l_web = CompositeShell(name='Laminat Web', layup=get_web_layup(p1, p1_thickness, orientation_step), dtype=dtype)

    return l_shell, l_web


def get_test_ply_data_lightworks(thickness_step, stiffness_step, dtype):
    p1 = Transverse_Isotropic_lightworks(
        134.7e9 + stiffness_step, 7.7e9 + stiffness_step, 0.369, 0.5, 4.2e9 + stiffness_step, name='Hexcel T800/M21', density=1590,
    )
    p1_thickness = 0.184e-3 + thickness_step
    return p1, p1_thickness


def get_shells_isotropic_lightworks(dtype, thickness_step, stiffness_step):
    alu_density = 2820
    alu_E = 71e9 + stiffness_step
    alu_nu = 0.32

    p1, p1_thickness = get_test_ply_data_lightworks(thickness_step, stiffness_step, dtype)

    alu_material = Isotropic_lightworks(alu_E, alu_nu, name='Alu', density=alu_density)
    alu = Sheet(alu_material, 24*p1_thickness, name='Alu')

    return alu, alu


def get_shells_laminate_lightworks(dtype, thickness_step, stiffness_step, orientation_step):
    p1, p1_thickness = get_test_ply_data_lightworks(thickness_step, stiffness_step, dtype)

    l_shell = Laminate(
        name='Laminat Shell',
        layers={
            i: {'material': ply, 'thickness': ply_thickness, 'angle': orientation}
            for i, (ply, ply_thickness, orientation) in enumerate(get_shell_layup(p1, p1_thickness, orientation_step))
        }
    )
    l_web = Laminate(
        name='Laminat Web',
        layers={
            i: {'material': ply, 'thickness': ply_thickness, 'angle': orientation}
            for i, (ply, ply_thickness, orientation) in enumerate(get_web_layup(p1, p1_thickness, orientation_step))
        }
    )

    return l_shell, l_web


def get_discreet_geometry(profiles_path, material_shell, material_web, element_length=0.05):

    web_line_1 = (Vector([0.5, -1]), Vector([0.5, 1]))
    web_line_2 = (Vector([0.3, -1]), Vector([0.3, 1]))
    # web_line_3 = (Vector([0.7, -1]), Vector([0.7, 1]))
    # web_line_4 = (Vector([0.4, -1]), Vector([0.4, 1]))
    # web_line_5 = (Vector([0, -1]), Vector([0, 1]))
    # web_line_6 = (Vector([-2, 0]), Vector([2, 0]))

    airfoil_spline = {
        'DegMin': 3,
        'DegMax': 15,
        'Continuity': 4,  # = GeomAbs_C2
        'Tol3D': 1.0e-4,
    }

    geometry = WingCrossSectionGeometryDefinition(load_profile_points(
        os.path.join(profiles_path, 'NACA-2412-cos-50.txt'), True), material_shell,
        webs=[(web_line_2, material_web), (web_line_1, material_web)],
        element_size=element_length,
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )
    discreet_geometry = geometry.get_discreet_geometry(
        CompositeElement, element_length=element_length,
    )
    return discreet_geometry


def cs_calculation(profiles_path, dtype, use_composite_material, use_lightworks_materials, thickness_step, stiffness_step, orientation_step, lc_step):
    if use_lightworks_materials:
        if use_composite_material:
            material_shell, material_web = get_shells_laminate_lightworks(dtype, thickness_step, stiffness_step, orientation_step)
        else:
            material_shell, material_web = get_shells_isotropic_lightworks(dtype, thickness_step, stiffness_step)
    else:
        if use_composite_material:
            material_shell, material_web = get_shells_laminate_predocs(dtype, thickness_step, stiffness_step, orientation_step)
        else:
            material_shell, material_web = get_shells_isotropic_predocs(dtype, thickness_step, stiffness_step)

    discreet_geometry = get_discreet_geometry(profiles_path, material_shell, material_web)

    # Calc stiffness
    materials = {s.shell for s in discreet_geometry.components}
    for material in materials:
        if use_lightworks_materials:
            material.stiffness = get_stiffness_for_shell_VCP(material, CompositeElement, engineering_constants_method='song', dtype=dtype)
        else:
            material.stiffness = get_stiffness_for_shell(material, CompositeElement, engineering_constants_method='song', dtype=dtype)

    # Create cross section processor
    cs_processor = HybridCrossSectionProcessor(2, 11.1, hybrid_processor='Jung', dtype=dtype)
    cs_processor.discreet_geometry = discreet_geometry
    cs_processor._update_if_required()

    test_load_case = ClassicCrossSectionLoadsWithBimoment(Vector([1 + lc_step, 0, 0]), Vector([0, 0, 0]), 0)

    displacements, load_states = cs_processor.calc_load_case(test_load_case)
    # displacements = cs_processor.calc_displacements(test_load_case)

    e0 = discreet_geometry.elements[0]

    return {
        # 'K_Jung': cs_processor._main_cs_processor.discreet_geometry.elements[0].shell.stiffness.K_Jung,
        # 'K_normal': cs_processor._main_cs_processor.discreet_geometry.elements[0].shell.stiffness.K_normal,
        # 'torsion_compliance': np.array([[cs_processor._main_cs_processor.discreet_geometry.elements[0].shell.stiffness.torsion_compliance]]),

        # 'Q': cs_processor._main_cs_processor._Q,
        # 'P': cs_processor._main_cs_processor._P,
        # 'R': cs_processor._main_cs_processor._R,
        # 'b_l': cs_processor._main_cs_processor._b,
        # 'B_u': cs_processor._main_cs_processor._B,
        # 'p_v': cs_processor._main_cs_processor._p_v,
        # 'p_q': cs_processor._main_cs_processor._p_q,
        # 'K_bb': cs_processor._main_cs_processor._K_bb,
        # 'K_vv': cs_processor._main_cs_processor._K_vv,
        # 'K_bv': cs_processor._main_cs_processor._K_bv,

        'cs_stiffness': cs_processor.stiffness.stiffness_matrix,
        'cs_displacements': np.array(displacements.tolist()),
        'e0_strain': np.array([[fun(0) for fun in load_states[e0].strain_state.values()]]),
        'e0_stress': np.array([[fun(0) for fun in load_states[e0].stress_state.values()]]),
    }


def plot_results_matrix(result_dict, base_name, output_path):
    thickness_steps = list(result_dict.keys())
    method_strings = list(result_dict[thickness_steps[0]].keys())
    dummy_results = result_dict[thickness_steps[0]][method_strings[0]]
    result_keys = list(dummy_results.keys())

    for result_key in result_keys:
        log.info(f'plot {base_name} {result_key} ...')
        result_shape = dummy_results[result_key].shape

        fig, axes = plt.subplots(*result_shape, figsize=(result_shape[1] * 4, result_shape[0] * 3), sharex=True, squeeze=False)
        fig.suptitle(result_key)

        for r in range(result_shape[0]):
            for c in range(result_shape[1]):
                ax = axes[r, c]
                for method_string in method_strings:
                    ax.plot(
                        thickness_steps,
                        [result_dict[thickness_step][method_string][result_key][r, c] for thickness_step in thickness_steps],
                        label=method_string,
                    )
                # ax.set_yscale('log')
                ax.legend()

        ax.invert_xaxis()
        ax.set_xscale('log')

        plt.savefig(os.path.join(output_path, f'{base_name}_{result_key}.png'))
        log.info(f'plot {base_name} {result_key} done')


def generate_gradient_plots(profiles_path, steps, step_func, use_composite_material, use_lightworks_materials, parameter_name, output_path):
    result_base_steps = {}
    result_gradients_steps = {}
    for step in steps:
        log.info(f'step = {step:.2E} ...')

        result_base = {}
        result_gradients = {}

        # CS
        # thickness_step_complex = step * 1.j
        results_base_cs = cs_calculation(profiles_path, np.complex128, use_composite_material, use_lightworks_materials, *step_func(step * 1.j))

        result_base['CS'] = {k: np.real(v) for k, v in results_base_cs.items()}
        result_gradients['CS'] = {k: np.imag(v) / step for k, v in results_base_cs.items()}

        result_base_steps[step] = result_base
        result_gradients_steps[step] = result_gradients

        # FD
        results_base_fd = cs_calculation(profiles_path, np.float64, use_composite_material, use_lightworks_materials, *step_func(0))
        results_step_fd = cs_calculation(profiles_path, np.float64, use_composite_material, use_lightworks_materials, *step_func(step))
        result_base['FD'] = results_base_fd
        result_gradients['FD'] = {}

        for (k1, v1), (k2, v2) in zip(results_base_fd.items(), results_step_fd.items()):
            assert k1 == k2
            result_gradients['FD'][k1] = (v2 - v1) / step

        log.info(f'step = {step:.2E} done')

    # plot_results_matrix(result_base_steps, f'{parameter_name}_base', output_path)
    # plot_results_matrix(result_gradients_steps, f'{parameter_name}_gradients', output_path)


steps_exp_list = np.linspace(1, 25, 30)


def test_cs_processor_gradient_thickness_predocs(profiles_path, tmp_dir):
    thickness_steps = [1e-3 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, thickness_steps, lambda step: (step, 0, 0, 0), False, False, 'thickness_pd_iso', tmp_dir)
    generate_gradient_plots(profiles_path, thickness_steps, lambda step: (step, 0, 0, 0), True, False, 'thickness_pd_comp', tmp_dir)


def test_cs_processor_gradient_stiffness_predocs(profiles_path, tmp_dir):
    stiffness_steps = [100e9 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, stiffness_steps, lambda step: (0, step, 0, 0), False, False, 'stiffness_pd_iso', tmp_dir)
    generate_gradient_plots(profiles_path, stiffness_steps, lambda step: (0, step, 0, 0), True, False, 'stiffness_pd_comp', tmp_dir)


def test_cs_processor_gradient_orientation_predocs(profiles_path, tmp_dir):
    orientation_steps = [1 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, orientation_steps, lambda step: (0, 0, step, 0), True, False, 'orientation_pd', tmp_dir)


def test_cs_processor_gradient_loads_predocs(profiles_path, tmp_dir):
    lc_steps = [1 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, lc_steps, lambda step: (0, 0, 0, step), False, False, 'loadcase_pd_iso', tmp_dir)
    generate_gradient_plots(profiles_path, lc_steps, lambda step: (0, 0, 0, step), True, False, 'loadcase_pd_comp', tmp_dir)


@pytest.mark.lightworks_required
def test_cs_processor_gradient_thickness_lightworks(profiles_path, tmp_dir):
    thickness_steps = [1e-3 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, thickness_steps, lambda step: (step, 0, 0, 0), False, True, 'thickness_lw_iso', tmp_dir)
    generate_gradient_plots(profiles_path, thickness_steps, lambda step: (step, 0, 0, 0), True, True, 'thickness_lw_comp', tmp_dir)


@pytest.mark.lightworks_required
def test_cs_processor_gradient_stiffness_lightworks(profiles_path, tmp_dir):
    stiffness_steps = [100e9 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, stiffness_steps, lambda step: (0, step, 0, 0), False, True, 'stiffness_lw_iso', tmp_dir)
    generate_gradient_plots(profiles_path, stiffness_steps, lambda step: (0, step, 0, 0), True, True, 'stiffness_lw_comp', tmp_dir)


@pytest.mark.lightworks_required
def test_cs_processor_gradient_orientation_lightworks(profiles_path, tmp_dir):
    orientation_steps = [1 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, orientation_steps, lambda step: (0, 0, step, 0), True, True, 'orientation_lw', tmp_dir)


@pytest.mark.lightworks_required
def test_cs_processor_gradient_loads_lightworks(profiles_path, tmp_dir):
    lc_steps = [1 * 10**(-e) for e in steps_exp_list]
    generate_gradient_plots(profiles_path, lc_steps, lambda step: (0, 0, 0, step), False, True, 'loadcase_lw_iso', tmp_dir)
    generate_gradient_plots(profiles_path, lc_steps, lambda step: (0, 0, 0, step), True, True, 'loadcase_lw_comp', tmp_dir)
