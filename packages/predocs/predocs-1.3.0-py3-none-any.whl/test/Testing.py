"""
This module provides classes for the automated testing of the different cross section processors.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import concurrent.futures as cf
import os
from abc import abstractmethod
from time import time
from typing import Any, Union, Optional

from PreDoCS.CrossSectionAnalysis.Display import plot_cross_section_element_values, \
    plot_cross_section, plot_cross_section_cells, plot_materials, plot_discreet_geometry
from PreDoCS.CrossSectionAnalysis.Interfaces import ClassicCrossSectionLoads, EulerBernoulliWithTorsionDisplacements, \
    TimoschenkoWithRestrainedWarpingDisplacements, ClassicCrossSectionLoadsWithBimoment, IElement, IElementLoadState, \
    ICrossSectionProcessor, ICrossSectionDisplacements, ICrossSectionLoads
from PreDoCS.CrossSectionAnalysis.Processors import IsotropicCrossSectionProcessor, \
    SongCrossSectionProcessor, JungCrossSectionProcessor, HybridCrossSectionProcessor
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.util import make_quadratic_function
from PreDoCS.util.geometry import transform_direction_m, create_transformation_matrix_2d
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)

PLOTS_PARALLEL = False  # True, if the plots are created parallel


def persist_element_load_state(load_state, element_length):
    """
    Replaces the strain and stress functions of the element with
    the corresponding values at the middle of the element.
    """
    result = {}
    for state_name, state in [
        ('strain_state', load_state.strain_state),
        ('stress_state', load_state.stress_state),
    ]:
        result[state_name] = {}
        for key, value in state.items():
            if callable(value):
                value = value(element_length / 2)
            result[state_name][key] = value

    return result


def flow2stress(e, ls, flow_name):
    """Returns a function of the element stress from a given element stress flow."""

    def flow2stress_i(s):
        return ls.stress_state[flow_name](s) / e.thickness

    return flow2stress_i


def get_composite_element_load_states_dict_Jung(
        element_load_states: dict[IElement, IElementLoadState], full_plots: bool
) -> list[tuple[dict[IElement, 'function'], bool, str, str, str]]:
    """
    This function returns data to plot for the element loads states of the Jung cross section processor.
    
    Parameters
    ----------
    element_load_states
        The element load states.
    full_plots
        True if all stress data should be returned, False for only normal and shear stress.

    Returns
    -------
    list[element_dict, plot_direction_as_arrow, unit, title_format, file_name]
    """
    load_states_dict = [
        ({e: flow2stress(e, ls, 'N_zz') for e, ls in element_load_states.items()},
         False, '$N/m^2$', r'$\sigma_{{zz}}$ [$N/m^2 = Pa$] through {}', '21-sigma_zz'),
        ({e: flow2stress(e, ls, 'N_zs') for e, ls in element_load_states.items()},
         True, '$N/m^2$', r'$\sigma_{{zs}}$ [$N/m^2 = Pa$] through {}', '22-sigma_zs'),
    ]
    if full_plots:
        load_states_dict += [
            ({e: ls.strain_state['epsilon_zz'] for e, ls in element_load_states.items()}, False, '-',
             r'$\epsilon_{{zz}}$ [-] through {}', '31-epsilon_zz'),
            ({e: ls.strain_state['kappa_zz'] for e, ls in element_load_states.items()}, False, '-',
             r'$\kappa_{{zz}}$ [-] through {}', '32-kappa_zz'),
            ({e: ls.strain_state['kappa_zs'] for e, ls in element_load_states.items()}, False, '-',
             r'$\kappa_{{zs}}$ [-] through {}', '33-kappa_zs'),
            ({e: ls.stress_state['N_zs'] for e, ls in element_load_states.items()}, True, '$N/m$',
             r'$N_{{zs}}$ [$N/m = Pa*m$] through {}', '34-N_zs'),
            ({e: ls.stress_state['M_ss'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{ss}}$ [$N$] through {}', '35-M_ss'),

            ({e: ls.stress_state['N_zz'] for e, ls in element_load_states.items()}, False, '$N/m$',
             r'$N_{{zz}}$ [$N/m = Pa*m$] through {}', '36-N_zz'),
            ({e: ls.stress_state['M_zz'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{zz}}$ [$N$] through {}', '37-M_zz'),
            ({e: ls.strain_state['gamma_zs'] for e, ls in element_load_states.items()}, True, '-',
             r'$\gamma_{{zs}}$ [-] through {}', '38-gamma_zs'),
            ({e: ls.strain_state['kappa_ss'] for e, ls in element_load_states.items()}, False, '-',
             r'$\kappa_{{ss}}$ [-] through {}', '39-kappa_ss'),
            ({e: ls.stress_state['M_zs'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{zs}}$ [$N$] through {}', '40-M_zs'),
            ({e: ls.stress_state['M_ss'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{ss}}$ [$N$] through {}', '41-M_ss'),
        ]
    return load_states_dict


def get_composite_element_load_states_dict_Song(
        element_load_states: dict[IElement, IElementLoadState], full_plots: bool
) -> list[tuple[dict[IElement, 'function'], bool, str, str, str]]:
    """
    This function returns data to plot for the element loads states of the Song cross section processor.

    Parameters
    ----------
    element_load_states
        The element load states.
    full_plots
        True if all stress data should be returned, False for only normal and shear stress flows.

    Returns
    -------
    list[element_dict, plot_direction_as_arrow, unit, title_format, file_name]
    """
    load_states_dict = [
        ({e: flow2stress(e, ls, 'N_zz') for e, ls in element_load_states.items()},
         False, '$N/m^2$', r'$\sigma_{{zz}}$ [$N/m^2 = Pa$] through {}', '21-sigma_zz'),
        ({e: flow2stress(e, ls, 'N_zs') for e, ls in element_load_states.items()},
         True, '$N/m^2$', r'$\sigma_{{zs}}$ [$N/m^2 = Pa$] through {}', '22-sigma_zs'),
        ({e: flow2stress(e, ls, 'N_zn') for e, ls in element_load_states.items()},
         False, '$N/m^2$', r'$\sigma_{{zn}}$ [$N/m^2 = Pa$] through {}', '23-sigma_zn')
    ]
    if full_plots:
        load_states_dict += [
            ({e: ls.strain_state['epsilon_zz_0'] for e, ls in element_load_states.items()}, False, '-',
             r'$\epsilon_{{zz}}^0$ [-] through {}', '31-epsilon_zz_0'),
            ({e: ls.strain_state['gamma_zs'] for e, ls in element_load_states.items()}, True, '-',
             r'$\gamma_{{zs}}$ [-] through {}', '38-gamma_zs'),
            ({e: ls.strain_state['kappa_zz'] for e, ls in element_load_states.items()}, False, '-',
             r'$\kappa_{{zz}}$ [-] through {}', '32-kappa_zz'),
            ({e: ls.strain_state['gamma_zn'] for e, ls in element_load_states.items()}, True, '-',
             r'$\gamma_{{zn}}$ [-] through {}', '38-gamma_zn'),

            ({e: ls.stress_state['N_zz'] for e, ls in element_load_states.items()}, False, '$N/m$',
             r'$N_{{zz}}$ [$N/m = Pa*m$] through {}', '36-N_zz'),
            ({e: ls.stress_state['N_zs'] for e, ls in element_load_states.items()}, True, '$N/m$',
             r'$N_{{zs}}$ [$N/m = Pa*m$] through {}', '34-N_zs'),
            ({e: ls.stress_state['M_zz'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{zz}}$ [$N$] through {}', '37-M_zz'),
            ({e: ls.stress_state['M_zs'] for e, ls in element_load_states.items()}, False, '$N$',
             r'$M_{{zs}}$ [$N$] through {}', '37-M_zs'),
            ({e: ls.stress_state['N_zn'] for e, ls in element_load_states.items()}, False, '$N/m$',
             r'$N_{{zn}}$ [$N/m = Pa*m$] through {}', '36-N_zn'),
            ({e: ls.stress_state['N_sn'] for e, ls in element_load_states.items()}, True, '$N/m$',
             r'$N_{{sn}}$ [$N/m = Pa*m$] through {}', '34-N_sn'),
        ]
    return load_states_dict


class CrossSectionTesting(ICrossSectionProcessor):
    """
    Abstract base class for the automated testing and result and plot generation
    of the different cross section processors. Functionalities provided are:

    - Generation of cross section data including internal loads und displacement reaction load cases.
    - Saving of cross section properties as JSON  persist data
    - Plot generation of the cross section and load cases.
    """
    load_cases_title_dict = {
        'extension': 'Normal force',
        'bending_x': 'Bending around the x-axis',
        'bending_y': 'Bending around the y-axis',
        'bending_X_PA': 'Bending around the x-principle-axis',
        'bending_Y_PA': 'Bending around the y-principle-axis',
        'transverse_x': 'Transverse force x-direction',
        'transverse_y': 'Transverse force y-direction',
        'transverse_X_PA': 'Transverse force x-principle-direction',
        'transverse_Y_PA': 'Transverse force y-principle-direction',
        'torsion': 'Torsion',
        'restrained_warping': 'Restrained warping',
    }

    displacement_reactions_title_dict = {
        'extension': 'Extension',
        'bending_x': 'Rotation around the x-axis',
        'bending_y': 'Rotation around the y-axis',
        'bending_X_PA': 'Rotation around the x-principle-axis',
        'bending_Y_PA': 'Rotation around the y-principle-axis',
        'transverse_x': 'Translation in x-direction',
        'transverse_y': 'Translation in y-direction',
        'transverse_X_PA': 'Translation in x-principle-direction',
        'transverse_Y_PA': 'Translation in y-principle-direction',
        'torsion': 'Twisting',
        'restrained_warping': 'Restrained warping',
    }

    @abstractmethod
    def get_cross_section_data_dict(self) -> dict[str, Any]:
        """
        Returns a dict with all the relevant cross section data.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_persist_displacements(self, displacements: ICrossSectionDisplacements) -> dict[str, Any]:
        """
        Returns persist data from the given cross section displacements.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_persist_internal_loads(self, internal_load: ICrossSectionLoads) -> dict[str, Any]:
        """
        Returns persist data from the given cross section internal loads.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_cross_section_persist_data_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Converts the given cross section data into a persistent format.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_displacement_reactions(self) -> list[ICrossSectionDisplacements]:
        """
        Returns all displacement reaction for the testing of the corresponding cross section processor.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_cases(self) -> list[ICrossSectionLoads]:
        """
        Returns all displacement reaction for the testing of the corresponding cross section processor.
        """
        raise NotImplementedError()

    @abstractmethod
    def plot_element_load_states(
            self,
            key: str,
            element_load_states: dict[IElement, IElementLoadState],
            plot_title: str,
            title_dict: dict[str, str],
            path: str,
            file_format: str,
            full_plots: bool,
            **kwargs,
    ) -> None:
        """
        This function plots the load states of the cross section processor.

        Parameters
        ----------
        key
            Key of the loads/displacements.
        element_load_states
            The element load states.
        plot_title
            Title of the plot.
        title_dict
            Dict of the plot titles.
        path
            Path where to save the plot.
        file_format
            File format for saving the plot.
        full_plots
            True if all stress data should be returned, False for only normal and shear stress.
        """
        raise NotImplementedError()

    @abstractmethod
    def cross_section_plots(
            self,
            data: dict[str, Any],
            path: str,
            file_format: str,
            plot_title: bool,
            **kwargs,
    ) -> None:
        """
        Create all cross section processor related plots.

        Parameters
        ----------
        data
            The cross section data to plot.
        path
            The path where to save the plots.
        file_format
            File format for saving the plots.
        plot_title
            True, if the title of the plot is displayed.
        """
        raise NotImplementedError()

    def get_base_cross_section_data_dict(self) -> dict[str, Any]:
        """
        Returns a dict with the basic cross section data.
        """
        return {
            'elastic_center': self.elastic_center,
            'principal_axis_angle': self.principal_axis_angle,
            'shear_center': self.shear_center,
            'stiffness_matrix': self._stiffness_matrix,
            'mass_matrix': self._inertia.inertia_matrix,
            'compliance_matrix': self._compliance_matrix,
        }

    def get_cross_section_data(
            self,
            displacement_reactions: Union[bool, dict[str, ICrossSectionDisplacements]] = True,
            internal_loads: Union[bool, dict[str, ICrossSectionLoads]] = True,
    ) -> dict[str, Any]:
        """
        Returns the cross section data for the given displacement reactions and internal loads.

        Parameters
        ----------
        displacement_reactions
            False for no calculation of load cases through displacement reactions.
            Given displacement reactions or True for the default displacement reactions.
        internal_loads
            False for no calculation of load cases through internal loads.
            Given internal loads or True for the default internal loads.
        """
        timer = time()
        self._update_if_required()
        calculation_time = {'cross_section_calculation': time() - timer}

        data = self.get_base_cross_section_data_dict()

        data.update(self.get_cross_section_data_dict())

        if not isinstance(displacement_reactions, bool) or displacement_reactions:
            if isinstance(displacement_reactions, bool):
                displacement_reactions = self.get_displacement_reactions()
            extra_transverse_force = isinstance(self, IsotropicCrossSectionProcessor)
            data['displacement_reactions'] = {}
            displacement_reactions_calculation_time = {}
            for key, displacements in displacement_reactions.items():
                timer = time()
                element_load_states = self.calc_element_load_states(
                    displacements,
                    Vector([0, 0]),
                ) if extra_transverse_force else self.calc_element_load_states(displacements)
                data['displacement_reactions'][key] = {
                    'displacements': displacements,
                    'element_load_states': element_load_states,
                }
                displacement_reactions_calculation_time[key] = time() - timer
            calculation_time['displacement_reactions_calculation'] = displacement_reactions_calculation_time

        if not isinstance(internal_loads, bool) or internal_loads:
            if isinstance(internal_loads, bool):
                internal_loads = self.get_load_cases()
            data['load_cases'] = {}
            load_cases_calculation_time = {}
            for key, internal_load in internal_loads.items():
                timer = time()
                displacements, element_load_states = self.calc_load_case(internal_load)
                data['load_cases'][key] = {
                    'internal_load': internal_load, 'displacements': displacements,
                    'element_load_states': element_load_states,
                }
                load_cases_calculation_time[key] = time() - timer
            calculation_time['load_cases_calculation'] = load_cases_calculation_time

        data['calculation_time'] = calculation_time

        return data

    def get_cross_section_persist_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Converts the given cross section data into a persistent format.
        """
        persist_data = self._get_cross_section_persist_data_dict(data)

        persist_data['elastic_center'] = data['elastic_center'].tolist()
        persist_data['principal_axis_angle'] = data['principal_axis_angle']
        persist_data['shear_center'] = data['shear_center'].tolist()
        persist_data['stiffness_matrix'] = data['stiffness_matrix'].tolist()
        persist_data['mass_matrix'] = data['mass_matrix'].tolist()
        persist_data['compliance_matrix'] = data['compliance_matrix'].tolist()

        persist_data['calculation_time'] = data['calculation_time']

        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict

        if 'displacement_reactions' in data:
            persist_data['displacement_reactions'] = {}
            for key, displacement_reaction in data['displacement_reactions'].items():
                displacements = displacement_reaction['displacements']
                element_load_states = displacement_reaction['element_load_states']
                persist_data['displacement_reactions'][key] = {
                    'displacements': self._get_persist_displacements(displacements),
                    'element_load_states': {e.id: persist_element_load_state(ls, element_reference_length_dict[e])
                                            for e, ls in element_load_states.items()}}

        if 'load_cases' in data:
            persist_data['load_cases'] = {}
            for key, load_case in data['load_cases'].items():
                internal_load = load_case['internal_load']
                displacements = load_case['displacements']
                element_load_states = load_case['element_load_states']
                persist_data['load_cases'][key] = {
                    'internal_load': self._get_persist_internal_loads(internal_load),
                    'displacements': self._get_persist_displacements(displacements),
                    'element_load_states': {e.id: persist_element_load_state(ls, element_reference_length_dict[e])
                                            for e, ls in element_load_states.items()}}

        return persist_data

    def _plot_element_load_states(
            self,
            load_states_dict: tuple[dict[IElement, 'function'], bool, str, str, str],
            load_name: str,
            plot_title: bool,
            path: str,
            file_format: str,
            **kwargs,
    ) -> None:
        """
        Plots the element load states for one cross section load case.

        Parameters
        ----------
        element_load_states
            The element load states.
        load_name
            Description of the load case.
        plot_title
            True, if the title of the plot is displayed.
        path
            The path where to save the plot.
        file_format
            File format for saving the plot.
        """
        for (element_dict, plot_direction_as_arrow, unit, title_format, file_name) in load_states_dict:
            kwargs.pop('plot_direction_as_arrow', None)
            kwargs.pop('values_are_functions', None)
            kwargs.pop('scale_unit', None)
            kwargs.pop('title', None)
            kwargs.pop('file', None)
            plot_cross_section_element_values(
                self,
                element_dict,
                plot_direction_as_arrow=plot_direction_as_arrow,
                values_are_functions=True,
                scale_unit=unit,
                title=title_format.format(load_name) if plot_title else None,
                file=os.path.join(path, '{}.{}'.format(file_name, file_format)),
                **kwargs,
            )

    def _make_plot(self, key, **kwargs) -> None:
        """
        Plots the element load states for one cross section load case.

        Parameters
        ----------
        key
            Key of the loads/displacements.
        """
        data = kwargs['data']
        path = kwargs['path']
        plot_type = kwargs['plot_type']
        actual_path = os.path.join(path, plot_type, key)
        log.info('Start ' + actual_path)
        if not os.path.exists(actual_path):
            os.makedirs(actual_path)
        self.plot_element_load_states(
            key,
            data[plot_type][key]['element_load_states'],
            kwargs['plot_title'],
            kwargs['title_dict'],
            actual_path, kwargs['file_format'],
            kwargs['full_plots'],
            cross_section_size=kwargs['cross_section_size'],
            **kwargs['kwargs']
        )
        log.info('Finished ' + actual_path)

    def create_cross_section_plots(
            self,
            data: dict[str, Any],
            path: str = '',
            file_format: str = 'png',
            cross_section_size: tuple[float, float] = (15, 10),
            plot_title: bool = True,
            displacement_reactions_to_plot: Optional[list[str]] = None,
            load_cases_to_plot: Optional[list[str]] = None,
            full_plots: bool = False,
            **kwargs,
    ) -> None:
        """
        Creates all plots of the cross section processor.

        Parameters
        ----------
        data
            The cross section data.
        path
            The path where to save the plot.
        file_format
            File format for saving the plot.
        cross_section_size
            Size of the plot in inches.
        plot_title
            True, if the title of the plot is displayed.
        displacement_reactions_to_plot
            Selection of displacement reactions to plot.
        load_cases_to_plot
            Selection of load cases to plot.
        full_plots
            True of all plots, False for a reduced number of plots.
        """
        max_display_value = kwargs.get('max_display_value', 0.3)
        if full_plots:
            plot_discreet_geometry(
                self.discreet_geometry, title='Cross section' if plot_title else None,
                file=os.path.join(path, '01-cross_section.' + file_format), cross_section_size=cross_section_size,
                bbox_inches='tight', **kwargs)
            plot_cross_section(
                self, title='Cross section' if plot_title else None,
                file=os.path.join(path, '02-cross_section.' + file_format), cross_section_size=cross_section_size,
                bbox_inches='tight', **kwargs)
            if len(self.discreet_geometry.cells) > 0:
                plot_cross_section_cells(
                    self, plot_cut_nodes=True, title='Cells' if plot_title else None,
                    file=os.path.join(path, '03-cells.' + file_format), cross_section_size=cross_section_size,
                    bbox_inches='tight', **kwargs)
            plot_materials(
                self.discreet_geometry, element_colors=['b', 'r'],
                title='Material distribution' if plot_title else None,
                plot_coordinate_systems=False, node_marker_size=0.001,
                file=os.path.join(path, '04-materials.' + file_format), cross_section_size=cross_section_size,
                bbox_inches='tight', **kwargs)
            plot_cross_section(
                self, title='Cross section' if plot_title else None,
                node_texts={n: n.id for n in self.discreet_geometry.nodes},
                element_texts={e: e.id for e in self.discreet_geometry.elements},
                file=os.path.join(path, '20-cross_section.' + file_format),
                cross_section_size=cross_section_size, bbox_inches='tight', **kwargs)
            self.cross_section_plots(
                data, path, file_format, plot_title, cross_section_size=cross_section_size, bbox_inches='tight',
                **kwargs)

        if PLOTS_PARALLEL:
            executor = cf.ThreadPoolExecutor()

        if 'displacement_reactions' in data.keys() and displacement_reactions_to_plot is not None:
            sub_kwargs = {
                'data': data,
                'path': path,
                'plot_type': 'displacement_reactions',
                'plot_title': plot_title,
                'title_dict': CrossSectionTesting.displacement_reactions_title_dict,
                'max_display_value': max_display_value,
                'file_format': file_format,
                'cross_section_size': cross_section_size,
                'full_plots': full_plots,
                'bbox_inches': 'tight',
                'kwargs': kwargs,
            }
            if PLOTS_PARALLEL:

                executor.map(lambda displacement_reaction_to_plot:
                             self._make_plot(displacement_reaction_to_plot, **sub_kwargs),
                             displacement_reactions_to_plot)
            else:
                for displacement_reaction in displacement_reactions_to_plot:
                    self._make_plot(displacement_reaction, **sub_kwargs)

        if 'load_cases' in data.keys() and load_cases_to_plot is not None:
            sub_kwargs = {
                'data': data,
                'path': path,
                'plot_type': 'load_cases',
                'plot_title': plot_title,
                'title_dict': CrossSectionTesting.load_cases_title_dict,
                'max_display_value': max_display_value,
                'file_format': file_format,
                'cross_section_size': cross_section_size,
                'full_plots': full_plots,
                'bbox_inches': 'tight',
                'kwargs': kwargs,
            }
            if PLOTS_PARALLEL:
                executor.map(lambda load_case_to_plot:
                             self._make_plot(load_case_to_plot, **sub_kwargs), load_cases_to_plot)
            else:
                for load_case in load_cases_to_plot:
                    self._make_plot(load_case, **sub_kwargs)


