"""
This module provides an import of CPACS wings in PreDoCS.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import concurrent.futures as cf
from typing import Optional, Callable, Union

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepTools import breptools_Write
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Trsf
from OCC.Display.OCCViewer import rgb_color
from OCC.Display.SimpleGui import init_display
from cpacs_interface.cpacs_interface import CPACSInterface
from cpacs_interface.cpacs_objects import LoadApplicationPoints, Shell
from PreDoCS.util.filters import find
from PreDoCS.util.occ import transform_shape, get_intersection_points, get_eta_xsi, transformation_matrix_2_occ

from PreDoCS.CrossSectionAnalysis.CrossSectionGeometry import CrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Interfaces import ICrossSectionProcessor
from PreDoCS.CrossSectionAnalysis.Processors import get_element_type_from_cross_section_processor_name, \
    get_cross_section_processor_from_name
from PreDoCS.LoadAnalysis.Load import LoadCase, DynamicReferencePoints
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.geometry import transform_location_m
from PreDoCS.util.occ import calc_cross_section_plane, point_to_vector, get_intersection_wire, transform_wire
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


class CPACS2PreDoCS:
    """
    This class provides methods for importing a CPACS wing in PreDoCS.
    
    Attributes
    ----------
    _loadcase_dict: dict(str, ILoadCase)
        Dict of the load case UID's from CPACS to the load cases of PreDoCS.
    _load_reference_points: DynamicReferencePoints
        The load reference points imported from CPACS
    _spars: dict(str, list, OCC.TopoDS.TopoDS_Shape, IMaterial, dict((float, float), (str, IMaterial)))
        Dict of all spars:
            key:
                - uID
            values:
                - list of spar position vectors in CPACS coordinate system
                - cut geometry of all spar segments of the wing
                - material
                - Dict of all cells of an uid of a spar segments of the wing.
                    Keys of the inner dict are the inner and outer border in eta coordinates and the value is
                    the uid of the spar cell and the material.
    _shells: list((str, str, OCC.TopoDS.TopoDS_Shape, IMaterial, list(OCC.TopoDS.TopoDS_Shape, IMaterial)))
        List of shells uids, type, shapes, the base material and a list of material regions with shape and material.
    """
    def __init__(self, cpacs_interface: CPACSInterface, loads_are_internal_loads: bool, get_element_stiffness_func: Callable,
                 wing_index: Optional[int] = None, wing_uid: Optional[str] = None,
                 component_segment_index: int = 0, **kwargs):
        """
        Constructor.
        

        Parameters
        ----------
        directory: str
            The directory of the CPACS file.
        filename: str
            The filename of the CPACS file.
        loads_are_internal_loads
            True if loads are internal loads (cut loads), False for external loads (nodal loads).
        name: str
            Value of the name element in the CPACS header. Only used, if the CPACS file does not exist.
        description: str
            Value of the description element in the CPACS header. Only used, if the CPACS file does not exist.
        creator: str
            Value of the creator element in the CPACS header. Only used, if the CPACS file does not exist.
        version: str
            Value of the version element in the CPACS header (This is NOT the CPACS version).
            Only used, if the CPACS file does not exist.
        wing_index: int (default: 0)
            Index of the wing, usually 0: wing, 1: htp, 2: vtp. Starts with 0. Alternative to wing_uid.
        wing_uid
            uID of the wing. Alternative to wing_idx.
        component_segment_index: int (default: 0)
            The component segment index of the wing. Starts with 0.
        """
        self._cpacs_interface = cpacs_interface
        self._loads_are_internal_loads = loads_are_internal_loads
        self._get_element_stiffness_func = get_element_stiffness_func

        if wing_index is None and wing_uid is None:
            log.warning('Neither wing_index nor wing_uid given, choose wing_index=0.')
            wing_index = 0

        if wing_index is not None and wing_uid is not None:
            log.warning(f'wing_index and wing_uid given, choose wing_index={wing_index}.')
            wing_uid = None

        if wing_index is not None:
            num_wings = cpacs_interface.tixi_handle.getNamedChildrenCount(cpacs_interface._xpath + '/wings', 'wing')
            assert wing_index < num_wings, f'wing_index is "{wing_index}", but only "{num_wings}" wings in CPACS file.'
        else:
            wing_path = cpacs_interface.tixi_handle.uIDGetXPath(wing_uid)
            if wing_path.endswith(']'):
                wing_index = int(wing_path.split('[')[-1][: -1]) - 1
            else:
                wing_index = 0

        self._wing_index = wing_index
        self._component_segment_index = component_segment_index

        self._wing_reference_position = None
        self._wing_reference_direction = None
        self._beam_reference_points = None

        self._read_required_initial = True
        self._read_cpacs()

    @property
    def cpacs_interface(self) -> CPACSInterface:
        return self._cpacs_interface

    def __getstate__(self):
        """Make pickle possible."""
        state = self.__dict__.copy()
        state['_cpacs_interface'] = None
        return state

    def __setstate__(self, state):
        """Make pickle possible."""
        self.__dict__.update(state)

    def _read_cpacs(self):
        """Reads the CPACS file."""
        read = self._cpacs_interface._read_required
        self._cpacs_interface.read(force_read=False)
        if read or self._read_required_initial:
            self._read_required_initial = False
            self._loadcase_dict, self._load_reference_points = self._read_cpacs_loads_data()

            wing_uid = self._cpacs_interface.tixi_handle.getTextAttribute(self.wing._xpath, 'uID')

            # Load wing reference direction
            wrds_wing = [
                lap for lap in self._cpacs_interface.load_application_points
                if lap.parent_uid == wing_uid and lap.uid == wing_uid + '_wing_reference_direction'
            ]
            if len(wrds_wing) > 0:
                points = [Vector(p) for p in wrds_wing[0].load_application_points_dict.values()]
                assert len(points) == 2
                self._wing_reference_position = points[0]
                self._wing_reference_direction = points[1].normalised

            # Load beam reference points
            brps_wing = [
                lap for lap in self._cpacs_interface.load_application_points
                if lap.parent_uid == wing_uid and lap.uid == wing_uid + '_beam_reference_points'
            ]
            if len(brps_wing) > 0:
                # assert len(brps_wing) == 1, f'Beam reference points for wing "{wing_uid}" are necessary.'
                self._beam_reference_points = [Vector(p) for p in brps_wing[0].load_application_points_dict.values()]

    @staticmethod
    def get_wing_load_application_points(cpacs_interface: CPACSInterface, wing_uid: str) -> LoadApplicationPoints:
        """
        Finds load application points for a wing.
        """
        lap = None

        laps_wing = [lap for lap in cpacs_interface.load_application_points if lap.parent_uid == wing_uid]
        if len(laps_wing) == 0:
            log.warning('No load application points were found in file!')

        elif len(laps_wing) == 1:
            lap = laps_wing[0]
        else:
            laps_wing_new = [lap for lap in laps_wing if lap.uid == wing_uid + '_load_application_points']
            if len(laps_wing_new) == 1:
                lap = laps_wing_new[0]
            else:
                log.warning(f'More than one set of load application points for wing "{wing_uid}" found, '
                            f'take the first one ({laps_wing[0].uid}).')
        return lap

    def _read_cpacs_loads_data(self):
        """
        Reads all Load Cases from a CPACS file.

        Returns
        -------
        dict(str, ILoadCase)
            Dict of the load case UID's from CPACS to the load case of PreDoCS.
        DynamicReferencePoints
            Object containing the load reference points of the selected wing_index
        """
        wing_uid = self._cpacs_interface.tixi_handle.getTextAttribute(self.wing._xpath, 'uID')
        loads_are_internal_loads = self._loads_are_internal_loads

        # Find load application points
        lap = self.get_wing_load_application_points(self._cpacs_interface, wing_uid)
        if lap is None:
            return None, None

        # TODO: sort by lap.load_application_points_dict.keys() ?
        load_reference_points = DynamicReferencePoints(
            [p.x for p in lap.load_application_points_dict.values()],
            [p.y for p in lap.load_application_points_dict.values()],
            [p.z for p in lap.load_application_points_dict.values()],
        )

        # Find all load cases for this load application point
        load_cases_all = self._cpacs_interface.flight_load_cases + self._cpacs_interface.ground_load_cases
        load_sets = []
        for lc in load_cases_all:
            load_sets.extend([ls for ls in (lc.cut_loads if loads_are_internal_loads else lc.nodal_loads)
                              if ls.load_application_points_uid == lap.uid])

        # Check if any Load Cases Exist in File, return _load_reference_points only if not
        if len(load_sets) == 0:
            log.warning(f'No loadcases (loads_are_internal_loads: {loads_are_internal_loads}) were found in file '
                        f'for wing "{wing_uid}"!')
            return None, load_reference_points

        # Get force and moment vectors from all load cases
        result = {}
        for ls in load_sets:
            if ls.parent.uid in result:
                log.warning(f'Loadcase uID "{ls.parent.uid}" already imported. It will be overwritten.')
            fx, fy, fz, mx, my, mz = ls.component_vectors
            result[ls.parent.uid] = LoadCase(ls.parent.name,
                                             fx, fy, fz, mx, my, mz,
                                             load_reference_points,
                                             internal_loads=loads_are_internal_loads)

        return result, load_reference_points

    def _generate_cross_section_data(
            self,
            cross_section_id,
            z2_cross_section,
            predocs_coord,
            element_type,
            processor_type,
            cut_components_uids: Optional[list[list[Union[str, int]]]] = None,
            skip_material_stiffness_calculation_and_update_processors: bool = False,
            **kwargs,
    ):
        """
        Create one cross section geometry at a given spanwise position of the wing,
        creates the cross section processor and perform the cross section analysis.
        Only the upper and lower wing shell with the material regions and the spars are imported.
        In this method the transformation from the CPACS coordinate system into the PreDoCS coordinate system is performed.
        
        Parameters
        ----------
        cross_section_id: int
            ID of the cross section.
        z2_cross_section: float
            The spanwise position where to create the geometries of the cross section. z_beam starts at the beam
            reference point and is orientated in the beam reference axis direction.
        get_section_parameter: func(float)
            Returns section parameters of z2 as input.
        c2p_transformation: gp_Trsf
            Base transformation form the CPACS to the PreDoCS coordinate system.
        element_type: class <- IElement
            The element type for the cross section.
        processor_type: class <- ICrossSectionProcessor
            The cross section processor.
        position_blurring: float
            The max distance from the node position to the given position.
        element_length: float (default: None)
            If not None, the elements are discretized by dividing the segments into elements with the same length.
            This element length is given by this parameter.
        segment_deflection: float (default: None)
            If not None, the elements are discretized by dividing the segments into elements, that the deflection
            area between the curve to the discreet geometry for a segment is equal to this parameter.
        use_fast_abscissa: bool (default: True)
            If True, a faster and simpler calculation of the abscissa is used
            (OCC.GCPnts.GCPnts_QuasiUniformAbscissa instead of OCC.GCPnts.GCPnts_UniformAbscissa and
            OCC.GCPnts.GCPnts_QuasiUniformDeflection instead of OCC.GCPnts.GCPnts_UniformDeflection).
            For True, the continuity of curve has to be at least C2.
        close_open_ends
            True, if open ends of the cross-section are closed, False if they are left open.
            If True, geometry_closing_threshold is ignored.
        geometry_closing_threshold
            If a geometry is given with two open ends that are not more than te_closing_threshold away from each other,
            the geometry is closed.
        cut_components_uids
            Cut cross-section geometry uids between the components with the given names i.e. to simulate a failed bonding.
            None for no cutting.
            Format for web-shell cut: (web_uid, shell_uid)
            Format for shell-shell cut (intersection_index is 0 or 1): (shell1_uid, shell2_uid, intersection_index)
        
        Returns
        -------
        CrossSectionGeometry
            The cross section geometry.
        ICrossSectionProcessor
            The cross section processors.
        """
        log.debug(f'Create CS for z2 = {z2_cross_section}')

        # DEBUG
        debug_plots = False#0.94 < z2_cross_section < 0.96#False#True#bool(strtobool(os.getenv('C2P_DEBUG_PLOTS', '0')))

        geometry = CrossSectionGeometry(z2_cross_section)

        cs_transformation_blade = transformation_matrix_2_occ(predocs_coord.transformation_aircraft_2_predocs(z2_cross_section))

        # Cut plane
        section_reference_point, section_reference_axis, z2_s_cs = predocs_coord.get_section_parameter(z2_cross_section)
        cross_section_plane = calc_cross_section_plane(section_reference_point,
                                                       section_reference_axis,
                                                       z2_s_cs)
        # eta_cs = z2_cross_section / self.halfspan

        if debug_plots:
            display, start_display, add_menu, add_function_to_menu = init_display()

            cross_section_plane_face = topods.Face(BRepBuilderAPI_MakeFace(cross_section_plane, -10, 10, -10, 10).Face())
            display.DisplayShape(cross_section_plane_face, color=rgb_color(0, 0, 1), transparency=0.5)

            # breptools_Write(cross_section_plane, 'cross_section_plane.brep')

        # # DEBUG
        # i = 0
        # for shell_uid, shell_shape, shell_material, shell_material_regions in self._shells:
        #     i += 1
        #     shell_wire = get_intersection_wire(shell_shape, cross_section_plane)
        #
        #     ii = 0
        #     for wire in shell_wire:
        #         ii += 1
        #         breptools.Write(wire, "{}_{}_{}.model".format(z_cross_section, i, ii))
        #         # from OCC.StlAPI import StlAPI_Writer
        #         #
        #         # # Export to STL
        #         # stl_writer = StlAPI_Writer()
        #         # stl_writer.SetASCIIMode(True)
        #         # stl_writer.Write(wire, "{}_{}_{}.stl".format(z_cross_section, i, ii))
        #     # assert len(shell_wire) == 1

        component_segment = self.component_segment

        # Shells
        if debug_plots:
            i = 0
        for shell in component_segment.shells:
            log.debug('Create shell')

            # Cutouts of the shape, if control surfaces are present
            up_dir = predocs_coord.up_dir_aircraft
            shell_shape = Shell.calc_shape_with_cutouts(shell, up_dir, debug_plots)

            # Cut shell with cross-section plane
            shell_wire = get_intersection_wire(shell_shape, cross_section_plane)#, d=(shell.uid if debug_plots else False))
            if shell_wire is None:
                raise RuntimeError('No intersection from the shell and the cross section plane for z2={}.'.format(z2_cross_section))
            #elif len(shell_wires) > 1:
            #    raise RuntimeError('No intersection from the shell and the cross section plane for z={}.'.format(z_cross_section))
            else:
                shell_wire_trans = transform_wire(shell_wire, cs_transformation_blade)

            # DEBUG
            if debug_plots:
                breptools_Write(shell_shape, 'shell_shape_{}.brep'.format(i))
                breptools_Write(transform_shape(shell_shape, cs_transformation_blade), 'shell_shape_trans_{}.brep'.format(i))

                breptools_Write(shell_wire, 'shell_wire_{}.brep'.format(i))
                breptools_Write(shell_wire_trans, 'shell_wire_trans_{}.brep'.format(i))

                display.DisplayShape(shell_shape, color=rgb_color(0,1,0), transparency=0.5)
                display.DisplayShape(shell_wire, color=rgb_color(1,0,0))

                # display.FitAll()
                # start_display()

            assembly = CrossSectionGeometry.Assembly(
                geometry,
                shell_wire_trans,
                shell.material,
                uid=shell.uid,
                assembly_type=shell.shell_name,
            )
            assembly.thickness_direction = 'inside'

            for cell in shell.cells:
                #log.debug(f'Material region: {material_region_uid}, {material_region_material.name}')

                # DEBUG
                if debug_plots:
                    breptools_Write(cell.shape, 'cell.shape_{}.brep'.format(i))
                    i += 1

                material_region_wire = get_intersection_wire(cell.shape, cross_section_plane)
                if material_region_wire is not None:
                    #log.debug(f'Used material region: {material_region_uid}, {material_region_material.layers}')
                    # Material region in this cross section
                    material_region_wire_trans = transform_wire(material_region_wire, cs_transformation_blade)

                    if debug_plots:

                        # display.DisplayShape(material_region_wire_trans, color=color(0, 0, 0))

                        breptools_Write(material_region_wire, 'material_region_wire_{}.brep'.format(i))
                        breptools_Write(material_region_wire_trans, 'material_region_wire_trans_{}.brep'.format(i))

                    assembly.add_material_region_from_wire(cell.uid, material_region_wire_trans, cell.material)
                # elif len(material_region_wires) > 1:
                #     raise RuntimeError('Material region geometry results in more than one material region in the cross section at z={}.'.
                #                        format(z_cross_section))
            geometry.add_profile_assembly(assembly)

        if debug_plots:
            display.FitAll()
            start_display()

        # Spars
        if debug_plots:
            i = 0
        for spar in component_segment.spars:
            # TODO: Web2?
            final_material = spar.material
            web_wire = get_intersection_wire(spar.cut_geometry, cross_section_plane)
            if web_wire is not None:
                # Spar cells
                spar_cell_uid = None
                assembly_type = 'Spar'

                # found_cell = True
                # for spar_cell in spar.spar_cells:
                #
                #     # DEBUG
                #     if debug_plots:
                #         breptools_Write(spar_cell.shape, 'spar_cell.shape_{}.brep'.format(i))
                #         i += 1
                #
                #     spar_cell_wire = get_intersection_wire(spar_cell.shape, cross_section_plane)
                #     if spar_cell_wire is not None:
                #         # Spar cell found
                #         if found_cell:
                #             raise RuntimeError('More than one spar cell for one spar of one cross section.')
                #         else:
                #             found_cell = True
                #
                #         spar_cell_wire_trans = transform_wire(spar_cell_wire, cs_transformation_blade)
                #
                #         if debug_plots:
                #             # display.DisplayShape(spar_cell_wire_trans, color=color(0, 0, 0))
                #
                #             breptools_Write(spar_cell_wire, 'spar_cell_wire_{}.brep'.format(i))
                #             breptools_Write(spar_cell_wire_trans, 'spar_cell_wire_trans_{}.brep'.format(i))
                #
                #         # Add spar
                #         geometry.add_web_from_wire(
                #             spar_cell_wire_trans,
                #             spar_cell.material,
                #             assembly_type=assembly_type,
                #             uid=spar.uid,
                #             spar_cell_uid=spar_cell.uid,
                #         )

                web_wire_trans = transform_wire(web_wire, cs_transformation_blade)

                # Get spar eta for the cross-section
                chord_face = component_segment.tigl_object.get_chordface().get_surface()
                ref_points = get_intersection_points(chord_face, web_wire)
                assert ref_points is not None

                # DEBUG
                if False:#len(ref_points) != 1:
                    display, start_display, add_menu, add_function_to_menu = init_display()

                    cross_section_plane_face = topods.Face(
                        BRepBuilderAPI_MakeFace(cross_section_plane, -1, 1, -1, 1).Face())
                    display.DisplayShape(cross_section_plane_face, color=color(0, 0, 1), transparency=0.5)

                    display.DisplayShape(spar.cut_geometry, color=color(0, 1, 0), transparency=0.5)
                    display.DisplayShape(web_wire, color=color(1, 0, 0), transparency=1)

                    display.DisplayShape(web_wire_trans, color=color(0, 0, 1), transparency=1)
                    display.DisplayShape(chord_face, color=color(0, 0, 1), transparency=0.5)

                    display.FitAll()
                    start_display()

                if len(ref_points) == 1:
                    chord_point = ref_points[0]
                    spar_eta = get_eta_xsi(component_segment, chord_point)[0]

                    # Search for spar cells
                    web_cells_cs = [
                        cell for cell in spar.spar_cells
                        if cell.spanwise_bounds[0] <= spar_eta < cell.spanwise_bounds[1]
                    ]
                    if len(web_cells_cs) == 1:
                        assembly_type = 'spar_cell'
                        cell = web_cells_cs[0]
                        spar_cell_uid = cell.uid
                        final_material = cell.material
                    elif len(web_cells_cs) > 1:
                        raise RuntimeError('More than one spar cell for one spar of one cross section.')
                    else:
                        log.warning(f'No spar cell found for eta {spar_eta}.')

                    # Add spar
                    geometry.add_web_from_wire(
                        web_wire_trans,
                        final_material,
                        assembly_type=assembly_type,
                        uid=spar.uid,
                        spar_cell_uid=spar_cell_uid,
                    )
                else:
                    log.warning(
                        f'Unable to find the intersection of the web "{spar.uid}" '
                        f'with the chord face at cross-section at z2={z2_cross_section:.3f} m, '
                        'but the cross-section plane cuts the spar geometry. '
                        'Maybe the cross-section is located on the spanwise edges of the spar.'
                    )

        # # DEBUG
        # import pickle
        # pickle.dump(geometry, open("geometry_{}.p".format(z2_cross_section), "wb"))

        # Create geometry
        discreet_geometry = geometry.create_discreet_cross_section_geometry(element_type=element_type, **kwargs)

        # Cut the geometry
        if cut_components_uids is not None:
            for cc in cut_components_uids:
                assert len(cc) >= 2

                # Find components
                components1 = [c for c in discreet_geometry.components if c.assembly_uid == cc[0]]
                components2 = [c for c in discreet_geometry.components if c.assembly_uid == cc[1]]

                # Find all nodes
                nodes1 = set()
                nodes2 = set()
                for e in discreet_geometry.elements:
                    if e.component in components1:
                        nodes1.update((e.node1, e.node2))
                    if e.component in components2:
                        nodes2.update((e.node1, e.node2))

                # Find common nodes
                common_nodes = nodes1 & nodes2
                common_nodes = sorted(common_nodes, key=lambda n: n.id)
                num_common_nodes = len(common_nodes)

                if num_common_nodes == 0:
                    log.warning(f'No intersection found for components "{cc[0]}" and "{cc[1]}". No cut will be added.')
                else:
                    if num_common_nodes == 1:
                        if len(cc) > 2:
                            log.warning(f'Only one intersection is found for the cut components uids "{cc}".')
                            # TODO: skip other
                        common_node = common_nodes[0]
                    elif num_common_nodes == 2:
                        assert len(cc) == 3
                        common_node = common_nodes[cc[2]]
                    else:
                        raise RuntimeError(f'{num_common_nodes} intersections found for components "{cc[0]}" and "{cc[1]}".')

                    # Cut geometry
                    nodes = set(discreet_geometry.get_neighbor_nodes(common_node))
                    nodes_component1 = nodes & nodes1
                    assert len(nodes_component1) == 1, f'Error while cutting the cross-section geometry: len(nodes_component1) == {len(nodes_component1)}'
                    discreet_geometry.cut_discreet_geometry(common_node, nodes_component1.pop())

        # # DEBUG
        # import pickle
        # from PreDoCS.CrossSectionAnalysis.Display import plot_discreet_geometry
        # pickle.dump(discreet_geometry, open("discreet_geometry_{}.p".format(z2_cross_section), "wb"))
        # plot_discreet_geometry(discreet_geometry, file="discreet_geometry_{}.png".format(z2_cross_section))

        if not skip_material_stiffness_calculation_and_update_processors:
            # Calc material stiffness for cross section processing
            materials = {s.shell for s in discreet_geometry.components}
            for material in materials:
                log.debug(f'Calculate material stiffness for "{material.name}"')
                material.stiffness = self._get_element_stiffness_func(material, element_type, **kwargs)

        # Create cross section processor and do the calculation
        cs_processor = processor_type(cross_section_id, z2_cross_section, **kwargs)
        cs_processor.discreet_geometry = discreet_geometry

        if not skip_material_stiffness_calculation_and_update_processors:
            cs_processor._update_if_required()
        
        return geometry, cs_processor

    # def get_cpacs2predocs_transformation(self, beam_reference_point, beam_reference_axis):
    #     """
    #     Returns the coordinate system transformation from the CPACS to the PreDoCS coordinate system.
    #
    #     Parameters
    #     ----------
    #     beam_reference_point: Vector
    #         The reference point of the beam at x_beam = y_beam = z_beam = 0.
    #     beam_reference_axis: Vector
    #         The beam reference axis from the beam reference point.
    #
    #     Returns
    #     -------
    #     OCC.gp.gp_Trsf
    #         Transformation from the CPACS to the PreDoCS coordinate system.
    #     """
    #     if self._x_axis_definition == 'old':
    #         return create_transformation_matrix_c2p(beam_reference_point, beam_reference_axis)
    #     elif self._x_axis_definition == 'global':
    #         return aircraft_predocs_transformation(beam_reference_point, beam_reference_axis)
    #     else:
    #         raise RuntimeError(f'Unknown x_axis_definition "{self._x_axis_definition}".')

    def generate_cross_section_data(
            self,
            predocs_coord,
            cross_section_processor_name,
            parallel_processing=True,
            **kwargs,
    ) -> tuple[list[CrossSectionGeometry], list[ICrossSectionProcessor]]:
        """
        Create the cross section geometries at given spanwise positions of the wing.
        Only the upper and lower wing shell with the material regions and the spars are imported.
        
        Parameters
        ----------
        predocs_coord: PreDoCSCoord
            Definition of the PreDoCS coordinate system.
        cross_section_processor_name: str
            Name of the cross section processor: 'Jung', 'hybrid', 'Song', 'Hardt' or 'Isotropic'.
        parallel_processing: bool (default: True)
            True for parallel cross section processing.
        position_blurring: float
            The max distance from the node position to the given position.
        element_length: float (default: None)
            If not None, the elements are discretized by dividing the segments into elements with the same length.
            This element length is given by this parameter.
        segment_deflection: float (default: None)
            If not None, the elements are discretized by dividing the segments into elements, that the deflection
            area between the curve to the discreet geometry for a segment is equal to this parameter.
        use_fast_abscissa: bool (default: True)
            If True, a faster and simpler calculation of the abscissa is used
            (OCC.GCPnts.GCPnts_QuasiUniformAbscissa instead of OCC.GCPnts.GCPnts_UniformAbscissa and
            OCC.GCPnts.GCPnts_QuasiUniformDeflection instead of OCC.GCPnts.GCPnts_UniformDeflection).
            For True, the continuity of curve has to be at least C2.
        
        Returns
        -------
        list(CrossSectionGeometry)
            List of the cross section geometries.
        list(ICrossSectionProcessor)
            List of the cross section processors.
        """
        # # The reference point of the beam at x_beam = y_beam = z_beam = 0.
        # beam_reference_points = predocs_coord.section_origin

        # The beam reference axis from the beam reference point.
        beam_reference_axes = predocs_coord.section_directions

        # The spanwise position where to create the geometries of the cross sections. z_beam starts at the beam
        # reference point and is orientated in the beam reference axis direction.
        z2_cross_sections = predocs_coord.z2_cs

        # The coordinate system transformation from the CPACS to the PreDoCS system
        for ii, beam_reference_axis in enumerate(beam_reference_axes):
            beam_reference_axes[ii] = beam_reference_axis.normalised

        element_type = get_element_type_from_cross_section_processor_name(cross_section_processor_name)
        processor_type = get_cross_section_processor_from_name(cross_section_processor_name)

        cross_sections = [(i+1, z2) for i, z2 in enumerate(z2_cross_sections)]

        # # Transformation
        # c2p_transformation = self.get_cpacs2predocs_transformation(
        #     beam_reference_points[0],
        #     beam_reference_axes[0],
        # )

        if parallel_processing:
            with cf.ThreadPoolExecutor(max_workers=len(cross_sections)) as executor:
                cs_processors = executor.map(lambda cross_section: self._generate_cross_section_data(
                    cross_section[0],
                    cross_section[1],
                    predocs_coord,
                    element_type,
                    processor_type,
                    **kwargs
                ), cross_sections)
                cs_processors = list(cs_processors)
        else:
            cs_processors = list()
            for cross_section_id, z2_cross_section in cross_sections:
                cs_processor = self._generate_cross_section_data(
                    cross_section_id,
                    z2_cross_section,
                    predocs_coord,
                    element_type,
                    processor_type,
                    **kwargs,
                )
                cs_processors.append(cs_processor)

        return [cs_geometry for cs_geometry, cs_processor in cs_processors], \
               [cs_processor for cs_geometry, cs_processor in cs_processors]

    def get_assembly_uids(self):
        result_dict = {}

        for shell in self.component_segment.shells:
            result_dict[shell.uid] = shell.shell_name

        for spar in self.component_segment.spars:
            result_dict[spar.uid] = 'Spar'

        return result_dict

    def get_spar_positions_dict(self, transformation_matrix):
        """
        Returns the spar positions in the PreDoCS coordinate system.

        Parameters
        ----------
        transformation_matrix: numpy.ndarray
            Transformation matrix from the CPACS coordinate system to the PreDoCS coordinate system.

        Returns
        -------
        dict(str, list(Vector))
            Dict of spar uid to positions list.
        """
        spar_positions_predocs_coord = {}
        component_segment = self.component_segment
        component_segment_tigl_object = component_segment.tigl_object
        for spar in component_segment.spars:
            spar_positions_predocs_list = []
            for pos in spar.spar_positions:
                eta, xsi = find(component_segment.spar_positions, 'uid', pos).position
                spar_position = point_to_vector(component_segment_tigl_object.get_point(eta, xsi))
                spar_positions_predocs = transform_location_m(transformation_matrix, spar_position)
                spar_positions_predocs_list.append(spar_positions_predocs)
            spar_positions_predocs_coord[spar.uid] = spar_positions_predocs_list

        return spar_positions_predocs_coord

    @property
    def wing(self):
        return self._cpacs_interface.wings[self._wing_index]

    @property
    def component_segment(self):
        return self.wing.component_segments[self._component_segment_index]

    @property
    def wingspan(self):
        """float: The span of the wing."""
        return self.wing.wingspan

    @property
    def halfspan(self):
        """float: The half span of the wing."""
        return self.wing.halfspan

    @property
    def wingroot(self):
        """Vector: Middle point of the wing root."""
        return self.wing.wingroot

    @property
    def wingtip(self):
        """Vector: Middle point of the wing tip."""
        return self.wing.wingtip

    @property
    def wingbox_trailing_point(self):
        """Vector: Trailing point of the wingbox and inner wing connection."""
        return self.wing.wingbox_trailing_point

    @property
    def wingtip_leading_point(self):
        """Vector: Leading point of the wing tip"""
        return self.wing.wingtip_leading_point

    @property
    def loadcase_dict(self):
        """Dictionary of all load cases"""
        self._read_cpacs()
        return self._loadcase_dict

    @property
    def load_reference_points(self):
        """The DynamicReferencePoints of the CPACS model"""
        self._read_cpacs()
        return self._load_reference_points

    @property
    def wing_reference_position(self) -> Vector:
        """The wing reference position of the CPACS model."""
        self._read_cpacs()
        return self._wing_reference_position

    @property
    def wing_reference_direction(self) -> Vector:
        """The wing reference direction of the CPACS model."""
        self._read_cpacs()
        return self._wing_reference_direction

    @property
    def beam_reference_points(self) -> list[Vector]:
        """The beam reference points of the CPACS model."""
        self._read_cpacs()
        return self._beam_reference_points
