"""
This Module provides the definition of a PreDoCS coordinate system including a transformation method.

Classes
-------
PreDoCSCoord:
    Definition of the PreDoCS coordinate system


code author:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from typing import Callable

import numpy as np
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax1

from PreDoCS.LoadAnalysis.Load import DynamicReferencePoints
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.geometry import transform_direction_m, transform_location_m, invert_transformation_matrix, \
    create_transformation_matrix_aircraft_2_predocs_old, create_transformation_aircraft_2_predocs_new, \
    create_transformation_aircraft_2_predocs_beam_cosy
from PreDoCS.util.occ import get_point_from_eta_xsi, get_eta_xsi, transformation_occ_2_matrix, get_le_and_te_position
from PreDoCS.util.util import line_line_intersection, pt_is_in_plane_dir, \
    get_matrix_interpolation_function
from PreDoCS.util.vector import Vector
from PreDoCS.util.data import interp1d

log = get_module_logger(__name__)


class PreDoCSCoord:
    """
    Definition of the PreDoCS coordinate systems.
    There are three coordinate systems:
    * 'aircraft': global coordinate system.
    * 'wing': wing coordinate system, z-axis corresponds to the wing axis, transformation constant over the beam length.
    * 'predocs': PreDoCS cross-section coordinate system, z-axis corresponds to the wing axis,
                 transformation is changing over the beam length if the beam is kinked.
    The beam axis is defined in the aircraft coordinate system.

    Attributes
    ----------
    _section_origins: list(Vector)
        Origins of the PreDoCS coordinate system in global coordinates for each wing section
    _section_directions: list(Vector)
        Z-axes of the PreDoCS coordinate system in global coordinates for each wing section
    """
    def __init__(
            self,
            section_origins,
            section_directions,
            section_lengths,
            beam_nodes_z2,
            x_axis_definition: str = 'new',
            component_segment: 'ComponentSegment' = None,
            wing_reference_position: Vector = None,
            wing_reference_direction: Vector = None,
            mold_angle: float = 0.0,
            twist_func=None,
    ):
        """
        Class initialisation - Here the PreDoCS coordinate system is defined

        The PreDoCS coordinate system class offers the possibility to create beam nodes. The number of beam nodes may be
        chosen freely.

        Parameters
        ----------
        origin: list(Vector)
            Reference points for the PreDoCS z-axis for each section, not necessarily in the PreDoCS origin
        z_axis: list(Vector)
            Z-axis directions of the PreDoCS coordinate system in global coordinates
        section_lengths: list(float)
            Length of each section of the beam. Contains multiple entries only for a kinked beam
        num_beam_nodes: float
            Number of beam nodes
        x_axis_definition
            Orientation of the cross-section x-axis. Possible options:
            - 'old': old PreDoCS definition. The PreDoCS x-axis is orthogonal to the PreDoCS z-axis and
                     lies within the x-y-plane of the global coordinate system. The PreDoCS y-axis points
                     upward perpendicular to both other axis (cross-product).
            - 'new': cross-section x-axis is aligned with the global x-axis.
            - 'beam_cosy': cross-section x-axis corresponds to the y-axis if the beam COSY (corresponds to the chord line).
        mold_angle
            The mould angle influences the spar orientation in the profile. According to figure 24 ("struct_angle") of
            [1], the mould angle is a rotation of the rotor plane around the pitch axis. The
            resulting structural reference plane is going from the blade root origin to the blade tip of the blade geometry
            which includes the prebend and twist. After this rotation of the outer geometry the spars are oriented
            vertically in the blade according to the division point given in figure 23 [1].
            [1] IEA Wind TCP Task 37_10MW.pdf
        """
        assert len(section_origins) == len(section_directions)
        assert len(section_origins) == len(section_lengths)
        self._section_origins = section_origins
        for ii, z_axis_sec in enumerate(section_directions):
            section_directions[ii] = z_axis_sec.normalised
        self._section_directions = section_directions
        self._section_lengths = section_lengths
        self._num_of_sections = len(section_origins)
        self._beam_start = section_origins[0]
        self._beam_end = section_origins[-1] + self._section_directions[-1] * self.section_lengths[-1]
        self._beam_length = sum(self.section_lengths)
        assert self._beam_length * 1.00001 >= self._beam_start.dist(self._beam_end), 'Beam z2 range is less than the distance from beam start point to beam end point.'

        self._wing_reference_position = wing_reference_position if wing_reference_position is not None else section_origins[0]
        self._wing_reference_direction = wing_reference_direction if wing_reference_direction is not None else section_directions[0]

        self._x_axis_definition = x_axis_definition
        self._beam_nodes_normal_direction = None
        self._cross_sections_normal_direction = None
        self._mold_angle = mold_angle
        self._twist_func = twist_func

        self._transformation_func_aircraft_2_predocs = self._get_transformation_function_aircraft_2_predocs(
            component_segment,
            num_points_per_segment=10,  # TODO: adapt 10?
        )

        # Beam coordinate-system
        if self._x_axis_definition == 'old':
            self._transformation_aircraft_2_wing = create_transformation_matrix_aircraft_2_predocs_old(
                self._wing_reference_position, self._wing_reference_direction,
            )
        elif self._x_axis_definition == 'new':
            self._transformation_aircraft_2_wing = transformation_occ_2_matrix(create_transformation_aircraft_2_predocs_new(
                self._wing_reference_position, self._wing_reference_direction,
            ))
        elif self._x_axis_definition == 'beam_cosy':
            self._transformation_aircraft_2_wing = transformation_occ_2_matrix(create_transformation_aircraft_2_predocs_beam_cosy(
                self._wing_reference_position, self._wing_reference_direction, Vector([1, 0, 0])
            ))
        else:
            raise RuntimeError(f'Unknown x_axis_definition "{self._x_axis_definition}".')
        self._transformation_wing_2_aircraft = invert_transformation_matrix(self._transformation_aircraft_2_wing)

        # Calculate the reference points and beam-wise positions of nodes and cross sections
        self._z2_bn = beam_nodes_z2
        self._z2_cs = [(beam_nodes_z2[i] + beam_nodes_z2[i+1]) / 2 for i in range(len(beam_nodes_z2)-1)]

        self._beam_nodes = self.create_points_wing(self._z2_bn)
        self._cross_section_origins = self.create_points_wing(self._z2_cs)

    @staticmethod
    def from_c2p(
            c2p,
            node_placement,
            orientation: str = 'load_reference_points',
            x_axis_definition: str = 'new',
            mold_angle: float = 0.0,
            ensure_cross_sections_in_shell: bool = True,
    ):
        """
        The PreDoCS coordinate system can be built from a CPACS2PreDoCS instance. Several orientations can be selected.

        Choices for PreDoCS coordinate system orientation: 'load_reference_points', 'beam_reference_points', 'wingspan', 'root-tip', '3d-beam', 'rear-spar'

        Parameters
        ----------
        c2p: CPACS2PreDoCS
            The complete CPACS import
        node_placement: int, list(float), str
            Specifies how the beam nodes are placed
            Available options:
            - int: this defines the number of beam nodes and they are placed equally on the z2 axis
            - list(float): Defines the beam nodes on the z2 axis directly
            - str:
                "ribs": Defines the beam nodes at the intersection of the z2-axis with the ribs.
        orientation
            The orientation of the PreDoCS coordinate system z-axis
        x_axis_definition
            Orientation of the cross-section x-axis. Possible options:
            - 'old': old PreDoCS definition. The PreDoCS x-axis is orthogonal to the PreDoCS z-axis and
                     lies within the x-y-plane of the global coordinate system. The PreDoCS y-axis points
                     upward perpendicular to both other axis (cross-product).
            - 'new': cross-section x-axis is aligned with the global x-axis.
            - 'beam_cosy': cross-section x-axis corresponds to the y-axis if the beam COSY (corresponds to the chord line).
        mold_angle
            The mould angle influences the spar orientation in the profile. According to figure 24 ("struct_angle") of
            [1], the mould angle is a rotation of the rotor plane around the pitch axis. The
            resulting structural reference plane is going from the blade root origin to the blade tip of the blade geometry
            which includes the prebend and twist. After this rotation of the outer geometry the spars are oriented
            vertically in the blade according to the division point given in figure 23 [1].
            [1] IEA Wind TCP Task 37_10MW.pdf
        ensure_cross_sections_in_shell
            Ensure that the cross-sections are placed in a way that even the first and the last cross-section plane
            cuts the leading and trailing edge of the wing shell.
            Only used, if node_placement is an integer.

        Returns
        -------
        predocs_coord: PreDoCSCoord
            The PreDoCS coordinate system created from CPACS data
        """
        wing_reference_position = None
        wing_reference_direction = None

        if orientation == 'load_reference_points':
            # Import the load reference points and create a reference axis starting at the wing root reference point.
            global_load_reference_points = c2p.load_reference_points
            section_origins, section_directions = global_load_reference_points.get_reference_axis()
            section_lengths = []
            for i in range(len(section_origins)-1):
                section_lengths.append(section_origins[i].dist(section_origins[i+1]))
            section_lengths.append(section_origins[-1].dist(Vector(global_load_reference_points.point_list[-1, :])))

        elif orientation == 'beam_reference_points':
            # Import the beam reference points and create a reference axis
            wing_reference_position = c2p.wing_reference_position
            wing_reference_direction = c2p.wing_reference_direction
            beam_reference_points = c2p.beam_reference_points
            section_origins = beam_reference_points[:-1]
            section_directions = []
            section_lengths = []
            for i in range(len(beam_reference_points)-1):  # iterate over all points
                segment_vector = beam_reference_points[i+1] - beam_reference_points[i]
                section_lengths.append(segment_vector.length)
                section_directions.append(segment_vector.normalised)

        elif orientation == 'wingspan':
            p1 = Vector([0, 0, 0])
            p2 = Vector([0, c2p.halfspan, 0])

            section_lengths = [p2.dist(p1)]

            # section_origins, section_directions
            section_origins = [p1]
            section_directions = p2 - p1
            section_directions = [section_directions.normalised]

        elif orientation == 'root-tip':
            p1 = c2p.wingroot
            p2 = c2p.wingtip

            section_lengths = [p2.dist(p1)]

            # section_origins, section_directions
            section_origins = [p1]
            section_directions = p2 - p1
            section_directions = [section_directions.normalised]

        elif orientation == '3d-beam':
            p1 = c2p.wingroot
            p2 = c2p.wingtip

            section_directions = list()
            section_origins = list()
            section_lengths = list()
            for ii in range(len(c2p.wing.sections)-1):
                p_ii = Vector(c2p.wing.sections[ii].translation)
                p_iip1 = Vector(c2p.wing.sections[ii+1].translation)
                section_directions.append(p_iip1 - p_ii)
                section_origins.append(p1 + p_ii)

                section_lengths.append(p_iip1.dist(p_ii))
                section_directions[ii] = section_directions[ii].normalised
        elif orientation == 'rear-spar':
            # Currently implemented for only one component segment
            spars = c2p.component_segment.spars

            assert len(spars) > 0, 'No spar definition given in the CPACS file!'

            # determine the rear spar
            if len(spars) >= 2:
                start_xis = [spar.position_points[0][1] for spar in spars]
                rear_spar = spars[np.argmax(start_xis)]
            elif len(spars) == 1:
                rear_spar = spars[0]

            rear_spar_points = [Vector(c2p.component_segment.tigl_object.get_point(eta, xi).Coord())
                                for eta, xi in rear_spar.position_points]

            section_origins = rear_spar_points[0:-1]
            section_directions = []
            section_lengths = []
            for ii in range(len(section_origins)):
                section_lengths.append(rear_spar_points[ii+1].dist(rear_spar_points[ii]))
                section_directions.append(rear_spar_points[ii+1] - rear_spar_points[ii])
                section_directions[ii] = section_directions[ii].normalised

        else:
            raise RuntimeError('Orientation "{}" not supported from PreDoCsCoord.'.format(orientation))

        # Node placement
        if isinstance(node_placement, int):
            if not ensure_cross_sections_in_shell:
                root_z2 = 0.0
                tip_z2 = sum(section_lengths)
            else:
                component_segment = c2p.component_segment

                def get_point_z2_section(ref_point, ref_dir, point):
                    z2_section = np.dot(ref_dir, point - ref_point)
                    return z2_section

                # Root
                ref_point = section_origins[0]
                ref_dir = section_directions[0]

                root_le, root_te = get_le_and_te_position(component_segment, 0.0)
                # root_le = point_to_vector(cs_tigl.get_leading_edge_point(0.0))
                # root_te = point_to_vector(cs_tigl.get_trailing_edge_point(0.0))
                root_le_z2_section = get_point_z2_section(ref_point, ref_dir, root_le)
                root_te_z2_section = get_point_z2_section(ref_point, ref_dir, root_te)
                root_z2 = max(0, root_le_z2_section, root_te_z2_section)

                # Tip
                tip_le, tip_te = get_le_and_te_position(component_segment, 1.0)
                # tip_le = point_to_vector(cs_tigl.get_leading_edge_point(1.0))
                # tip_te = point_to_vector(cs_tigl.get_trailing_edge_point(1.0))
                tip_le_z2_section = get_point_z2_section(ref_point, ref_dir, tip_le)
                tip_te_z2_section = get_point_z2_section(ref_point, ref_dir, tip_te)
                delta_z2 = sum(section_lengths[0:-1])
                tip_z2 = min(delta_z2 + section_lengths[-1], tip_le_z2_section + delta_z2, tip_te_z2_section + delta_z2)

            beam_nodes_z2 = np.linspace(root_z2, tip_z2, node_placement)
        elif isinstance(node_placement, list):
            assert np.all([0 <= node_placement_i <= sum(section_lengths) for node_placement_i in node_placement]), 'Beam nodes must lie between 0 and {}'.format(sum(section_lengths))
            beam_nodes_z2 = node_placement
        elif isinstance(node_placement, str) and node_placement == 'ribs':
            beam_nodes_z2 = []
            for ribs in c2p.component_segment.rib_definitions:
                start_point = Vector(c2p.component_segment.tigl_object.get_point(ribs.start_position[0], ribs.start_position[1]).Coord())
                end_point = Vector(c2p.component_segment.tigl_object.get_point(ribs.end_position[0], ribs.end_position[1]).Coord())

                rib_intersection = None
                for i in range(len(section_origins)):
                    rib_intersection_point = line_line_intersection(start_point, end_point - start_point,
                                                                    section_origins[i], section_directions[i])

                    if rib_intersection_point is not None:
                        rib_intersection = section_origins[i].dist(rib_intersection_point) + sum(section_lengths[0:i])
                        break

                assert rib_intersection is not None, 'No rib intersection found, cannot place beam node for it.'
                beam_nodes_z2.append(rib_intersection)
        else:
            raise RuntimeError(f'node_placement "{node_placement}" is not implemented!')

        # Read prebend and twist if available
        def read_span_values_list(tixi, xpath):
            if tixi.checkElement(xpath):
                span_list_xpath = xpath + '/span'
                span_list_size = tixi.getVectorSize(span_list_xpath)
                span_list = tixi.getFloatVector(span_list_xpath, span_list_size)
                values_xpath = xpath + '/values'
                values_size = tixi.getVectorSize(values_xpath)
                values = tixi.getFloatVector(values_xpath, values_size)
                assert span_list_size == values_size
                return interp1d(span_list, values)
            else:
                return None
        twist = read_span_values_list(c2p.cpacs_interface.tixi_handle, c2p.component_segment.xpath + '/twist')

        # Create PreDoCSCoord
        predocs_coord = PreDoCSCoord(
            section_origins=section_origins,
            section_directions=section_directions,
            section_lengths=section_lengths,
            beam_nodes_z2=beam_nodes_z2,
            x_axis_definition=x_axis_definition,
            component_segment=c2p.component_segment,
            wing_reference_position=wing_reference_position,
            wing_reference_direction=wing_reference_direction,
            mold_angle=mold_angle,
            twist_func=twist,
        )

        return predocs_coord

    # def __getstate__(self):
    #     """Make pickle possible."""
    #     state = self.__dict__.copy()
    #     state['_transformation_aircraft_to_predocs'] = transformation_occ_2_matrix(self._transformation_aircraft_to_predocs)
    #     return state
    #
    # def __setstate__(self, state):
    #     """Make pickle possible."""
    #     self.__dict__.update(state)
    #     self._transformation_aircraft_to_predocs = transformation_matrix_2_occ(self._transformation_aircraft_to_predocs)

    def z2_2_point_aircraft(self, z2: float) -> Vector:
        """
        Returns the position of the beam axis in the aircraft coordinate system for the beam coordinate z2.
        """
        section_origin, section_direction, z2_section = self.get_section_parameter(z2)
        return section_origin + z2_section * section_direction

    def z2_2_point_wing(self, z2: float) -> Vector:
        """
        Returns the position of the beam axis in the wing coordinate system for the beam coordinate z2.
        """
        point_aircraft = self.z2_2_point_aircraft(z2)
        point_predocs = transform_location_m(self.transformation_aircraft_2_wing, point_aircraft)
        return point_predocs

    def z2_2_point_predocs(self, z2: float) -> Vector:
        """
        Returns the position of the beam axis in the PreDoCS coordinate system for the beam coordinate z2.
        """
        point_aircraft = self.z2_2_point_aircraft(z2)
        point_predocs = transform_location_m(self.transformation_aircraft_2_predocs(z2), point_aircraft)
        return point_predocs

    def create_points_wing(self, z2_list: list[float]) -> list[Vector]:
        """
        The PreDoCS coordinate system class offers the possibility to create points
        in the wing coordinate system.

        Parameters
        ----------
        z2_list:
            z2 coordinates of the points

        Returns
        -------
        list[Vector]
            The points.
        """
        trsf = self.transformation_aircraft_2_wing
        return [transform_location_m(trsf, self.z2_2_point_aircraft(z2)) for z2 in z2_list]

    def create_drps_wing(self, z2_list: list[float]):
        """
        The PreDoCS coordinate system class offers the possibility to create dynamic reference points
        in the wing coordinate system.

        Parameters
        ----------
        z2_list:
            z2 coordinates of the points

        Returns
        -------
        DynamicReferencePoints
            The dynamic reference points.
        """
        # Create beam nodes
        num_points = len(z2_list)
        x = np.empty((num_points,))
        y = np.empty((num_points,))
        z = np.empty((num_points,))

        # get coords of each beam node
        for ii, point in enumerate(self.create_points_wing(z2_list)):
            x[ii] = point.x
            y[ii] = point.y
            z[ii] = point.z

        beam_nodes_global = DynamicReferencePoints(x, y, z)
        beam_nodes = beam_nodes_global.transform_reference_points(self.transformation_aircraft_2_wing)

        return beam_nodes

    def point_2_z2_aircraft(self, point: Vector, tolerance: float = 1e-5, return_none_if_not_on_beam: bool = False) -> float | None:
        """
        Returns the z2 parameter from a given point in the aircraft coordinate system.

        Parameters
        ----------
        point
            The point in aircraft coordinates.
        return_none_if_not_on_beam
            If True, None is returned, if the point is not in the area of the beam.
        """
        num_sections = len(self.section_directions)
        # intersection between beam node plane and load axis
        intersection_section = num_sections
        for j in range(num_sections):  # decide in which section the beam_node lies
            intersection_section -= 1
            section_idx = num_sections - 1 - j
            ref_point = self.section_origins[section_idx]
            ref_dir = self.section_directions[section_idx]
            if pt_is_in_plane_dir(ref_point, ref_dir, point):
                z2_section = np.dot(ref_dir, point - ref_point)
                if z2_section > self.section_lengths[section_idx] + tolerance:
                    if return_none_if_not_on_beam:
                        return None
                    else:
                        log.warning(
                            'Point is outside of the beam range (beyond tip): '
                            f'z2 = {self.beam_length - self.section_lengths[section_idx] + z2_section} > '
                            f'beam_length = {self.beam_length}'
                        )
                return z2_section + sum(self.section_lengths[i] for i in range(intersection_section))

        # Point is beyond root
        ref_point = self.section_origins[0]
        ref_dir = self.section_directions[0]
        z2_section = np.dot(ref_dir, point - ref_point)
        if z2_section < -tolerance:
            if return_none_if_not_on_beam:
                return None
            else:
                log.warning(f'Point is outside of the beam range (beyond root): z2 = {z2_section}')
        return z2_section

    def point_2_z2_wing(self, point: Vector, tolerance: float = 1e-5, return_none_if_not_on_beam: bool = False) -> float | None:
        """
        Returns the z2 beam parameter from a given point in the wing coordinate system.

        Parameters
        ----------
        point
            The point in the wing coordinate system.
        return_none_if_not_on_beam
            If True, None is returned, if the point is not in the area of the beam.
        """
        return self.point_2_z2_aircraft(
            transform_location_m(self.transformation_wing_2_aircraft, point),
            tolerance=tolerance,
            return_none_if_not_on_beam=return_none_if_not_on_beam,
        )

    def is_point_on_beam_axis_aircraft(self, point: Vector, tolerance: float = 1e-5) -> bool:
        """
        Checks if the given point in the global CPACS coordinate system lies on the beam axis with a given tolerance.
        """
        z2_point = self.point_2_z2_aircraft(point, tolerance, return_none_if_not_on_beam=True)
        if z2_point is None:
            return False
        else:
            point_proj = self.z2_2_point_aircraft(z2_point)
            dist = point.dist(point_proj)
            if dist > tolerance:
                return False
            else:
                return True

    def is_point_on_beam_axis_predocs(self, point: Vector, tolerance: float = 1e-5) -> bool:
        """
        Checks if the given point in the PreDoCS beam coordinate system lies on the beam axis with a given tolerance.
        """
        return self.is_point_on_beam_axis_aircraft(
            transform_location_m(self.transformation_wing_2_aircraft, point),
            tolerance=tolerance,
        )

    def get_section_parameter(self, z2):
        """
        Return the section parameter of the 1d z2-coordinate, which include the origin and direction of the section,
        in which z2 lies. Furthermore, the length from the origin to z2 within the section is given as z2_section

        Parameters
        ----------
        z2: float
            z2 coordinate

        Returns
        -------
        section_origin: Vector
            Origin point of the corresponding section
        section_dir: Vector
            Direction of the corresponding section
        z2_section: float
            Distance from the section_origin to the given z2 coordinate
        """
        section_dir = self.section_directions
        section_origin = self.section_origins

        num_section, z2_section = self.get_section(z2)

        return section_origin[num_section], section_dir[num_section], z2_section

    def get_section(self, z2):
        """
        This method returns the section and the correlated z2_section (section coordinate, beginning at the origin of
        the corresponding section) coordinate of the global 1d coordinate z2.

        Parameters
        ----------
        z2: float
            z2-coordinate

        Returns
        -------
        num_section: int
            indicates the number of the corresponding section, starting with 0
        z2_section: float
            Distance from the section origin to z2
        """
        section_origin = self.section_origins

        num_section = 0
        for ii in range(len(section_origin)-1):
            section_length = section_origin[ii].dist(section_origin[ii+1])
            if z2 > section_length:
                z2 -= section_length
                num_section += 1
            else:
                break

        z2_section = z2

        assert num_section <= self.num_of_sections, f'Section {z2} is not in the beam z2 range.'
        return num_section, z2_section

    @property
    def wing_reference_position(self):
        """Origin of the wing coordinate system in global coordinates"""
        return self._wing_reference_position

    @property
    def wing_reference_direction(self):
        """Beam axis of the wing coordinate system in global coordinates"""
        return self._wing_reference_direction

    @property
    def up_dir_aircraft(self) -> Vector:
        """Up direction in the aircraft coordinate system."""
        return transform_direction_m(self.transformation_wing_2_aircraft, Vector([0, 1.0, 0])).normalised

    @property
    def beam_length(self):
        """The length of the PreDoCS beam"""
        return self._beam_length

    @property
    def beam_start(self):
        """The starting point of the PreDoCS beam in global coordinates"""
        return self._beam_start

    @property
    def beam_end(self):
        """The end point of the PreDoCS beam in global coordinates"""
        return self._beam_end

    def _get_transformation_function_aircraft_2_predocs(self, component_segment: 'ComponentSegment', num_points_per_segment: int) -> Callable:
        """
        Returns a function of the beam coordinate z2 that returns the transformation matrix
        from the aircraft to the PreDoCS cross-section coordinate system.
        """
        beam_reference_points = self.section_origins
        section_interpol_functions = []
        num_nodes = len(beam_reference_points)
        z2_start_section = 0.0
        for i in range(num_nodes):
            z2_sections = []
            matrices = []
            section_dir = self.section_directions[i].normalised
            section_length = self.section_lengths[i]
            for z2_section in np.linspace(0, section_length, num_points_per_segment):
                origin = beam_reference_points[i] + z2_section * section_dir
                z2 = z2_start_section + z2_section
                z2_norm = z2 / self._beam_length
                assert 0 <= z2_norm <= 1

                if self._x_axis_definition == 'old':
                    matrix = create_transformation_matrix_aircraft_2_predocs_old(origin, section_dir)
                elif self._x_axis_definition == 'new':
                    trsf = create_transformation_aircraft_2_predocs_new(
                        origin, section_dir,
                    )

                    # Twist and mold angle correction
                    mold_angle_transformation = gp_Trsf()
                    if self._mold_angle is not None:
                        log.debug('Mold angle correction')
                        mold_angle_rotation_ax = gp_Ax1(gp_Pnt(), gp_Dir(0, 1, 0))
                        mold_angle_transformation.SetRotation(mold_angle_rotation_ax, np.deg2rad(-self._mold_angle))

                    pretwist_transformation = gp_Trsf()
                    if self._twist_func is not None:
                        pretwist_rotation_ax = gp_Ax1(gp_Pnt(), gp_Dir(0, 0, 1))
                        pretwist_transformation.SetRotation(pretwist_rotation_ax, float(np.deg2rad(self._twist_func(z2_norm))))

                    matrix = transformation_occ_2_matrix(
                        pretwist_transformation * trsf * mold_angle_transformation
                    )

                elif self._x_axis_definition == 'beam_cosy':
                    eta, _ = get_eta_xsi(component_segment, origin)
                    chord_dir = (get_point_from_eta_xsi(component_segment, eta, 1) - get_point_from_eta_xsi(component_segment, eta, 0)).normalised

                    matrix = transformation_occ_2_matrix(create_transformation_aircraft_2_predocs_beam_cosy(
                        origin, section_dir, chord_dir,
                    ))
                else:
                    raise RuntimeError(f'Unknown x_axis_definition "{self._x_axis_definition}".')
                z2_sections.append(z2_section)
                matrices.append(matrix)

            z2_start_section += section_length

            interpol_func = get_matrix_interpolation_function(z2_sections, matrices, kind='linear', fill_value=None)
            section_interpol_functions.append(interpol_func)

        def predocs_beam_coordinate_system_function(z2: float, section_interpol_functions=section_interpol_functions) -> np.ndarray:
            i_section, z2_section = self.get_section(z2)
            length_section = self.section_lengths[i_section]
            assert 0 <= z2_section <= length_section
            interpol_func_ = section_interpol_functions[i_section]
            res = interpol_func_(z2_section)
            return res

        return predocs_beam_coordinate_system_function

    def transformation_aircraft_2_predocs(self, z2: float) -> np.ndarray:
        """
        The transformation matrix from aircraft to PreDoCS cross-section coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return self._transformation_func_aircraft_2_predocs(z2)

    def transformation_predocs_2_aircraft(self, z2: float) -> np.ndarray:
        """
        The transformation matrix from PreDoCS cross-section to aircraft coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return invert_transformation_matrix(self._transformation_func_aircraft_2_predocs(z2))

    @property
    def transformation_aircraft_2_wing(self) -> np.ndarray:
        """
        The transformation matrix from aircraft to wing coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return self._transformation_aircraft_2_wing

    @property
    def transformation_wing_2_aircraft(self) -> np.ndarray:
        """
        The transformation matrix from wing to aircraft coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return self._transformation_wing_2_aircraft

    def transformation_wing_2_predocs(self, z2: float) -> np.ndarray:
        """
        The transformation matrix from wing to PreDoCS cross-section coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return self._transformation_func_aircraft_2_predocs(z2) @ self.transformation_wing_2_aircraft

    def transformation_predocs_2_wing(self, z2: float) -> np.ndarray:
        """
        The transformation matrix from PreDoCS cross-section to wing coordinate system.

        Return
        ------
        np.ndarray
            Transformation matrix.
        """
        return self.transformation_aircraft_2_wing @ invert_transformation_matrix(self._transformation_func_aircraft_2_predocs(z2))

    @property
    def beam_nodes(self):
        return self._beam_nodes

    @property
    def cross_section_origins(self):
        return self._cross_section_origins

    @property
    def z2_cs(self):
        return self._z2_cs

    @property
    def z2_bn(self):
        return self._z2_bn

    @property
    def num_of_sections(self):
        return self._num_of_sections

    @property
    def section_lengths(self):
        return self._section_lengths

    @property
    def section_directions(self):
        return self._section_directions

    @property
    def section_origins(self):
        return self._section_origins

    @property
    def beam_nodes_normal_direction(self):
        """
        Normal direction of each beam node. Nodes directly on a kink get the normal direction of the previous section

        In PreDoCS CS, such that the direction for the first node is [0, 0, 1].
        """
        if self._beam_nodes_normal_direction is None:
            z2_bn = self._z2_bn

            transformation_matrix = self.transformation_aircraft_2_wing

            normal_dir = []
            for z2_bn_i in z2_bn:
                section_origin, section_dir, z2_section = self.get_section_parameter(z2_bn_i)

                normal_dir.append(transform_direction_m(transformation_matrix, section_dir))

            self._beam_nodes_normal_direction = normal_dir

        return self._beam_nodes_normal_direction

    @property
    def cross_sections_normal_direction(self):
        """
        Normal direction of each cross section.

        In PreDoCS CS, such that the direction for the first node is [0, 0, 1].
        """
        if self._cross_sections_normal_direction is None:
            z2_cs = self._z2_cs

            transformation_matrix = self.transformation_aircraft_2_wing

            normal_dir = []
            for z2_cs_i in z2_cs:
                section_origin, section_dir, z2_section = self.get_section_parameter(z2_cs_i)

                normal_dir.append(transform_direction_m(transformation_matrix, section_dir))

            self._cross_sections_normal_direction = normal_dir

        return self._cross_sections_normal_direction
