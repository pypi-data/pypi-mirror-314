"""
This module contains geometry helping functions.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2023 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.geometry import *
except ImportError:
    log.info('Modul cpacs_interface.utils.geometry not found. Use PreDoCS geometry utils class.')

    import numpy as np
    from OCC.Core import gp
    from OCC.Core.gp import gp_Ax3, gp_Trsf, gp_Ax2
    from numpy import cos, sin, deg2rad
    from scipy.spatial.transform import Rotation as R

    from PreDoCS.util.occ import vector_to_point, vector_to_direction
    from PreDoCS.util.vector import Vector

    def two_d_rotation(angle: float) -> np.ndarray:
        c = cos(deg2rad(angle))
        s = sin(deg2rad(angle))
        rot_mat = np.array([[c, s],
                            [-s, c]])
        return rot_mat


    def transform_direction_m(augmented_transformation_matrix, vector):
        """
        Transformation of a direction vector with an augmented transformation matrix (only linear mapping, no translation).
        [https://en.wikipedia.org/wiki/Affine_transformation]

        Parameters
        ----------
        augmented_transformation_matrix: numpy.ndarray
            Augmented transformation matrix.
        vector: Vector
            Vector to transform.

        Returns
        -------
        Vector
            Transformed vector.
        """
        vector_length = vector.shape[0]
        transformation_matrix = augmented_transformation_matrix[0:vector_length, 0:vector_length]

        v = np.dot(transformation_matrix, vector)
        return Vector(v.flatten())


    def transform_location_m(augmented_transformation_matrix, vector):
        """
        Transformation of a location vector with an augmented transformation matrix.
        [https://en.wikipedia.org/wiki/Affine_transformation]

        Parameters
        ----------
        augmented_transformation_matrix: numpy.ndarray
            Augmented transformation matrix.
        vector: Vector
            Vector to transform.

        Returns
        -------
        Vector
            Transformed vector.
        """
        y_ = np.dot(augmented_transformation_matrix, np.append(vector, 1))
        return Vector(y_.flatten()[:-1])


    def transform_displacements_vectors(u: Vector, rot: Vector, transformation_matrix: np.ndarray) -> tuple[
        Vector, Vector]:
        """
        Transforms beam displacements into another coordinate system
        """
        u_new = transform_direction_m(transformation_matrix, u)
        rot_new = transform_direction_m(transformation_matrix, rot)
        return u_new, rot_new


    def transform_displacements_list(displacements: list[float], transformation_matrix: np.ndarray) -> list[float]:
        """
        Transforms beam displacements into another coordinate system

        Parameters
        ----------
        displacements
            List of displacements: ux, uy, uz, rotx, roty, rotz
        """
        u_new, rot_new = transform_displacements_vectors(Vector(displacements[0:3]), Vector(displacements[3:6]),
                                                         transformation_matrix)
        return list(u_new) + list(rot_new)


    def create_transformation_matrix_by_angles(translation, phi, theta, psi):
        """
        Create the 4x4 transformation matrix by a 3x1 translation vector and 3 angles in radians

        Parameters
        ----------
        translation: ndarray
            [[x, y, z]]
        phi: float
            rotation around x in radians
        theta: float
            rotation around y in radians
        psi: float
            rotation around x in radians

        Return
        ------
        T: ndarray
            4x4 affine transformation matrix
        """
        sin = np.sin(phi)
        cos = np.cos(phi)

        r1 = np.asarray([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])

        sin = np.sin(theta)
        cos = np.cos(theta)

        r2 = np.asarray([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])

        sin = np.sin(psi)
        cos = np.cos(psi)

        r3 = np.asarray([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

        r = r3 @ r2 @ r1

        T1 = np.concatenate([r, translation], axis=1)
        T = np.concatenate([T1, [[0, 0, 0, 1]]], axis=0)

        return T


    def create_rotation_matrix_from_directions(dir_1, dir_2):
        """
        Creates a rotation matrix between dir_1 and dir_2, that yield dir_1 = T * dir_2, where T is the rotation matrix

        Parameters
        ----------
        dir_1: Vector
            [x1, y1, z1]
        dir_2: Vector
            [x2, y2, z2]

        Return
        ------
        T: ndarray
            3x3 rotation matrix
        """

        dir_1 = dir_1.normalised
        dir_2 = dir_2.normalised

        # Calculate the rotation axis
        rot_axis = Vector(np.cross(dir_1, dir_2))
        rot_angle = np.arcsin(rot_axis.length)  # Angle from cross product of two vectors with length 1

        if rot_angle < 1e-10:  # No rotation needed, return identity matrix
            return np.identity(3)
        else:  # Euler axis
            rot_axis = rot_angle * rot_axis.normalised

            # get Rotation and return as matrix
            rotation = R.from_rotvec(rot_axis)

            return rotation.as_matrix()


    def create_transformation_matrix_2d(alpha=0., translation_vector=Vector([0., 0.]), scaling=1.):
        """
        Creates an augmented transformation matrix for a two-dimensional transformation.
        [https://en.wikipedia.org/wiki/Affine_transformation]

        Parameters
        ----------
        alpha: float (default: 0.)
            Rotation angle in the plane in RAD.
        translation_vector: Vector (default: Vector([0., 0.]))
            Translation vector in the plane.
        scaling: float (default: 1.)
            Scale factor.

        Returns
        -------
        numpy.ndarray
            Augmented transformation matrix.
        """
        scale = np.array([[scaling, 0, 0],
                          [0, scaling, 0],
                          [0, 0, 1]])
        translate = np.array([[1, 0, translation_vector.x],
                              [0, 1, translation_vector.y],
                              [0, 0, 1]])
        rotate = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                           [np.sin(alpha), np.cos(alpha), 0],
                           [0, 0, 1]])
        return translate @ rotate @ scale


    def invert_transformation_matrix(transformation_matrix):
        """
        Invert a given transformation matrix and return is. A rotary matrix is inverted if transposed.

        A Transformation matrix contains a rotary matrix and a translational part to convert between coordinate systems.
        The rotary matrix is the upper left 3x3 Matrix, were each column represents a base vector of the new coordinate
        system. The upper right 3x1 vector is the translational vector directing towards the origin of the original
        coordinate system from the perspective of the new coordinate system.

        Parameters
        ----------
        transformation_matrix: ndarray
            4x4 ndarray

        Return
        ------
        back_transformation_matrix: np.ndarray
            4x4 ndarray
        """
        # from numpy.linalg import inv
        # from cpacs_interface.utils.occ import transformation_occ_2_matrix, transformation_matrix_2_occ
        # trsf = transformation_matrix_2_occ(transformation_matrix)
        # trsf_inv = trsf.Inverted()
        # inv_mat = transformation_occ_2_matrix(trsf_inv)

        # Get rotary matrix
        transformation_rotary_matrix = transformation_matrix[0:3, 0:3]

        # Invert rotary matrix and translation vector
        back_transformation_matrix_rotary = transformation_rotary_matrix.transpose()
        # back_transformation_matrix_rotary = inv(transformation_rotary_matrix)

        # Get transformation vector and change direction (Points from one coordinate system origin to the other)
        transformation_translation_vector = transformation_matrix[0:3, 3]

        # Transform translation vector into PreDoCS coordinates (PreDoCS origin from global)
        back_transformation_translation_vector = - back_transformation_matrix_rotary @ transformation_translation_vector

        # Set inverted matrix together
        back_transformation_matrix = np.concatenate(
            [back_transformation_matrix_rotary, back_transformation_translation_vector.reshape(3, 1)], axis=1)
        back_transformation_matrix = np.concatenate([back_transformation_matrix, [[0, 0, 0, 1]]])

        # assert np.allclose(back_transformation_matrix, inv_mat)

        return back_transformation_matrix


    def create_transformation_matrix_aircraft_2_predocs_old(reference_point, reference_axis_z):
        """
        Returns the

        A Transformation matrix contains a rotary matrix and a translational part to convert between coordinate systems.
        The rotary matrix is the upper left 3x3 Matrix, were each column represents a base vector of the new coordinate
        system. The upper right 3x1 vector is the translational vector directing towards the origin of the original
        coordinate system from the perspective of the new coordinate system.

        The PreDoCS coordinate system is defined having its origin at the wing root, with the z-axis as wing axis. The
        x-axis is in the x-y-plane of the original coordinate system and perpendicular to the z-axis. The y axis is
        perpendicular to the x-axis and the y-axis in the sense of a right-handed coordinate system.

        The x-base-vector is therefore defined as the projection of the given z-base-vector into the original x-y-plane
        rotated by +90 degree.

        The y-base-vector is calculated as the negative cross-product of the x-base-vector and the z-base-vector

        Parameters
        ----------
        reference_point: Vector
            The origin for the PreDoCS coordinate system
        reference_axis_z: Vector
            The z axis of the PreDoCS coordinate system
        Return
        ------
        transformation_matrix: ndarray
            The transformation matrix
        """
        # Rotation angle = 90°
        alpha = np.pi / 2

        # Rotary matrix
        rotary_matrix = np.asarray([[np.cos(alpha), -np.sin(alpha)],
                                    [np.sin(alpha), np.cos(alpha)]])

        # Normalise reference axis z
        reference_axis_z = reference_axis_z.normalised

        # x reference axis
        axis_z = reference_axis_z[0:2]
        axis_x = np.dot(rotary_matrix, axis_z)
        reference_axis_x = Vector(np.concatenate([axis_x, [0]])).normalised

        # y reference axis is orthogonal to x and z axis. The sign is to achieve a rightful coordinate system
        reference_axis_y = - np.cross(reference_axis_x, reference_axis_z)
        assert np.allclose(np.cross(reference_axis_x, reference_axis_y),
                           reference_axis_z), 'Error creating PreDoCS coordinate system transformation'

        # 3D Rotary Matrix the columns of the rotary matrix are the base vectors of the new coordinate system
        rotary_matrix_3d = np.concatenate([[reference_axis_x], [reference_axis_y], [reference_axis_z]])

        # Translational vector in predocs coordinate system
        global_origin_from_predocs = -np.dot(rotary_matrix_3d, reference_point)

        # Affine Transformation
        transformation_matrix = np.concatenate(
            [rotary_matrix_3d, np.asanyarray([global_origin_from_predocs]).transpose()], axis=1)
        transformation_matrix = np.concatenate([transformation_matrix, [[0, 0, 0, 1]]])

        return transformation_matrix


    def create_transformation_aircraft_2_predocs_new(
            reference_position: Vector, reference_direction: Vector,
    ) -> gp_Trsf:
        """
        Transformation from the global aircraft COSY to the PreDoCS cross-section COSY (z-axis is beam axis)
        at a given point on the reference axis.

        * PreDoCS z-axis equals `reference_direction`
        * PreDoCS y-axis is calculated by negative cross product of `reference_direction` and (1|0|0) (usually pointing upwards in PreDoCS cross-section).
        * PreDoCS x-axis is calculated by cross product of PreDoCS y-axis and `reference_direction` (usually pointing forward in PreDoCS cross-section).
        """
        aircraft_axis = gp.gp_XOY()

        ref_pos = vector_to_point(reference_position)
        ref_dir = vector_to_direction(reference_direction)
        chord_dir = vector_to_direction(Vector([1, 0, 0]))

        # Generate PreDoCS axes
        predocs_y_axis = -ref_dir.Crossed(chord_dir)
        predocs_x_axis = predocs_y_axis.Crossed(ref_dir)

        # PreDoCS COSY definition
        predocs_axis = gp_Ax2(ref_pos, ref_dir, predocs_x_axis)

        # Transformation
        aircraft_2_predocs_transformation = gp_Trsf()
        aircraft_2_predocs_transformation.SetTransformation(
            gp_Ax3(aircraft_axis),
            gp_Ax3(predocs_axis),
        )

        return aircraft_2_predocs_transformation


    def create_beam_cosy_Ax3(
            reference_position: Vector, reference_direction: Vector, chord_direction: Vector,
    ) -> gp_Ax3:
        """
        Returns the PreDoCS cross-section COSY (z-axis is beam axis, beam_cosy convention)
        at a given point on the reference axis.

        * PreDoCS z-axis equals `reference_direction`
        * PreDoCS y-axis is calculated by cross product of `reference_direction` and `chord_direction` (usually pointing downwards in PreDoCS cross-section).
        * PreDoCS x-axis is calculated by cross product of PreDoCS y-axis and `reference_direction` (usually pointing backward in PreDoCS cross-section).
        """
        ref_pos = vector_to_point(reference_position)
        ref_dir = vector_to_direction(reference_direction)  # a1
        chord_dir = vector_to_direction(chord_direction)

        # Generate PreDoCS axes
        predocs_y_axis = ref_dir.Crossed(chord_dir)  # a3
        predocs_x_axis = predocs_y_axis.Crossed(ref_dir)  # a2

        # PreDoCS COSY definition
        predocs_axis = gp_Ax2(ref_pos, ref_dir, predocs_x_axis)
        return gp_Ax3(predocs_axis)


    def create_transformation_aircraft_2_predocs_beam_cosy(
            reference_position: Vector, reference_direction: Vector, chord_direction: Vector,
    ) -> gp_Trsf:
        """
        Transformation from the global aircraft COSY to the PreDoCS cross-section COSY (z-axis is beam axis, beam_cosy convention)
        at a given point on the reference axis.

        * PreDoCS z-axis equals `reference_direction`
        * PreDoCS y-axis is calculated by cross product of `reference_direction` and `chord_direction` (usually pointing downwards in PreDoCS cross-section).
        * PreDoCS x-axis is calculated by cross product of PreDoCS y-axis and `reference_direction` (usually pointing backward in PreDoCS cross-section).
        """
        aircraft_axis = gp_Ax3(gp.gp_XOY())

        # PreDoCS COSY definition
        predocs_axis = create_beam_cosy_Ax3(reference_position, reference_direction, chord_direction)

        # Transformation
        aircraft_2_predocs_transformation = gp_Trsf()
        aircraft_2_predocs_transformation.SetTransformation(
            aircraft_axis,
            predocs_axis,
        )

        return aircraft_2_predocs_transformation


    def one_minus_cosine_spacing(num_points: int) -> np.ndarray:
        """Returns a (1 - cos)-spacing."""
        return (1 - np.cos(np.linspace(0, np.pi, num_points))) / 2


    def rdp(points, epsilon):
        """
        Implementation of the Ramer–Douglas–Peucker algorithm
        (https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm).

        Source: https://towardsdatascience.com/simplify-polylines-with-the-douglas-peucker-algorithm-ac8ed487a4a1

        Parameters
        ----------
        points
        epsilon

        Returns
        -------

        """
        # get the start and end points
        start = np.tile(np.expand_dims(points[0], axis=0), (points.shape[0], 1))
        end = np.tile(np.expand_dims(points[-1], axis=0), (points.shape[0], 1))

        # find distance from other_points to line formed by start and end
        dist_point_to_line = np.abs(np.cross(end - start, points - start, axis=-1)) / np.linalg.norm(end - start,
                                                                                                     axis=-1)
        # get the index of the points with the largest distance
        max_idx = np.argmax(dist_point_to_line)
        max_value = dist_point_to_line[max_idx]

        result = []
        if max_value > epsilon:
            partial_results_left = rdp(points[:max_idx + 1], epsilon)
            result += [list(i) for i in partial_results_left if list(i) not in result]
            partial_results_right = rdp(points[max_idx:], epsilon)
            result += [list(i) for i in partial_results_right if list(i) not in result]
        else:
            result += [points[0], points[-1]]

        return result
