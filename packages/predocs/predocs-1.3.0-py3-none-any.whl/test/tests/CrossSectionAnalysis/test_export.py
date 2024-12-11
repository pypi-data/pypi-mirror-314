"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os

from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from test.CrossSections import get_wing_cross_section_geometry_definition_dict
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElement, CompositeElement
from PreDoCS.CrossSectionAnalysis.Processors import IsotropicCrossSectionProcessor
from PreDoCS.util.vector import Vector
from PreDoCS.CrossSectionAnalysis.Interfaces import ClassicCrossSectionLoads
from PreDoCS.CrossSectionAnalysis.Export import export_EnSight_Gold, generate_BECAS_input, \
    write_discreet_geometry_to_ABAQUS_file
import pytest


@pytest.mark.unit_tests
def test_cross_section_geometry_export(data_dir, tmp_dir):
    geometry_ids = [
        100]  # TODO: list(range(100,107)) + list(range(200,207)) + [210,211,220,221,222] + [500,501] + list(range(700,707)) + [710,711]
    wing_cs_definition_dict = get_wing_cross_section_geometry_definition_dict(os.path.join(data_dir, 'profiles'))
    for geometry_id in geometry_ids:
        # Isotropic Element
        discreet_geometry = wing_cs_definition_dict[geometry_id].get_discreet_geometry(IsotropicElement,
                                                                                       element_length=0.01)
        write_discreet_geometry_to_ABAQUS_file(discreet_geometry,
                                               os.path.join(tmp_dir, 'tests', 'test_isotropic_{}.inp'.format(geometry_id)))
        generate_BECAS_input(discreet_geometry, os.path.join(tmp_dir, 'tests', 'test_isotropic_{}'.format(geometry_id)))

        # Composite Element
        discreet_geometry = wing_cs_definition_dict[geometry_id].get_discreet_geometry(CompositeElement,
                                                                                       element_length=0.01)
        write_discreet_geometry_to_ABAQUS_file(discreet_geometry,
                                               os.path.join(tmp_dir, 'tests', 'test_composite_{}.inp'.format(geometry_id)))
        generate_BECAS_input(discreet_geometry, os.path.join(tmp_dir, 'tests', 'test_composite_{}'.format(geometry_id)))


@pytest.mark.unit_tests
def test_EnSight_Gold_export(tmp_dir, cs_definition):
    discreet_geometry = cs_definition.get_discreet_geometry(element_type=IsotropicElement, element_length=0.1)
    
    # Calc stiffness
    materials = {s.shell for s in discreet_geometry.components}
    for material in materials:
        material.stiffness = get_stiffness_for_shell(material, IsotropicElement, engineering_constants_method='song')
            
    # Create cross section processor
    cs_processor = IsotropicCrossSectionProcessor()
    cs_processor.discreet_geometry = discreet_geometry
    tmp, load_states = cs_processor.calc_load_case(ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([1, 0, 0])))
    
    export_EnSight_Gold(discreet_geometry, 'test_export', tmp_dir, load_states=load_states)
