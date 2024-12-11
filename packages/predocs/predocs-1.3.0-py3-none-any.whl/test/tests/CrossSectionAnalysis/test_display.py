"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
from random import random

import pytest

from PreDoCS.CrossSectionAnalysis.Display import plot_discreet_geometry, \
    plot_cross_section, plot_cross_section_cells, \
    plot_cross_section_element_values
from PreDoCS.CrossSectionAnalysis.Processors import IsotropicCrossSectionProcessor, \
    HybridCrossSectionProcessor, JungCrossSectionProcessor
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElement, \
    CompositeElement
from PreDoCS.MaterialAnalysis.Shells import get_stiffness_for_shell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.vector import Vector
from test.CrossSections import get_wing_cross_section_geometry_definition_dict

log = get_module_logger(__name__)


@pytest.mark.slow
def test_cross_section_plots(data_dir, tmp_dir):
    #geometry_ids = list(range(100,107)) + list(range(200,207)) + [210,211,220,221,222] + [500,501] + list(range(700,707)) + [710,711]
    geometry_ids = [106]# TODO: [106, 206, 210, 222, 500, 706, 711]
    processor_types = [
        (IsotropicCrossSectionProcessor, IsotropicElement),
        (JungCrossSectionProcessor, CompositeElement),
        (HybridCrossSectionProcessor, CompositeElement),
    ]
    wing_cs_definition_dict = get_wing_cross_section_geometry_definition_dict(os.path.join(data_dir, 'profiles'))
    for geometry_id in geometry_ids:
        log.info(geometry_id)
        for processor_type, element_type in processor_types:
            processor_label = 'P{}'.format(processor_types.index((processor_type, element_type)))
            discreet_geometry = wing_cs_definition_dict[geometry_id].get_discreet_geometry(element_type, element_length=0.05)
            plot_discreet_geometry(discreet_geometry, file=os.path.join(tmp_dir, 'tests', '{}_plot_geometry_{}.png'.format(geometry_id, processor_label)))
            
            # Calc stiffness
            materials = {s.shell for s in discreet_geometry.components}
            for material in materials:
                material.stiffness = get_stiffness_for_shell(material, element_type, engineering_constants_method='song')
            
            # Create cross section processor
            cs_processor = processor_type()
            cs_processor.discreet_geometry = discreet_geometry
            if isinstance(cs_processor, JungCrossSectionProcessor):
                cs_processor._shear_center = Vector([0, 0])
            plot_cross_section(cs_processor, file=os.path.join(tmp_dir, 'tests', '{}_plot_cross_section_{}.png'.format(geometry_id, processor_label)))
            plot_cross_section_cells(cs_processor, file=os.path.join(tmp_dir, 'tests', '{}_plot_cross_section_cells_{}.png'.format(geometry_id, processor_label)))
            
            elements = cs_processor.discreet_geometry.elements
            demo_values = {e: random() for e in elements}
            plot_cross_section_element_values(cs_processor, demo_values,
                file=os.path.join(tmp_dir, 'tests', '{}_plot_cross_section_element_values_{}.png'.
                                  format(geometry_id, processor_label)))

            demo_functions = {e: lambda s: random() + s * random() for e in elements}
            plot_cross_section_element_values(cs_processor, demo_functions, values_are_functions=True,
                file=os.path.join(tmp_dir, 'tests', '{}_plot_cross_section_element_functions{}.png'.
                                  format(geometry_id, processor_label)))
