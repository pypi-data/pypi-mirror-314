"""
This module contains helping function for the work with OpenCASCADE.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2023 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.occ import *

except ImportError:
    log.info('Modul cpacs_interface.utils.occ not found. Use PreDoCS OCC utils.')

    from random import random
    from typing import List, Union, Optional

    import numpy as np
    from OCC.Core.Approx import Approx_Curve3d
    from OCC.Core.BRep import BRep_Tool
    from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_Curve, BRepAdaptor_Surface
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
    from OCC.Core.BRepBndLib import brepbndlib
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Transform, \
        BRepBuilderAPI_MakeFace
    from OCC.Core.BRepFeat import BRepFeat_SplitShape
    from OCC.Core.BRepLProp import BRepLProp_SLProps
    from OCC.Core.Bnd import Bnd_Box
    from OCC.Core.Extrema import Extrema_ExtFlag
    from OCC.Core.GCPnts import GCPnts_AbscissaPoint, GCPnts_AbscissaPoint_Length
    from OCC.Core.GProp import GProp_GProps
    from OCC.Core.Geom import Geom_Plane, Geom_Line, Geom_Surface
    from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve, GeomAPI_IntCS, GeomAPI_ProjectPointOnSurf, \
        GeomAPI_PointsToBSpline
    from OCC.Core.GeomAbs import GeomAbs_C2, GeomAbs_C1, GeomAbs_C0
    from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface
    from OCC.Core.TColgp import TColgp_HArray1OfPnt
    from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX, TopAbs_FACE, TopAbs_ShapeEnum
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopoDS import topods, TopoDS_Face, TopoDS_Iterator, TopoDS_Shape, TopoDS_Shell, TopoDS_Compound, \
        TopoDS_Wire
    from OCC.Core.gp import gp_Vec, gp_Pln, gp_Pnt, gp_Dir, gp_Trsf

    def ad_occt_installed():
        """
        Instead of:
        from cpacs_interface.utils.globals import ad_occt_installed
        """
        return False

    if not ad_occt_installed():
        from OCC.Display.OCCViewer import rgb_color as color
        from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
        from OCC.Core.BRepAdaptor import BRepAdaptor_HCompCurve, BRepAdaptor_HCurve
    else:
        from OCC.Core.Standard import Standard_Real

    from PreDoCS.util.vector import Vector


    def edge_from_points(start_point, end_point):
        """
        Returns a edge from two points.

        Parameters
        ----------
        start_point: Vector
            Start point.
        end_point: Vector
            End point.

        Returns
        -------
        OCC.TopoDS.TopoDS_Edge
            The edge.
        """
        return BRepBuilderAPI_MakeEdge(
            gp_Pnt(float(start_point.x), float(start_point.y), float(start_point.z) if len(start_point) > 2 else 0),
            gp_Pnt(float(end_point.x), float(end_point.y), float(end_point.z) if len(end_point) > 2 else 0)).Edge()


    def point_list_to_wire(point_list, closed_wire: bool = False, spline: Union[bool, dict[str, object]] = False):
        """
        Returns a wire from a point list.

        Parameters
        ----------
        point_list: list(Vector)
            List of points. If the vectors are two elements in size, 0 is added as the z-element.
        closed_wire: bool (default: False)
            True for closed wire, False for open wire.
        spline
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


        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The wire.
        """
        point_list = [Vector([p.x, p.y, 0]) if len(p) == 2 else p for p in point_list]
        wire_builder = BRepBuilderAPI_MakeWire()
        if (isinstance(spline, bool) and spline) or isinstance(spline, dict):
            # Interpolate profile with a spline
            if not isinstance(spline, dict):
                spline = dict()
            points_array = TColgp_HArray1OfPnt(0, len(point_list) - 1)
            for i, v in enumerate(point_list):
                points_array.SetValue(i, vector_to_point(v))

            curve_builder = GeomAPI_PointsToBSpline(
                points_array,
                spline.get('DegMin', 3),
                spline.get('DegMax', 8),
                spline.get('Continuity', GeomAbs_C2),
                spline.get('Tol3D', 1.0e-3),
            )

            curve = curve_builder.Curve()
            edge_builder = BRepBuilderAPI_MakeEdge(curve)
            edge = edge_builder.Edge()
            wire_builder.Add(edge)
        else:
            # No spline interpolation
            for i_edge in range((len(point_list) - 1)):
                p1 = point_list[i_edge]
                p2 = point_list[i_edge + 1]
                wire_builder.Add(edge_from_points(p1, p2))
        if closed_wire:
            wire_builder.Add(edge_from_points(point_list[-1], point_list[0]))
        return wire_builder.Wire()


    def plane_to_face(plane: gp_Pln) -> TopoDS_Face:
        """
        Converts a plane into a face.

        Parameters
        ----------
        plane: gp_Pln
            The plane.

        Returns
        -------
        TopoDS_Face
            Converted face from plane.
        """
        return BRepBuilderAPI_MakeFace(plane).Face()


    def get_intersection_wire(geometry1, geometry2, tolerance: Optional[float] = None):
        """
        Returns the intersection wire from the two geometries.

        Parameters
        ----------
        geometry1: OCC.TopoDS.TopoDS_Shape
            The first geometry.
        geometry2: OCC.TopoDS.TopoDS_Shape
            The second geometry.

        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The intersection wire.
        """
        intersection_shape = get_intersection_shape(geometry1, geometry2, tolerance=tolerance)

        # # DEBUG
        # from OCC.Core.BRepTools import breptools_Write
        # from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
        #
        # breptools_Write(intersection_shape, f'intersection_shape_{d}.brep')
        # breptools_Write(geometry1, f'geometry1_{d}.brep')
        # breptools_Write(topods.Face(BRepBuilderAPI_MakeFace(geometry2, -2, 2, -2, 2).Face()), f'geometry2_{d}.brep')

        wire_builder = BRepBuilderAPI_MakeWire()
        edge_explorer = TopExp_Explorer(intersection_shape, TopAbs_EDGE)
        has_intersection = False
        while edge_explorer.More():
            has_intersection = True
            wire_builder.Add(topods.Edge(edge_explorer.Current()))
            edge_explorer.Next()

        if has_intersection:
            wire_builder.Build()
            if wire_builder.IsDone():
                return wire_builder.Wire()
            else:
                # # DEBUG
                # from OCC.Display.SimpleGui import init_display
                # from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
                # from OCC.Core.BRepTools import breptools_Write
                # from OCC.Display.OCCViewer import rgb_color as color
                #
                # display, start_display, add_menu, add_function_to_menu = init_display()
                # plane = BRepBuilderAPI_MakeFace(geometry2, -10, 10, -10, 10)
                # display.DisplayShape(geometry1, update=True, color=color(1, 0, 0))
                # display.DisplayShape(plane.Face(), update=True, color=color(0, 1, 0))
                # display.FitAll()
                # start_display()
                # display, start_display, add_menu, add_function_to_menu = init_display()
                # edge_explorer.ReInit()
                # i = 0
                # while edge_explorer.More():
                #     shape = edge_explorer.Current()
                #     breptools_Write(topods.Edge(shape), 'shape_{}.brep'.format(i))
                #     display.DisplayShape(shape, update=True)
                #     edge_explorer.Next()
                #     i += 1
                # display.FitAll()
                # start_display()
                raise RuntimeError('get_intersection_wire() BRepBuilderAPI_WireError {}'.format(wire_builder.Error()))
        else:
            return None


    def vertex_to_vector(vertex):
        """
        Converts an OpenCASCADE Vertex to a PreDoCS Vector.

        Parameters
        ----------
        vertex: OCC.TopoDS.TopoDS_Vertex
            The vertex.

        Returns
        -------
        Vector
            The vector.
        """
        return point_to_vector(BRep_Tool.Pnt(vertex))


    def point_to_vector(point):
        """
        Converts an OpenCASCADE Point to a PreDoCS Vector.

        Parameters
        ----------
        point: OCC.gp.gp_Pnt
            The point.

        Returns
        -------
        Vector
            The vector.
        """
        if ad_occt_installed():
            return Vector([point.X().getValue(), point.Y().getValue(), point.Z().getValue()])
        else:
            return Vector([point.X(), point.Y(), point.Z()])


    def vector_to_point(vector):
        """
        Converts a PreDoCS Vector to an OpenCASCADE Point.

        Parameters
        ----------
        vector: Vector
            The vector.

        Returns
        -------
        point: OCC.gp.gp_Pnt
            The point.
        """
        if ad_occt_installed():
            point = gp_Pnt()
            point.SetX(Standard_Real(float(vector.x)))
            point.SetY(Standard_Real(float(vector.y)))
            point.SetZ(Standard_Real(float(vector.z)))
            return point
        else:
            return gp_Pnt(float(vector.x), float(vector.y), float(vector.z))


    def vector_to_direction(vector: Vector):
        """
        Converts a PreDoCS Vector to an OpenCASCADE direction.

        Parameters
        ----------
        vector: Vector
            The vector.

        Returns
        -------
        point: OCC.gp.gp_Dir
            The direction.
        """
        return gp_Dir(float(vector.x), float(vector.y), float(vector.z))


    def vector_to_occ_vector(vector):
        """
        Converts a PreDoCS Vector to an OpenCASCADE Vector.

        Parameters
        ----------
        vector
            The vector.

        Returns
        -------
        point: OCC.gp.gp_Vec
            The point.
        """
        return gp_Vec(float(vector.x), float(vector.y), float(vector.z))


    def get_intersection_shape(geometry1, geometry2, tolerance: float = 1e-3):
        """
        Returns the intersection shape from the two geometries.

        Parameters
        ----------
        geometry1: OCC.TopoDS.TopoDS_Shape
            The first geometry.
        geometry2: OCC.TopoDS.TopoDS_Shape
            The second geometry.

        Returns
        -------
        OCC.TopoDS.TopoDS_Shape
            The intersection shape.
        """
        assert isinstance(geometry1, TopoDS_Shape) or isinstance(geometry1, Geom_Surface)
        assert isinstance(geometry2, TopoDS_Shape) or isinstance(geometry2, Geom_Surface) or isinstance(geometry2,
                                                                                                        gp_Pln)
        section = BRepAlgoAPI_Section(geometry1, geometry2, False)
        section.Approximation(True)
        if tolerance is not None:
            section.SetFuzzyValue(tolerance)
        section.Build()
        result_shape = section.Shape()
        return result_shape


    def get_intersection_points(geometry1, geometry2, tolerance: Optional[float] = None):
        """
        Returns the intersection points from the two geometries.

        Parameters
        ----------
        geometry1: OCC.TopoDS.TopoDS_Shape
            The first geometry.
        geometry2: OCC.TopoDS.TopoDS_Shape
            The second geometry.

        Returns
        -------
        list(Vector)
            The intersection points.
        """
        result_shape = get_intersection_shape(geometry1, geometry2, tolerance)
        return get_shape_vertices(result_shape)


    def get_shape_vertices(shape, with_boundary_vertices=True, only_forward: bool = False) -> List[Vector]:
        """
        Returns the vertices of the shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape.
        with_boundary_vertices: bool (default: True)
            False, if the first and the last vertices should be deleted.

        Returns
        -------
        list(Vector)
            The points.
        """
        vertex_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
        vertices = []
        is_wire = isinstance(shape, TopoDS_Wire)
        while vertex_explorer.More():
            # consider only vertices with Orientation TopAbs_FORWARD (=0)
            if not only_forward or (not vertex_explorer.Current().Orientation() or is_wire):
                vertices.append(topods.Vertex(vertex_explorer.Current()))
            vertex_explorer.Next()

        if not with_boundary_vertices:
            del vertices[0]
            del vertices[-1]

        return [vertex_to_vector(v) for v in vertices]


    def get_shape_vertices_forward(shape, with_boundary_vertices=True) -> List[Vector]:
        """
        Returns the vertices of the shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape.
        with_boundary_vertices: bool (default: True)
            False, if the first and the last vertices should be deleted.

        Returns
        -------
        list(Vector)
            The points.
        """
        return get_shape_vertices(shape, with_boundary_vertices=with_boundary_vertices, only_forward=True)


    def get_wire_boundary_points(wire):
        """
        Returns the boundary points of a wire.

        Parameters
        ----------
        wire: OCC.TopoDS.TopoDS_Wire
            The wire.

        Returns
        -------
        Vector
            The first boundary point.
        Vector
            The second boundary point.
        """
        vertices = get_shape_vertices(wire)
        return vertices[0], vertices[-1]


    def get_curve_boundary_points(curve_adaptor):
        """
        Returns the boundary points of a curve.

        Parameters
        ----------
        curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            The curve adaptor.

        Returns
        -------
        Vector
            The first boundary point.
        Vector
            The second boundary point.
        """
        return get_point_from_curve_parameter(curve_adaptor, curve_adaptor.FirstParameter()), \
            get_point_from_curve_parameter(curve_adaptor, curve_adaptor.LastParameter())


    def get_point_from_curve_parameter(curve_adaptor, s):
        """
        Returns a point of a curve from the curve parameter.

        Parameters
        ----------
        curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            The curve adaptor.
        s: float
            The curve parameter.

        Returns
        -------
        Vector
            The point.
        """
        point = curve_adaptor.Value(s)
        return point_to_vector(point)


    def get_curve_parameter_from_point(curve, point, tolerance: float = 1e-3, exception_on_failure: bool = True):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        point: Vector
            The point.
        tolerance
            Tolerance for the distance between curve and point.
        exception_on_failure
            True, if an exception is raised if no curve parameter is found, False for None as return value.

        Returns
        -------
        float
            The curve parameter from the point.
        """
        projection = GeomAPI_ProjectPointOnCurve(vector_to_point(point), curve)
        if projection.NbPoints() > 0:
            distance = projection.LowerDistance()
            # p_proj = projection.NearestPoint()
            if distance > tolerance:
                if exception_on_failure:
                    raise RuntimeError(
                        f'Unsafe projection from point so curve, distance {distance:.3E} > tolerance {tolerance:.3E}.')
                else:
                    return None
            parameter = projection.LowerDistanceParameter()
        else:
            if exception_on_failure:
                raise RuntimeError('No projection of the point on the curve is found')
            else:
                return None

        return parameter


    def is_point_on_curve(curve, point, position_blurring):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        point: Vector
            The point.
        position_blurring: float
            The max distance from the point to the curve at which the point is considered as on the curve.

        Returns
        -------
        bool
            True, if the point is on the curve.
        """
        projection = GeomAPI_ProjectPointOnCurve(vector_to_point(point), curve)
        if projection.NbPoints() > 0:
            if projection.LowerDistance() <= position_blurring:
                return True
            else:
                return False
        else:
            return False


    def is_point_on_plane(point: Vector, plane: gp_Pln, position_blurring: float) -> bool:
        """
        Checks if the given point is on the given plane considering the position blurring.

        Parameters
        ----------
        point: Vector
            The point.
        plane: gp_Pln
            The plane.
        position_blurring: float
            The max distance from the point to the plane at which the point is considered as on the curve.

        Returns
        -------
        bool:
            True, if the point is on the plane.
        """
        point = vector_to_point(point)
        dist = plane.Distance(point)
        if dist < position_blurring:
            return True
        return False


    def transform_direction(direction: Vector, transformation: gp_Trsf) -> Vector:
        """
        Transforms a direction.

        Parameters
        ----------
        direction
            The direction to transform.
        transformation
            Transformation to perform.

        Returns
        -------
        Vector
            The transformed direction.
        """
        return point_to_vector(vector_to_direction(direction).Transformed(transformation))


    def transform_point(point: Vector, transformation: gp_Trsf) -> Vector:
        """
        Transforms a point.

        Parameters
        ----------
        point
            The point to transform.
        transformation
            Transformation to perform.

        Returns
        -------
        Vector
            The transformed point.
        """
        return point_to_vector(vector_to_point(point).Transformed(transformation))


    def transform_shape(shape, transformation):
        """
        Transforms a shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape to transform.
        transformation: OCC.gp.gp_Trsf
            Transformation to perform.

        Returns
        -------
        OCC.TopoDS.TopoDS_Shape
            The transformed shape.
        """
        return BRepBuilderAPI_Transform(shape, transformation).Shape()


    def transform_wire(shape, transformation):
        """
        Transforms a wire.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape to transform.
        transformation: OCC.gp.gp_Trsf
            Transformation to perform.

        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The transformed wire.
        """
        return topods.Wire(transform_shape(shape, transformation))


    def line_plane_intersection(line_origin, line_direction, plane_origin, plane_normal):
        """
        Find the intersection point of a line and a plane in 3D space.

        The line is described by its origin and a direction vector. The plane is described by its origin and a normal vector

        Parameters
        ----------
        line_origin: Vector
            Origin of the line.
        line_direction: Vector
            Direction of the line
        plane_origin: Vector
            Origin of the plane
        plane_normal: Vector
            Normal of the plane
        Returns
        -------
        intersection_point: Vector
            The intersection of line and Plane
        """
        # Transform into OCC objects
        line_origin = vector_to_point(line_origin)
        line_direction = vector_to_direction(line_direction)
        line = Geom_Line(line_origin, line_direction)

        plane_origin = vector_to_point(plane_origin)
        plane_normal = vector_to_direction(plane_normal)
        plane = Geom_Plane(plane_origin, plane_normal)

        # Calculate intersection point
        intersection_point = GeomAPI_IntCS(line, plane)

        # Check for successful calculation
        if not intersection_point.IsDone():
            log.warning('No intersection found')

        intersection_point = intersection_point.Point(1)

        # Transform OCC point object into vector object
        intersection_point = point_to_vector(intersection_point)

        return intersection_point


    def is_curve_clockwise(curve_adptor, ref_point):
        """
        Returns if a curve is clockwise or counter-clockwise relative to a given point.

        Parameters
        ----------
        curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            The curve adaptor.
        ref_point: Vector
            The reference point.

        Returns
        -------
        bool
            True, if the curve is clockwise; False, if the curve is counter-clockwise.
        """
        parameters = np.linspace(curve_adptor.FirstParameter(), curve_adptor.LastParameter(), 10)
        res = 0
        for parameter in parameters:
            P = gp_Pnt()
            V1 = gp_Vec()
            curve_adptor.D1(parameter, P, V1)
            cross_product = np.cross(point_to_vector(P) - ref_point, point_to_vector(V1))
            res += cross_product[2]

        if res > 0:
            return False
        elif res < 0:
            return True
        else:
            raise RuntimeError('Can not calculate clockwise of the curve.')


    class WireToCurveParameters(object):
        """
        This class stores the parameters for the conversion of a wire into a b-spline curve.

        Attributes
        ----------
        tolerance: float (default: 1e-7)
            3D tolerance.
        continuity: int (default: 2)
            Continuity of the curve, has to be 0, 1 or 2.
        max_segments: int (default: 200)
            Maximum b-spline segments.
        max_degrees: int (default: 12)
            Maximum b-spline degrees. Has to be lower or equal 25.
        """

        def __init__(self):
            self.tolerance = 1e-7
            self.continuity = 2
            self.max_segments = 200
            self.max_degrees = 12


    def create_curve_from_curve_adaptor(curve_adaptor, wire_to_curve_parameters=WireToCurveParameters()):
        """
            Returns if an approximated curve (b-spline) from a curve adaptor.

            Parameters
            ----------
            curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
                The curve adaptor.
            wire_to_curve_parameters: WireToCurveParameters
                The wire to curve parameters.

            Returns
            -------
            OCC.Geom.Geom_BSplineCurve
                The curve.
        """
        # log.warning('create_curve_from_curve_adaptor should be avoided, rather use the curve direct.')

        # Approximate curve from curve adaptor
        continuity = GeomAbs_C0
        if wire_to_curve_parameters.continuity == 1:
            continuity = GeomAbs_C1
        elif wire_to_curve_parameters.continuity == 2:
            continuity = GeomAbs_C2
        approx = Approx_Curve3d(curve_adaptor, wire_to_curve_parameters.tolerance,
                                continuity,
                                wire_to_curve_parameters.max_segments,
                                wire_to_curve_parameters.max_degrees)

        if approx.IsDone() and approx.HasResult():
            return approx.Curve()
        else:
            raise RuntimeError('Curve adaptor can not approximated by a curve')


    def create_curve_from_wire(wire, wire_to_curve_parameters=WireToCurveParameters()):
        """
            Returns if an approximated curve (b-spline) from a wire.

            Parameters
            ----------
            wire: OCC.TopoDS.TopoDS_Wire
                The wire.
            wire_to_curve_parameters: WireToCurveParameters
                The wire to curve parameters.

            Returns
            -------
            OCC.Geom.Geom_BSplineCurve
                The curve.
        """
        # Approximate curve from wire
        curve_adaptor = BRepAdaptor_HCompCurve(BRepAdaptor_CompCurve(wire))
        return create_curve_from_curve_adaptor(curve_adaptor, wire_to_curve_parameters)


    def create_curve_from_edge(edge, wire_to_curve_parameters=WireToCurveParameters()):
        """
            Returns if a approximated curve (b-spline) from a edge.

            Parameters
            ----------
            edge: OCC.TopoDS.TopoDS_Edge
                The edge.
            wire_to_curve_parameters: WireToCurveParameters
                The wire to curve parameters.

            Returns
            -------
            OCC.Geom.Geom_BSplineCurve
                The curve.
        """
        # Approximate curve from edge
        curve_adaptor = BRepAdaptor_HCurve(BRepAdaptor_Curve(edge))
        return create_curve_from_curve_adaptor(curve_adaptor, wire_to_curve_parameters)


    def get_shell_area(shell):
        """
        Calculates the area of a shell.

        Parameters
        ----------
        shell: OCC.TopoDS.TopoDS_Shell
            The shell.

        Returns
        -------
        float
            The area of the shell.
        """
        surface_properties = GProp_GProps()
        brepgprop_SurfaceProperties(shell, surface_properties)
        return surface_properties.Mass()


    def calc_cross_section_plane(beam_reference_point, beam_reference_axis, z_cross_section):
        """
        Calculates a cross section plane from the given parameters.

        Parameters
        ----------
        beam_reference_point: Vector
            The reference point of the beam at x_beam = y_beam = z_beam = 0.
        beam_reference_axis: Vector
            The beam reference axis from the beam reference point.
        z_cross_section: float
            The spanwise position where to create the cross section plane. z_beam starts at the beam
            reference point and is orientated in the beam reference axis direction.

        Returns
        -------
        Occ.gp.gp_Pln
            The cross section plane.
        """
        reference_dir = vector_to_direction(beam_reference_axis)
        return gp_Pln(
            vector_to_point(beam_reference_point).Translated(gp_Vec(reference_dir).Multiplied(z_cross_section)),
            reference_dir,
        )


    def get_shape_side_lengths(face: TopoDS_Face) -> List[float]:
        """
        Get side length of all sides of the given face.

        Parameters
        ----------
        face: TopoDS_Face
            The face.

        Returns
        -------
        List[float]:
            List of all side lengths of the face.
        """
        side_length = list()
        wire = TopoDS_Iterator(face).Value()
        edges = TopoDS_Iterator(wire)

        while edges.More():
            curve_adapt = BRepAdaptor_Curve(edges.Value())
            side_length.append(GCPnts_AbscissaPoint().Length(curve_adapt, curve_adapt.FirstParameter(),
                                                             curve_adapt.LastParameter(), 1e-6))
            edges.Next()
        return side_length


    def split_face_with_wire(face: TopoDS_Face, wire: TopoDS_Wire) -> List[TopoDS_Shape]:
        """
        Splits the given face into two shapes, seperated by the given wire.

        Parameters
        ----------
        face: TopoDS_Face
            The face.
        wire: TopoDS_Wire
            The wire which splits the face into two shapes.

        Returns
        -------
        List[TopoDS_Shape]:
            List of split shapes from face
        """
        split = BRepFeat_SplitShape(face)
        split.Add(wire, face)
        split.Build()

        return [split.Modified(face).First(), split.Modified(face).Last()]


    def get_normal_on_face(face: TopoDS_Face) -> gp_Dir:
        """
        Gets the normal vector of the given face.

        Parameters
        ----------
        face: TopoDS_Face
            The face.

        Returns
        -------
        gp_Dir:
            Direction of the normal vector.
        """
        adapt = BRepAdaptor_Surface(face)
        geom_face = BRep_Tool.Surface(face)
        uv = ShapeAnalysis_Surface(geom_face).ValueOfUV(get_shell_mid_point(face), 0.01).Coord()
        prop = BRepLProp_SLProps(adapt, uv[0], uv[1], 1, 1.e-3)
        return prop.Normal()


    def get_shell_mid_point(shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Face, TopoDS_Shape]) -> gp_Pnt:
        """
        Gets the coordinates of the midpoint of the given face, shape, shell or compound.

        Parameters
        ----------
        shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Face, TopoDS_Shape]
            Shell, Compound, Face or Shape

        Returns
        -------
        gp_Pnt:
            Midpoint.
        """
        prop = GProp_GProps()
        brepgprop_SurfaceProperties(shell, prop)
        return prop.CentreOfMass()


    def get_shapes_of_type(root_shape, TopAbs_Type: TopAbs_ShapeEnum, TopoDS_class) -> List[TopoDS_Shape]:
        shapes = []
        it = TopExp_Explorer(root_shape, TopAbs_Type)
        while it.More():
            shape = it.Value()
            assert isinstance(shape, TopoDS_class)
            shapes.append(shape)
            it.Next()
        return shapes


    def get_faces_from_shell(shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Shape]) -> List[TopoDS_Face]:
        """
        Gets all the faces from the given shell, compound or shape.

        Parameters
        ----------
        shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Shape]
            Shell, Compound or shape.

        Returns
        -------
        List[TopoDS_Face]:
            List of faces within the given shell.
        """
        if isinstance(shell, TopoDS_Face):
            return [shell]
        else:
            return get_shapes_of_type(shell, TopAbs_FACE, TopoDS_Face)


    def calc_cross_section_wires(component_segment, cross_section_plane: gp_Pln):
        """
        Calc the cross section wires from the intersection of a plane with a component segment.

        Parameters
        ----------
        component_segment: ComponentSegment
            The component segment.
        cross_section_plane
            The cross section plane.

        Returns
        -------
        upper_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the upper shell of the component segment.
            Wire direction is from the TE to the LE.
        lower_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the lower shell of the component segment.
            Wire direction is from LE to the lower TE.
        """
        upper_shape = component_segment._tigl_object.get_upper_shape().shape()
        lower_shape = component_segment._tigl_object.get_lower_shape().shape()

        upper_wire = get_intersection_wire(upper_shape, cross_section_plane)
        if upper_wire is None:
            raise RuntimeError('No intersection from the shell and the cross section plane.')
        lower_wire = get_intersection_wire(lower_shape, cross_section_plane)
        if lower_wire is None:
            raise RuntimeError('No intersection from the shell and the cross section plane.')

        return upper_wire, lower_wire


    def is_point_on_shape(point: Vector, shape: TopoDS_Shape, surface: Geom_Surface, tolerance: float,
                          return_distance: bool = False) -> Union[bool, tuple[bool, float]]:
        """
        Checks if a point is on a surface with a given tolerance.
        This function is used to substitute the CTiglAbstractGeometricComponent::GetIsOn function
        because of the hardcoded tolerance of 3 cm.
        """
        # fast check with bounding box
        bounding_box = Bnd_Box()
        brepbndlib.Add(shape, bounding_box)
        xmin, ymin, zmin, xmax, ymax, zmax = bounding_box.Get()

        if point.x < xmin - tolerance or point.x > xmax + tolerance or point.y < ymin - tolerance or point.y > ymax + tolerance or point.z < zmin - tolerance or point.z > zmax + tolerance:
            return (False, np.inf) if return_distance else False

        projection = GeomAPI_ProjectPointOnSurf()
        projection.Init(vector_to_point(point), surface)
        projection.SetExtremaFlag(Extrema_ExtFlag.Extrema_ExtFlag_MIN)
        distance = projection.LowerDistance()
        if projection.NbPoints() > 0 and distance < tolerance:
            return (True, distance) if return_distance else True
        else:
            return (False, distance) if return_distance else False


    def get_tigl_surface_from_point(point, segments, side_string, tolerance: float = 1e-3,
                                    min_distance: bool = False) -> tuple[int, Geom_Surface]:
        """
        Returns the surface of a given point.

        Parameters
        ----------
        point: Vector
            The point.
        segments: list(tigl3.configuration.CCPACSWingSegment)
            A list of all segments of the wing.
        side_string: str
            Name of the shell side, where point is located ('upper' or 'lower') or 'chord' for the chord face.
        min_distance
            If True, the minimal distance segment is returned.

        Returns
        -------
        int
            Segment index.
        Geom_Surface
            Surface in which the point is located, None if side_string is 'chord'.
        """
        # from OCC.Core.BRepTools import breptools_Write
        # from OCC.Display.SimpleGui import init_display
        # display, start_display, add_menu, add_function_to_menu = init_display()
        #
        # display.DisplayShape(vector_to_point(point), color=color(1, 0, 0), transparency=1)
        # log.warning(point)

        if min_distance:
            tolerance = 100
        surfaces = []
        distances = []
        for i, segment in enumerate(segments):
            # Workaround, because the python warping of segment.get_loft is not working
            if side_string == 'upper':
                shape = segment.get_upper_shape()
                surface = segment.get_upper_surface()
            elif side_string == 'lower':
                shape = segment.get_lower_shape()
                surface = segment.get_lower_surface()
            elif side_string == 'chord':
                shape = None
                surface = None
            else:
                raise RuntimeError(f'side_string "{side_string}" not valid')

            # if shape:
            #     breptools_Write(shape, f'segment_{i}.brep')
            #     display.DisplayShape(shape, color=color(0, 1, 0), transparency=0.5)

            # Don't use segment.get_is_on because tolerance is too high (3 cm)
            if shape:
                is_on, distance = is_point_on_shape(point, shape, surface, tolerance, return_distance=True)
                if is_on:
                    surfaces.append((i + 1, surface))
                    distances.append(distance)

        # display.FitAll()
        # start_display()

        # # Segment not found with the more exact method, use TIGL function
        # if len(surfaces) == 0:
        #     if not use_tigl_function:
        #         log.warning('get_tigl_surface_from_point: Segment not found with the more exact method, use TIGL function')
        #     for i, segment in enumerate(segments):
        #         if segment.get_is_on(vector_to_point(point)):
        #             if side_string == 'upper':
        #                 surface = segment.get_upper_surface()
        #             elif side_string == 'lower':
        #                 surface = segment.get_lower_surface()
        #             elif side_string == 'chord':
        #                 surface = None
        #             else:
        #                 raise RuntimeError(f'side_string "{side_string}" not valid')
        #             surfaces.append((i+1, surface))

        if min_distance:
            if len(distances) == 0:
                # from OCC.Core.BRepTools import breptools_Write
                # for i, segment in enumerate(segments):
                #     # Workaround, because the python warping of segment.get_loft is not working
                #     if side_string == 'upper':
                #         shape = segment.get_upper_shape()
                #         surface = segment.get_upper_surface()
                #     elif side_string == 'lower':
                #         shape = segment.get_lower_shape()
                #         surface = segment.get_lower_surface()
                #     elif side_string == 'chord':
                #         shape = None
                #         surface = None
                #     else:
                #         raise RuntimeError(f'side_string "{side_string}" not valid')
                #
                #     breptools_Write(shape, f'shape_{i}.brep')
                #     # breptools_Write(surface, f'surface_{i}.brep')
                # log.warning(point)
                raise RuntimeError('Point not on any segment')
            surfaces = [surfaces[distances.index(np.min(distances))]]

        if len(surfaces) == 0:
            raise RuntimeError('Point not on any segment')
        elif len(surfaces) > 1:
            log.warning(
                'get_tigl_surface_from_point: Point found on more than one segment, inaccurate material distribution possible.')
        return surfaces[0]


    def get_surface_parameters_from_point(surface, point: Vector, return_distance: bool = False):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        surface: OCC.Geom.Geom_Surface
            The surface.
        point
            The point.

        Returns
        -------
        float, float
            The surface parameters of the point.
        """
        point_to_project = vector_to_point(point)

        projection = GeomAPI_ProjectPointOnSurf()
        projection.Init(point_to_project, surface)
        projection.SetExtremaFlag(Extrema_ExtFlag.Extrema_ExtFlag_MIN)
        if projection.NbPoints() > 0:
            distance = projection.LowerDistance()
            parameters = projection.LowerDistanceParameters()
            log.debug(
                f'parameters: {parameters}, distance: {distance}, NearestPoint: {point_to_vector(projection.NearestPoint())}')
        else:
            raise RuntimeError('No projection of the point on the surface is found')

        return (parameters, distance) if return_distance else parameters


    def get_point_from_eta_xsi(component_segment, eta: float, xsi: float) -> Vector:
        """
        Returns a given eta-xsi position as point on the chord face of a component segment.

        Parameters
        ----------
        component_segment
            The component segment.
        eta
            The eta position of the projected point.
        xsi
            The xsi position of the projected point.

        Returns
        -------
        Vector
            The point.
        """
        return point_to_vector(component_segment._tigl_object.get_point(eta, xsi))


    def get_eta_xsi_with_projection_direction(component_segment, point, projection_direction) -> (float, float):
        """
        Projects a point along a direction to the chord face of a component segment and returns the eta-xsi position.

        Parameters
        ----------
        component_segment
            The component segment.
        point: Vector
            The point.
        projection_direction: Vector
            The projection direction.

        Returns
        -------
        float
            The eta position of the projected point.
        float
            The xsi position of the projected point.
        """
        chord_face = component_segment._tigl_object.get_chordface().get_surface()
        projection_line = Geom_Line(vector_to_point(point), vector_to_direction(projection_direction))

        cs_intersection = GeomAPI_IntCS(projection_line, chord_face)
        num_intersections = cs_intersection.NbPoints()
        if num_intersections == 1:
            point_on_chord = cs_intersection.Point(1)
            return component_segment._tigl_object.get_eta_xsi(point_on_chord)
        else:
            raise RuntimeError(f'{num_intersections} intersections with the chord face, not one.')


    def get_eta_xsi(component_segment, point: Vector) -> tuple[float, float]:
        """
        Projects a point normal to the chord face of a component segment and returns the eta-xsi position.

        Parameters
        ----------
        component_segment
            The component segment.
        point: Vector
            The point.

        Returns
        -------
        float
            The eta position of the projected point.
        float
            The xsi position of the projected point.
        """
        return component_segment._tigl_object.get_eta_xsi(vector_to_point(point))


    def get_spar_eta_xsi_from_span(spar: 'Spar', span: float, wing_aircraft_transformation: gp_Trsf,
                                   debug_plot: bool = False) -> (float, float):
        """
        Returns the eta-xsi position of a spar at a given spanwise position.

        Parameters
        ----------
        spar
            The spar.
        span
            The spanwise position where to calculate the eta-xsi position of the spar.
        wing_aircraft_transformation
            Transformation from the wing COSY to the aircraft COSY.

        Returns
        -------
        float
            The eta position of the projected point.
        float
            The xsi position of the projected point.
        """
        component_segment = spar._parent
        chord_face = component_segment._tigl_object.get_chordface().get_surface()
        spar_cut_geometry = spar.cut_geometry
        cut_plane = gp_Pln(
            gp_Pnt(0, span, 0).Transformed(wing_aircraft_transformation),
            gp_Dir(0, 1, 0).Transformed(wing_aircraft_transformation),
        )

        # DEBUG
        if debug_plot:
            from OCC.Display.SimpleGui import init_display
            display, start_display, add_menu, add_function_to_menu = init_display()

            from OCC.Core.TopoDS import topods
            from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace

            cross_section_plane_face = topods.Face(
                BRepBuilderAPI_MakeFace(cut_plane, -10, 10, -10, 10).Face())
            display.DisplayShape(cross_section_plane_face, color=color(0, 0, 1), transparency=0.5, update=True)

            display.DisplayShape(chord_face, color=color(0, 1, 0), transparency=0.5, update=True)
            display.DisplayShape(spar_cut_geometry, color=color(1, 0, 0), transparency=0.5, update=True)

            display.FitAll()
            start_display()

        # Spar span-plane intersection
        spar_plane_intersection = get_intersection_wire(spar_cut_geometry, cut_plane)
        if spar_plane_intersection is None:
            log.warning('No spar-cross-section intersection.')
            return None, None

        # Wire chord-face intersection
        ref_points = get_intersection_points(chord_face, spar_plane_intersection)
        if ref_points is None or len(ref_points) != 1:
            log.warning('Not one intersection of the cross-section spar position and the chord face.')
            return None, None

        # Project position to wing
        rel_pos = get_eta_xsi(component_segment, ref_points[0])

        log.debug('get_spar_eta_xsi_from_span: ... done')
        return rel_pos


    def get_layup_at_spanwise_position(layers, eta, with_positioning=False):
        """
        Returns the layup at a given relative spanwise position.

        Parameters
        ----------
        layers: list(Layer)
            The layers.
        eta: float
            Relative spanwise position (0 .. 1).
        with_positioning: bool (default: False)
            If True, the positioning arguments ae included in the result.

        Returns
        -------
        list(dict)
            The layup at the given position.
        """
        # print(eta)
        result = []
        for layer in layers:
            if layer.spanwise_borders[0] <= eta <= layer.spanwise_borders[1]:
                layer_dict = {
                    # 'layer': layer,
                    'layer_name': layer.name,
                    'material': layer.material.name,
                    'thickness': float(layer.thickness(eta)),
                    'fiber_direction': float(layer.fiber_orientation(eta)),
                }
                if hasattr(layer, 'ply_index_global'):
                    layer_dict['ply_index_global'] = layer.ply_index_global
                if hasattr(layer, 'labels'):
                    layer_dict['labels'] = layer.labels
                if with_positioning:
                    layer_dict['layer_positioning'] = layer.layer_positioning
                    layer_dict['positioning_arguments'] = layer.positioning_arguments.copy()
                    layer_dict['s_start'] = None
                    layer_dict['s_end'] = None
                result.append(layer_dict)
        # df.thickness.clip(lower=0)
        return result


    def get_spar_cell_positions(y_spar_start, y_spar_end, later_analysis_positions_nodes):
        """
        Get the spar cell positions with respect to the later analysis positions of a wing.

        Parameters
        ----------
        y_spar_start: float
            Spanwise position where the spar starts.
        y_spar_end: float
            Spanwise position where the spar ends.
        later_analysis_positions_nodes: list(float)
            Spanwise positions where the analysis is performed.

        Returns
        -------
        numpy.array
            The spanwise positions of the spar cell nodes.
        """
        y_spar_cell_positions = list(
            later_analysis_positions_nodes[np.logical_and(later_analysis_positions_nodes >= y_spar_start,
                                                          later_analysis_positions_nodes <= y_spar_end)])
        if y_spar_start not in y_spar_cell_positions:
            y_spar_cell_positions.insert(0, y_spar_start)
        if y_spar_end not in y_spar_cell_positions:
            y_spar_cell_positions.append(y_spar_end)
        return np.array(y_spar_cell_positions)


    def split_faces(face: Union[TopoDS_Face, TopoDS_Shape],
                    wires: List[TopoDS_Wire],
                    new_faces: List[TopoDS_Face] = None) -> List[TopoDS_Face]:
        """
        Splits the given face into multiple faces each seperated by a wire. The number of returned faces is one higher
        than the number of wires.

        Parameters
        ----------
        face: TopoDS_Face
            Base face.
        wires: List[TopoDS_Wire]
            List of wires which are used to split the base face.
        new_faces: List[TopoDS_Face]
            List of faces. When calling this method, keep this parameter None.

        Returns
        -------
        List[TopoDS_Face]:
            List of split faces.
        """
        wires = wires.copy()
        if new_faces is None:
            new_faces = list()
        if len(wires) and get_intersection_wire(face, wires[0]) is not None:
            tmp_faces = split_face_with_wire(face, wires[0])
            wires.pop(0)
            for face in tmp_faces:
                split_faces(face, wires, new_faces)
        else:
            if face not in new_faces:
                new_faces.append(face)
        return new_faces


    def get_shape_surface_area(shape: TopoDS_Shape) -> float:
        """
        Calculates the area of a shape instance

        Parameters
        ----------
        shape

        Returns
        -------
        float
            the area
        """
        props = GProp_GProps()
        brepgprop_SurfaceProperties(shape, props)
        return props.Mass()


    def get_normal_from_shape(shape: TopoDS_Shape) -> np.ndarray:
        faces = get_faces_from_shell(shape)
        assert len(faces) > 0, 'No faces found for shape.'
        face = faces[0]
        assert isinstance(face, TopoDS_Face)
        return np.asarray(get_normal_on_face(face).Coord())


    # def project_vector_on_surface(surface: TopoDS_Shape, vector: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    #     """
    #     Projects a given vector onto a surface using its normal vector.
    #     Parameters
    #     ----------
    #     surface: TopoDS_Shape
    #         The surface.
    #     vector: np.ndarray
    #         The vector.
    #
    #     Returns
    #     -------
    #     np.ndarray:
    #         The vector projected onto the surface.
    #     """
    #     normal = get_normal_from_shape(surface)
    #     return np.cross(normal, np.cross(vector, normal)), normal

    # def get_buckling_length(surface: TopoDS_Shape, material_orientation: np.ndarray) -> np.ndarray:
    #     """
    #     Calculates the buckling length of the surface. For reference see Hypersizer V7.1 Help "Buckling spans".
    #
    #     Parameters
    #     ----------
    #     surface: TopoDS_Shape
    #         The surface.
    #     material_orientation: np.ndarray
    #         The material orientation of the surface material.
    #
    #     Returns
    #     -------
    #     np.ndarray:
    #         Buckling lengths. First entry is the length in material orientation.
    #     """
    #     # TODO consider orthotropy direction of the material if it is set in the cpacs file
    #     face = get_faces_from_shell(surface)[0]
    #
    #     # project material orientation onto surface.
    #     material_orientation, normal = project_vector_on_surface(surface, material_orientation)
    #     # calculate transverse material orientation
    #     material_transverse_direction = np.cross(material_orientation, normal)
    #
    #     # get center of the surface
    #     center = np.asarray(get_shell_mid_point(surface).Coord())
    #
    #     # get corner points of the surface
    #     corner_points = list()
    #     for point in get_shape_vertices(surface, False):
    #         if point not in corner_points:
    #             corner_points.append(point)
    #
    #     # Calculate buckling length for material and transverse orientation
    #     length_buckling = list()
    #     for orientation in [material_orientation, material_transverse_direction]:
    #         # create plane in selected orientation
    #         cross_sec_plane = calc_cross_section_plane(Vector(center), Vector(orientation), 0)
    #         cross_sec_face = plane_to_face(cross_sec_plane)
    #         x_wire = get_intersection_wire(surface, cross_sec_face)
    #
    #         # cut surface through center point along selected orientation
    #         part_shapes = split_face_with_wire(face, x_wire)
    #
    #         # process each side
    #         cxy_list = list()
    #         XY_list = list()
    #         for xy_face in part_shapes:
    #             # get center of each side
    #             xy_center = np.asarray(get_shell_mid_point(xy_face).Coord())
    #
    #             # calculate the distance between the center of the split surface and the plane which was used to cut the
    #             # surface
    #             cxy_intersection = line_plane_intersection(Vector(xy_center), Vector(orientation),
    #                                                        Vector(center), Vector(orientation))
    #             cxy = np.linalg.norm(cxy_intersection - xy_center)
    #
    #             # get the corner points of the side which are also the corner points of the whole shape
    #             xy_corner_points = list()
    #             for point in get_shape_vertices(xy_face, False):
    #                 if point in corner_points and point not in xy_corner_points:
    #                     xy_corner_points.append(point)
    #
    #             # calculate the distance between the corner points of the split surface and the plane which was used to
    #             # cut the surface. Store the bigger distance.
    #             XY = list()
    #             for corner in xy_corner_points:
    #                 XY1_intersection = line_plane_intersection(Vector(corner), Vector(orientation),
    #                                                            Vector(center), Vector(orientation))
    #                 XY.append(np.linalg.norm(XY1_intersection - corner))
    #             XY = max(XY)
    #             cxy_list.append(cxy)
    #             XY_list.append(XY)
    #
    #         # calculate the buckling lengths
    #         length_buckling.append(
    #             2 * (min([cxy_list[0], XY_list[0] - cxy_list[0]]) + min([cxy_list[1], XY_list[1] - cxy_list[1]])))
    #
    #     return np.array(length_buckling)

    def get_random_color():
        return color(random(), random(), random())


    def transformation_occ_2_matrix(trsf: gp_Trsf) -> np.ndarray:
        """
        Converts OpenCASCADE transformation (gp_Trsf) to PreDoCS transformation (numpy.ndarray).
        """
        mat = []
        for r in range(3):
            col = []
            for c in range(4):
                col.append(trsf.Value(r + 1, c + 1))
            mat.append(col)
        mat.append([0, 0, 0, 1])
        return np.array(mat)


    def transformation_matrix_2_occ(trsf_mat: np.ndarray) -> gp_Trsf:
        """
        Converts PreDoCS transformation (numpy.ndarray) to an OpenCASCADE transformation (gp_Trsf).
        """
        trsf = gp_Trsf()
        trsf.SetValues(*trsf_mat[0:3, 0:4].flatten())
        return trsf


    def get_le_and_te_lines(component_segment) -> tuple[TopoDS_Wire, TopoDS_Wire]:
        """
        In global CPACS coordinate system.
        """
        wing_to_global_transformation = (
            component_segment.parent._tigl_object.get_transformation().get_transformation_matrix()
        )
        le = wing_to_global_transformation.transform(component_segment._tigl_object.get_leading_edge_line())
        te = wing_to_global_transformation.transform(component_segment._tigl_object.get_trailing_edge_line())
        return le, te


    def get_le_and_te_position(component_segment, eta: float) -> tuple[Vector, Vector]:
        """
        In global CPACS coordinate system.
        """
        le, te = get_le_and_te_lines(component_segment)

        le_curve = BRepAdaptor_CompCurve(le, True)
        le_len = GCPnts_AbscissaPoint_Length(le_curve)
        le_point = gp_Pnt()
        le_curve.D0(le_len * eta, le_point)

        te_curve = BRepAdaptor_CompCurve(te, True)
        te_len = GCPnts_AbscissaPoint_Length(te_curve)
        te_point = gp_Pnt()
        te_curve.D0(te_len * eta, te_point)

        return point_to_vector(le_point), point_to_vector(te_point)
