"""
Project description:
Maintainer:

.. codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
.. created:: 08.03.2019
"""
import logging
import os

import numpy as np
import pytest
from deepdiff import DeepDiff

from PreDoCS.CrossSectionAnalysis.Display import plot_materials
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)
logging.getLogger('matplotlib').setLevel(logging.ERROR)

try:
    from PreDoCS.SolverInterface.SolverInterfaceBase import PreDoCS_SolverControl
    from PreDoCS.SolverInterface.SolverInterfacePreDoCS import PreDoCS_SolverPreDoCS
except ImportError:
    log.warning('cpacs_interface not installed')


pytestmark = pytest.mark.cpacs_interface_required


def load_CTNT_solver(data_dir):
    # CTNT use case
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
        parallel_process=False,
        engineering_constants_method='with_poisson_effect',
        hybrid_processor='Jung',
        front_spar_uid=front_spar_uid,
        rear_spar_uid=rear_spar_uid,
        calc_element_load_state_functions=True,
        calc_element_load_state_min_max=True,
        mold_angle=0
    )

    # Initialise Model
    solver = PreDoCS_SolverPreDoCS(predocs_ctrl)

    # Create PreDoCS Model
    solver.build_model()
    log.info('Model created successfully')

    return solver


def assert_discreet_geometries(dg1, dg2):
    for n1, n2 in zip(dg1.nodes, dg2.nodes):
        assert n1.id == n2.id
        assert n1.position == n2.position

    for e1, e2 in zip(dg1.elements, dg2.elements):
        assert e1.id == e2.id
        assert e1.position == e2.position
        assert e1.component == e2.component
        assert e1.segment == e2.segment

    for c1, c2 in zip(dg1.components, dg2.components):
        assert c1.id == c2.id
        assert c1.shell.uid == c2.shell.uid
        assert (c1.material_region is None and c2.material_region is None) or (c1.material_region.uid == c2.material_region.uid)
        assert c1.midsurface_offset == c2.midsurface_offset

    for s1, s2 in zip(dg1.segments, dg2.segments):
        assert s1.id == s2.id
        assert s1.elements == s2.elements
        assert s1.reference_length(dg1) == s2.reference_length(dg2)
        assert s1.node1 == s2.node1
        assert s1.node2 == s2.node2

    for c1, c2 in zip(dg1.cells, dg2.cells):
        assert c1.nodes == c2.nodes
        assert c1.elements == c2.elements
        assert c1.segments == c2.segments
        assert c1.cut_node == c2.cut_node
        assert c1.position == c2.position
        assert c1.area == c2.area


def test_solver_interface_deterministic_new_solvers(data_dir, tmp_path):
    solver1 = load_CTNT_solver(data_dir)
    cs_processor1 = solver1.cs_processors[0]
    sm1 = cs_processor1.stiffness.stiffness_matrix
    dg1 = cs_processor1.discreet_geometry

    solver2 = load_CTNT_solver(data_dir)
    cs_processor2 = solver2.cs_processors[0]
    sm2 = cs_processor2.stiffness.stiffness_matrix
    dg2 = cs_processor2.discreet_geometry

    diff = sm2 - sm1
    diff_rel = diff / sm1 * 100

    assert np.all(diff == 0)

    # Plot different geometries
    plot_kwargs = dict(
        plot_layup=False,
        plot_element_ids=True,
        plot_segment_ids=True,
        plot_component_ids=False,
        plot_node_ids=False,
        show=True,
        cross_section_size=(15, 7),
        element_colors='tab20',
        material_colors='tab20',
    )
    plot_materials(dg1, title='ref', file=os.path.join(tmp_path, 'ref.png'), **plot_kwargs)
    plot_materials(dg2, title='res', file=os.path.join(tmp_path, 'res.png'), **plot_kwargs)

    assert_discreet_geometries(dg1, dg2)

    # Compare all matrices of the cross section processors
    def filter_dict2(fd):
        return {k: v for k, v in fd.items() if isinstance(v, np.ndarray)}
    cs_diff = DeepDiff(
        filter_dict2(cs_processor1._main_cs_processor.__dict__),
        filter_dict2(cs_processor2._main_cs_processor.__dict__),
        math_epsilon=1e-3
    )

    assert len(cs_diff) == 0


def test_solver_interface_deterministic_new_generated_discreet_geometry(data_dir, tmp_path):
    solver = load_CTNT_solver(data_dir)

    # Compare data from same geometry
    cs_processor = solver.cs_processors[0]
    cs_geometry = solver._cs_geometry[0]

    build_geometry_kwargs = dict(
        cross_section_processor_name='Hybrid',
        element_length=0.05,
        segment_deflection=None,
        method='with_poisson_effect',  # Engineering constants method
        hybrid_processor='Jung',
    )

    def calc_stiffness_matrix(cs_processor, geometry):
        discreet_geometry = geometry.create_discreet_cross_section_geometry(
            element_type=CompositeElement, **build_geometry_kwargs
        )

        materials = {s.shell for s in discreet_geometry.components}
        for material in materials:
            log.debug(f'Calculate material stiffness for "{material.name}"')
            material.stiffness = get_stiffness_for_shell(material, CompositeElement, **build_geometry_kwargs)

        cs_processor.discreet_geometry = discreet_geometry
        cs_processor._update_if_required()
        return cs_processor.stiffness.stiffness_matrix, discreet_geometry

    sm1, dg1 = calc_stiffness_matrix(cs_processor, cs_geometry)
    sm2, dg2 = calc_stiffness_matrix(cs_processor, cs_geometry)

    diff1 = sm2 - sm1
    assert np.all(diff1 == 0)
