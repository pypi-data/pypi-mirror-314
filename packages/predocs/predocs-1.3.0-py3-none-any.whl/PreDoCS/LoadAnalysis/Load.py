"""
This module contains classes and methods to store and transform loads used in PreDoCS for stress/strain calculations

Classes
-------
LoadCase:
    stores load vectors for each degree of freedom and a set of load reference points.
DynamicReferencePoints:
    stores positioning vectors for each degree of freedom where loads can be applied.

.. codeauthor:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import matplotlib.pyplot as plt
import numpy as np

from PreDoCS.LoadAnalysis.Interfaces import ILoadCase, ILoadReferencePoints
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.globals import DuplicateFilter
from PreDoCS.util.inout import export_csv
from PreDoCS.util.util import create_moved_load_vector
from PreDoCS.util.geometry import transform_direction_m
from PreDoCS.util.data import interp1d
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


class LoadCase(ILoadCase):
    """
    Definition of a load case

    Attributes
    ----------
    _name: str
        Name/Code of the load case
    _fx: tuple(float)
        Load vector in global coordinate system
    _fy: tuple(float)
        Load vector in global coordinate system
    _fz: tuple(float)
        Load vector in global coordinate system
    _mx: tuple(float)
        Moment vector in global coordinate system
    _my: tuple(float)
        Moment vector in global coordinate system
    _mz: tuple(float)
        Moment vector in global coordinate system
    _load_reference_points: DynamicReferencePoints
        Load reference points for the load case
    """

    def __init__(self, name, fx, fy, fz, mx, my, mz, load_reference_points, internal_loads):
        """
        Class initialisation

        Parameters
        ----------
        name: str
            Name/Code of the load case
        fx: ndarray
            Load vector in global coordinate system
        fy: ndarray
            Load vector in global coordinate system
        fz: ndarray
            Load vector in global coordinate system
        mx: ndarray
            Moment vector in global coordinate system
        my: ndarray
            Moment vector in global coordinate system
        mz: ndarray
            Moment vector in global coordinate system
        load_reference_points: DynamicReferencePoints
            Load reference points for the load case
        internal_loads: bool
            True if the loads are cut loads, False if the loads are nodal loads
        """
        # Check for nan values
        assert (not np.any(np.isnan(np.array([fx, fy, fz, mx, my, mz])))), 'Loads must not contain nan.'
        self._name = name
        self._fx = np.asarray(fx)
        self._fy = np.asarray(fy)
        self._fz = np.asarray(fz)
        self._mx = np.asarray(mx)
        self._my = np.asarray(my)
        self._mz = np.asarray(mz)
        self._length = len(self._fx)
        self._load_reference_points = load_reference_points
        self._internal_loads = internal_loads

    def plot_load_case3D(self, title=None):
        """Generates a 3D plot of a load case, showing the resulting loads on the load reference points"""

        # Load reference points
        x = self.load_reference_points.x
        y = self.load_reference_points.y
        z = self.load_reference_points.z

        # Figure
        fig = plt.figure(figsize=(10, 4))

        # Forces
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.scatter(x, y, z, c='r', marker='o')
        ax1.quiver(x, y, z, self.fx/5000.0, self.fy/5000.0, self.fz/5000.0)
        ax1.set_xlim([20, 40])
        ax1.set_ylim([0, 30])
        ax1.set_zlim([-10, 20])
        ax1.view_init(30, -45)
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax1.set_zlabel('Z axis')
        ax1.set_title('Load Case: {}'.format(self.name))
        #ax1.set_aspect('equal')

        # Moments
        ax2 = fig.add_subplot(122, projection='3d')
        ax2.scatter(x, y, z, c='r', marker='o')
        ax2.quiver(x, y, z, self.mx / 5000.0, self.my / 5000.0, self.mz / 5000.0)
        ax2.set_xlim([20, 40])
        ax2.set_ylim([0, 30])
        ax2.set_zlim([-10, 20])
        ax2.view_init(60, -45)
        ax2.set_xlabel('X axis')
        ax2.set_ylabel('Y axis')
        ax2.set_zlabel('Z axis')
        #ax2.set_aspect('equal')

        if title:
            fig.suptitle(title)

        return fig

    def plot_load_case2D(self, title=None):
        """Generates a 2D plot of a load case, showing each load vector versus wing coordinate eta"""
        eta = self.load_reference_points.eta

        # Figure
        fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(12, 12))

        # Set figure intervall
        eta_start = np.floor(eta[0] - 2)
        eta_end = np.ceil(eta[-1] + 2)
        eta_lim = (eta_start, eta_end)

        # Forces - upper line
        ax1 = ax[0, 0]
        ax1.plot(eta, self.fx, '-rs')
        ax1.grid(True)
        ax1.set(xlabel='eta', ylabel='FX', xlim=eta_lim)

        ax2 = ax[0, 1]
        ax2.plot(eta, self.fy, '-rs')
        ax2.grid(True)
        ax2.set(xlabel='eta', ylabel='FY', title='Load Case: {}'.format(self.name))

        ax3 = ax[0, 2]
        ax3.plot(eta, self.fz, '-rs')
        ax3.grid(True)
        ax3.set(xlabel='eta', ylabel='FZ')

        # Moments - lower line
        ax4 = ax[1, 0]
        ax4.plot(eta, self.mx, '-bs')
        ax4.grid(True)
        ax4.set(ylabel='MX')

        ax5 = ax[1, 1]
        ax5.plot(eta, self.my, '-bs')
        ax5.grid(True)
        ax5.set(ylabel='MY')

        ax6 = ax[1, 2]
        ax6.plot(eta, self.mz, '-bs')
        ax6.grid(True)
        ax6.set(ylabel='MZ')

        if title:
            fig.suptitle(title)

        return fig

    def transformed_load_case(self, transformation_matrix, new_name: str = None) -> 'LoadCase':
        """
        Transforms the load case from one coordinate system to another coordinate system.

        Through this transformation only perspective is changed. No moving or interpolation of the loads is realised.

        Parameters
        ----------
        transformation_matrix: 4x4 array
            Upper left 3x3 matrix is the rotary matrix and
            the last column the translation vector for z2.
        new_name
            Name of the new load_case

        Returns
        -------
        LoadCase
            Load case in PreDoCS coordinate system with changed name.
        """
        transformed_load_reference_points = self.load_reference_points.transform_reference_points(transformation_matrix)

        rotary_matrix = transformation_matrix[0:3, 0:3]
        force_vector = np.concatenate([[self.fx], [self.fy], [self.fz]])
        moment_vector = np.concatenate([[self.mx], [self.my], [self.mz]])

        transformed_vf = np.dot(rotary_matrix, force_vector)
        transformed_vm = np.dot(rotary_matrix, moment_vector)

        return LoadCase(
            new_name if new_name else self.name,
            transformed_vf[0], transformed_vf[1], transformed_vf[2],
            transformed_vm[0], transformed_vm[1], transformed_vm[2],
            transformed_load_reference_points, self.internal_loads,
        )

    def moved_load_case(self, load_reference_points_new: 'DynamicReferencePoints', new_name: str = None) -> 'LoadCase':
        """
        Loads are moved to the new load reference points. The moved forces resulting in changed moments.

        Parameters
        ----------
        load_reference_points_new: DynamicReferencePoints
            Points on the cross sections were loads need to be applied.
        new_name
            Name of the new load_case

        Returns
        -------
        LoadCase
            Load case in PreDoCS coordinate system with loads at the application points.
        """
        # Move loads
        force_vector_new = []
        moment_vector_new = []
        for va, vn, fa, ma in zip(
                self.load_reference_points.point_list, load_reference_points_new.point_list,
                self.force_vec, self.moment_vec
        ):
            fn, mn = create_moved_load_vector(va, vn, fa, ma)
            force_vector_new.append(fn)
            moment_vector_new.append(mn)
        fv = np.asarray(force_vector_new)
        mv = np.asarray(moment_vector_new)

        return LoadCase(
            new_name if new_name else self.name,
            fv[:, 0], fv[:, 1], fv[:, 2],
            mv[:, 0], mv[:, 1], mv[:, 2],
            load_reference_points_new, self.internal_loads,
        )

    def interpolated_loadcase_internal(
            self,
            predocs_coord: 'PreDoCSCoord',
            z2_old: list[float],
            z2_new: list[float],
            interpolation_method='linear',
            new_name: str = None,
    ) -> 'LoadCase':
        """
        Interpolate load case loads on the same load reference axis. Extrapolation is possible.

        Parameters
        ----------
        z2_old
            The given spanwise positions of the loads.
        z2_new
            The new spanwise positions of the loads.
        interpolation_method: str (default: 'linear')
            scipy.interpolate.interp1d interpolation method for the interpolation. Only used for internal loads.
        new_name
            Name of the new load_case

        Returns
        -------
        LoadCase
            Load case with interpolated loads.
        """
        fx = self._interpolate_internal_loads(z2_new, z2_old, self.fx, interpolation_method)
        fy = self._interpolate_internal_loads(z2_new, z2_old, self.fy, interpolation_method)
        fz = self._interpolate_internal_loads(z2_new, z2_old, self.fz, interpolation_method)
        mx = self._interpolate_internal_loads(z2_new, z2_old, self.mx, interpolation_method)
        my = self._interpolate_internal_loads(z2_new, z2_old, self.my, interpolation_method)
        mz = self._interpolate_internal_loads(z2_new, z2_old, self.mz, interpolation_method)

        lrp_new = DynamicReferencePoints.from_vector_list([predocs_coord.z2_2_point_wing(z2) for z2 in z2_new])
        return LoadCase(
            new_name if new_name else self.name,
            fx, fy, fz, mx, my, mz,
            lrp_new, self.internal_loads,
        )

    def interpolated_loadcase_external(self, predocs_coord: 'PreDoCSCoord', new_name: str = None) -> 'LoadCase':
        """
        Interpolate load case loads on the same load reference axis. Extrapolation is possible.

        The method interpolate_loadcase interpolates nodal loads given at self.load_reference_points and calculates
        nodal loads at given beam_nodes. The interpolation algorithm interpolates the nodal loads in between the first
        and the last self.load_reference_points. Beam nodes outside the interval [load_reference_points[0],
        load_reference_points[-1]] are given a zero load vector. For the interpolation the last section, where the
        point lies in positive direction is used. If there is no corresponding section found, the first is used.

        Parameters
        ----------
        beam_nodes: DynamicReferencePoints
            Are used to determine the plane, to which the loads are interpolated.
        beam_nodes_normal_direction: list(Vector)
            Normal direction for each beam node
        interpolation_method: str (default: 'linear')
            scipy.interpolate.interp1d interpolation method for the interpolation. Only used for internal loads.
        new_name
            Name of the new load_case

        Returns
        -------
        LoadCase
            Load case with interpolated loads.
        """
        beam_nodes_drps = predocs_coord.create_drps_wing(predocs_coord.z2_bn)
        lrp = self.load_reference_points

        # Check if load axis coincides with the beam axis
        for point in lrp.point_list:
            assert predocs_coord.is_point_on_beam_axis_predocs(point), 'All external load points have to lie on the beam axis.'

        straight_beam = np.allclose(beam_nodes_drps.x - np.mean(beam_nodes_drps.x), 0) and np.allclose(beam_nodes_drps.y - np.mean(beam_nodes_drps.y), 0)
        straight_lra = np.allclose(lrp.x - np.mean(lrp.x), 0) and np.allclose(lrp.y - np.mean(lrp.y), 0)

        z = predocs_coord.z2_bn

        if straight_beam and straight_lra:
            # Straight beam and straight load reference axis
            zp = lrp.z
        else:
            # Kinked beam
            def drp_to_z2(drp) -> list[float]:
                z2_list = []
                for i, point in enumerate(drp.point_list):
                    z2 = predocs_coord.point_2_z2_wing(point, return_none_if_not_on_beam=True)
                    assert z2 is not None, f'Can not interpolate external load, because {point} is not defined on the beam.'
                    # section_idx, z2_section = predocs_coord.get_section(z2)
                    # lrp_section_info.append((section_idx, z2_section))
                    z2_list.append(z2)
                return z2_list
            zp = drp_to_z2(lrp)

        # z1...zn determine for beam nodes
        z_diff = np.mean(np.diff(z))
        z = np.concatenate([[z[0] - z_diff / 2], z + z_diff / 2])
        z = z.reshape([len(z), 1])

        # z1*...zn* determine for load reference points
        zp_diff = np.mean(np.diff(zp))
        zp = np.concatenate([[zp[0] - zp_diff / 2], zp + zp_diff / 2])
        zp = zp.reshape([len(zp), 1])

        # Interpolation function
        # TODO check if it works with scipy interpolation nearest extrapolate with value 0
        # TODO create distributed loads --> interpolate --> sum up
        fx = self._interpolate_external_loads(z, zp, self.fx)
        fy = self._interpolate_external_loads(z, zp, self.fy)
        fz = self._interpolate_external_loads(z, zp, self.fz)
        mx = self._interpolate_external_loads(z, zp, self.mx)
        my = self._interpolate_external_loads(z, zp, self.my)
        mz = self._interpolate_external_loads(z, zp, self.mz)

        return LoadCase(new_name if new_name else self.name, fx, fy, fz, mx, my, mz, beam_nodes_drps, self.internal_loads)

    @staticmethod
    def _interpolate_external_loads(z, zp, fp):
        """
        Interpolate loads without changing the total sum.

        Parameters
        ----------
        z: ndarray
            The z-coordinates at which the loads are calculated
        zp: ndarray
            The z-coordinates at which the loads are given
        fp: ndarray
            The Loads

        Returns
        -------
        f_vec: ndarray
            The interpolated loads
        """
        # join z coordinates
        z_ges = np.concatenate([z, zp])
        z_ges = np.sort(z_ges, axis=0)
        z_ges = np.unique(z_ges, axis=0)

        # Determine size of transformation matrix
        # Number of interpolation points in front of the first given point zp
        size1 = np.sum(z < zp[0])

        # Maximum number of interpolation points between two given points zp
        size2 = 0
        for i_zp in range(len(zp)-1):
            size2_int = np.sum((zp[i_zp] < z_ges) * (z_ges <= zp[i_zp + 1]))
            if size2_int > size2:
                size2 = size2_int

        # Number of interpolation points behind the last given point zp
        size3 = np.sum(z > zp[-1])

        # Size of the Transformation Matrix
        size_transformation_matrix = np.max([size2+size1, size2+size3])

        # Define transformation matrix to distribute loads on z_ges
        loadfactor_size = [len(zp) - 1, size_transformation_matrix]
        loadfactor = np.zeros(loadfactor_size)
        for i_zp in range(len(zp) - 1):
            z_ges_in_zp = z_ges[(zp[i_zp] <= z_ges) * (z_ges <= zp[i_zp + 1])]
            factor = np.diff(z_ges_in_zp) / np.diff(np.concatenate([zp[i_zp], zp[i_zp + 1]]))
            while factor.size < size_transformation_matrix:
                factor = np.concatenate([factor, [np.nan]])
            loadfactor[i_zp] = factor

        # Add zero loads at points z in zges which are outside the intervall zp1...zpn
        if z[0] < zp[0]:
            # Add zero loads where z<zp[0]
            factor = loadfactor[0][~np.isnan(loadfactor[0])]
            factor = np.append(np.zeros([1, size1]), factor)
            while factor.size < size_transformation_matrix:
                factor = np.concatenate([factor, [np.nan]])
            loadfactor[0] = factor

        if zp[-1] < z[-1]:
            # Add zero loads where z>zp[-1]
            factor = loadfactor[-1][~np.isnan(loadfactor[-1])]
            factor = np.append(factor, np.zeros([1, size3]))
            while factor.size < size_transformation_matrix:
                factor = np.concatenate([factor, [np.nan]])
            loadfactor[-1] = factor

        # Distribute loads on z_ges
        f_ges = np.multiply(fp.reshape([len(fp), 1]), loadfactor)
        f_ges = f_ges[~np.isnan(f_ges)].flatten()

        if 0:
            assert np.isclose(sum(fp), sum(f_ges))

        # Sum up loads on z
        f_vec = np.zeros([len(z) - 1, 1])
        for i_z in range(len(z) - 1):
            # values of z_ges in front of the second point of z summed at the interval z0-z1 (z1 = second point).
            if i_z == 0:
                z_in_zges = (z_ges <= z[i_z + 1])
                z_in_zges = z_in_zges.reshape([len(z_in_zges), 1])
            # if z_in_zges between 2 values
            elif i_z < len(z) - 2:
                z_in_zges = (z[i_z] <= z_ges) * (z_ges <= z[i_z + 1])
                z_in_zges = z_in_zges.reshape([len(z_in_zges), 1])
            # if last values
            else:
                z_in_zges = (z[i_z] <= z_ges)
                z_in_zges = z_in_zges.reshape([len(z_in_zges), 1])

            # Get index of the True intervals
            f_int_idx = np.multiply(z_in_zges[1:], z_in_zges[0:-1])
            f_int_idx = f_int_idx.flatten()
            f_vec[i_z] = np.sum(f_ges[f_int_idx])

        f_vec = f_vec.flatten()

        return f_vec

    @staticmethod
    def _interpolate_internal_loads(z2, z2p, fp, interpolation_method):
        """
        Interpolate internal loads (changing the total sum).

        Parameters
        ----------
        z2: ndarray
            The z-coordinates at which the internal loads are calculated
        z2p: ndarray
            The z-coordinates at which the internal loads are given
        fp: ndarray
            The internal loads
        interpolation_method: str
            scipy.interpolate.interp1d interpolation method for the interpolation.

        Returns
        -------
        ndarray
            The interpolated internal loads
        """
        f_func = interp1d(
            z2p,
            fp,
            kind=interpolation_method,
            bounds_error=False,
            fill_value="extrapolate"
        )
        return f_func(z2).flatten()

    # def moved_loads_to_load_application_points(self, load_application_points, new_name: str = None):
    #     """
    #     Loads are moved within the cross section plane from the load reference points to the load application points.
    #
    #     While the normal forces act at the origin of the PreDoCS beam coordinate system, the shear forces need to be
    #     applied to the pole (center of shear) of the cross section. For this reason the pole-positions on each cross
    #     section are extracted and saved into the load_application_points. In this method the normal forces are extracted
    #     from the force vector and replaced by zeros. The resulting vector then is moved to the load application points,
    #     with respect to the resulting change in moment. Afterwards the original normal forces are assimilated into the
    #     force vector again. For the moments no transformation is needed since moments are constant within a cross section.
    #
    #     Parameters
    #     ----------
    #     load_application_points: DynamicReferencePoints
    #         Points on the cross sections were loads need to be applied.
    #     new_name
    #         Name of the new load_case
    #
    #     Returns
    #     -------
    #     LoadCase
    #         Load case in PreDoCS coordinate system with loads at the application points.
    #     """
    #     # Get old and new load reference points
    #     load_positions_new = load_application_points.point_list
    #     load_positions_old = self.load_reference_points.point_list
    #
    #     # Extract normal forces from force vector to avoid moments from normal forces (pop)
    #     force_vector_old = self.force_vec
    #     normal_forces = np.copy(force_vector_old[:, 2])
    #     force_vector_old[:, 2] = 0
    #
    #     # Get moment vector
    #     moment_vector_old = self.moment_vec
    #
    #     # Move loads
    #     force_vector_new = []
    #     moment_vector_new = []
    #     for va, vn, fa, ma in zip(load_positions_old, load_positions_new, force_vector_old, moment_vector_old):
    #         fn, mn = create_moved_load_vector(va, vn, fa, ma)
    #         force_vector_new.append(fn)
    #         moment_vector_new.append(mn)
    #
    #     # Reintegrate normal forces
    #     fv = np.asarray(force_vector_new)
    #     fv[:, 2] = normal_forces
    #
    #     mv = np.asarray(moment_vector_new)
    #
    #     # Create nodal loads
    #     beam_nodal_loads = LoadCase(new_name if new_name else self.name,
    #                                 fv[:, 0], fv[:, 1], fv[:, 2], mv[:, 0], mv[:, 1], mv[:, 2],
    #                                 load_application_points, self.internal_loads)
    #
    #     return beam_nodal_loads

    def transformed_loads_to_local_loads(self, z2, transformation_wing_2_aircraft, transformation_aircraft_2_predocs, new_name: str = None) -> 'LoadCase':
        """
        Loads of one cross-section are rotated to fit the local, kinked, PreDoCS system.

        Parameters
        ----------
        z2: list(float)
            z2 coordinate of the load points.
        transformation_predocs_beam_2_cpacs
            Transformation to global CPACS coordinate system.
        transformation_cpacs_2_predocs_cs
            Returns the local transformation matrix from CPACS to PreDoCS for a given z2.
        new_name
            Name of the new load_case

        Returns
        -------
        LoadCase
            Load case in PreDoCS coordinate system with loads in local coordinate system.
        """
        force_vec_new = []
        moment_vec_new = []
        for z2_i, force_i, moment_i in zip(z2, self.force_vec, self.moment_vec):
            force_vec_cpacs = transform_direction_m(transformation_wing_2_aircraft, force_i)
            moment_vec_cpacs = transform_direction_m(transformation_wing_2_aircraft, moment_i)

            force_vec_new.append(transform_direction_m(transformation_aircraft_2_predocs(z2_i), force_vec_cpacs))
            moment_vec_new.append(transform_direction_m(transformation_aircraft_2_predocs(z2_i), moment_vec_cpacs))

        fv = np.asarray(force_vec_new)
        mv = np.asarray(moment_vec_new)

        # Create nodal loads
        beam_nodal_loads = LoadCase(new_name if new_name else self.name,
                                    fv[:, 0], fv[:, 1], fv[:, 2], mv[:, 0], mv[:, 1], mv[:, 2],
                                    self.load_reference_points, self.internal_loads)

        return beam_nodal_loads

    def sorted_by_degree_of_freedom(self) -> 'LoadCase':
        """
        This method returns loads in a format needed by Beam.get_load_vector for FEM calculations

        The format is a list of tuple, were each tuple contains a beam node index, a load direction described as degree
        of freedom and the according load. The beam nodes are in a range [0..n], the dof in a range [0...5] representing
        the loads (fx, fy, fz, mx, my, mz).

        Returns
        -------
        load_dof_list: List
            [(beam_node, dof, load), (beam_node, dof, load)...]
        """
        # Generate matrix containing loads for all 6 DOF
        load_matrix = np.concatenate([self.force_vec, self.moment_vec], axis=1)

        load_dof_list = []
        for i_node in range(load_matrix.shape[0]):
            for i_load in range(load_matrix.shape[1]):
                load_dof_list.append((i_node, i_load, load_matrix[i_node, i_load]))

        return load_dof_list

    @staticmethod
    def plot_load_redistribution(loadcase, loadcase_interp, load_key='fx', export=False, path='', title=None):
        """
        Generates a 2D plot showing the redistribution of fz

        Parameters
        ----------
        loadcase: LoadCase or LoadCaseInterp
            Original Load Case
        loadcase_interp: LoadCaseInterp
            Load Case for comparison
        """
        # Data from original loadcase
        z = loadcase.load_reference_points.z
        eta_diff = loadcase.load_reference_points.eta_diff
        z_mid = z - eta_diff * 0.5
        z_mid = np.concatenate([z_mid, [z_mid[-1]+eta_diff[-1]]])
        f_orig = getattr(loadcase, load_key)
        n_z = f_orig / eta_diff
        n_z_mid = np.concatenate([n_z, [n_z[-1]]])

        # Data from interpolated loadcase
        z_int = loadcase_interp.load_reference_points.z
        eta_diff_int = loadcase_interp.load_reference_points.eta_diff
        z_mid_int = z_int - eta_diff_int * 0.5
        z_mid_int = np.concatenate([z_mid_int, [z_mid_int[-1]+eta_diff_int[-1]]])
        f_orig_int = getattr(loadcase_interp, load_key)
        n_z_int = f_orig_int / eta_diff_int
        n_z_mid_int = np.concatenate([n_z_int, [n_z_int[-1]]])

        # Set figure intervall
        z_start = np.floor(z[0] - 2)
        z_end = np.ceil(z[-1] + 2)

        # Figure
        fig, ax = plt.subplots(4, 1, sharey=True, figsize=(30, 20))

        # Forces - upper line
        ax1 = ax[0]
        ax1.plot(z, f_orig, 'rs')
        ax1.grid(True)
        ax1.set(xlabel='z', ylabel='F_z', xlim=(z_start, z_end), title='Load Case: {}'.format(loadcase.name))
        ax1.set_xticks(z, minor=False)

        ax2 = ax[1]
        ax2.bar(z, n_z, width=eta_diff[0], edgecolor='r', facecolor='None')
        ax2.set(xlabel='z', ylabel='n_z', xlim=(z_start, z_end))

        ax3 = ax[2]
        ax3.bar(z_int, n_z_int, width=eta_diff_int[0], edgecolor='b', facecolor='None')
        ax3.set(xlabel='z', ylabel='n_z', xlim=(z_start, z_end), title='Load Case: {}'.format(loadcase_interp.name))

        ax4 = ax[3]
        ax4.plot(z_int, f_orig_int, 'bs')
        ax4.grid(True)
        ax4.set(xlabel='z', ylabel='F_z', xlim=(z_start, z_end))
        ax4.set_xticks(z_int, minor=False)

        if title:
            fig.suptitle(title)

        if export:
            # Normalise loads by max load
            max_load = max(f_orig_int.max(), f_orig.max(), n_z_mid.max(), n_z_mid_int.max(), key=abs)
            if max_load == 0:
                # Prevent division by 0
                max_load = 1

            export_csv(z, f_orig/max_load, name='load_predocs_cord.csv', path=path)
            export_csv(z_mid, n_z_mid/max_load, name='distributed_load_predocs_cord.csv', path=path)
            export_csv(z_int, f_orig_int/max_load, name='interpolated_load_predocs_cord.csv', path=path)
            export_csv(z_mid_int, n_z_mid_int/max_load, name='interpolated_distributed_load_predocs_cord.csv', path=path)
            pass

        return fig

    @property
    def force_vec(self):
        """
        Returns force vectors as an array of type F = [fx, fy, fz] were f is the vector of all x forces...

        The Method returns forces as an array where each row represents one force vector. This matrix is
        especially useful for iterations over all forces.

        Returns
        -------
        force_vec : ndarray
            reference point coordinate matrix
        """
        force_vec = [[fx, fy, fz] for fx,fy,fz in zip(self.fx, self.fy, self.fz)]
        force_vec = np.asarray(force_vec)

        return force_vec

    @property
    def moment_vec(self):
        """
        Returns force vectors as an array of type F = [fx, fy, fz] were f is the vector of all x forces...

        The Method returns forces as an array where each row represents one force vector. This matrix is
        especially useful for iterations over all forces.

        Returns
        -------
        moment_vec: ndarray
            reference point coordinate matrix
        """
        moment_vec = [[mx, my, mz] for mx, my, mz in zip(self.mx, self.my, self.mz)]
        moment_vec = np.asarray(moment_vec)

        return moment_vec

    @property
    def name(self):
        return self._name

    @property
    def fx(self):
        return self._fx

    @property
    def fy(self):
        return self._fy

    @property
    def fz(self):
        return self._fz

    @property
    def mx(self):
        return self._mx

    @property
    def my(self):
        return self._my

    @property
    def mz(self):
        return self._mz

    @property
    def length(self):
        return self._length

    @property
    def load_reference_points(self):
        return self._load_reference_points

    @property
    def internal_loads(self):
        return self._internal_loads