class IsotropicTestCrossSection(CrossSectionTesting, IsotropicCrossSectionProcessor):
    """
    Testing class for the `IsotropicCrossSectionProcessor`.
    """

    def __init__(self, discreet_discreet_geometry):
        CrossSectionTesting.__init__(self)
        IsotropicCrossSectionProcessor.__init__(self)
        self.discreet_geometry = discreet_discreet_geometry

    def get_cross_section_data_dict(self):
        self._update_if_required()
        data = {}
        data['EA'] = self._EA
        data['ES_x'] = self._ES_x
        data['ES_y'] = self._ES_y
        data['EI_x'] = self._EI_x
        data['EI_y'] = self._EI_y
        data['EI_xy'] = self._EI_xy
        data['EI_X'] = self._EI_X
        data['EI_Y'] = self._EI_Y
        data['GI_t'] = self._GI_t

        data['q_c_X'] = {}
        data['q_c_Y'] = {}
        data['q_X'] = {}
        data['q_Y'] = {}

        for element in self.discreet_geometry.elements:
            l = element.length
            data['q_c_X'][element] = make_quadratic_function(l, element.integral_values_0['q_c_X'],
                                                             element.integral_values_l['q_c_X'],
                                                             element.integral_values_l_half['q_c_X'])
            data['q_c_Y'][element] = make_quadratic_function(l, element.integral_values_0['q_c_Y'],
                                                             element.integral_values_l['q_c_Y'],
                                                             element.integral_values_l_half['q_c_Y'])
            data['q_X'][element] = make_quadratic_function(l, element.integral_values_0['q_X'],
                                                           element.integral_values_l['q_X'],
                                                           element.integral_values_l_half['q_X'])
            data['q_Y'][element] = make_quadratic_function(l, element.integral_values_0['q_Y'],
                                                           element.integral_values_l['q_Y'],
                                                           element.integral_values_l_half['q_Y'])

        data['q_c_X_mean'] = {element: element.q_X_c_mean for element in self._discreet_geometry.elements}
        data['q_c_Y_mean'] = {element: element.q_Y_c_mean for element in self._discreet_geometry.elements}
        data['q_X_mean'] = {element: element.q_X_mean for element in self._discreet_geometry.elements}
        data['q_Y_mean'] = {element: element.q_Y_mean for element in self._discreet_geometry.elements}
        data['q_t_1'] = {element: element.q_t_1 for element in self._discreet_geometry.elements}
        return data

    def _get_persist_displacements(self, displacements):
        return {
            'extension': displacements.extension,
            'curvature': displacements.curvature.tolist(),
            'twisting': displacements.twisting,
        }

    def _get_persist_internal_loads(self, internal_load):
        return {
            'forces': internal_load.forces.tolist(),
            'moments': internal_load.moments.tolist(),
        }

    def _get_cross_section_persist_data_dict(self, data):
        persist_data = {}
        persist_data['EA'] = data['EA']
        persist_data['ES_x'] = data['ES_x']
        persist_data['ES_y'] = data['ES_y']
        persist_data['EI_x'] = data['EI_x']
        persist_data['EI_y'] = data['EI_y']
        persist_data['EI_xy'] = data['EI_xy']
        persist_data['EI_X'] = data['EI_X']
        persist_data['EI_Y'] = data['EI_Y']
        persist_data['GI_t'] = data['GI_t']
        return persist_data

    def get_displacement_reactions(self):
        X_vector = transform_direction_m(
            create_transformation_matrix_2d(alpha=self.principal_axis_angle), Vector([1, 0])
        )
        Y_vector = transform_direction_m(
            create_transformation_matrix_2d(alpha=self.principal_axis_angle), Vector([0, 1])
        )

        displacement_reactions = {}
        displacement_reactions['extension'] = EulerBernoulliWithTorsionDisplacements(1e-5, Vector([0, 0]), 0.)
        displacement_reactions['bending_x'] = EulerBernoulliWithTorsionDisplacements(0, Vector([1e-5, 0]), 0.)
        displacement_reactions['bending_y'] = EulerBernoulliWithTorsionDisplacements(0, Vector([0, 1e-5]), 0.)
        displacement_reactions['bending_X_PA'] = EulerBernoulliWithTorsionDisplacements(0, X_vector, 0.)
        displacement_reactions['bending_Y_PA'] = EulerBernoulliWithTorsionDisplacements(0, Y_vector, 0.)
        displacement_reactions['torsion'] = EulerBernoulliWithTorsionDisplacements(0, Vector([0, 0]), 1e-5)

        return displacement_reactions

    def get_load_cases(self):
        self._update_if_required()
        X_vector = transform_direction_m(self._transform_principal_axis_to_cross_section_atm, Vector([1, 0]))
        X_vector_3d = Vector([X_vector.x, X_vector.y, 0])
        Y_vector = transform_direction_m(self._transform_principal_axis_to_cross_section_atm, Vector([0, 1]))
        Y_vector_3d = Vector([Y_vector.x, Y_vector.y, 0])

        load_cases = {}
        load_cases['extension'] = ClassicCrossSectionLoads(Vector([0, 0, 1]), Vector([0, 0, 0]))
        load_cases['bending_x'] = ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([1, 0, 0]))
        load_cases['bending_y'] = ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([0, 1, 0]))
        load_cases['bending_X_PA'] = ClassicCrossSectionLoads(Vector([0, 0, 0]), X_vector_3d)
        load_cases['bending_Y_PA'] = ClassicCrossSectionLoads(Vector([0, 0, 0]), Y_vector_3d)
        load_cases['transverse_x'] = ClassicCrossSectionLoads(Vector([1, 0, 0]), Vector([0, 0, 0]))
        load_cases['transverse_y'] = ClassicCrossSectionLoads(Vector([0, 1, 0]), Vector([0, 0, 0]))
        load_cases['transverse_X_PA'] = ClassicCrossSectionLoads(X_vector_3d, Vector([0, 0, 0]))
        load_cases['transverse_Y_PA'] = ClassicCrossSectionLoads(Y_vector_3d, Vector([0, 0, 0]))
        load_cases['torsion'] = ClassicCrossSectionLoads(Vector([0, 0, 0]), Vector([0, 0, 1]))

        return load_cases

    def plot_element_load_states(self, key, element_load_states, plot_title, title_dict, path, file_format, full_plots,
                                 **kwargs):
        load_states_dict = [({e: flow2stress(e, ls, 'normal_flow') for e, ls in element_load_states.items()},
                             False, '$N/m^2$', 'Normalspannungsverteilung [$N/m^2 = Pa$] through {}',
                             '21-normal-stress'),
                            ({e: flow2stress(e, ls, 'shear_flow') for e, ls in element_load_states.items()},
                             True, '$N/m^2$', 'Schubspannungsverteilung [$N/m^2 = Pa$] through {}', '22-shear-stress')
                            ]
        if full_plots:
            load_states_dict += [({e: ls.strain_state['normal_strain'] for e, ls in element_load_states.items()},
                                  False, '-', 'Normaldehnungsverteilung [-] through {}', '31-normal-strain'),
                                 ({e: ls.stress_state['normal_flow'] for e, ls in element_load_states.items()},
                                  False, '$N/m$', 'Normalflussverteilung [$N/m = Pa*m$] through {}', '32-normal-flow'),
                                 ({e: ls.strain_state['shear_strain'] for e, ls in element_load_states.items()},
                                  True, '-', 'Schubdehnungsverteilung [-] through {}', '34-shear_strain'),
                                 ({e: ls.stress_state['shear_flow'] for e, ls in element_load_states.items()},
                                  True, '$N/m$', 'Schubflussverteilung [$N/m = Pa*m$] through {}', '35-shear-flow')
                                 ]
        self._plot_element_load_states(load_states_dict, title_dict[key], plot_title, path, file_format, **kwargs)

    def cross_section_plots(self, data, path, file_format, plot_title, **kwargs):
        plot_cross_section_element_values(self, data['q_X'], plot_direction_as_arrow=True, values_are_functions=True,
                                          title='Schubflussverteilung [$N/m = Pa*m$] through 1-Kraft in X-Richtung' if plot_title else None,
                                          file=os.path.join(path, '11-q_X.' + file_format), **kwargs)
        plot_cross_section_element_values(self, data['q_Y'], plot_direction_as_arrow=True, values_are_functions=True,
                                          title='Schubflussverteilung [$N/m = Pa*m$] through 1-Kraft in Y-Richtung' if plot_title else None,
                                          file=os.path.join(path, '12-q_Y.' + file_format), **kwargs)
        plot_cross_section_element_values(self, data['q_t_1'], plot_direction_as_arrow=True,
                                          title='Schubflussverteilung [$N/m = Pa*m$] through 1-Verdrillung' if plot_title else None,
                                          file=os.path.join(path, '13-q_t_1.' + file_format), **kwargs)


