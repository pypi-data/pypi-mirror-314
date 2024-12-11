"""
This module provides classes for building cross section geometries.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from copy import deepcopy
from math import ceil
from typing import Optional, Union

import numpy as np
from OCC.Core.BRepGProp import brepgprop_LinearProperties
from OCC.Core.BRepTools import BRepTools_ShapeSet
from OCC.Core.GCPnts import GCPnts_AbscissaPoint_Length, GCPnts_UniformAbscissa, GCPnts_UniformDeflection, \
    GCPnts_QuasiUniformDeflection, GCPnts_QuasiUniformAbscissa
from OCC.Core.GProp import GProp_GProps
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.TopAbs import TopAbs_WIRE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods
from scipy.spatial.distance import cdist

from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Interfaces import INode
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.occ import get_point_from_curve_parameter, \
    get_curve_parameter_from_point, \
    get_intersection_points, point_list_to_wire, edge_from_points, \
    get_shape_vertices, point_to_vector, is_curve_clockwise, get_curve_boundary_points, create_curve_from_wire, \
    create_curve_from_edge, is_point_on_curve
from PreDoCS.util.util import is_number
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


def load_profile_points(input_file, has_header):
    """
    Loads points of a profile contur. File from http://airfoiltools.com/airfoil/naca4digit
    
    Parameters
    ----------
    input_file: str
        The input file.
    has_header: bool
        True, if the first row is a header row.
    
    Returns
    -------
    list(Vector)
        The profile contur points.
    """
    with open(input_file) as f:
        if has_header:
            f.readline()
        points = []
        for row in f:
            p = row.split()
            points.append(Vector([float(p[0]), float(p[1])]))
    return points


class CrossSectionGeometry(object):
    """
    This class represents a non discreet beam cross section geometry.
    From an object of this class a DiscreetCrossSectionGeometry object can be build.
    A cross section geometry is made of several assemblies like profiles or webs.
    
    Attributes
    ----------
    _assemblies: list(Assembly)
        List of assemblies of the cross section geometry.
    _nodes: list(INode)
        List of nodes of the cross section geometry.
    _id_counter: dict(str, int)
        ID counter for the geometry. Is used for generating unique ID's for the cross section,
        i.e. node ID's or element ID's.
    _z_cross_section: float
        The z-position of the cross section.
    """
    def __init__(self, z2_cross_section=0):
        """
        Constructor.
        
        Parameters
        ----------
        z2_cross_section: float (default: 0)
            The z2-position of the cross section.
        """
        self._z2_cross_section = z2_cross_section
        self._assemblies = []
        self._nodes = []
        self._id_counter = {'nodes': 1, 'elements': 1, 'components': 1}
    
    @property
    def z2_cross_section(self):
        """float: The z-position of the cross section."""
        return self._z2_cross_section

    @property
    def assemblies(self):
        """list(Assembly): List of assemblies of the cross section geometry."""
        return self._assemblies
    
    def _get_new_id(self, key):
        """
        Returns a new unique ID for the given key.
        
        Parameters
        ----------
        key: str
            The key.
        
        Returns
        -------
        int
            The unique ID.
        """
        new_id = self._id_counter[key]
        self._id_counter[key] = new_id + 1
        return new_id

    def __add_node(self, position: Vector) -> 'Node':
        # New node
        node = DiscreetCrossSectionGeometry.Node(self._get_new_id('nodes'), position)
        self._nodes.append(node)
        return node

    def _get_node_from_position(self, position, position_blurring):
        """
        Returns node for a given position or creates a new node.
        
        Parameters
        ----------
        position: Vector
            The position.
        position_blurring: float
            The max distance from the node position to the given position.
        
        Returns
        -------
        INode
            The node.
        """
        nodes = self._nodes
        if len(nodes) == 0:
            # New node
            return self.__add_node(position)
        else:
            positions_array = np.array([n.position for n in nodes])[:, 0:2]
            dist_matrix = cdist(positions_array, [[position.x, position.y]], 'euclidean')
            possible_nodes = (dist_matrix <= position_blurring).sum()
            if possible_nodes > 1:
                raise RuntimeError('Max one node for one position possible')
            elif possible_nodes == 1:
                i_min = np.argmin(dist_matrix)
                # min_val = dist_matrix[i_min, 0]
                return nodes[i_min]
            else:
                # New node
                return self.__add_node(position)

    def create_discreet_cross_section_geometry(self, element_type, **kwargs):
        """
        Creates a discreet cross section geometry with the information in this object.
        For further parameters see `CrossSectionGeometry.Assembly.get_elements`.
        
        Parameters
        ----------
        element_type: class <- IElement
            The element type.
        close_open_ends
            True, if open ends of the cross-section are closed, False if they are left open.
            If True, geometry_closing_threshold is ignored.
        geometry_closing_threshold
            If a geometry is given with two open ends that are not more than te_closing_threshold away from each other,
            the geometry is closed.

        Returns
        -------
        DiscreetCrossSectionGeometry
            The discreet cross section geometry.
        """
        close_open_ends = kwargs.get('close_open_ends', True)
        geometry_closing_threshold = kwargs.get('geometry_closing_threshold', None)

        # Calc geometry center of the shells to determine the thickness direction
        shell_assemblies = [a for a in self._assemblies if a.assembly_type in ['upperShell', 'lowerShell']]
        if len(shell_assemblies) > 0:
            cg = Vector([0, 0, 0])
            mass = 0
            for assembly in shell_assemblies:
                props = GProp_GProps()
                brepgprop_LinearProperties(assembly.wire, props)
                geometry_center = point_to_vector(props.CentreOfMass())
                m = props.Mass()
                cg = cg + m * geometry_center
                mass = mass + m
            geometry_center = cg / mass
            kwargs['geometry_center'] = geometry_center
            log.debug(f'CS {self._z2_cross_section:.2f} m: geometry_center: {geometry_center}')

        # Add the discreet elements
        discreet_geometry = DiscreetCrossSectionGeometry()
        for assembly in self._assemblies:
            discreet_geometry.add_elements(assembly.get_elements(element_type, **kwargs))

        open_ends = list({n for n in discreet_geometry.nodes if len(list(discreet_geometry.get_neighbor_nodes(n))) == 1})
        if close_open_ends or geometry_closing_threshold:
            if len(open_ends) == 2:
                gap = open_ends[0].position.dist(open_ends[1].position)
                if close_open_ends or geometry_closing_threshold >= gap:
                    # Close the geometry, if there are two open ends
                    log.info(
                        f'Cross-section geometry (z2={self.z2_cross_section:.3f} m) has 2 open ends and is closed by PreDoCS'
                    )

                    # Close by adding an element of the shell for the gap
                    lower_shell_te_node = open_ends[0] if open_ends[0].position.y < open_ends[1].position.y else open_ends[1]
                    upper_shell_te_node = (set(open_ends) - {lower_shell_te_node}).pop()
                    lower_shell_te_element = discreet_geometry.get_adjacent_elements(lower_shell_te_node)[0]
                    upper_shell_te_element = discreet_geometry.get_adjacent_elements(upper_shell_te_node)[0]
                    lower_to_upper = lower_shell_te_element.node2 == lower_shell_te_node
                    discreet_geometry.add_element(self.get_element(
                        element_type,
                        lower_shell_te_node.position if lower_to_upper else upper_shell_te_node.position,
                        upper_shell_te_node.position if lower_to_upper else lower_shell_te_node.position,
                        lower_shell_te_element.component if lower_to_upper else upper_shell_te_element.component,
                        kwargs.get('position_blurring', 1e-7),
                    ))
            elif close_open_ends and (len(open_ends) > 2 or len(open_ends) == 1):
                raise RuntimeError('Cross section geometry has {} open ends'.format(len(open_ends)))

        discreet_geometry._update_if_required()
        return discreet_geometry
    
    def get_element(self, element_type, position1, position2, component, position_blurring):
        """
        Returns a new element between the given positions. If there are nodes in the range of position_blurring
        of the positions, these nodes are selected, otherwise new nodes are created.
        
        Parameters
        ----------
        element_type: class <- IElement
            The element type.
        position1: Vector
            The position of the start node of the element.
        position2: Vector
            The position of the end node of the element.
        component: Component
            Component of the element.
        position_blurring: float
            The max distance from a position to a existing node position.
        
        Returns
        -------
        IElement
            The new element.
        """
        node1 = self._get_node_from_position(Vector([position1.x, position1.y]), position_blurring)
        node2 = self._get_node_from_position(Vector([position2.x, position2.y]), position_blurring)
        return element_type(self._get_new_id('elements'), node1, node2, component)
    
    def get_component(self, material, midsurface_offset, assembly_type=None, assembly_uid=None, extra_data=None):
        """
        Returns a new component.
        
        Parameters
        ----------
        material: IMaterial
            Material of the component.
        midsurface_offset: float
            The midsurface offset defines the distance in normal direction of the contur (as a fraction of the element thickness)
            from the reference surface (connecting the nodes of the element) to the midsurface of the contur.
            The value is from -0.5 to +0.5. 0 means that reference surface and the midsurface are indentical.
        assembly_type: str (default: None)
            The type of the assembly.
        assembly_uid: str (default: None)
            The uID of the assembly.
        extra_data: dict (default: None)
            Additional data.
        
        Returns
        -------
        Component
            The new component.
        """
        res = DiscreetCrossSectionGeometry.Component(self._get_new_id('components'), material, midsurface_offset)
        res.assembly_type = assembly_type
        res.assembly_uid = assembly_uid
        res.extra_data = extra_data
        return res
    
    def add_profile_assembly(self, assembly):
        """
        Add a geometry assembly of the outer shape to the cross section geometry.
        
        Parameters
        ----------
        assembly: Assembly
            The assembly to add.
        """
        self._assemblies.append(assembly)
    
    def _get_intersection_with_assemblies(self, wire):
        """
        Computes the intersections from a wire with the assemblies of the cross section geometry cross section.
        
        Parameters
        ----------
        wire: OCC.TopoDS.TopoDS_Wire
            The wire.
        
        Returns
        -------
        int
            Number of intersections found.
        list((Assembly, list(Vector))
            List of intersection points of the wire with the assemblies.
        """
        intersections = []
        num_intersections = 0
        for assembly in self._assemblies:
            intersection = get_intersection_points(assembly.wire, wire)
            if len(intersection) > 0:
                num_intersections += len(intersection)
                intersections.append((assembly, intersection))
        return num_intersections, intersections
    
    def add_web_from_wire(self, web_line_wire, material, assembly_type, uid='', spar_cell_uid=None, web_parts: bool = False):
        """
        Add a web to the cross section geometry from a given wire. The intersections from the wire with the airfoil are
        computed. Can only called after the outer shape of the profile is added to the cross section.
        
        Parameters
        ----------
        web_line_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the web line.
        material: IMaterial
            The material of the web.
        assembly_type: str
            The type of the assembly.
        uid: str (default: '')
            The uID of the assembly.
        spar_cell_uid: str (default: None)
            The uID of the spar cell.
        """
        # Find intersections with other assemblies
        num_intersections, intersections = self._get_intersection_with_assemblies(web_line_wire)

        if web_parts:
            # Add web
            if not (num_intersections == 1 or num_intersections == 2):
                log.warning(f'The web intersects at {num_intersections} points with the profile, but it has to be ' +
                            'connected at one or two points to the profile. The web is not added. Add profile geometry first.')
                return
            self.add_web(CrossSectionGeometry.Assembly(self, web_line_wire, material, uid=uid, assembly_type=assembly_type,
                                                       extra_data={'spar_cell_uid': spar_cell_uid}), web_parts=web_parts)
        else:
            if not num_intersections == 2:
                log.warning(f'The web intersects at {num_intersections} points with the profile, but it has to be '+
                            'connected with both ends to the profile. The web is not added. Add profile geometry first.')
                return
            if len(intersections) == 1:
                # Intersection with one assembly
                web_wire = point_list_to_wire([intersections[0][1][0], intersections[0][1][1]], closed_wire=False)
            else:
                # Intersection with two assemblies
                web_wire = point_list_to_wire([intersections[0][1][0], intersections[1][1][0]], closed_wire=False)

            # Add web
            self.add_web(CrossSectionGeometry.Assembly(self, web_wire, material, uid=uid, assembly_type=assembly_type,
                                                       extra_data={'spar_cell_uid': spar_cell_uid}), web_parts=web_parts)

    def add_web_from_line(self, web_line_start_point, web_line_end_point, material, assembly_type, uid='',
                          spar_cell_uid=None, web_parts: bool = False):
        """
        Add a web to the cross section geometry from a given line. The intersections from the wire with the airfoil are
        computed. Can only called after the outer shape of the profile is added to the cross section.

        Parameters
        ----------
        web_line_start_point: Vector
            The start point of the web line.
        web_line_end_point: Vector
            The end point of the web line.
        material: IMaterial
            The material of the web.
        assembly_type: str
            The type of the assembly.
        uid: str (default: '')
            The uID of the assembly.
        spar_cell_uid: str (default: None)
            The uID of the spar cell.
        """
        web_wire = point_list_to_wire([web_line_start_point, web_line_end_point], closed_wire=False)
        self.add_web_from_wire(web_wire, material, assembly_type, uid, spar_cell_uid, web_parts=web_parts)

    def add_web(self, web_assembly, web_parts: bool = False):
        """
        Add a web to the cross section geometry.
        Can only called after the outer shape of the profile is added to the cross section.
        
        Parameters
        ----------
        web_assembly: Assembly
            The web assembly to add.
        """
        # Get intersection points and assemblies
        web_wire = web_assembly.wire
        num_intersections, intersections = self._get_intersection_with_assemblies(web_wire)

        if web_parts:
            # Add web
            if not (num_intersections == 1 or num_intersections == 2):
                raise RuntimeError(f'The web intersects at {num_intersections} points with the profile, but it has to be '
                            'connected at one or two points to the profile. The web is not added. Add profile geometry first.')

            for assembly, points in intersections:
                for point in points:
                    assembly.add_additional_fixed_node_point(point)
                    web_assembly.add_additional_fixed_node_point(point)

        else:
            if not num_intersections == 2:
                raise RuntimeError(f'The web intersects at {num_intersections} points with the profile, but it has to be connected with both ends to the profile. Add profile geometry first.')

            if len(intersections) == 1:
                # Intersection with one assembly
                assembly, points = intersections[0]
                assembly.add_additional_fixed_node_point(points[0])
                assembly.add_additional_fixed_node_point(points[1])
                web_assembly.add_additional_fixed_node_point(points[0])
                web_assembly.add_additional_fixed_node_point(points[1])
            else:
                # Intersection with two assemblies
                assembly, points1 = intersections[0]
                assembly.add_additional_fixed_node_point(points1[0])
                web_assembly.add_additional_fixed_node_point(points1[0])
                assembly2, points2 = intersections[1]
                assembly2.add_additional_fixed_node_point(points2[0])
                web_assembly.add_additional_fixed_node_point(points2[0])

        # Add web
        self._assemblies.append(web_assembly)

    class AssemblyMaterialRegion(object):
        """
        This class represents a material region of a geometry assembly. A material region is defined by the
        between two given parameters of the assembly curve.
        
        Attributes
        ----------
        _boundary_node_parameters: (float, float)
            The start and end parameter of the material region.
        _material: IMaterial
            The material of the material region.
        _component: Component
            The discreet cross section geometry component of the material region.
        _uid: str
            The uid of the material region.
        _component: Component
            The discreet cross section geometry component of the material region.
        """
        def __init__(self, uid, boundary_node_parameters, material):
            """
            Constructor.
            
            Parameters
            ----------
            uid: str
                The uid of the material region.
            boundary_node_parameters: (float, float)
                The start and end parameter of the material region.
            material: IMaterial
                The material of the material region.
            """
            self._boundary_node_parameters = boundary_node_parameters
            self._material = material
            self._uid = uid
            self._component = None
        
        @property
        def uid(self):
            """str: The uid of the material region."""
            return self._uid

        @property
        def boundary_node_parameters(self):
            """(float, float): The start and end parameter of the material region."""
            return self._boundary_node_parameters
        
        @property
        def material(self):
            """IMaterial: The material of the material region."""
            return self._material

        @property
        def component(self):
            """Component: The discreet cross section geometry component of the material region."""
            return self._component

        @component.setter
        def component(self, value):
            self._component = value

    class Assembly(object):
        """
        This class represents a assembly of the cross section geometry, i.e. a part of the wing shell or a shear web.
        The geometry is made of one base material and with material regions several materials can be defined.
        
        Attributes
        ----------
        _cross_section_geometry: CrossSectionGeometry
            The cross section geometry the assembly belongs to.
        _wire: OCC.TopoDS.TopoDS_Wire
            The geometry wire of the geometry assembly in the cross section plane.
        _curve: OCC.Geom.Geom_Curve
            The geometry curve of the geometry assembly in the cross section plane.
        _curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            The curve adaptor of the geometry assembly in the cross section plane.
        _material: IMaterial
            The base material of the geometry assembly.
        _material_regions: list(AssemblyMaterialRegion)
            List of material regions for the material distribution.
        _additional_fixed_node_points: list(Vector)
            List of additional fixed points for the discretization,
             i.e. the points where a web is connected to this geometry assembly.
        _thickness_direction: str
            - 'inside' if the wire is the outer border of the assembly as seen from the assembly CoG.
            - 'outside' if the wire is the inner border of the assembly as seen from the assembly CoG.
            - 'center' if the wire is in the middle of the assembly.
        _components: list(Component)
            The discreet cross section geometry components of the assembly.
        _uid: str
            The uid of the assembly.
        _assembly_type: str
            The type of the assembly.
        """
        def __init__(self, cross_section_geometry, wire, material, material_regions=None,
                     thickness_direction='center', uid=None, assembly_type=None, extra_data=None,
                     geometry_center: Vector = None):
            """
            Constructor.
            
            Parameters
            ----------
            cross_section_geometry: CrossSectionGeometry
                The cross section geometry the assembly belongs to.
            wire: OCC.TopoDS.TopoDS_Wire
                The geometry wire of the geometry assembly in the cross section plane.
            material: IMaterial
                The base material of the geometry assembly.
            material_regions: list(AssemblyMaterialRegion) (default: None)
                List of material regions for the material distribution. None for no material regions.
            thickness_direction: str (default: 'center')
                - 'inside' if the wire is the outer border of the assembly as seen from the assembly CoG.
                - 'outside' if the wire is the inner border of the assembly as seen from the assembly CoG.
                - 'center' if the wire is in the middle of the assembly.
            uid: str (default: None)
                The uid of the assembly.
            assembly_type: str (default: None)
                The type of the assembly.
            extra_data: dict (default: None)
                Additional data.
            geometry_center
                The geometry center used for the determination of the thickness direction.
                If not set, the geometry center of the assembly is used.
            """
            self._cross_section_geometry = cross_section_geometry
            self._wire = wire
            self._curve, self._curve_adaptor = self._get_curve_from_wire(wire)
            self._material = material
            self._material_regions = material_regions if material_regions is not None else []
            self._additional_fixed_node_points = []
            self._thickness_direction = thickness_direction
            self._components = []
            self._uid = uid
            self._assembly_type = assembly_type
            self._geometry_center = geometry_center
            if extra_data:
                self._extra_data = extra_data
            else:
                self._extra_data = {}

        @classmethod
        def _get_curve_from_wire(cls, wire):
            # self._curve_adaptor = BRepAdaptor_CompCurve(wire)
            # self._curve = geomadaptor_MakeCurve(self._curve_adaptor)
            curve = create_curve_from_wire(wire)
            curve_adaptor = GeomAdaptor_Curve(curve)
            return curve, curve_adaptor

        def __getstate__(self):
            """Make pickle possible."""
            state = self.__dict__.copy()

            # Remove the unpicklable entries.
            shape_set = BRepTools_ShapeSet()
            shape_set.Add(self._wire)
            state['_wire_string'] = shape_set.WriteToString()

            # curve_set = GeomTools_CurveSet()
            # curve_set.Add(self._curve)
            # state['_curve_string'] = curve_set.WriteToString()

            del state['_wire']
            del state['_curve']
            del state['_curve_adaptor']

            return state

        def __setstate__(self, state):
            """Make pickle possible."""
            self.__dict__.update(state)

            shape_set = BRepTools_ShapeSet()
            shape_set.ReadFromString(state['_wire_string'])
            for i in range(shape_set.NbShapes() + 1):
                if i == shape_set.NbShapes():
                    raise RuntimeError('No wire found in state.')
                shape = shape_set.Shape(i + 1)
                if shape.ShapeType() == TopAbs_WIRE:
                    self._wire = topods.Wire(topods.Wire(shape.Located(shape_set.Locations().Location(1))))
                    break

            # curve_set = GeomTools_CurveSet()
            # curve_set.ReadFromString(state['_curve_string'])
            # self._curve = curve_set.Curve(1)

            # self._curve_adaptor = BRepAdaptor_CompCurve(self._wire)

            self._curve, self._curve_adaptor = self._get_curve_from_wire(self._wire)

            del self.__dict__['_wire_string']
            # del self.__dict__['_curve_string']

        @property
        def uid(self):
            """str: The uid of the assembly."""
            return self._uid

        @property
        def assembly_type(self):
            """str: The type of the assembly."""
            return self._assembly_type

        @property
        def extra_data(self):
            """dict: Additional data."""
            return self._extra_data

        @property
        def wire(self):
            """OCC.TopoDS.TopoDS_Wire: The geometry wire of the geometry assembly in the cross section plane."""
            return self._wire

        @property
        def material_regions(self):
            """
            list(AssemblyMaterialRegion):
                List of material regions for the material distribution.
            """
            return self._material_regions

        @property
        def thickness_direction(self):
            """
            str:
                - 'inside' if the wire is the outer border of the assembly as seen from the assembly CoG.
                - 'outside' if the wire is the inner border of the assembly as seen from the assembly CoG.
                - 'center' if the wire is in the middle of the assembly.
            """
            return self._thickness_direction

        @thickness_direction.setter
        def thickness_direction(self, value):
            self._thickness_direction = value

        @property
        def components(self):
            """list(Component): The discreet cross section geometry components of the assembly."""
            return self._components

        @property
        def geometry_center(self) -> Vector:
            """
            The geometry center used for the determination of the thickness direction.
            If not set, the geometry center of the assembly is used.
            """
            if self._geometry_center is None:
                props = GProp_GProps()
                brepgprop_LinearProperties(self._wire, props)
                return point_to_vector(props.CentreOfMass())
            else:
                return self._geometry_center

        @property
        def clockwise(self):
            """bool: True, if the assembly contur coordinate is clockwise around the CoG of the assembly."""
            return is_curve_clockwise(self._curve_adaptor, self.geometry_center)
        
        def add_additional_fixed_node_point(self, point):
            """
            Adds an additional fixed point for the discretization,
            i.e. the points where a web is connected to this geometry assembly.
            
            Parameters
            ----------
            point: Vector
                Additional fixed point for the discretization.
            """
            self._additional_fixed_node_points.append(point)

        def node_parameters_for_discretization(
                self, position_blurring, fixed_node_parameters, **kwargs,
        ):
            """
            Returns the curve parameters of the flexible nodes between the given fixed nodes.
            
            Parameters
            ----------
            position_blurring: float
                The max distance from the node position to the given position.
            fixed_node_parameters: list(float) / set(float)
                Parameters of the fixed nodes.
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
            list(float)
                Parameters of the fixed and flexible nodes.
            """
            # Arguments
            element_length = kwargs.get('element_length')
            segment_deflection = kwargs.get('segment_deflection')
            use_fast_abscissa = bool(kwargs.get('use_fast_abscissa', True))

            fixed_node_parameters_on_base_curve = sorted(set(fixed_node_parameters))  # Remove duplicates
            fixed_node_points = [get_point_from_curve_parameter(self._curve_adaptor, parameter)
                                 for parameter in fixed_node_parameters_on_base_curve]
            result_points = [get_point_from_curve_parameter(self._curve_adaptor, parameter)
                             for parameter in fixed_node_parameters]

            # For each edge of the wire
            edge_explorer = TopExp_Explorer(self._wire, TopAbs_EDGE)
            while edge_explorer.More():
                edge = topods.Edge(edge_explorer.Current())
                edge_explorer.Next()

                edge_curve = create_curve_from_edge(edge)
                edge_curve_adaptor = GeomAdaptor_Curve(edge_curve)
                # edge_curve_adaptor = BRepAdaptor_Curve(edge)
                # edge_curve = edge_curve_adaptor.Curve()

                if edge_curve_adaptor.Continuity() < 2:
                    log.warning('Curve continuity below C2. May cause problems in cross section geometry discretization.')

                # Get fixed points of the edge
                edge_boundary_points = list(get_curve_boundary_points(edge_curve_adaptor))
                edge_fixed_node_points = (
                    edge_boundary_points +
                    [
                        point for point in fixed_node_points
                        if is_point_on_curve(edge_curve, Vector([point.x, point.y, self._cross_section_geometry.z2_cross_section]), position_blurring)
                    ]
                )
                edge_fixed_node_points = CrossSectionGeometry.Assembly.get_unique_point_list(edge_fixed_node_points,
                                                                                             position_blurring)
                edge_fixed_node_parameters_on_edge_curve = sorted([get_curve_parameter_from_point(edge_curve, Vector([point.x, point.y, point.z]))
                                                                   for point in edge_fixed_node_points])

                # For each segment between the fixed points
                for segment_idx in range(len(edge_fixed_node_parameters_on_edge_curve)-1):
                    start_parameter = edge_fixed_node_parameters_on_edge_curve[segment_idx]
                    end_parameter = edge_fixed_node_parameters_on_edge_curve[segment_idx+1]
                    segment_length = GCPnts_AbscissaPoint_Length(edge_curve_adaptor, start_parameter, end_parameter)
                    if is_number(segment_deflection):
                        # Distribution for maximum deflection between the curve and the polygon
                        # that results from the computed points
                        result_edge_parameters = self.curve_discretization_segment_deflection(
                            edge_curve_adaptor, start_parameter, end_parameter, segment_deflection, use_fast_abscissa, segment_length,
                        )

                        # If element_length is given, further split the elements
                        if is_number(element_length):
                            additional_edge_parameters = set()
                            result_edge_parameters_sorted = sorted(result_edge_parameters)
                            for i in range(len(result_edge_parameters_sorted) - 1):
                                s1 = result_edge_parameters_sorted[i]
                                s2 = result_edge_parameters_sorted[i + 1]
                                segment_length_element = GCPnts_AbscissaPoint_Length(edge_curve_adaptor, s1, s2)
                                if segment_length_element > element_length:
                                    additional_edge_parameters.update(self.curve_discretization_element_length(
                                        edge_curve_adaptor, s1, s2, element_length, segment_length_element,
                                    ))
                            result_edge_parameters.update(additional_edge_parameters)

                    elif is_number(element_length):
                        # Equidistant distribution on the curve
                        result_edge_parameters = self.curve_discretization_element_length(
                            edge_curve_adaptor, start_parameter, end_parameter, element_length, use_fast_abscissa, segment_length,
                        )
                    else:
                        raise RuntimeError('Curve discretization method not known')
                    result_points += [
                        get_point_from_curve_parameter(edge_curve_adaptor, parameter)
                        for parameter in result_edge_parameters
                    ]

                # Get resulting curve parameters
                result_points = CrossSectionGeometry.Assembly.get_unique_point_list(result_points, position_blurring)

                # # DEBUG
                # from matplotlib import pyplot as plt
                # fig, ax = plt.subplots()
                # ax.scatter([p.x for p in result_points], [p.y for p in result_points])
                # ax.axis('equal')
                # plt.savefig(r'H:\Daniel\git\PreDoCS\tmp\d.png')

                result_parameters = {
                    get_curve_parameter_from_point(self._curve, Vector([point.x, point.y, point.z]))
                    for point in result_points
                }

            return sorted(result_parameters | set(fixed_node_parameters))

        @classmethod
        def curve_discretization_segment_deflection(
                cls,
                edge_curve_adaptor,
                start_parameter: float,
                end_parameter: float,
                segment_deflection: float,
                use_fast_abscissa: bool,
                segment_length: float = None
        ) -> set[float]:
            """
            Distribution for maximum deflection between the curve and the polygon
            that results from the computed points.
            """
            if segment_length is None:
                segment_length = GCPnts_AbscissaPoint_Length(edge_curve_adaptor, start_parameter, end_parameter)

            if use_fast_abscissa:
                uniform_deflection = GCPnts_QuasiUniformDeflection()
            else:
                uniform_deflection = GCPnts_UniformDeflection()
            uniform_deflection.Initialize(edge_curve_adaptor, float(segment_deflection * segment_length),
                                          start_parameter, end_parameter)
            if uniform_deflection.IsDone():
                result_edge_parameters = {
                    uniform_deflection.Parameter(i)
                    for i in range(1, uniform_deflection.NbPoints() + 1)
                }
                return result_edge_parameters
            else:
                raise RuntimeError('Curve discretization not possible')

        @classmethod
        def curve_discretization_element_length(
                cls,
                edge_curve_adaptor,
                start_parameter: float,
                end_parameter: float,
                max_element_length: float,
                use_fast_abscissa: bool,
                segment_length: float = None
        ) -> set[float]:
            """
            Equidistant distribution on the curve.
            """
            if segment_length is None:
                segment_length = GCPnts_AbscissaPoint_Length(edge_curve_adaptor, start_parameter, end_parameter)

            num_points = int(max(2, ceil(segment_length / float(max_element_length))))
            if use_fast_abscissa:
                uniform_abscissa = GCPnts_QuasiUniformAbscissa()
            else:
                uniform_abscissa = GCPnts_UniformAbscissa()
            uniform_abscissa.Initialize(edge_curve_adaptor, num_points, start_parameter, end_parameter)
            if uniform_abscissa.IsDone():
                result_edge_parameters = {
                    uniform_abscissa.Parameter(i)
                    for i in range(1, uniform_abscissa.NbPoints() + 1)
                }
                return result_edge_parameters
            else:
                raise RuntimeError('Curve discretization not possible')

        def get_material_region_from_parameter(self, curve_parameter):
            """
            Returns the material region from the geometry assembly at a given curve parameter.
            
            Parameters
            ----------
            curve_parameter: float
                Parameter of the position where to find the material region.
            
            Returns
            -------
            AssemblyMaterialRegion
                The material region at the position, None for the base assembly.
            """
            results = []
            for material_region in self._material_regions:
                s_min = min(material_region.boundary_node_parameters)
                s_max = max(material_region.boundary_node_parameters)
                if s_min <= curve_parameter <= s_max:
                    results.append((material_region, s_max - s_min))
            if len(results) == 0:
                return None
            elif len(results) == 1:
                return results[0][0]
            elif len(results) > 1:
                log.warning(
                    'More than one material regions for one parameter in cross-section at '
                    f'z2={self._cross_section_geometry.z2_cross_section:.4f} m. Use smaller material region.'
                )
                mr_length = [r[1] for r in results]
                l_min_idx = mr_length.index(min(mr_length))
                return results[l_min_idx][0]

        def add_material_region_from_wire(self, uid, wire, material, position_blurring: float = 1e-4):
            """
            Adds a material region to the geometry assembly from a given wire and a material.
            
            Parameters
            ----------
            uid: str
                UID of the material region.
            wire: OCC.TopoDS.TopoDS_Wire
                The geometry wire of the material region in the cross section plane.
            material: IMaterial
                The material of the material region.
            """
            curve_material_region, curve_adaptor_material_region = self._get_curve_from_wire(wire)
            # get_wire_boundary_points does not work in a few cases (first wire vertex is not the start vertex)
            start_point_material_region, end_point_material_region = get_curve_boundary_points(curve_adaptor_material_region)

            # Get curve parameter
            z1 = start_point_material_region.z if start_point_material_region.shape[0] == 3 else self._cross_section_geometry.z2_cross_section
            z2 = end_point_material_region.z if end_point_material_region.shape[0] == 3 else self._cross_section_geometry.z2_cross_section

            s1 = get_curve_parameter_from_point(
                self._curve,
                Vector([start_point_material_region.x, start_point_material_region.y, z1]),
                tolerance=position_blurring,
                exception_on_failure=False,
            )
            s2 = get_curve_parameter_from_point(
                self._curve,
                Vector([end_point_material_region.x, end_point_material_region.y, z2]),
                tolerance=position_blurring,
                exception_on_failure=False,
            )

            if s1 is None and s2 is None:
                #raise RuntimeError('No intersection of the material region wire bounds and the shell wire %s found.' % uid)
                log.debug(f"Material region {uid} is not overlapping with shell {self._uid} at current cross section")
                # return and do not add material region to assembly:
                return
            if s1 is None or s2 is None:
                # Try to get intersection points for the case that the material region wire is larger than the assembly
                log.debug('Only one intersection of the material region wire bounds and the shell wire found. '
                            'Try to set the other as border nodes of the assembly.')

                # # DEBUG
                # from cpacs_interface.utils.occ import vector_to_point
                # from OCC.Core.BRepTools import breptools_Write
                # from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
                # from OCC.Core.TopoDS import topods
                # breptools_Write(wire, f'wire.brep')
                #
                # breptools_Write(topods.Vertex(BRepBuilderAPI_MakeVertex(vector_to_point(start_point_material_region)).Shape()), f'start_point_material_region.brep')
                # breptools_Write(topods.Vertex(BRepBuilderAPI_MakeVertex(vector_to_point(end_point_material_region)).Shape()), f'end_point_material_region.brep')

                new_s = []
                start_point_assembly, end_point_assembly = get_curve_boundary_points(self._curve_adaptor)
                if is_point_on_curve(curve_material_region, start_point_assembly, position_blurring):
                    new_s.append(get_curve_parameter_from_point(self._curve, start_point_assembly))
                if is_point_on_curve(curve_material_region, end_point_assembly, position_blurring):
                    new_s.append(get_curve_parameter_from_point(self._curve, end_point_assembly))
                if len(new_s) == 1:
                    if s1 is None:
                        s1 = new_s[0]
                    if s2 is None:
                        s2 = new_s[0]
                elif len(new_s) == 2:
                    new_s = sorted(new_s)
                    s1 = new_s[0]
                    s2 = new_s[1]
                else:
                    raise RuntimeError('Unable to calculate the material region wire bounds.')

            material_region = CrossSectionGeometry.AssemblyMaterialRegion(uid, (s1, s2), material)
            self._material_regions.append(material_region)

        def add_material_region_from_points(self, uid, start_point, end_point, material, tolerance: float = 1e-2):
            """
            Adds a material region to the geometry assembly between two points.
            
            Parameters
            ----------
            uid: str
                UID of the material region.
            start_point: Vector
                Start point of the material region.
            end_point: Vector
                End point of the material region.
            material: IMaterial
                The material of the material region.
            """
            z1 = start_point.z if start_point.shape[0] == 3 else self._cross_section_geometry.z2_cross_section
            z2 = end_point.z if end_point.shape[0] == 3 else self._cross_section_geometry.z2_cross_section

            s1 = get_curve_parameter_from_point(self._curve, Vector([start_point.x, start_point.y, z1]), tolerance=tolerance)
            s2 = get_curve_parameter_from_point(self._curve, Vector([end_point.x, end_point.y, z2]), tolerance=tolerance)
            #log.debug('from {} and {} -> {}, {}'.format(start_point, end_point, s1, s2))

            material_region = CrossSectionGeometry.AssemblyMaterialRegion(uid, (s1, s2), material)
            self._material_regions.append(material_region)
    
        @staticmethod
        def get_unique_point_list(points, position_blurring):
            """
            Removes double points from a point list. Points with distance smaller than position_blurring
            are treated as the same point.
    
            Parameters
            ----------
            points: list(Vector)
                List of points.
            position_blurring: float
                The max distance from one point to a other different point.
    
            Returns
            -------
            list(Vector)
                The resulting list with removed duplicates.
            """
            # Remove duplicate points

            if len(points) > 2:
                # New, fast method
                points_array = np.array(points)
                dist_matrix = cdist(points_array, points_array, 'euclidean')
                res = [point for i, point in enumerate(points) if i == 0 or np.min(dist_matrix[i, 0:i]) > position_blurring]
                # new = [point for i, point in enumerate(points) if i == num_points-1 or np.min(dist_matrix[i, i+1:]) > position_blurring]
            else:
                # Old, slow method
                num_points = len(points)
                double_points_idx = list()
                for i in range(num_points):
                    for ii in range(i + 1, num_points):
                        if (points[ii] - points[i]).length < position_blurring:
                            # Same point
                            double_points_idx.append(ii)
                res = [points[i] for i in range(num_points) if i not in double_points_idx]

            return res
    
        @staticmethod
        def get_unique_parameter_list(parameter, parameter_blurring):
            """
            Removes double points from a point list. Points that distance is smaller than position_blurring
            are treated as the same point.
    
            Parameters
            ----------
            parameter: list(float)
                List of points.
            parameter_blurring: float
                The max difference from one parameter to a other different parameter.
    
            Returns
            -------
            list(float)
                The resulting list with removed duplicates.
            """
            # Maintain first and last parameter
            parameter = sorted(parameter)
            if (parameter[1] - parameter[0]) < parameter_blurring:
                del parameter[1]
            if (parameter[-1] - parameter[-2]) < parameter_blurring:
                parameter[-2]
    
            # Remove duplicate parameter
            num_parameter = len(parameter)
            double_parameter_idx = list()
            for i in range(num_parameter):
                for ii in range(i + 1, num_parameter):
                    if (parameter[ii] - parameter[i]) < parameter_blurring:
                        # Same parameter
                        double_parameter_idx.append(ii)
            return [parameter[i] for i in range(num_parameter) if i not in double_parameter_idx]
    
        def get_elements(self, element_type, **kwargs):
            """
            Returns the discreet elements of the geometry assembly.
            For further parameters see `CrossSectionGeometry.Assembly.node_parameters_for_discretization`.
            
            Parameters
            ----------
            element_type: class <- IElement
                The element type.
            
            Returns
            -------
            list(IElement)
                List of elements of the geometry assembly.
            """
            position_blurring = kwargs['position_blurring'] if 'position_blurring' in kwargs else 1e-5

            curve_adaptor = self._curve_adaptor
            curve = self._curve

            curve_length = GCPnts_AbscissaPoint_Length(curve_adaptor)
            curve_parameter_length = curve_adaptor.LastParameter() - curve_adaptor.FirstParameter()
            parameter_blurring = curve_parameter_length * position_blurring / curve_length
    
            component_fixed_node_points = list()
    
            # Material region border nodes
            for material_region in self._material_regions:
                component_fixed_node_points.append(get_point_from_curve_parameter(curve_adaptor, material_region.boundary_node_parameters[0]))
                component_fixed_node_points.append(get_point_from_curve_parameter(curve_adaptor, material_region.boundary_node_parameters[1]))
    
            fixed_node_points = component_fixed_node_points + self._additional_fixed_node_points  # Additional fixed nodes

            # Add wire vertices, i.e. kinks except of start and end point
            shape_points = get_shape_vertices(self._wire, with_boundary_vertices=False)
            fixed_node_points.extend(shape_points)

            # Add start and end points
            fixed_node_points.append(get_point_from_curve_parameter(curve_adaptor, curve_adaptor.FirstParameter()))
            fixed_node_points.append(get_point_from_curve_parameter(curve_adaptor, curve_adaptor.LastParameter()))

            # Remove duplicate points
            component_fixed_node_points = CrossSectionGeometry.Assembly.get_unique_point_list(component_fixed_node_points, position_blurring)
            fixed_node_points = CrossSectionGeometry.Assembly.get_unique_point_list(fixed_node_points, position_blurring)
    
            # Get fixed node parameters
            component_fixed_node_parameters = sorted(CrossSectionGeometry.Assembly.get_unique_parameter_list(
                [
                    get_curve_parameter_from_point(curve, Vector([point.x, point.y, point.z]))
                    for point in component_fixed_node_points
                ] + [curve_adaptor.LastParameter(), curve.FirstParameter()], parameter_blurring))
            fixed_node_parameters = sorted(CrossSectionGeometry.Assembly.get_unique_parameter_list(
                [
                    get_curve_parameter_from_point(curve, Vector([point.x, point.y, point.z]))
                    for point in fixed_node_points
                ] + [curve_adaptor.LastParameter(), curve_adaptor.FirstParameter()], parameter_blurring))
    
            # Get all node parameters (fixed and flexible)
            node_parameters = self.node_parameters_for_discretization(
                position_blurring,
                fixed_node_parameters,
                **{k: v for k, v in kwargs.items() if not k == 'position_blurring'},
            )
            node_parameters = sorted(CrossSectionGeometry.Assembly.get_unique_parameter_list(
                node_parameters, parameter_blurring))
            #print(node_parameters)

            # Reverse the node parameters, if thickness direction for the element placement points to
            # the opposite direction of the wire/curve normal direction
            if self.assembly_type in ['upperShell', 'lowerShell']:
                reversed_nodes = False
            else:
                if (self._thickness_direction == 'inside' and not self.clockwise) or \
                   (self._thickness_direction == 'outside' and self.clockwise):
                    reversed_nodes = True
                else:
                    reversed_nodes = False

            if reversed_nodes:
                node_parameters.reverse()
                component_fixed_node_parameters.reverse()

            elements = []
            # For each component
            for component_idx in range(len(component_fixed_node_parameters)-1):
                if reversed_nodes:
                    component_node_parameters = [n for n in node_parameters
                                                 if component_fixed_node_parameters[component_idx] + parameter_blurring >= n >=
                                                 component_fixed_node_parameters[component_idx + 1] - parameter_blurring]
                else:
                    component_node_parameters = [n for n in node_parameters
                                                 if component_fixed_node_parameters[component_idx] - parameter_blurring <= n <=
                                                 component_fixed_node_parameters[component_idx + 1] + parameter_blurring]
                
                mean_component_node_parameter = (component_node_parameters[0] + component_node_parameters[-1]) / 2.
                material_region = self.get_material_region_from_parameter(mean_component_node_parameter)
                if material_region is None:
                    material = deepcopy(self._material)
                else:
                    material = material_region.material

                component = self._cross_section_geometry.get_component(material, self.midsurface_offset,
                                                                       assembly_type=self.assembly_type,
                                                                       assembly_uid=self.uid,
                                                                       extra_data=self.extra_data)
                self._components.append(component)
                component.assembly = self
                if material_region is not None:
                    material_region.component = component
                    component.material_region = material_region

                # For each element
                for element_idx in range(len(component_node_parameters)-1):
                    position1 = get_point_from_curve_parameter(curve_adaptor, component_node_parameters[element_idx])
                    position2 = get_point_from_curve_parameter(curve_adaptor, component_node_parameters[element_idx+1])
                    element = self._cross_section_geometry.get_element(element_type, position1, position2,
                                                                       component, position_blurring)
                    elements.append(element)
            return elements
        
        @property
        def midsurface_offset(self):
            """float: Midsurface offset of the geometry assembly."""
            if self._thickness_direction == 'center':
                return 0
            elif self._thickness_direction == 'inside':
                return 0.5
            elif self._thickness_direction == 'outside':
                return -0.5
            else:
                log.warning(f'Thickness direction "{self._thickness_direction}" not known, thickness_direction is set to "center".')
                return 0


class WingCrossSectionGeometryDefinition(object):
    """
    Simple definition of a typical wing cross section, means an outer aerodynamic profile with inner shear webs.
    
    Attributes
    ----------
    profile_points: list(Vector)
        The list of all points of the outer profile.
        The profile is closed between the first and the last point in the list.
    profile_material: IMaterial
        Base material of the profile.
    material_regions: list(((float, float), IMaterial))
        List of material regions of the profile.
        ((start_point, end_point), material)
    webs: list(((Vector, Vector), IMaterial))
        List of webs. (Vector, Vector) are the start and the end points of the line where to create the web,
        IMaterial the web material.
    material_region_lines: list(((Vector, Vector), IMaterial))
        List of material regions defined by the intersection point of the profile with the given line.
        ((line_start_point, line_end_point), material)
    element_size: float (default: None)
        The max length of the cross section elements. If the value not equals None, max_element_size
        in the get_geometry method is overwritten.
    profile_thickness_direction: str
            - 'inside' if the wire is the outer border of the profile as seen from the profile CoG.
            - 'outside' if the wire is the inner border of the profile as seen from the profile CoG.
            - 'center' if the wire is in the middle of the profile.
    profile_spline
        True, if the points should be interpolated by a spline (default options).
        For further options for the spline creation use a dict with following keys:
        - 'DegMin': int
        	default value is 3
        - 'DegMax': int,optional
        	default value is 8
        - 'Continuity': GeomAbs_Shape,optional
        	default value is GeomAbs_C2
        - 'Tol3D': float,optional
        	default value is 1.0e-3
    """
    def __init__(
            self,
            profile_points,
            profile_material,
            material_regions=None,
            webs=None,
            material_region_lines=None,
            element_size=None,
            profile_thickness_direction='inside',
            te_cutoff_x: Optional[float] = None,
            profile_spline: Union[bool, dict[str, object]] = False,
            base_material_as_material_region: bool = False,
            close_open_ends: bool = True,
            web_parts: bool = False,
    ):
        """
        Constructor.
        
        Parameters
        ----------
        profile_points: list(Vector)
            The list of all points of the outer profile.
            The profile is closed between the first and the last point in the list.
        profile_material: IMaterial
            Base material of the profile.
        material_regions: list((IMaterial, (float, float))) (default: None)
            List of material regions of the profile. None for no material regions.
            (material, (start_point, end_point))
        webs: list(((Vector, Vector), IMaterial)) (default: None)
            List of webs. (Vector, Vector) are the start and the end points of the line where to create the web,
            IMaterial the web material. None for no webs.
        material_region_lines: list((IMaterial, (Vector, Vector))) (default: None)
            List of material regions defined by the intersection point of the profile with the given line.
            None for no material region_lines.
            (material, (line_start_point, line_end_point))
        element_size: float (default: None)
            The max length of the cross section elements. If the value not equals None, max_element_size
            in the get_geometry method is overwritten.
        profile_thickness_direction: str (default: 'inside')
            - 'inside' if the wire is the outer border of the profile as seen from the profile CoG.
            - 'outside' if the wire is the inner border of the profile as seen from the profile CoG.
            - 'center' if the wire is in the middle of the profile.
        profile_spline
            True, if the points should be interpolated by a spline (default options).
            For further options for the spline creation use a dict with following keys:
            - 'DegMin': int
                default value is 3
            - 'DegMax': int,optional
                default value is 8
            - 'Continuity': GeomAbs_Shape,optional
                default value is GeomAbs_C2
            - 'Tol3D': float,optional
                default value is 1.0e-3
        base_material_as_material_region
            If True, a material region with the base material is assigned to the whole geometry.
            Only used to generate a good TE mesh for the BACAS export.
        close_open_ends
            True, if open ends of the contour are closed.
        web_parts
            True, if web are also added without intersection the contour at two points to create open cross-section geometries.
        """
        self.profile_points = profile_points
        self.profile_material = profile_material
        self.material_regions = material_regions if material_regions is not None else []
        self.webs = webs if webs is not None else []
        self.material_region_lines = material_region_lines if material_region_lines is not None else []
        self.element_size = element_size
        self.profile_thickness_direction = profile_thickness_direction
        self.te_cutoff_x = te_cutoff_x
        self.profile_spline = profile_spline
        self.base_material_as_material_region = base_material_as_material_region
        self.close_open_ends = close_open_ends
        self.web_parts = web_parts
    
    def get_geometry(self, **kwargs):
        """
        Returns the cross section geometry from the given definition.

        Returns
        -------
        CrossSectionGeometry
            The cross section geometry.
        """
        close_open_ends = self.close_open_ends
        if 'close_open_ends' in kwargs:
            close_open_ends = kwargs['close_open_ends']

        geometry = CrossSectionGeometry()
        profile_points = self.profile_points

        # Cut off profile TE
        if self.te_cutoff_x is not None:
            profile_points = [p for p in profile_points if p[0] < self.te_cutoff_x]

        # Add profile
        profile_wire = point_list_to_wire(profile_points, closed_wire=close_open_ends, spline=self.profile_spline)
        profile = CrossSectionGeometry.Assembly(geometry, profile_wire, self.profile_material,
                                                thickness_direction=self.profile_thickness_direction)
        if self.base_material_as_material_region:
            profile.add_material_region_from_points('', profile_points[0], profile_points[-1], self.profile_material)  # For TE corners
        geometry.add_profile_assembly(profile)

        # Add material regions
        for (start_point, end_point), material in self.material_regions:
            profile.add_material_region_from_points('', start_point, end_point, material)
        
        # Add material regions from lines
        for (line_start_point, line_end_point), material in self.material_region_lines:
            cut_points = get_intersection_points(profile_wire, edge_from_points(line_start_point, line_end_point))
            assert len(cut_points) == 2
            profile.add_material_region_from_points('', cut_points[0], cut_points[1], material)

        # Add webs
        for (web_line_start_point, web_line_end_point), web_material in self.webs:
            geometry.add_web_from_line(web_line_start_point, web_line_end_point, web_material, 'Spar', web_parts=self.web_parts)

        return geometry

    def get_discreet_geometry(self, element_type, **kwargs):
        """
        Returns the discreet cross section geometry from the given definition.
        For further parameters see `CrossSectionGeometry.Assembly.get_elements`.

        Parameters
        ----------
        element_type: class <- IElement
            The element type.

        Returns
        -------
        DiscreetCrossSectionGeometry
            The discreet cross section geometry.
        """
        if 'close_open_ends' not in kwargs:
            kwargs['close_open_ends'] = self.close_open_ends

        geometry = self.get_geometry(**kwargs)

        if self.element_size is not None:
            kwargs['element_length'] = self.element_size

        return geometry.create_discreet_cross_section_geometry(element_type, **kwargs)