class DynamicReferencePoints(ILoadReferencePoints):
    """
    Definition of dynamic reference points

    This class represents a set of points defined by there x, y, z coordinates in vectorized form. These reference
    points in three dimensional space can be used for example to define points of load application for nodal loads.
    Further the reference points may be used to define the axis of a beam model.

    Attributes
    ----------
    _x: ndarray
        Load reference points in global coordinate system
    _y: ndarray
        Load reference points in global coordinate system
    _z: ndarray
        Load reference points in global coordinate system
    """
    def __init__(self, x, y, z):
        """
        DynamicReferencePoints are initialised with a wing index and lists (vectors) of x-, y- and z-coordinates

        Parameters
        ----------
        x: tuple(float)
            Load reference points in global coordinate system
        y: tuple(float)
            Load reference points in global coordinate system
        z: tuple(float)
            Load reference points in global coordinate system
        """
        self._x = np.asarray(x)
        self._y = np.asarray(y)
        self._z = np.asarray(z)
        self._eta, self._eta_dist, self._wing_length = self._calc_eta()

    @staticmethod
    def from_vector_list(positions: list[Vector]) -> 'DynamicReferencePoints':
        return DynamicReferencePoints(
            [p.x for p in positions],
            [p.y for p in positions],
            [p.z for p in positions],
        )

    @DuplicateFilter(log)
    def _calc_eta(self):
        """
        Calculates eta: span-wise coordinate of the wing along the wing reference points.

        Returns
        -------
        eta: ndarray
            The coordinate along the wing axis
        eta_dist: ndarray
            The reference length for each reference point
        wing_length: scalar
            The wing length
        """
        x_diff = np.diff(self._x)
        y_diff = np.diff(self._y)
        z_diff = np.diff(self._z)

        # Finite differences in matrix form for norm evaluation
        vector_diff = np.concatenate([[x_diff], [y_diff], [z_diff]], axis=0)

        # Reference length for each force
        eta_dist = np.linalg.norm(vector_diff, axis=0)

        # Reference coordinates in eta are the cumulative sum of eta_diff
        eta = eta_dist.cumsum()
        eta = np.append(0, eta)

        # Add load reference length
        eta_dist = np.append(eta_dist, eta_dist.mean())

        wing_length = eta[-1]

        #assert all(z_diff<z_diff[0]+0.001) and all(z_diff>z_diff[0]-0.001),\
        #    'Dynamic reference z-coordinates are not equally distributed.'
        if not all(eta_dist<eta_dist[0]+0.001) and not all(eta_dist>eta_dist[0]-0.001):
            log.warning('Dynamic reference eta_l are not equally distributed.')

        return eta, eta_dist, wing_length

    @staticmethod
    def create_from_2points(p1, p2, num):
        """
        The Method create_from_2points creates a set of num load reference points starting from p1(x,y,z) to p2(x,y,z).

        The DynamicReferencePoint returned by this method are linear and equally distributed points between p1 and p2.
        The points p1 and p2 are included in the set.

        Parameters
        ----------
        p1: List(float, float, float)
            Starting point of the set
        p2: List(float, float, float)
            Ending point of the set
        num: int
            number of DynamicReferencePoints
        Returns
        -------
        DynamicReferencePoints
            New set of dynamic reference points created from two points
        """
        x = np.linspace(p1[0], p2[0], num)
        y = np.linspace(p1[1], p2[1], num)
        z = np.linspace(p1[2], p2[2], num)

        return DynamicReferencePoints(x, y, z)

    def transform_reference_points(self, transformation_matrix):
        """
        Transforms reference points from one coordinate system to another using a transformation_matrix.

        The Transformation includes rotation and translation. The Transformation is realised as a matrix multiplication.

        Parameters
        ----------
        transformation_matrix: ndarray
            4x4 array were the upper left 3x3 matrix is the rotary matrix and the last column the translation vector
        Returns
        -------
        transformed_reference_points: DynamicReferencePoints
            The set of dynamic reference points transformed in the new coordinate system.
        """
        reference_xyz = self.point_list
        xyz = np.concatenate([reference_xyz, np.ones([len(reference_xyz), 1])], axis=1).transpose()
        transformed_xyz = np.dot(transformation_matrix, xyz)

        x = transformed_xyz[0, :]
        y = transformed_xyz[1, :]
        z = transformed_xyz[2, :]

        transformed_reference_points = DynamicReferencePoints(x, y, z)

        return transformed_reference_points

    def get_reference_axis(self) -> (list[Vector], list[Vector]):
        """
        Creates reference points and reference axes vector directing from the point along the reference point axis.
        A new reference point and direction is created for each section, where the direction does not match the previous
        one.

        Returns
        -------
        reference_points: list(Vector)
            The origin of each section for the PreDoCS coordinate system
        reference_axes: list(Vector)
            The z axis of each section of the PreDoCS coordinate system
        """
        reference_points = []
        reference_axes = []
        for i, (x_i, y_i, z_i) in enumerate(zip(self.x[0:-1], self.y[0:-1], self.z[0:-1])): # iterate over all points
            p1 = np.asarray((x_i, y_i, z_i))
            p2 = np.asarray((self.x[i+1], self.y[i+1], self.z[i+1]))
            reference_point = Vector(p1)
            reference_axis = Vector(p2-p1).normalised

            if i == 0 or not np.allclose(reference_axes[-1], reference_axis, rtol=1e-3):
                # add new reference point and direction if it does not match previous one or is the first
                reference_points.append(reference_point)
                reference_axes.append(reference_axis)

        return reference_points, reference_axes

    @property
    def point_list(self):
        """
        Return coordinates as array of type M = [vx, vy, vz] were vx is the vector of all x coordinates...

        The Method returns the load reference points as an array where each row represents one point. This matrix is
        especially useful for iterations over all points.

        Returns
        -------
        reference_xyz: ndarray
            reference point coordinate matrix
        """
        reference_xyz = [[x, y, z] for x, y, z in zip(self.x, self.y, self.z)]
        reference_xyz = np.asarray(reference_xyz)

        return reference_xyz

    # @property
    # def z_list(self):
    #     """
    #     This Method returns the z-coordinates of the reference points as a copy of self.z in a ndarray
    #     """
    #     # Convert to list returns as COPY!!! of ndarray as a list. Therefore changing the z_cross_section does not
    #     # effect the reference points itself, which is important!
    #     _z_list = self.z.tolist()
    #     return _z_list

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def eta(self):
        return self._eta

    @property
    def eta_diff(self):
        return self._eta_dist

    @property
    def wing_length(self):
        return self._wing_length

    @property
    def size(self):
        return len(self.eta)