class AdvancedTestCrossSection(CrossSectionTesting):
    """
    Testing class for the cross section processors based on the Timoschenko beam theory with restrained warping.
    """

    def __init__(self):
        CrossSectionTesting.__init__(self)

    def _get_persist_displacements(self, displacements):
        return {
            'strain': displacements.strain.tolist(),
            'curvature': displacements.curvature.tolist(),
            'twisting_derivation': displacements.twisting_derivation,
        }

    def _get_persist_internal_loads(self, internal_load):
        return {
            'forces': internal_load.forces.tolist(),
            'moments': internal_load.moments.tolist(),
            'bimoment': internal_load.bimoment,
        }

    def get_displacement_reactions(self):
        X_vector = transform_direction_m(
            create_transformation_matrix_2d(alpha=self.principal_axis_angle), Vector([1, 0])
        )
        X_vector_3d = Vector([X_vector.x, X_vector.y, 0])
        Y_vector = transform_direction_m(
            create_transformation_matrix_2d(alpha=self.principal_axis_angle), Vector([0, 1])
        )
        Y_vector_3d = Vector([Y_vector.x, Y_vector.y, 0])

        displacement_reactions = {}
        displacement_reactions['extension'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 1e-5]), Vector([0, 0, 0]), 0.
        )
        displacement_reactions['bending_x'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), Vector([1e-5, 0, 0]), 0.
        )
        displacement_reactions['bending_y'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), Vector([0, 1e-5, 0]), 0.
        )
        displacement_reactions['bending_X_PA'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), X_vector_3d * 1e-5, 0.
        )
        displacement_reactions['bending_Y_PA'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), Y_vector_3d * 1e-5, 0.
        )
        displacement_reactions['transverse_x'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([1e-5, 0, 0]), Vector([0, 0, 0]), 0.
        )
        displacement_reactions['transverse_y'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 1e-5, 0]), Vector([0, 0, 0]), 0.
        )
        displacement_reactions['transverse_X_PA'] = TimoschenkoWithRestrainedWarpingDisplacements(
            X_vector_3d * 1e-5, Vector([0, 0, 0]), 0.
        )
        displacement_reactions['transverse_Y_PA'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Y_vector_3d * 1e-5, Vector([0, 0, 0]), 0.
        )
        displacement_reactions['torsion'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), Vector([0, 0, 1e-5]), 0.
        )
        displacement_reactions['restrained_warping'] = TimoschenkoWithRestrainedWarpingDisplacements(
            Vector([0, 0, 0]), Vector([0, 0, 0]),
            1e-5
        )
        return displacement_reactions

    def get_load_cases(self):
        X_vector = transform_direction_m(create_transformation_matrix_2d(alpha=self.principal_axis_angle),
                                         Vector([1, 0]))
        X_vector_3d = Vector([X_vector.x, X_vector.y, 0])
        Y_vector = transform_direction_m(create_transformation_matrix_2d(alpha=self.principal_axis_angle),
                                         Vector([0, 1]))
        Y_vector_3d = Vector([Y_vector.x, Y_vector.y, 0])

        load_cases = {}
        load_cases['extension'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 1]), Vector([0, 0, 0]), 0.)
        load_cases['bending_x'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), Vector([1, 0, 0]), 0.)
        load_cases['bending_y'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), Vector([0, 1, 0]), 0.)
        load_cases['bending_X_PA'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), X_vector_3d, 0.)
        load_cases['bending_Y_PA'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), Y_vector_3d, 0.)
        load_cases['transverse_x'] = ClassicCrossSectionLoadsWithBimoment(Vector([1, 0, 0]), Vector([0, 0, 0]), 0.)
        load_cases['transverse_y'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 1, 0]), Vector([0, 0, 0]), 0.)
        load_cases['transverse_X_PA'] = ClassicCrossSectionLoadsWithBimoment(X_vector_3d, Vector([0, 0, 0]), 0.)
        load_cases['transverse_Y_PA'] = ClassicCrossSectionLoadsWithBimoment(Y_vector_3d, Vector([0, 0, 0]), 0.)
        load_cases['torsion'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), Vector([0, 0, 1]), 0.)
        load_cases['restrained_warping'] = ClassicCrossSectionLoadsWithBimoment(Vector([0, 0, 0]), Vector([0, 0, 0]), 1)

        return load_cases

    def cross_section_plots(self, data, path, file_format, plot_title, **kwargs):
        # plot_cross_section_element_values(
        #     self,
        #     data['psi'],
        #     plot_direction_as_arrow=True,
        #     plot_numbers=True,
        #     title='Torsional function values of the elements' if plot_title else None,
        #     file=path + '/3-psi.' + file_format,
        #     **kwargs,
        # )
        # plot_cross_section_element_values(
        #     self, data['F_w'],
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='Warping function values of the elements' if plot_title else None,
        #     file=path + '/4-F_w.' + file_format,
        #     **kwargs,
        # )
        # elements = self._discreet_geometry.elements
        # plot_cross_section_element_values(
        #     self,
        #     dict([(e, e.r_n(self.pole)) for e in elements]),
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='r_n' if plot_title else None,
        #     file=os.path.join(path + '/5-r_n.' + file_format),
        #     **kwargs,
        # )
        # plot_cross_section_element_values(
        #     self,
        #     dict([(e, e.a_mean(self.pole)) for e in elements]),
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='a_mean' if plot_title else None,
        #     file=os.path.join(path + '/6-a_mean.' + file_format),
        #     **kwargs,
        # )
        pass


