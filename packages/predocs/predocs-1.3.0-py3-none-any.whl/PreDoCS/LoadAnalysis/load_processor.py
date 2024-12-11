"""
The Module load processor handles the transformation of imported loads into a load matrix for FEM calculations.

code author:: Hendrik Traub <Hendrik.Traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import os
import traceback

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull, QhullError

from PreDoCS.CrossSectionAnalysis.Display import _save_and_show
from PreDoCS.LoadAnalysis.Load import DynamicReferencePoints, LoadCase
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)


class LoadProcessor:
    """
    The load processor handles the transformation of imported loads into loads used by PreDoCS.

    The following steps need to be done for such an import:
    - Coordinate transformation: global CPACS --> PreDoCS beam
    - for internal loads:
        - move to beam axis
        - interpolate along beam axis
        - move to target points
        - Load moving: beam node cross section intersection --> beam node poles (here moments are adjusted to the moved forces)
        - Transform the load vectors to the cross section coordinate system orientation
    - for external loads:
        - Load Interpolation: load reference points --> beam node cross-section intersection (only not kinked beams)
        - Load moving: beam node cross section intersection --> beam node poles (here moments are adjusted to the moved forces)
        - Reformatting: beam node poles (DynamicReferencePoints) --> beam node poles (List(beam node, dof, load))

    """

    def __init__(self, loadcase_dict, predocs_coord, interpolation_method='linear'):
        """

        Parameters
        ----------
        loadcase_dict: dict
            Dictionary {'loadcase_name': LoadCase, ...}
        predocs_coord: PreDoCSCoord
            PreDoCS coordinate System
        interpolation_method: str (default: 'linear')
            scipy.interpolate.interp1d interpolation method for the interpolation. Only used for internal loads.
        """
        self.predocs_coord = predocs_coord

        load_case_dict_transformed = {}
        load_case_dict_interpolated_nodes = {}
        load_case_dict_interpolated_elements = {}
        for key, lc in loadcase_dict.items():
            # The Loads are transformed in the PreDoCS beam coordinate system with an affine transformation matrix
            lc_transformed = lc.transformed_load_case(
                predocs_coord.transformation_aircraft_2_wing, lc.name + '_PreDoCS_beam',
            )

            if lc.internal_loads:
                # Internal loads

                # Move loads to beam axis
                z2_old = [predocs_coord.point_2_z2_wing(lrp) for lrp in lc_transformed.load_reference_points.point_list]
                positions_old_on_beam = [predocs_coord.z2_2_point_wing(z2) for z2 in z2_old]
                lrp_on_beam = DynamicReferencePoints.from_vector_list(positions_old_on_beam)
                loads_on_beam = lc_transformed.moved_load_case(lrp_on_beam, lc.name + '_on_beam')

                # Internal loads at the node positions
                lc_interpolated_nodes = loads_on_beam.interpolated_loadcase_internal(
                    predocs_coord,
                    z2_old,
                    predocs_coord.z2_bn,
                    interpolation_method,
                    lc.name + '_interpolated',
                )
                load_case_dict_interpolated_nodes[key] = lc_interpolated_nodes

                # Internal loads at the element positions
                lc_interpolated_elements = loads_on_beam.interpolated_loadcase_internal(
                    predocs_coord,
                    z2_old,
                    predocs_coord.z2_cs,
                    interpolation_method,
                    lc.name + '_interpolated',
                )
                load_case_dict_interpolated_elements[key] = lc_interpolated_elements

            else:
                # External loads
                ref_points, ref_axis = lc_transformed.load_reference_points.get_reference_axis()

                # Move loads to beam axis
                if len(ref_axis) == 1:
                    # Straight load axis: move loads to beam axis
                    z2_old = [predocs_coord.point_2_z2_wing(lrp) for lrp in
                              lc_transformed.load_reference_points.point_list]
                    positions_old_on_beam = [predocs_coord.z2_2_point_wing(z2) for z2 in z2_old]
                    lrp_on_beam = DynamicReferencePoints.from_vector_list(positions_old_on_beam)
                    loads_on_beam = lc_transformed.moved_load_case(lrp_on_beam, lc.name + '_on_beam')
                else:
                    # Kinked axis: check if load axis coincides with the beam axis
                    for point in lc_transformed.load_reference_points.point_list:
                        assert predocs_coord.is_point_on_beam_axis_predocs(point), \
                            'For a kinked load axis, all external load points have to lie on the beam axis.'
                    loads_on_beam = lc_transformed

                # Interpolate loads to the node positions
                lc_interpolated_nodes = loads_on_beam.interpolated_loadcase_external(
                    predocs_coord,
                    lc.name + '_interpolated',
                )
                load_case_dict_interpolated_nodes[key] = lc_interpolated_nodes

            load_case_dict_transformed[key] = lc_transformed

        # Transform the element loads to local coordinate system for the cross-section analysis (element loads)
        load_case_dict_elements = self._transformed_loads_to_local_loads(
            predocs_coord.z2_cs,
            predocs_coord.transformation_aircraft_2_predocs,
            predocs_coord.transformation_wing_2_aircraft,
            load_case_dict_interpolated_elements,
        )

        # Create load matrix for beam fem calculations
        load_case_dict_dof = self._get_load_matrix(load_case_dict_interpolated_nodes)

        # Load case dictionaries
        self._load_cases_imported = loadcase_dict
        self._load_cases_transformed = load_case_dict_transformed
        self._load_cases_interpolated_nodes = load_case_dict_interpolated_nodes
        self._load_cases_interpolated_elements = load_case_dict_interpolated_elements
        # self._load_cases_nodal = load_case_dict_interpolated_nodes  # TODO: remove
        self._load_cases_elements = load_case_dict_elements
        self._load_cases_dof = load_case_dict_dof

    # def update_poles(self, predocs_coord, poles):
    #
    #     # # Move loads to pole positions of extracted from cs_processors (node loads)
    #     # load_case_dict_nodal = self._moved_loads_to_load_application_points(
    #     #     poles,
    #     #     predocs_coord.z2_bn,
    #     #     predocs_coord.section_point_2_point,
    #     #     self._load_cases_interpolated_nodes,
    #     # )
    #     #
    #     # # Move loads to pole positions of extracted from cs_processors (element loads)
    #     # load_case_dict_elements = self._moved_loads_to_load_application_points(
    #     #     poles,
    #     #     predocs_coord.z2_cs,
    #     #     predocs_coord.section_point_2_point,
    #     #     self._load_cases_interpolated_elements,
    #     # )



    # @staticmethod
    # def _moved_loads_to_load_application_points(poles, z2_beam_nodes, section_point_2_point, load_cases_interpolated):
    #     """
    #     This method moves the loads in each load case to the load application points for the cross section processor.
    #
    #     It has to be ensured the loads are already given at a position within the cross section of the beam node
    #     (plane perpendicular to the beam axis at a beam node) before they can be moved to the load application points.
    #
    #     Parameters
    #     ----------
    #     poles: list
    #         list of [(x1, y1, z1), (x2, y2, z2), ...] the poles (load application points) of each cross section.
    #     z2_beam_nodes: List
    #         list of beam node z2-coordinates
    #     section_point_2_point: method
    #         transforms a point in a section to PreDoCS coordinates
    #     load_cases_interpolated: dict
    #         dict of all load cases
    #     """
    #     # Create the set of load application points from the poles calculated in the cross-section processors
    #     # load application points are the end points of each beam element
    #     load_application_points = DynamicReferencePoints.create_load_application_points(
    #         poles, z2_beam_nodes, section_point_2_point
    #     )
    #
    #     # Move loads to the pole of the cross section
    #     load_cases = load_cases_interpolated
    #     load_cases_nodal = {}
    #     for key, lc in load_cases.items():
    #         load_cases_nodal[key] = lc.moved_loads_to_load_application_points(load_application_points, lc.name + '_moved')
    #
    #     return load_cases_nodal

    @staticmethod
    def _transformed_loads_to_local_loads(z2_cs, transformation_aircraft_2_predocs, transformation_wing_2_aircraft,
                                       load_cases):
        # Transform loads to a local coordinate system
        load_cases_transformed = {}
        for key, lc in load_cases.items():
            load_cases_transformed[key] = lc.transformed_loads_to_local_loads(
                z2_cs,
                transformation_wing_2_aircraft,
                transformation_aircraft_2_predocs,
                lc.name + '_transformed',
            )

        return load_cases_transformed

    @staticmethod
    def _get_load_matrix(load_cases_nodal):
        """
        This method returns all load cases in a format needed by Beam.get_load_vector for FEM calculations

        Parameters
        ----------
        self: LoadProcessor
            The load processor

        Returns
        -------
        load_cases_dof: dict
            The dictionary of load cases in matrix form for FEM calculations
        """
        load_cases = load_cases_nodal
        load_cases_dof = {}
        for key in load_cases.keys():
            load_cases_dof[key] = load_cases[key].sorted_by_degree_of_freedom()

        return load_cases_dof

    def plot_load_cases(self, name=None, load_set=None, path: str = None, base_file_name: str = None):
        """
        This method plots the loads of defined load cases and load sets.

        The available sets for plotting are: set = ['import', 'transform', 'interpolate', 'move']

        If combined in a list, multiple sets are plotted at once

        Parameters
        ----------
        self: LoadProcessor
            The load processor
        name: str
            The load case to plot
        load_set: unity(List, tuple, str)
            The load set to plot
        Returns
        -------
        fig: list
            list of figures of each load set plotted
        """
        if all([name is None, load_set is None]):
            log.error('No load case and/or load_set selected')
        else:
            fig = []
            title = 'internal loads' if self._load_cases_imported[name].internal_loads else 'external loads'
            # Import
            if 'import' in load_set:
                load_case = self._load_cases_imported[name]
                fig.append(load_case.plot_load_case2D(title + ': imported'))

            # Import
            if 'transform' in load_set:
                load_case = self._load_cases_transformed[name]
                fig.append(load_case.plot_load_case2D(title + ': transformed'))

            # Import
            if 'interpolate' in load_set:
                load_case = self._load_cases_interpolated_nodes[name]
                fig.append(load_case.plot_load_case2D(title + ': interpolated_nodes'))

            # # Import
            # if 'shift' in load_set:
            #     load_case = self._load_cases_nodal[name]
            #     fig.append(load_case.plot_load_case2D(title))

            if path is not None:
                for i, f in enumerate(fig):
                    _save_and_show(f, os.path.join(path, f'loadcase_{name}_{i}.png'))
            if base_file_name is not None:
                for i, f in enumerate(fig):
                    _save_and_show(f, base_file_name.format(i))

            return fig

    def plot_load_redistribution(self, load_case_key, load_key,
                                 export=False, path=None):
        self.load_cases_transformed[load_case_key].\
            plot_load_redistribution(self._load_cases_transformed[load_case_key],
                                     self._load_cases_interpolated_nodes[load_case_key],
                                     load_key=load_key, export=export, path=path,
                                     title='internal loads' if self.load_cases_imported[
                                         load_case_key].internal_loads else 'external loads')

    def plot_load_envelopes(self,
                            loads_type: str = 'forces',
                            one_plot: bool = True,
                            file_format_str: str = None, **kwargs):
        """
        This method plots load envelopes.

        Parameters
        ----------
        loads_type:
            'forces' or 'moments'.
        one_plot
            True, if all envelopes should be plotted in one plot.
        file_format_str
            Format string for the files where to save the plots.
        cmap: str
            The matplotlib color map string.
        """
        # Arguments
        figsize = kwargs.get('figsize', (7, 5))

        load_cases = self._load_cases_interpolated_nodes

        if loads_type == 'forces':
            label = 'Force'
            unit = 'N'
            envelope_vectors = [lc.force_vec for lc in load_cases.values()]
        elif loads_type == 'moments':
            label = 'Moment'
            unit = 'Nm'
            envelope_vectors = [lc.moment_vec for lc in load_cases.values()]
        else:
            raise RuntimeError(f'Unkonwn loads_type {loads_type}')

        if one_plot:
            title = kwargs.get('title', f'{label}-Envelope')
            fig, ax = plt.subplots(figsize=figsize)
            fig.suptitle(title)

            num_cs = len(self.predocs_coord.z2_cs)
            cmap_str = kwargs.get('cmap', None)
            if cmap_str is None:
                # Set default color maps
                if num_cs <= 10:
                    cmap_str = 'tab10'
                elif num_cs <= 20:
                    cmap_str = 'tab20'
                else:
                    raise RuntimeError('No default color map for more than 20 plots! '
                                       'Please set "cmap" argument manually.')
            cmap = plt.get_cmap(cmap_str)
            colors = cmap(range(cmap.N))
        else:
            title = kwargs.get('title', f'{label}-Envelope @ z = {{:.2}} m')

        for i, z_cs in enumerate(self.predocs_coord.z2_cs):
            if not one_plot:
                fig, ax = plt.subplots(figsize=figsize)
                if title is not None:
                    fig.suptitle(title.format(z_cs))

            points = np.array([v[i, (0, 1)] for v in envelope_vectors])

            if one_plot:
                color = colors[i]
            else:
                color = 'k'

            ax.scatter(points[:, 0], points[:, 1], color=color)
            try:
                hull = ConvexHull(points)
                for ii, simplex in enumerate(hull.simplices):
                    ax.plot(points[simplex, 0], points[simplex, 1], ls='-', color=color,
                            label=f'z = {z_cs:.2} m' if ii == 0 else None)
            except QhullError:
                log.warning(traceback.format_exc())

            if one_plot:
                ax.legend()
            else:
                ax.set_xlabel(f'x-{label} [{unit}]')
                ax.set_ylabel(f'y-{label} [{unit}]')
                ax.grid()

                # Save and show figure
                if file_format_str:
                    _save_and_show(fig, file_format_str.format(z_cs), **kwargs)

        if one_plot:
            ax.set_xlabel(f'x-{label} [{unit}]')
            ax.set_ylabel(f'y-{label} [{unit}]')
            ax.grid()

            # Save and show figure
            if file_format_str:
                _save_and_show(fig, file_format_str, **kwargs)

    @property
    def load_cases_imported(self):
        """Load cases in global CPACS coordinate system"""
        return self._load_cases_imported

    @property
    def load_cases_transformed(self):
        """Load cases in PreDoCS coordinate system"""
        return self._load_cases_transformed

    @property
    def load_cases_interpolated_nodes(self):
        """Load cases with load reference points in beam nodes"""
        return self._load_cases_interpolated_nodes

    @property
    def load_cases_interpolated_elements(self):
        """Load cases with load reference points in beam elements"""
        return self._load_cases_interpolated_elements

    # @property
    # def load_cases_nodal(self):
    #     """Load cases with beam nodes as load reference points (cross section poles)"""
    #     return self._load_cases_nodal

    @property
    def load_cases_elements(self):
        """Load cases with beam elements as load reference points (cross section poles)"""
        #assert self.loads_are_internal_loads
        return self._load_cases_elements

    @property
    def load_cases_dof(self):
        """Load cases at beam nodes in FEM matrix format"""
        return self._load_cases_dof
