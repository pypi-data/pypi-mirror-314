"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

import numpy as np
import pytest
from OCC.Display.OCCViewer import rgb_color as color
from OCC.Display.SimpleGui import init_display

from PreDoCS.CrossSectionAnalysis.Display import plot_discreet_geometry, \
    plot_cross_section_element_values
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.vector import Vector
from PreDoCS.WingAnalysis.Display import display_wing_geometries, \
    display_beam_cross_sections, display_beam_axis, plot_beam_displacements

log = get_module_logger(__name__)

try:
    from PreDoCS.WingAnalysis.CPACS2PreDoCS import CPACS2PreDoCS
    from PreDoCS.WingAnalysis.cpacs_interface_predocs import CPACSInterfacePreDoCS
    from PreDoCS.WingAnalysis.BeamFEM import Beam, BeamElement4NodeWithWarping
    from PreDoCS.WingAnalysis.PreDoCSCoord import PreDoCSCoord
except ImportError:
    log.warning('cpacs_interface not installed')


pytestmark = pytest.mark.cpacs_interface_required


def test_cpacs2predocs(tmp_dir, data_dir, export_plots=False):
    """
    Don't compare physical values between PreDoCS and CPACS. Only tests the import methods.
    """
    cpacs_interface = CPACSInterfacePreDoCS(os.path.join(data_dir, 'CPACS'), 'IEA-15-240-RWT_CPACS.xml')
    c2p = CPACS2PreDoCS(cpacs_interface, loads_are_internal_loads=True, get_element_stiffness_func=get_stiffness_for_shell)
   
    # Input
    wing_length = c2p.halfspan
    num_beam_elements = 8  # Number of beam FEM elements
    # z2_nodes = [wing_length/num_beam_elements*i for i in range(num_beam_elements+1)] # Positions of the nodes of the FE model
    # z2_cross_sections = [z2 for z2 in z2_nodes] # Positions of the cross sections for the cross section analysis
    # z2_cross_sections[0] += 0.1
    # z2_cross_sections[-1] -= 0.1
    # points_to_plot = 100 # Number of points over the beam axis for plotting the results

    beam_reference_point = Vector([0, 0, 0])
    beam_reference_axis = Vector([0, 1, 0])

    beam_nodes_z2 = np.linspace(0, wing_length, num_beam_elements + 1)
    predocs_coord = PreDoCSCoord([beam_reference_point], [beam_reference_axis], [wing_length], beam_nodes_z2)
    z2_cross_sections = predocs_coord.z2_cs
    z2_nodes = predocs_coord.z2_bn
    z2_2_point_wing = predocs_coord.z2_2_point_wing

    # Create the cross section geometries at given spanwise positions of the wing and
    # computes the cross section stiffness and inertia data from the cross section geometries.
    # Only the upper and lower wing shell with the cells and the spars are imported.
    cs_geometries, cs_processors = c2p.generate_cross_section_data(
        predocs_coord,
        'Hybrid',  # The cross section processor type
        False,  # True for parallel processing
        element_length=0.1,
        hybrid_processor='Jung',
    )

    cs_data = [(cs_processor.stiffness, cs_processor.inertia) for cs_processor in cs_processors]

    if export_plots:
        i = 0
        for processor in cs_processors:
            plot_discreet_geometry(processor.discreet_geometry, file=os.path.join(tmp_dir, 'tests', 'test_cpacs2predocs_geometry_{}.png'.format(i)))
            i += 1
            
    # Stiffness and inertia distribution

    if export_plots:
        Beam.plot_stiffness_and_inertia(
            cs_data, z2_cross_sections, wing_length,
            file_format_string=os.path.join(tmp_dir, 'tests', 'test_cpacs2predocs_stiffness_{}.png')
        )
        
    # Beam FE model creation
    beam = Beam.create_beam(cs_data, z2_cross_sections, z2_nodes, z2_2_point_wing, BeamElement4NodeWithWarping)

    # Beam FE model calculations
    clamped_end = [(0, i, 0) for i in range(6)]
    load_vector = beam.get_load_vector(node_loads=[(num_beam_elements, 0, 100e3)])
    beam_displacements_list, node_reactions_vector_list = beam.static_analysis(clamped_end, [load_vector])
    beam_displacements_function = lambda z2: beam.post_processing(beam_displacements_list[0], z2)[0]
    cross_section_displacements_function = lambda z2: beam.post_processing(beam_displacements_list[0], z2)[1]
    
    # Stain and strss distribution of one cross section for the load case
    cross_section_index = 3 # Index of the cross section for the stress plot
    cs_processor = cs_processors[cross_section_index] # The coresponding cross section processor
    z2_cross_section = z2_cross_sections[cross_section_index] # The z-position of the cross section
    
    # The cross section displacements from the FEM analysis
    cross_section_displacements = cross_section_displacements_function(z2_cross_section)
    
    # Calculate the load states from the cross section displacements
    load_states = cs_processor.calc_element_load_states(cross_section_displacements)
    
    if export_plots:
        points_to_plot = 100
        z2_to_plot = np.array(range(points_to_plot)) / (points_to_plot-1) * wing_length
        displacements = np.array([[z2] + beam_displacements_function(z2) for z2 in z2_to_plot])
        plot_beam_displacements({'PreDoCS': displacements}, num_plots=6, plot_size=(5,3), title='CPACS Test',
                                file=os.path.join(tmp_dir, 'tests', 'test_cpacs2predocs_displacements.png'))
        
        # 3D Result Viewer with undeformed and deformed state
        viewer3d, start_display, add_menu, add_function_to_menu = init_display()

        display_wing_geometries(viewer3d, c2p)
        display_beam_cross_sections(
            viewer3d=viewer3d,
            predocs_coord=predocs_coord,
            discreet_cross_section_geometries=[p.discreet_geometry for p in cs_processors],
            beam_displacements=beam_displacements_function,
        )
        display_beam_axis(viewer3d, predocs_coord, color=color(0, 0, 0))
        display_beam_axis(viewer3d, predocs_coord, beam_displacements_function, color=color(1, 1, 1))

        viewer3d.FitAll()
        viewer3d.ExportToImage(os.path.join(tmp_dir, 'tests', '3d-export.png'))
        
        # Plot the normal flow for all cross section elements
        element_data = {element: load_state.stress_state['N_zz'] for element, load_state in load_states.items()}
        plot_cross_section_element_values(cs_processor, element_data, values_are_functions=True,
                                          max_display_value=-0.5, plot_value_numbers=False,
                                          cross_section_size=(15,8), title='Normal flow N_zz')