class HybridTestCrossSection(AdvancedTestCrossSection, HybridCrossSectionProcessor):
    """
    Testing class for the `HybridCrossSectionProcessor`.
    """

    def __init__(self, discreet_geometry, hybrid_processor):
        AdvancedTestCrossSection.__init__(self)
        HybridCrossSectionProcessor.__init__(self, hybrid_processor=hybrid_processor)
        self.discreet_geometry = discreet_geometry

    def get_base_cross_section_data_dict(self):
        data = {}
        data['elastic_center'] = self.elastic_center
        data['principal_axis_angle'] = self.principal_axis_angle
        data['shear_center'] = self.shear_center
        data['stiffness_matrix'] = self.stiffness.stiffness_matrix
        data['mass_matrix'] = self._inertia.inertia_matrix
        data['compliance_matrix'] = self._main_cs_processor._compliance_matrix
        return data


class SongTestCrossSection(AdvancedTestCrossSection, SongCrossSectionProcessor):
    """
    Testing class for the `SongCrossSectionProcessor`.
    """

    def __init__(self, discreet_geometry):
        AdvancedTestCrossSection.__init__(self)
        SongCrossSectionProcessor.__init__(self)
        self.discreet_geometry = discreet_geometry

    def get_cross_section_data_dict(self):
        self._update_if_required()
        data = {}
        # data['psi'] = {element: element.torsional_function_value for element in self._discreet_geometry.elements}
        # data['F_w'] = {element: element.mean_warping_function_value for element in self._discreet_geometry.elements}
        return data

    def _get_cross_section_persist_data_dict(self, data):
        persist_data = {}
        # persist_data['psi'] = self._get_persist_element_dict(data['psi'])
        # persist_data['F_w'] = self._get_persist_element_dict(data['F_w'])
        return persist_data

    def plot_element_load_states(self, key, element_load_states, plot_title, title_dict, path, file_format, full_plots,
                                 **kwargs):
        load_states_dict = get_composite_element_load_states_dict_Song(element_load_states, full_plots)
        self._plot_element_load_states(load_states_dict, title_dict[key], plot_title, path, file_format, **kwargs)


