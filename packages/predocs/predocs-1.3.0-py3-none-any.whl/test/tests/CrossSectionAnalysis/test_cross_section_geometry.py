"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
import pickle

import pytest

from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import CrossSectionGeometry, load_profile_points, \
    WingCrossSectionGeometryDefinition
from PreDoCS.CrossSectionAnalysis.Display import plot_discreet_geometry
from PreDoCS.CrossSectionAnalysis.Export import write_discreet_geometry_to_ABAQUS_file, \
    generate_BECAS_input
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElement
from PreDoCS.MaterialAnalysis.Shells import IsotropicShell
from PreDoCS.util.occ import point_list_to_wire
from PreDoCS.util.vector import Vector


@pytest.mark.unit_tests
def test_profile_web_geometry(tmp_dir, data_dir, alu, alu_thick, export_geometry=False):
    cs_geometry = CrossSectionGeometry()
    profile_wire = point_list_to_wire(load_profile_points(os.path.join(data_dir, 'profiles', 'rectangle.txt'), False), closed_wire=True)
    profile = CrossSectionGeometry.Assembly(cs_geometry, profile_wire, alu)
    profile.add_material_region_from_points('id', Vector([0,0]), Vector([0.5,0]), alu_thick)
    cs_geometry.add_profile_assembly(profile)
    cs_geometry.add_web_from_line(Vector([0.5,-1]), Vector([0.5, 1]), alu_thick, 'Spar')
    cs_geometry.add_web(CrossSectionGeometry.Assembly(cs_geometry, point_list_to_wire([Vector([0.5,0.25]), Vector([1, 0.25])]), alu_thick))
    discreet_geometry = cs_geometry.create_discreet_cross_section_geometry(element_type=IsotropicElement, element_length=0.1)
    if export_geometry:
        plot_discreet_geometry(discreet_geometry, file=os.path.join(tmp_dir, 'test_profile_web_geometry.png'), cross_section_size=(15,10))
        #write_discreet_geometry_to_ABAQUS_file(geometry, 'test_profile_web_geometry.inp')
        #generate_BECAS_input(discreet_geometry, './test_profile_web_geometry/')
    
#     materials = {s.material for s in discreet_geometry.components}
#     for material in materials:
#         material.stiffness = get_stiffness_for_material(material, IsotropicElement)
#     cs_processor = IsotropicCrossSectionProcessor()
#     cs_processor.discreet_geometry = discreet_geometry
#     #cs_processor._update_if_required()


@pytest.mark.unit_tests
def test_geometry_definition(tmp_dir, cs_definition, export_geometry=False):
    discreet_geometry = cs_definition.get_discreet_geometry(element_type=IsotropicElement, element_length=0.1)
    if export_geometry:
        plot_discreet_geometry(discreet_geometry, file=os.path.join(tmp_dir, 'test_geometry_definition.png'),
                               cross_section_size=(15, 10))
        write_discreet_geometry_to_ABAQUS_file(discreet_geometry, os.path.join(tmp_dir, 'test_geometry_definition.inp'))
        generate_BECAS_input(discreet_geometry, os.path.join(tmp_dir, 'test_geometry_definition'))


@pytest.mark.unit_tests
def test_geometry_pickle(tmp_dir, cs_definition):
    geometry = cs_definition.get_geometry()

    # Save
    pickle.dump(geometry, open(os.path.join(tmp_dir, 'geometry.p'), 'wb'))

    # Load
    geometry_load = pickle.load(open(os.path.join(tmp_dir, 'geometry.p'), 'rb'))


@pytest.mark.unit_tests
def test_hybrid_discretization(data_dir, tmp_dir, profiles_path, alu_material, export_geometry=True):
    # Geometry
    airfoil_spline = {
        'DegMin': 3,
        'DegMax': 15,
        'Continuity': 4,  # = GeomAbs_C2
        'Tol3D': 1.0e-4,
    }
    geometry_points = load_profile_points(os.path.join(data_dir, 'profiles', 'NACA-2412-cos-50.txt'), True)
    alu = IsotropicShell(alu_material, 5e-3, name='Alu')
    alu_thick = IsotropicShell(alu_material, 10e-3, name='Alu thick')
    geometry = WingCrossSectionGeometryDefinition(
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
        te_cutoff_x=0.98,
        profile_spline=airfoil_spline,
        base_material_as_material_region=True,
    )

    # Discreet geometry
    discreet_geometry_element_length = geometry.get_discreet_geometry(
        element_type=IsotropicElement,
        element_length=0.02,
    )
    discreet_geometry_segment_deflection = geometry.get_discreet_geometry(
        element_type=IsotropicElement,
        segment_deflection=1e-4,
    )
    discreet_geometry_hybrid = geometry.get_discreet_geometry(
        element_type=IsotropicElement,
        segment_deflection=1e-4,
        element_length=0.02,
    )

    assert len(discreet_geometry_element_length.elements) == 108
    assert len(discreet_geometry_segment_deflection.elements) == 131
    assert len(discreet_geometry_hybrid.elements) == 150

    # Plots
    if export_geometry:
        cross_section_size = (10, 5)
        plot_discreet_geometry(
            discreet_geometry_element_length,
            file=os.path.join(tmp_dir, 'test_discreet_geometry_element_length.png'),
            cross_section_size=cross_section_size,
        )
        plot_discreet_geometry(
            discreet_geometry_segment_deflection,
            file=os.path.join(tmp_dir, 'test_discreet_geometry_segment_deflection.png'),
            cross_section_size=cross_section_size,
        )
        plot_discreet_geometry(
            discreet_geometry_hybrid,
            file=os.path.join(tmp_dir, 'test_discreet_geometry_hybrid.png'),
            cross_section_size=cross_section_size,
        )