def test_read_spar_cells(tmp_dir, data_dir):
    cpacs_interface = CPACSInterfacePreDoCS(os.path.join(data_dir, 'CPACS'), 'Beam_Composite_Export_Test_32_spar_cells.xml')
    c2p = CPACS2PreDoCS(cpacs_interface, loads_are_internal_loads=False, get_element_stiffness_func=get_stiffness_for_shell)

    spar = c2p.wing.component_segments[0].spars[0]
    assert spar.spar_cells[0].uid == 'spar_cell1'
    assert spar.spar_cells[1].uid == 'spar_cell2'


def test_create_spar_cells(tmp_dir, data_dir):
    cpacs_interface = CPACSInterfacePreDoCS(os.path.join(data_dir, 'CPACS'), 'Beam_Composite_Export_Test_32_spar_cells.xml')
    c2p = CPACS2PreDoCS(cpacs_interface, loads_are_internal_loads=False, get_element_stiffness_func=get_stiffness_for_shell)

    # Input
    wing_length = c2p.halfspan
    num_beam_elements = 10  # Number of beam FEM elements
    beam_nodes_z2 = np.linspace(0, wing_length, num_beam_elements + 1)
    # z_nodes = [wing_length / num_beam_elements * i for i in
    #            range(num_beam_elements + 1)]  # Positions of the nodes of the FE model
    # z_cross_sections = [(z_nodes[i] + z_nodes[i+1])/2 for i in range(len(z_nodes)-1)]  # Positions of the cross sections for the cross section analysis

    beam_reference_point = Vector([0, 0, 0])
    beam_reference_axis = Vector([0, 1, 0])

    predocs_coord = PreDoCSCoord([beam_reference_point], [beam_reference_axis], [wing_length], beam_nodes_z2)

    # Create the cross section geometries at given spanwise positions of the wing and
    # computes the cross section stiffness and inertia data from the cross section geometries.
    # Only the upper and lower wing shell with the cells and the spars are imported.
    cs_geometries, cs_processors = c2p.generate_cross_section_data(
        predocs_coord,
        'Hybrid',  # The cross section processor type
        False,  # True for parallel processing
        element_length=0.05,
        hybrid_processor='Jung',
    )

    cs_mass_density = [cs_processor.inertia.inertia_matrix[0, 0] for cs_processor in cs_processors]

    # Beam data
    length = 10
    radius = 0.5
    SymmetricBalanced_area_density = 10 * 0.001 * 1600
    SymmetricBalancedIso_area_density = 8 * 0.001 * 1600
    shell_mass = length * np.pi * radius * SymmetricBalanced_area_density
    spar_mass = length * 2 * radius * SymmetricBalanced_area_density
    spar_mass_iso = length * 2 * radius * SymmetricBalancedIso_area_density
    wing_mass = 2*shell_mass + spar_mass
    wing_mass_iso = 2*shell_mass + spar_mass_iso

    high_density = wing_mass / wing_length
    low_density = wing_mass_iso / wing_length

    assert np.allclose(cs_mass_density,
                             [high_density, high_density, low_density, low_density, low_density,
                              low_density, low_density, low_density, high_density, high_density],
                             rtol=2.5e-2)


def test_wing_uid(tmp_dir, data_dir):
    cpacs_interface = CPACSInterfacePreDoCS(os.path.join(data_dir, 'CPACS'), 'Rect_Beam_vtp.xml')

    c2p1 = CPACS2PreDoCS(
        cpacs_interface,
        loads_are_internal_loads=False,
        get_element_stiffness_func=get_stiffness_for_shell,
        wing_index=0,
    )

    assert c2p1._wing_index == 0

    c2p2 = CPACS2PreDoCS(
        cpacs_interface,
        loads_are_internal_loads=False,
        get_element_stiffness_func=get_stiffness_for_shell,
        wing_uid='vtp',
    )

    assert c2p2._wing_index == 1