class HybridSongTestCrossSection(HybridTestCrossSection):
    """
    Testing class for the `HybridCrossSectionProcessor` with the `SongCrossSectionProcessor` as main processor.
    """

    def __init__(self, discreet_geometry):
        HybridTestCrossSection.__init__(self, discreet_geometry, 'Song')

    def get_cross_section_data_dict(self):
        self._update_if_required()
        data = {}
        # data['psi'] = {element: element.torsional_function_value for element in self._discreet_geometry.elements}
        # data['F_w'] = {element: element.mean_warping_function_value for element in self._discreet_geometry.elements}
        return data

    def _get_cross_section_persist_data_dict(self, data):
        persist_data = {}
        # persist_data['psi'] = self._get_persist_element_dict(data['psi'])
        # persist_data['F_w'] = self._get_persist_element_dict(data['F_w'])
        return persist_data

    def plot_element_load_states(
            self, key, element_load_states, plot_title, title_dict, path, file_format, full_plots, **kwargs
    ):
        load_states_dict = get_composite_element_load_states_dict_Song(element_load_states, full_plots)
        self._plot_element_load_states(load_states_dict, title_dict[key], plot_title, path, file_format, **kwargs)


class JungTestCrossSection(AdvancedTestCrossSection, JungCrossSectionProcessor):
    """
    Testing class for the `JungCrossSectionProcessor`.
    """

    def __init__(self, discreet_geometry):
        AdvancedTestCrossSection.__init__(self)
        JungCrossSectionProcessor.__init__(self)
        self.discreet_geometry = discreet_geometry

    def get_cross_section_data_dict(self):
        self._update_if_required()
        data = {}
        # data['psi'] = {element: element.torsional_function_value for element in self._discreet_geometry.elements}
        # data['F_w'] = {element: element.mean_warping_function_value for element in self._discreet_geometry.elements}
        return data

    def _get_cross_section_persist_data_dict(self, data):
        persist_data = {}
        # persist_data['psi'] = self._get_persist_element_dict(data['psi'])
        # persist_data['F_w'] = self._get_persist_element_dict(data['F_w'])
        return persist_data

    def plot_element_load_states(self, key, element_load_states, plot_title, title_dict, path, file_format, full_plots,
                                 **kwargs):
        load_states_dict = get_composite_element_load_states_dict_Jung(element_load_states, full_plots)
        self._plot_element_load_states(load_states_dict, title_dict[key], plot_title, path, file_format, **kwargs)


class HybridJungTestCrossSection(HybridTestCrossSection):
    """
    Testing class for the `HybridCrossSectionProcessor` with the `JungCrossSectionProcessor` as main processor.
    """

    def __init__(self, discreet_geometry):
        HybridTestCrossSection.__init__(self, discreet_geometry, 'Jung')

    def get_cross_section_data_dict(self):
        self._update_if_required()
        data = {}
        data['b'] = self._main_cs_processor._b
        data['B'] = self._main_cs_processor._B
        data['K_bb'] = self._main_cs_processor._K_bb
        data['K_bv'] = self._main_cs_processor._K_bv
        data['K_vv'] = self._main_cs_processor._K_vv
        data['p'] = self._main_cs_processor._p
        # data['psi'] = {element: element.torsional_function_value for element in self._discreet_geometry.elements}
        # data['F_w'] = {element: element.mean_warping_function_value for element in self._discreet_geometry.elements}
        return data

    def _get_cross_section_persist_data_dict(self, data):
        persist_data = {}
        persist_data['b'] = data['b'].tolist()
        persist_data['B'] = data['B'].tolist()
        persist_data['K_bb'] = data['K_bb'].tolist()
        persist_data['K_bv'] = data['K_bv'].tolist()
        persist_data['K_vv'] = data['K_vv'].tolist()
        persist_data['p'] = data['p'].tolist()
        # persist_data['psi'] = self._get_persist_element_dict(data['psi'])
        # persist_data['F_w'] = self._get_persist_element_dict(data['F_w'])
        return persist_data

    def plot_element_load_states(self, key, element_load_states, plot_title, title_dict, path, file_format, full_plots,
                                 **kwargs):
        load_states_dict = get_composite_element_load_states_dict_Jung(element_load_states, full_plots)
        self._plot_element_load_states(load_states_dict, title_dict[key], plot_title, path, file_format, **kwargs)

    def cross_section_plots(self, data, path, file_format, plot_title, **kwargs):
        # plot_cross_section_element_values(
        #     self,
        #     data['psi'],
        #     plot_direction_as_arrow=True,
        #     plot_numbers=True,
        #     title='Torsional function values of the elements' if plot_title else None,
        #     file=path + '/3-psi.' + file_format,
        #     **kwargs,
        # )
        # plot_cross_section_element_values(
        #     self, data['F_w'],
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='Warping function values of the elements' if plot_title else None,
        #     file=path + '/4-F_w.' + file_format,
        #     **kwargs,
        # )
        # elements = self._discreet_geometry.elements
        # plot_cross_section_element_values(
        #     self,
        #     dict([(e, e.r_n(self.pole)) for e in elements]),
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='r_n' if plot_title else None,
        #     file=os.path.join(path + '/5-r_n.' + file_format),
        #     **kwargs,
        # )
        # plot_cross_section_element_values(
        #     self,
        #     dict([(e, e.a_mean(self.pole)) for e in elements]),
        #     plot_direction_as_arrow=False,
        #     plot_numbers=True,
        #     title='a_mean' if plot_title else None,
        #     file=os.path.join(path + '/6-a_mean.' + file_format),
        #     **kwargs,
        # )

        elements = self._main_cs_processor.discreet_geometry.elements
        plot_cross_section_element_values(
            self,
            {e: e.f_r_1[0,0] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_1[0,0]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_1_0,0.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.f_r_2[0,0] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_2[0,0]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_2_0,0.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.f_r_3[0,0] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_3[0,0]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_3_0,0.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.f_r_3[0,1] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_3[0,1]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_3_0,1.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.f_r_3[1,0] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_3[1,0]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_3_1,0.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.f_r_3[1,1] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='f_r_3[1,1]' if plot_title else None,
            file=os.path.join(path + '/5-f_r_3_1,1.' + file_format),
            **kwargs,
        )

        plot_cross_section_element_values(
            self,
            {e: e.torsional_function_value for e in elements},
            plot_direction_as_arrow=False,
            plot_numbers=False,
            title='torsional_function_value' if plot_title else None,
            file=os.path.join(path + '/6-torsional_function_value.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.r_midsurface(self._discreet_geometry, self.pole) for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='r_midsurface' if plot_title else None,
            file=os.path.join(path + '/7-r_midsurface.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: (e.node1.integral_values['omega'] + e.node2.integral_values['omega']) / 2 for e in elements},
            plot_direction_as_arrow=False,
            plot_numbers=False,
            title='omega' if plot_title else None,
            file=os.path.join(path + '/8-omega.' + file_format),
            **kwargs,
        )
        # for i in range(5):
        #     plot_cross_section_element_values(
        #         self,
        #         {e: e.b[0, i] for e in elements},
        #         plot_direction_as_arrow=True,
        #         plot_numbers=False,
        #         title=f'b_{{1, {i+1}}}' if plot_title else None,
        #         file=os.path.join(path + f'/9-b_1,{i+1}.' + file_format),
        #         **kwargs,
        #     )
        plot_cross_section_element_values(
            self,
            {e: e.B[0, 0] * self._main_cs_processor._K_bb_inv[0, 2] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='B_element[0, 0] * K_bb_inv[0, 2]' if plot_title else None,
            file=os.path.join(path + '/10-B_element[0, 0] x K_bb_inv[0, 2].' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.B[0, 1] * self._main_cs_processor._K_bb_inv[1, 2] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='B_element[0, 1] * K_bb_inv[1, 2]' if plot_title else None,
            file=os.path.join(path + '/10-B_element[0, 1] x K_bb_inv[1, 2].' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.B[0, 2] * self._main_cs_processor._K_bb_inv[2, 2] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='B_element[0, 2] * K_bb_inv[2, 2]' if plot_title else None,
            file=os.path.join(path + '/10-B_element[0, 2] x K_bb_inv[2, 2].' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.B[0, 3] * self._main_cs_processor._K_bb_inv[3, 2] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='B_element[0, 3] * K_bb_inv[3, 2]' if plot_title else None,
            file=os.path.join(path + '/10-B_element[0, 3] x K_bb_inv[3, 2].' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: e.B[0, 4] * self._main_cs_processor._K_bb_inv[4, 2] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='B_element[0, 4] * K_bb_inv[4, 2]' if plot_title else None,
            file=os.path.join(path + '/10-B_element[0, 4] x K_bb_inv[4, 2].' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: - self._main_cs_processor._K_bb_inv[0, 2] * e.integral_values_0['int_A11_ds'] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='-K_bb_inv[0, 2] * int_A11_ds1' if plot_title else None,
            file=os.path.join(path + '/10- -K_bb_inv[0, 2] x int_A11_ds1.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: -self._main_cs_processor._K_bb_inv[1, 2] * e.integral_values_0['int_A11_y_ds'] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='-K_bb_inv[1, 2] * int_A11_y_ds1' if plot_title else None,
            file=os.path.join(path + '/10- -K_bb_inv[1, 2] x int_A11_y_ds1.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: self._main_cs_processor._K_bb_inv[2, 2] * e.integral_values_0['int_A11_x_ds'] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='K_bb_inv[2, 2] * int_A11_x_ds1' if plot_title else None,
            file=os.path.join(path + '/10-K_bb_inv[2, 2] x int_A11_x_ds1.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: -2 * self._main_cs_processor._K_bb_inv[3, 2] * e.integral_values_0['int_B16_ds'] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='-2 * K_bb_inv[3, 2] * int_B16_ds1' if plot_title else None,
            file=os.path.join(path + '/10- -2 x K_bb_inv[3, 2] x int_B16_ds1.' + file_format),
            **kwargs,
        )
        plot_cross_section_element_values(
            self,
            {e: self._main_cs_processor._K_bb_inv[4, 2] * e.integral_values_0['int_A11_omega_ds'] for e in elements},
            plot_direction_as_arrow=True,
            plot_numbers=False,
            title='K_bb_inv[4, 2] * int_A11_omega_ds1' if plot_title else None,
            file=os.path.join(path + '/10-K_bb_inv[4, 2] x int_A11_omega_ds1.' + file_format),
            **kwargs,
        )

