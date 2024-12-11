# cython: profile=True
"""
This module contains processors for the calculation of cross section properties.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from abc import abstractmethod

import numpy as np
from scipy.optimize import minimize_scalar

from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Interfaces import EulerBernoulliWithTorsionStiffness, \
    TimoschenkoWithRestrainedWarpingStiffness, EulerBernoulliWithTorsionDisplacements, \
    TimoschenkoWithRestrainedWarpingDisplacements, IElementLoadState, TimoschenkoStiffness, TimoschenkoDisplacements
from PreDoCS.CrossSectionAnalysis.Interfaces import ICrossSectionProcessor, \
    CrossSectionInertia, IElement
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement, IsotropicElement
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.globals import DuplicateFilter
from PreDoCS.util.filters import find
from PreDoCS.util.util import (enclosed_area_vector, get_elatic_center_and_bending_principal_axis_angle, \
                               symmetrize, idx, calc_shear_center, get_shear_principal_axis_stiffness_and_angle, \
                               get_function_with_bounds, CoG_from_inertia_matrix)
from PreDoCS.util.geometry import transform_direction_m, transform_location_m, create_transformation_matrix_2d
from PreDoCS.util.dtypes import cython_dtype_from_dtype, lgs_solve
from PreDoCS.util.vector import Vector


import cython
# override with Python import if not in compiled code
if cython.compiled:
    from cython.cimports import numpy as np


log = get_module_logger(__name__)


def get_element_type_from_cross_section_processor_name(name):
    """
    Returns the element class for the given cross section processor string.

    Parameters
    ----------
    name: str
        Name of the cross section processor ('Song', 'Jung', 'JungWithoutWarping', 'Hybrid', 'Isotropic').

    Returns
    -------
    class <- IElement:
        The element class.
    """
    if name in ['Song', 'Jung', 'JungWithoutWarping', 'Hybrid']:
        return CompositeElement
    elif name == 'Isotropic':
        return IsotropicElement
    else:
        raise RuntimeError('Unknown cross section processor name')


def get_cross_section_processor_from_name(name):
    """
    Returns the cross section processor class for the given cross section processor string.

    Parameters
    ----------
    name: str
        Name of the cross section processor ('Song', 'Jung', 'JungWithoutWarping', 'Hybrid', 'Isotropic').

    Returns
    -------
    class <- ICrossSectionProcessor:
        The cross section processor class.
    """
    if name == 'Song':
        return SongCrossSectionProcessor
    if name == 'Hybrid':
        return HybridCrossSectionProcessor
    elif name == 'Jung':
        return JungCrossSectionProcessor
    elif name == 'JungWithoutWarping':
        return JungWithoutWarpingCrossSectionProcessor
    elif name == 'Isotropic':
        return IsotropicCrossSectionProcessor
    else:
        raise RuntimeError(f'Unknown cross section processor name "{name}"')


class ElementLoadState(IElementLoadState):
    """
    Stain and stress state of an element.

    Attributes
    ----------
    _strain_state: dict(str, float)
        Stain state of an element.
    _stress_state: dict(str, float)
        Stress state of an element.
    """

    def __init__(self, strain_state, stress_state):
        """
        Constructor.

        Parameters
        ----------
        strain_state: dict(str, float)
            Stain state of an isotropic element.
        stress_state: dict(str, float)
            Stress state of an isotropic element.
        """
        self._strain_state = strain_state
        self._stress_state = stress_state

    @property
    def strain_state(self):
        """dict(str, float): Stain state of an element."""
        return self._strain_state

    @strain_state.setter
    def strain_state(self, value):
        self._strain_state = value

    @property
    def stress_state(self):
        """dict(str, float): Stress state of an element."""
        return self._stress_state

    @stress_state.setter
    def stress_state(self, value):
        self._stress_state = value


class CrossSectionProcessor(ICrossSectionProcessor):
    """
    Represents a basis cross section processor.

    Attributes
    ----------
    _id: int
        Id of the cross section.
    _z_beam: float
        Z-coordinate of the cross section in the beam.

    _update_required: bool
        True, if a new calculation is required.

    _discreet_geometry: DiscreetCrossSectionGeometry
        The discreet geometry of the cross section.
  
    _elastic_center: Vector
        Elastic center of the cross section.
    _principal_axis_angle: float
        Angle between elastic coordinate system and principal axis coordinate system in RAD.
    _shear_center: Vector
        Shear center of the cross section.
   
    _transform_cross_section_to_elastic_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
    _transform_elastic_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
    _transform_elastic_to_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the elastic to the principal axis coordinate system.
    _transform_principal_axis_to_elastic_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the principal axis to the elastic coordinate system.
    _transform_cross_section_to_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the principal axis coordinate system.
    _transform_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the principal axis to the cross section coordinate system.

    _stiffness: IStiffness
        Stiffness for the cross section.
    _cog: Vector
        Center of gravity of the cross section.
    _cross_section_inertia_matrix: IInertia
        Inertia for the cross section.
    """
    def __init__(self, cross_section_id=0, z_beam=0.0, open_cs: bool = True, dtype=np.float64, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        open_cs
            True to allow open cross-sections, False for closed cross-sections only.
        dtype
            Data type used for the calculations.
        """
        self._update_required = False
        self._discreet_geometry = None
        self._id = cross_section_id
        self._z_beam = z_beam
        self._shear_center = None
        self._open_cs = open_cs
        self._dtype = dtype
        self._cython_dtype = cython_dtype_from_dtype(dtype)

    @property
    def id(self) -> int:
        """Id of the cross section."""
        return self._id

    @property
    def z_beam(self) -> float:
        """Z-coordinate of the cross section in the beam."""
        return self._z_beam

    @property
    def open_cs(self) -> bool:
        """Can process open cross-sections."""
        return self._open_cs

    @property
    def dtype(self):
        """Data type used for the calculations."""
        return self._dtype

    @property
    def discreet_geometry(self) -> DiscreetCrossSectionGeometry:
        """The discreet geometry for the cross section analysis."""
        return self._discreet_geometry
    
    @discreet_geometry.setter
    def discreet_geometry(self, value):
        if not self._open_cs:
            open_ends = list({n for n in value.nodes if len(list(value.get_neighbor_nodes(n))) == 1})
            assert len(open_ends) == 0, 'Cross Section geometry is not closed. This PreDoCS cross-section processor only work with closed cross secitons.'
        self._discreet_geometry = value
        self._update_required = True

    def force_update(self) -> None:
        """
        Forced update of the cached values.
        """
        self._update_required = True
        self._update_if_required()

        
    @property
    def stiffness(self):
        """ICrossSectionStiffness: Returns the cross section stiffness."""
        self._update_if_required()
        return self._stiffness
    
    @property
    def CoG(self):
        """Vector: Center of gravity of the cross section."""
        self._update_if_required()
        return self._cog

    @property
    def inertia(self):
        """IInertia: Returns the cross section inertia."""
        self._update_if_required()
        return self._inertia

    @property
    def pole(self):
        """
        Vector:
             Rotation pole of the rigid body rotation of the cross section.
        """
        self._update_if_required()
        return self._shear_center

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _calc_inertia(self):
        """
        See [Chen2010]_, https://en.wikipedia.org/wiki/Moment_of_inertia.
        
        Returns
        -------
        Vector
            Center of gravity of the cross section.
        IInertia
            Returns the cross section inertia.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        M_half_py = np.zeros((6, 6), dtype=dtype)
        M_half = cython.declare(cython_dtype[:, :], M_half_py)
        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            density: cython_dtype = element.shell.density
            t_el: cython_dtype = element.thickness

            M_half[0, 0] += density * l * t_el
            # M_half[0,1] += 0
            # M_half[0,2] += 0
            # M_half[0,3] += 0
            # M_half[0,4] += 0
            M_half[0, 5] += (1 / 2) * density * l * t_el * (-y1 - y2)
            M_half[1, 1] += density * l * t_el
            # M_half[1,2] += 0
            # M_half[1,3] += 0
            # M_half[1,4] += 0
            M_half[1, 5] += (1 / 2) * density * l * t_el * (x1 + x2)
            M_half[2, 2] += density * l * t_el
            M_half[2, 3] += (1 / 2) * density * l * t_el * (y1 + y2)
            M_half[2, 4] += (1 / 2) * density * l * t_el * (-x1 - x2)
            # M_half[2,5] += 0
            M_half[3, 3] += (1 / 12) * density * t_el * (4 * l ** 2 * (
                        y1 ** 2 + y1 * y2 + y2 ** 2) + t_el ** 2 * x1 ** 2 - 2 * t_el ** 2 * x1 * x2 + t_el ** 2 * x2 ** 2) / l
            M_half[3, 4] += (1 / 12) * density * t_el * (-2 * l ** 2 * (
                        2 * x1 * y1 + x1 * y2 + x2 * y1 + 2 * x2 * y2) + t_el ** 2 * x1 * y1 - t_el ** 2 * x1 * y2 - t_el ** 2 * x2 * y1 + t_el ** 2 * x2 * y2) / l
            # M_half[3,5] += 0
            M_half[4, 4] += (1 / 12) * density * t_el * (4 * l ** 2 * (
                        x1 ** 2 + x1 * x2 + x2 ** 2) + t_el ** 2 * y1 ** 2 - 2 * t_el ** 2 * y1 * y2 + t_el ** 2 * y2 ** 2) / l
            # M_half[4,5] += 0
            M_half[5, 5] += (1 / 12) * density * t_el * (4 * l ** 2 * (
                        x1 ** 2 + x1 * x2 + x2 ** 2 + y1 ** 2 + y1 * y2 + y2 ** 2) + t_el ** 2 * x1 ** 2 - 2 * t_el ** 2 * x1 * x2 + t_el ** 2 * x2 ** 2 + t_el ** 2 * y1 ** 2 - 2 * t_el ** 2 * y1 * y2 + t_el ** 2 * y2 ** 2) / l

        M = symmetrize(M_half_py)
        inertia = CrossSectionInertia(M)
        return CoG_from_inertia_matrix(M), inertia

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def calc_inertia_beam(self, l_beam: float) -> np.ndarray:
        """
        See https://en.wikipedia.org/wiki/Moment_of_inertia.

        Parameters
        ----------
        l_beam
            Length of the beam element.

        Returns
        -------
        np.ndarray
            Returns the cross-section inertia matrix (6x6) of a beam element with the length l_beam.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        M_beam_half_py = np.zeros((6, 6), dtype=dtype)
        M_beam_half = cython.declare(cython_dtype[:, :], M_beam_half_py)
        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            density: cython_dtype = element.shell.density
            t_el: cython_dtype = element.thickness

            M_beam_half[0, 0] += density * l * l_beam * t_el
            # M_beam_half[0,1] += 0
            # M_beam_half[0,2] += 0
            # M_beam_half[0,3] += 0
            # M_beam_half[0,4] += 0
            M_beam_half[0, 5] += (1 / 2) * density * l * l_beam * t_el * (-y1 - y2)
            M_beam_half[1, 1] += density * l * l_beam * t_el
            # M_beam_half[1,2] += 0
            # M_beam_half[1,3] += 0
            # M_beam_half[1,4] += 0
            M_beam_half[1, 5] += (1 / 2) * density * l * l_beam * t_el * (x1 + x2)
            M_beam_half[2, 2] += density * l * l_beam * t_el
            M_beam_half[2, 3] += (1 / 2) * density * l * l_beam * t_el * (y1 + y2)
            M_beam_half[2, 4] += (1 / 2) * density * l * l_beam * t_el * (-x1 - x2)
            # M_beam_half[2,5] += 0
            M_beam_half[3, 3] += (1 / 12) * density * l_beam * t_el * (l ** 2 * (
                        l_beam ** 2 + 4 * y1 ** 2 + 4 * y1 * y2 + 4 * y2 ** 2) + t_el ** 2 * x1 ** 2 - 2 * t_el ** 2 * x1 * x2 + t_el ** 2 * x2 ** 2) / l
            M_beam_half[3, 4] += (1 / 12) * density * l_beam * t_el * (-2 * l ** 2 * (
                        2 * x1 * y1 + x1 * y2 + x2 * y1 + 2 * x2 * y2) + t_el ** 2 * x1 * y1 - t_el ** 2 * x1 * y2 - t_el ** 2 * x2 * y1 + t_el ** 2 * x2 * y2) / l
            # M_beam_half[3,5] += 0
            M_beam_half[4, 4] += (1 / 12) * density * l_beam * t_el * (l ** 2 * (
                        l_beam ** 2 + 4 * x1 ** 2 + 4 * x1 * x2 + 4 * x2 ** 2) + t_el ** 2 * y1 ** 2 - 2 * t_el ** 2 * y1 * y2 + t_el ** 2 * y2 ** 2) / l
            # M_beam_half[4,5] += 0
            M_beam_half[5, 5] += (1 / 12) * density * l_beam * t_el * (4 * l ** 2 * (
                        x1 ** 2 + x1 * x2 + x2 ** 2 + y1 ** 2 + y1 * y2 + y2 ** 2) + t_el ** 2 * x1 ** 2 - 2 * t_el ** 2 * x1 * x2 + t_el ** 2 * x2 ** 2 + t_el ** 2 * y1 ** 2 - 2 * t_el ** 2 * y1 * y2 + t_el ** 2 * y2 ** 2) / l

        M_beam = symmetrize(M_beam_half_py)
        return M_beam

    @property
    def elastic_center(self):
        """Vector: Elastic center of the cross section."""
        self._update_if_required()
        return self._elastic_center
    
    @property
    def principal_axis_angle(self):
        """
        float:
            Angle between elastic coordinate system and principal axis coordinate system in RAD.
        """
        self._update_if_required()
        return self._principal_axis_angle
    
    @property
    def shear_center(self):
        """Vector: Shear center of the cross section."""
        self._update_if_required()
        return self._shear_center
    
    def _set_augmented_transformation_matrices(self):
        """
        Calculates the augmented transformation matrices.
        """
        self._transform_cross_section_to_elastic_atm = create_transformation_matrix_2d(0, -self._elastic_center)
        self._transform_elastic_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_elastic_atm)

        self._transform_elastic_to_principal_axis_atm = create_transformation_matrix_2d(-self._principal_axis_angle, Vector([0, 0]))
        self._transform_principal_axis_to_elastic_atm = np.linalg.inv(self._transform_elastic_to_principal_axis_atm)

        self._transform_cross_section_to_principal_axis_atm = \
            self._transform_elastic_to_principal_axis_atm @ self._transform_cross_section_to_elastic_atm
        self._transform_principal_axis_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_principal_axis_atm)

        if hasattr(self, '_shear_center') and hasattr(self, '_shear_principal_axis_angle'):
            cs2shear_atm = create_transformation_matrix_2d(0, -self._shear_center)
            shear2shear_pa_atm = create_transformation_matrix_2d(-self._shear_principal_axis_angle, Vector([0, 0]))

            self._transform_cross_section_to_shear_principal_axis_atm = shear2shear_pa_atm @ cs2shear_atm
            self._transform_shear_principal_axis_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_shear_principal_axis_atm)

    @property
    def transform_cross_section_to_elastic_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_elastic_atm
    
    @property
    def transform_elastic_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_elastic_to_cross_section_atm
    
    @property
    def transform_elastic_to_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the elastic to the principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_elastic_to_principal_axis_atm
    
    @property
    def transform_principal_axis_to_elastic_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the principal axis to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_principal_axis_to_elastic_atm

    @property
    def transform_cross_section_to_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_principal_axis_atm
    
    @property
    def transform_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_principal_axis_to_cross_section_atm

    @staticmethod
    def get_cutted_discreet_geometry_from_discreet_geometry(discreet_geometry):
        """
        Cut all cells of a multicell discreet geometry in such a way that no closed cells remain.

        Parameter
        ---------
        discreet_geometry: DiscreetCrossSectionGeometry
            The uncutted discreet geometry.

        Returns
        -------
        DiscreetCrossSectionGeometry
            The cutted discreet geometry.
        """
        # Cut cells
        cutted_discreet_geometry = discreet_geometry.copy()
        nodes_used = set()

        # For each cell
        segment_border_nodes = set(cutted_discreet_geometry.segment_border_nodes)
        for cell in discreet_geometry.cells:
            # Select cut node
            branch_nodes = {n for n in cutted_discreet_geometry.nodes if
                            len(cutted_discreet_geometry.get_neighbor_nodes(n)) > 2}
            cell_nodes = set(cell.nodes)
            unused_branch_nodes_in_cell = (branch_nodes & cell_nodes) - nodes_used
            if len(unused_branch_nodes_in_cell) > 0:
                cut_node = sorted(unused_branch_nodes_in_cell, key=lambda n: n.id)[0]
            else:
                cut_node = sorted(cell_nodes & segment_border_nodes, key=lambda n: n.id)[0]
            cell.cut_node = cut_node

            # Cut
            nodes_set = set(cutted_discreet_geometry.get_neighbor_nodes(cut_node)) & (cell_nodes - nodes_used)
            neighbors_cut_node = sorted(nodes_set, key=lambda n: n.id)
            # log.debug(f'cut: cut node {cut_node.id}, other node: {neighbors_cut_node[0].id}')
            cutted_discreet_geometry.cut_discreet_geometry(cut_node, neighbors_cut_node[0], skip_segment_border_nodes_check=True)
            nodes_used.update(cell_nodes)

        return cutted_discreet_geometry

    def _get_elements_cut_uncut_dict(self):
        elements_uncut = self._discreet_geometry.elements
        elements_cut_uncut_dict = {
            e_cut: find(elements_uncut, 'id', e_cut.id) for e_cut in self._cutted_discreet_geometry.elements
        }
        return elements_cut_uncut_dict

    def _set_contur_integral_values_recursive(self, contur_integrals_function, contur_integral_names):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        # TODO: bei add_branches_on_nodes False hat das Ergebnis des s-Integrals keine Richtung?

        for n in self._cutted_discreet_geometry.nodes:
            n.visited = False

        elements_cut_uncut_dict = self._get_elements_cut_uncut_dict()

        start_node = self._cutted_discreet_geometry.nodes[0]
        start_node.integral_values.update({name: 0 for name in contur_integral_names})
        self._set_contur_integral_values_recursive_inner(start_node, contur_integrals_function, contur_integral_names, elements_cut_uncut_dict)

    def _set_contur_integral_values_recursive_inner(self, last_node, contur_integrals_function, contur_integral_names, elements_cut_uncut_dict):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        node_midsurface_positions = self._cutted_discreet_geometry.node_midsurface_positions
        neighbor_nodes = [n for n in self._cutted_discreet_geometry.get_neighbor_nodes(last_node) if not n.visited]
        for current_node in neighbor_nodes:

            current_node.visited = True
            element = self._cutted_discreet_geometry.get_element_from_nodes(last_node, current_node)
            element_uncut = elements_cut_uncut_dict[element]

            integration_in_element_direction = element.node1 == last_node
            element_uncut.is_in_global_integration_direction = integration_in_element_direction

            if integration_in_element_direction:
                # Integration in element direction
                last_position = node_midsurface_positions[element.node1]
                next_position = node_midsurface_positions[element.node2]
            else:
                # Integration against element direction
                last_position = node_midsurface_positions[element.node2]
                next_position = node_midsurface_positions[element.node1]

            last_values = last_node.integral_values
            l_values, l_half_values = contur_integrals_function(element, integration_in_element_direction,
                                                                last_node, current_node,
                                                                last_position, next_position,
                                                                last_values)

            current_node.integral_values.update(l_values)

            if integration_in_element_direction:
                element_uncut.integral_values_0.update(last_values)
                element_uncut.integral_values_l_half.update(l_half_values)
                element_uncut.integral_values_l.update(l_values)
            else:
                element_uncut.integral_values_0.update(l_values)
                element_uncut.integral_values_l_half.update(l_half_values)
                element_uncut.integral_values_l.update(last_values)
                # element_uncut.integral_values_0.update({k: -v for k, v in l_values.items()})
                # element_uncut.integral_values_l_half.update({k: -v for k, v in l_half_values.items()})
                # element_uncut.integral_values_l.update({k: -v for k, v in last_values.items()})

            self._set_contur_integral_values_recursive_inner(current_node, contur_integrals_function, contur_integral_names, elements_cut_uncut_dict)

    def _set_contur_integral_values(self, contur_integrals_function, contur_integral_names):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        node_midsurface_positions = self._cutted_discreet_geometry.node_midsurface_positions
        elements_cut_uncut_dict = self._get_elements_cut_uncut_dict()

        # TODO: bei add_branches_on_nodes False hat das Ergebnis des s-Integrals keine Richtung?
        for e in self._cutted_discreet_geometry.elements:
            e.visited = False

        for n in self._cutted_discreet_geometry.nodes:
            n.num_visits = 0

        # Free ends
        free_ends = [n for n in self._cutted_discreet_geometry.nodes if
                       len(list(self._cutted_discreet_geometry.get_neighbor_nodes(n))) == 1]
        start_nodes = free_ends
        end_node = start_nodes.pop()

        for start_node in start_nodes:
            # print('Start node: ' + str(start_node.id))
            last_node = start_node
            last_node.num_visited = 1
            last_node.integral_values.update({name: 0 for name in contur_integral_names})
            current_node = self._cutted_discreet_geometry.get_neighbor_nodes(start_node)[0]

            while True:
                element = self._cutted_discreet_geometry.get_element_from_nodes(last_node, current_node)
                element_uncut = elements_cut_uncut_dict[element]

                if element.visited:
                    raise RuntimeError('One element can not be processed more than one time.')

                current_node.num_visits += 1
                element.visited = True

                integration_in_element_direction = element.node1 == last_node
                element_uncut.is_in_global_integration_direction = integration_in_element_direction

                if integration_in_element_direction:
                    # Integration in element direction
                    last_position = node_midsurface_positions[element.node1]
                    next_position = node_midsurface_positions[element.node2]
                else:
                    # Integration against element direction
                    last_position = node_midsurface_positions[element.node2]
                    next_position = node_midsurface_positions[element.node1]

                last_values = last_node.integral_values
                l_values, l_half_values = contur_integrals_function(
                    element,
                    integration_in_element_direction,
                    last_node,
                    current_node,
                    last_position,
                    next_position,
                    last_values,
                )

                if integration_in_element_direction:
                    element_uncut.integral_values_0.update(last_values)
                    element_uncut.integral_values_l_half.update(l_half_values)
                    element_uncut.integral_values_l.update(l_values)
                else:
                    # TODO: nur relevant für s-Integrale mit Richtung?
                    element_uncut.integral_values_0.update({k: -l_values[k] for k in contur_integral_names
                                                            if k in l_values})
                    element_uncut.integral_values_l_half.update({k: -l_half_values[k] for k in contur_integral_names
                                                                 if k in l_half_values})
                    element_uncut.integral_values_l.update({k: -last_values[k] for k in contur_integral_names
                                                            if k in last_values})

                current_node_neighbors = list(self._cutted_discreet_geometry.get_neighbor_nodes(current_node))
                if len(current_node_neighbors) == 2:
                    # Normal node
                    if current_node.num_visits > 1:
                        raise RuntimeError('A non branch node can be visited only once')
                    current_node.integral_values.update(l_values)

                    # Go on for the path
                    tmp = current_node
                    nodes_set = set(current_node_neighbors) - {last_node}
                    assert len(nodes_set) == 1
                    current_node = nodes_set.pop()
                    last_node = tmp
                elif len(current_node_neighbors) > 2:
                    # Branch node
                    if current_node.num_visits > 1:
                        # Node already visited
                        current_node.integral_values.update({k: current_node.integral_values[k] + v
                                                             for k, v in l_values.items()})
                        if len(current_node_neighbors) == current_node.num_visits:
                            raise RuntimeError('Path finished on a branch node, not allowed')
                        elif len(current_node_neighbors) == current_node.num_visits + 1:
                            # Only one not visited branch, go on for the path
                            # print('Only one not visited branch, go on for the path: ' + str(current_node.id))
                            tmp = current_node
                            current_node = None
                            for node in current_node_neighbors:
                                element = self._cutted_discreet_geometry.get_element_from_nodes(tmp, node)
                                if not element.visited:
                                    current_node = node
                                    break
                            if not current_node:
                                raise RuntimeError('Path finished on a branch node, not allowed (all neighbor nodes already visited)')
                            last_node = tmp
                        else:
                            # Termination condition: Not enough visits
                            # print('Termination condition: Not enough visits: ' + str(current_node.id))
                            break
                    else:
                        # Termination condition: first visit at a branch node
                        # print('Termination condition: first visit at a branch node: ' + str(current_node.id))
                        current_node.integral_values.update(l_values)
                        break
                else:
                    # Free node
                    if not current_node == end_node:
                        raise RuntimeError('Path does not finished at an end node')
                    # print('End node: ' + str(current_node.id))
                    # TODO: Werte müssen gleich sein
                    #if not add_branches_on_nodes:
                    # log.warning(
                    #     '{} must equal {}'.format(current_node.integral_values, l_values,
                    #         # {k: current_node.integral_values[k] for k in contur_integral_names},
                    #         #                       {k: l_values[k] for k in contur_integral_names}
                    #     )
                    # )
                    break

    @DuplicateFilter(log)
    def update_components(self, component2material, processor_type, get_element_stiffness_func):
        """
        Update the processor's component and material properties. Only the abd matrix is needed for skins.

        Parameter
        ---------
        component2material: dict
            Translation dictionary from PreDoCS component to material
        processor_type: str
            The processor type needed for the stiffness calculation
        """
        element_type = get_element_type_from_cross_section_processor_name(processor_type)
        for component in self.discreet_geometry.components:
            if component in component2material:
                # Update material
                component.shell = component2material[component]

                # Update material stiffness
                # TODO Think about shifting stiffness to component instead of material.
                component.shell.stiffness = get_element_stiffness_func(component.shell, element_type, dtype=self._dtype)
            else:
                log.warning(f'Component "{component.id}" with material "{component.shell.name}" '
                            #f'from {component.node1.position} to {component.node2.position} '
                            'could not be updated because it is not part of the structural model / optimisation process.')

        # Update processor
        self._update_required = True

    def calc_element_min_max_load_state(self, element, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        log.warning('''The generic CrossSectionProcessor.calc_element_min_max_load_state method is very slow.
                        Please overwrite it in every subclass.''')
        load_state = self.calc_element_load_state(element, displacements)
        l = self._discreet_geometry.element_reference_length_dict[element]

        min_strain_state = {}
        max_strain_state = {}
        for key, func in load_state.strain_state.items():
            min_strain_state[key] = minimize_scalar(func, bounds=(0, l), method='bounded').fun
            max_strain_state[key] = minimize_scalar(lambda s: -func(s), bounds=(0, l), method='bounded').fun

        min_stress_state = {}
        max_stress_state = {}
        for key, func in load_state.stress_state.items():
            min_stress_state[key] = minimize_scalar(func, bounds=(0, l), method='bounded').fun
            max_stress_state[key] = minimize_scalar(lambda s: -func(s), bounds=(0, l), method='bounded').fun

        return ElementLoadState(min_strain_state, min_stress_state),\
               ElementLoadState(max_strain_state, max_stress_state)

    def calc_element_min_max_load_states(self, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(IElement, (IElementLoadState, IElementLoadState))
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        return {e: self.calc_element_min_max_load_state(e, displacements) for e in self.discreet_geometry.elements}


class BaseCompositeCrossSectionProcessor(CrossSectionProcessor):
    """
    Base methods for composite cross section processing.
    
    Attributes
    ----------
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
    """
    
    @property
    def transform_cross_section_to_shear_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_shear_principal_axis_atm
    
    @property
    def transform_shear_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_shear_principal_axis_to_cross_section_atm
    
    def _set_torsional_function_values(self, cells):
        """
        Sets the torsional function values of the elements.

        Parameters
        ----------
        cells: list(Cell)
            List of the cells of the cross section.
        """
        dtype = self._dtype

        segments = self._discreet_geometry.segments
        num_segments = len(segments)

        if np.any([e._shell is not None for e in self._discreet_geometry.elements]):
            # Element has individual shells (materials)
            element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
            L_list = []
            alpha_list = []
            for segment in segments:
                elements = segment.elements
                l = np.array([element_reference_length_dict[e] for e in elements], dtype=dtype)
                alpha = np.array([e.shell.stiffness.torsion_compliance for e in elements], dtype=dtype)
                L_segment = np.sum(np.multiply(l, alpha))
                alpha_segment = L_segment / np.sum(l)
                L_list.append(L_segment)
                alpha_list.append(alpha_segment)
            L = np.diag(L_list)
            alpha = np.array(alpha_list, dtype=dtype)
        else:
            l = np.array([segment.reference_length(self._discreet_geometry) for segment in segments], dtype=dtype)
            alpha = np.array([segment.shell.stiffness.torsion_compliance for segment in segments], dtype=dtype)
            L = np.diag(np.multiply(l, alpha))

        M = self._get_segment_cell_mapping(segments, cells)
        M_T = M.T
        A_enclosed = enclosed_area_vector(cells)
        
        # Solve LGS
        lambda_ = lgs_solve(M @ L @ M_T, 2. * A_enclosed, dtype=dtype)

        psi = np.multiply(alpha, M_T @ lambda_)
        
        # Set the torsional function values to the elements
        for segment_index in range(num_segments):
            segment = segments[segment_index]
            psi_segment = psi[segment_index]
            for element in segment.elements:
                is_in_dir = DiscreetCrossSectionGeometry.is_element_in_direction_of_segment(element, segment)
                if is_in_dir == True:
                    element.torsional_function_value = psi_segment
                elif is_in_dir == False:
                    element.torsional_function_value = -psi_segment
                else:
                    # Not in cell
                    if not self._open_cs:
                        raise RuntimeError('Open cross-section part.')
                    else:
                        element.torsional_function_value = 0
    
    def _get_warping(self, pole):
        """
        Returns the warping of the nodes.

        Parameters
        ----------
        pole: Vector
            Rotation pole for the warping calculation.
        
        Returns
        -------
        dict(INode, float)
            Warping for each node.
        """
        nodes = self._discreet_geometry.nodes
        start_node = nodes[0]
        warping_dict = {start_node: 0.}  # INode: float
        for node in set(nodes) - {start_node}:
            path = self._discreet_geometry.get_shortest_path(start_node, node)
            F_w = 0.
            for node_index in range(len(path)-1):
                e = self._discreet_geometry.get_element_from_nodes(path[node_index], path[node_index+1])
                l = self._discreet_geometry.element_reference_length_dict[e]
                if e.node1 == path[node_index]:
                    # Integration in element direction
                    F_w += (e.r_midsurface(self._discreet_geometry, pole) - e.torsional_function_value) * l
                else:
                    F_w -= (e.r_midsurface(self._discreet_geometry, pole) - e.torsional_function_value) * l
            warping_dict[node] = F_w
        
        return {node: value for (node, value) in warping_dict.items()}
    
    def _set_element_warping(self, node_warpings):
        """
        Sets the warping function values of the elements.
        
        Parameters
        ----------
        node_warpings: dict(INode, float)
            Warping for each node.
        """
        elements = self._discreet_geometry.elements
        for element in elements:
            element.node1_warping = node_warpings[element.node1]
            element.node2_warping = node_warpings[element.node2]

    def _get_segment_cell_mapping(self, segments, cells):
        """
        Returns the segment-cell-mapping matrix with respect to the cell circulating and the segment direction.
        
        Parameters
        ----------
        segments: list(Segments)
            List of segments.
        cells: list(Cell)
            List of cells.
        
        Returns
        -------
        numpy.ndarray
            Segment-cell-mapping matrix.
        """
        dtype = self._dtype
        
        num_segments = len(segments)
        num_cells = len(cells)
        Z = np.zeros((num_cells, num_segments), dtype=dtype)
        # Create mapping matrix
        for cell_index in range(num_cells):
            cell = cells[cell_index]
            for segment_index in range(num_segments):
                segment = segments[segment_index]
            
                if segment in cell.segments:
                    is_in_dir = DiscreetCrossSectionGeometry.is_segment_in_direction_of_cell(segment, cell)
                    if is_in_dir == True:
                        Z[cell_index, segment_index] = 1.
                    elif is_in_dir == False:
                        Z[cell_index, segment_index] = -1.
                    else:
                        # Not in cell
                        if not self._open_cs:
                            raise RuntimeError('Open cross-section part.')
                        else:
                            pass

        return Z

    def calc_element_load_states(self, displacements):
        """
        Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        return {e: self.calc_element_load_state(e, displacements) for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.
        
        Parameters
        ----------
        internal_loads: ICrossSectionLoads
            Cross section internal loads.
        
        Returns
        -------
        ICrossSectionDisplacements
            Displacements of the cross section.
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements, self.calc_element_load_states(displacements)

    def _set_segment_cell_mapping(self, identity_matrix_size, cells):
        """
        Returns the segment-cell-mapping matrix with respect to the cell circulating and the segment direction.

        Parameters
        ----------
        identity_matrix_size: int
            Size of the identity matrix.
        cells: list(Cell) (default: None)
            List of cells.

        Returns
        -------
        numpy.ndarray
            Segment-cell-mapping matrix.
        """
        dtype = self._dtype

        segments = self._discreet_geometry.segments
        num_cells = len(cells)
        Z_dict = {}
        I = np.identity(identity_matrix_size)

        # Create mapping matrix
        for segment in segments:
            Z = np.zeros((identity_matrix_size, identity_matrix_size*num_cells), dtype=dtype)
            for cell_index in range(num_cells):
                cell = cells[cell_index]
                if segment in cell.segments:
                    is_in_dir = DiscreetCrossSectionGeometry.is_segment_in_direction_of_cell(segment, cell)
                    if is_in_dir == True:
                        Z[:, identity_matrix_size*cell_index:identity_matrix_size*(cell_index+1)] = I
                    elif is_in_dir == False:
                        Z[:, identity_matrix_size*cell_index:identity_matrix_size*(cell_index+1)] = -I
                    else:
                        # Not in cell
                        if not self._open_cs:
                            raise RuntimeError('Open cross-section part.')
                        else:
                            Z = None
            Z_dict[segment] = Z
        self._Z_dict = Z_dict


class IsotropicCrossSectionProcessor(CrossSectionProcessor):
    """
    Represents a isotropic cross section analysis. The cross section has to be thin-walled and made of isotropic
    material. The discreet geometry has to be made of one or multiple closed sections.
    It is possible to calculate the normal flow per element through extension and bending.
    Furthermore the shear flow through torsion and transverse force is calculated.
    Four displacements(extension, two curvatures, twisting) from the internal loads can be determined.
    The calculations are based of [Mahnken2015]_, pp. 436 and [Wiedemann2007]_, pp. 372-376.

    Coordinate systems:
        * x-y: cross section coordinate system, arbitrary.
        * i-j: elastic coordinate system, same alignment as x-y but origin in the elastic center of the cross section.
        * X-Y: principal axis coordinate system, same origin as i-j but axis alignment to the principal axis.

    Attributes
    ----------
    _cutted_discreet_geometry: DiscreetCrossSectionGeometry
        The cutted discreet geometry of the cross section.

    _EA: float
        Extension stiffness.

    _ES_x: float
        Elastic moment of area around the x-axis.
    _ES_y: float
        Elastic moment of area around the y-axis.

    _EI_x: float
        Elastic second moment of area around the x-axis.
    _EI_y: float
        Elastic second moment of area around the y-axis.
    _EI_xy: float
        Elastic moment of deviation around the x- and y-axis.

    _EI_X: float
        Elastic principal second moment of area around the X-axis.
    _EI_Y: float
        Elastic principal second moment of area around the Y-axis.
    _GI_t: float
        Torsional stiffness of the cross section.

    _stiffness_matrix: numpy.ndarray
        Stiffness matrix for Euler-Bernoulli bending.
    _compliance_matrix: numpy.ndarray
        Complience matrix for Euler-Bernoulli bending.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam, **kwargs)

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            self._cog, self._inertia = self._calc_inertia()

            sm = self._get_stiffness_matrix()
            self._stiffness_matrix = sm
            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)

            self._EA = sm[0, 0]
            self._ES_x = sm[0, 1]
            self._ES_y = -sm[0, 2]
            self._EI_x = sm[1, 1]
            self._EI_y = sm[2, 2]
            self._EI_xy = sm[1, 2]

            # self._elastic_center =  Vector([self._ES_y / self._EA, self._ES_x / self._EA])
            self._elastic_center, psma, self._principal_axis_angle = get_elatic_center_and_bending_principal_axis_angle(
                sm)
            self._EI_X = psma.x
            self._EI_Y = psma.y

            self._set_augmented_transformation_matrices()

            Z_matrix = self._cell_element_mapping(self._discreet_geometry.cells, self._discreet_geometry.elements)

            if len(self._discreet_geometry.cells) == 0:
                # Give only a warning instead of raise an exception, because shear center calculation is used for
                # open cross-sections in the hybrid processor
                log.warning('For open cross sections, IsotropicCrossSectionProcessor can not calculate '
                            'torsional stiffness and stress distributions due to torsion. '
                            'Dummy values for torsion stiffness and shear stress distributions are set.')
                # Set dummy value
                self._GI_t = 1
                for e in self._discreet_geometry.elements:
                    e.q_t_1 = 1
            else:
                self._GI_t = self._get_torsional_stiffness_and_set_element_shear_flow_from_torsion_distribution(Z_matrix)

            self._cutted_discreet_geometry = self.get_cutted_discreet_geometry_from_discreet_geometry(
                self._discreet_geometry)
            self._set_element_shear_flow_from_transverse_force_distribution(Z_matrix)

            self._shear_center = calc_shear_center(
                self._discreet_geometry,
                {e: (e.q_X_mean, e.q_Y_mean) for e in self._discreet_geometry.elements},
                self._transform_cross_section_to_principal_axis_atm,
                self._transform_principal_axis_to_cross_section_atm,
            )

            self._stiffness = EulerBernoulliWithTorsionStiffness(self._stiffness_matrix, self._GI_t)

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _get_stiffness_matrix(self):
        """
        Returns the stiffness matrix of the cross section.

        Returns
        -------
        numpy.ndarray
            3x3 cross section stiffness matrix.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        S_half_py = np.zeros((3, 3), dtype=dtype)
        S_half = cython.declare(cython_dtype[:, :], S_half_py)
        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y
            
            E_e: cython_dtype = element.shell.stiffness.E
            t_e: cython_dtype = element.thickness
            
            int_const = l
            int_x = l/2*(x1+x2)
            int_y = l/2*(y1+y2)
            int_x_x = l/3*(x1**2+x1*x2+x2**2)
            int_y_y = l/3*(y1**2+y1*y2+y2**2)
            int_x_y = l/6*((2*x1+x2)*y1 + (x1+2*x2)*y2)
            
            S_half[idx(11)] += E_e*int_const*t_e
            S_half[idx(12)] += E_e*int_y*t_e
            S_half[idx(13)] += -E_e*int_x*t_e
            S_half[idx(22)] += E_e*int_y_y*t_e
            S_half[idx(23)] += -E_e*int_x_y*t_e
            S_half[idx(33)] += E_e*int_x_x*t_e

        return symmetrize(S_half_py)

    def _element_shear_compliance_vector(self, elements):
        """
        Parameters
        ----------
        elements: list(IsotropicElement)
            List of elements.

        Returns
        -------
        numpy.ndarray
            Vector of the shear compliance of the elements (l/(G*t)).
        """
        dtype = self._dtype
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        S_vector = [element_reference_length_dict[element] / (element.shell.stiffness.G * element.thickness) for element in elements]
        return np.array(S_vector, dtype=dtype)

    def _cell_element_mapping(self, cells, elements) -> np.ndarray:
        """
        Returns the cells-elements mapping matrix with respect to the global machining direction.

        Parameters
        ----------
        cells: list(Cell)
            List of cells.
        elements: list(IsotropicElement)
            List of elements.

        Returns
        -------
        numpy.ndarray
            Cells-elements mapping matrix.
        """
        dtype = self._dtype

        num_elements = len(elements)
        num_cells = len(cells)
        Z = np.zeros((num_elements, num_cells), dtype=dtype)

        # Create mapping matrix
        for element_idx, element in enumerate(elements):
            Z_row = np.zeros(num_cells, dtype=dtype)
            for cell_index, cell in enumerate(cells):
                if element in cell.elements:
                    is_in_dir = DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(element, cell.elements)
                    if is_in_dir == True:
                        Z_row[cell_index] = 1.
                    elif is_in_dir == False:
                        Z_row[cell_index] = -1.
                    else:
                        # Not in cell
                        if not self._open_cs:
                            raise RuntimeError('Open cross-section part.')
                        else:
                            pass
            Z[element_idx, :] = Z_row

        return Z

    def _get_torsional_stiffness_and_set_element_shear_flow_from_torsion_distribution(self, Z_matrix: np.ndarray):
        """
        Calculates the torsional stiffness of the cross section.

        Returns
        -------
        float
            The torsional stiffness of the cross section.
        """
        dtype = self._dtype

        # Calc shear flow closed cells
        elements = self._discreet_geometry.elements
        cells = self._discreet_geometry.cells
        A_enclosed = enclosed_area_vector(cells)

        # Cell-element mapping matrix (with element directions)
        # Z_matrix = self._cell_element_mapping(cells, elements)
        Z_T_matrix = np.transpose(Z_matrix)
        S_matrix = np.diag(self._element_shear_compliance_vector(
            elements))  # Element shear compliance as diagonal matrix

        # Setup LSG for the distribution of the circulating shear flows to the cells (coeff * q_0/twisting = b)
        coeff = np.dot(Z_T_matrix, np.dot(S_matrix, Z_matrix))
        b = np.multiply(2., A_enclosed)

        # Solve LGS
        torsional_shar_flow_distribution_vector = lgs_solve(coeff, b, dtype=dtype)

        # Torsional stiffness of the cross section
        GI_t = 2. * np.dot(A_enclosed, torsional_shar_flow_distribution_vector)

        # Shear flow per "1"-twisting
        q_t_1 = np.dot(Z_matrix, torsional_shar_flow_distribution_vector)
        for i in range(len(elements)):
            elements[i].q_t_1 = q_t_1[i]

        return GI_t

    def _contur_integral_functions(self, element, integration_in_element_direction,
                                   last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the contur integral values for one element.

        Parameters
        ----------
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        # Element position in principal axis coordinate system
        last_pos_principal_axis = transform_location_m(self._transform_cross_section_to_principal_axis_atm, last_position)
        next_pos_principal_axis = transform_location_m(self._transform_cross_section_to_principal_axis_atm, current_position)

        x1 = last_pos_principal_axis.x
        x2 = next_pos_principal_axis.x
        y1 = last_pos_principal_axis.y
        y2 = next_pos_principal_axis.y

        l = self._discreet_geometry.element_reference_length_dict[element]
        E = element.shell.stiffness.E
        t = element.thickness

        l_values = {}
        l_half_values = {}

        l_values['q_c_X'] = last_values['q_c_X'] - t * E * l * (x1 + x2) / 2 / self._EI_Y
        l_values['q_c_Y'] = last_values['q_c_Y'] - t * E * l * (y1 + y2) / 2 / self._EI_X

        l_half_values['q_c_X'] = last_values['q_c_X'] - t * E * l * (3 * x1 + x2) / 8 / self._EI_Y
        l_half_values['q_c_Y'] = last_values['q_c_Y'] - t * E * l * (3 * y1 + y2) / 8 / self._EI_X

        return l_values, l_half_values

    def _set_element_shear_flow_from_transverse_force_distribution(self, Z_matrix: np.ndarray):
        """
        Calculates the shear flow distribution for the elements trough transverse force in principal axis direction.
        [Wiedemann2007]_, pp. 373-376
        """
        dtype = self._dtype

        # Clear contur integral values
        for n in self._cutted_discreet_geometry.nodes:
            n.integral_values = dict()
        for e in self._cutted_discreet_geometry.elements:
            e.integral_values_0 = dict()
            e.integral_values_l_half = dict()
            e.integral_values_l = dict()
        for n in self._discreet_geometry.nodes:
            n.integral_values = dict()
        for e in self._discreet_geometry.elements:
            e.integral_values_0 = dict()
            e.integral_values_l_half = dict()
            e.integral_values_l = dict()

        # Shear flow at the cutted cross section
        self._set_contur_integral_values(self._contur_integral_functions, ['q_c_X', 'q_c_Y'])

        # Shear flow at the closed cross section
        cells = self._discreet_geometry.cells
        elements = self._discreet_geometry.elements
        num_elements = len(elements)
        # Cell-element mapping matrix (with element directions)
        # Z_matrix = self._cell_element_mapping(cells, elements)
        Z_T_matrix = np.transpose(Z_matrix)
        S_matrix = np.diag(self._element_shear_compliance_vector(
            elements))  # Element shear compliance as diagonal matrix

        # Shear flow at the cutted cross section as vector
        q_c_X_vector = np.zeros(num_elements, dtype=dtype)
        q_c_Y_vector = np.zeros(num_elements, dtype=dtype)
        for i in range(num_elements):
            element = elements[i]

            q_c_X1 = element.integral_values_0['q_c_X']
            q_c_X2 = element.integral_values_l['q_c_X']
            q_c_X3 = element.integral_values_l_half['q_c_X']
            element.q_X_c_mean = (q_c_X1 + q_c_X2 + 4*q_c_X3)/6
            q_c_X_vector[i] = element.q_X_c_mean

            q_c_Y1 = element.integral_values_0['q_c_Y']
            q_c_Y2 = element.integral_values_l['q_c_Y']
            q_c_Y3 = element.integral_values_l_half['q_c_Y']
            element.q_Y_c_mean = (q_c_Y1 + q_c_Y2 + 4*q_c_Y3)/6
            q_c_Y_vector[i] = element.q_Y_c_mean

        # Setup LSG for the distribution of the circulating shear flows to the cells (coeff * q_0_i = b_i)
        coeff = Z_T_matrix @ S_matrix @ Z_matrix
        b_X = - Z_T_matrix @ S_matrix @ q_c_X_vector
        b_Y = - Z_T_matrix @ S_matrix @ q_c_Y_vector

        # Solve LGS
        q_0_X_vector = lgs_solve(coeff, b_X, dtype=dtype)
        q_0_Y_vector = lgs_solve(coeff, b_Y, dtype=dtype)

        # Resulting shear flow
        delta_q_X_vector = Z_matrix @ q_0_X_vector
        delta_q_Y_vector = Z_matrix @ q_0_Y_vector

        # Set resulting shear flow in the elements
        for i in range(num_elements):
            elements[i].q_X_mean = elements[i].q_X_c_mean + delta_q_X_vector[i]
            elements[i].integral_values_0['q_X'] = elements[i].integral_values_0['q_c_X'] + delta_q_X_vector[i]
            elements[i].integral_values_l['q_X'] = elements[i].integral_values_l['q_c_X'] + delta_q_X_vector[i]
            elements[i].integral_values_l_half['q_X'] = elements[i].integral_values_l_half['q_c_X'] + delta_q_X_vector[i]

            elements[i].q_Y_mean = elements[i].q_Y_c_mean + delta_q_Y_vector[i]
            elements[i].integral_values_0['q_Y'] = elements[i].integral_values_0['q_c_Y'] + delta_q_Y_vector[i]
            elements[i].integral_values_l['q_Y'] = elements[i].integral_values_l['q_c_Y'] + delta_q_Y_vector[i]
            elements[i].integral_values_l_half['q_Y'] = elements[i].integral_values_l_half['q_c_Y'] + delta_q_Y_vector[i]

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicInternalLoads
            Cross section internal loads.

        Returns
        -------
        EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        """
        dtype = self._dtype

        self._update_if_required()

        epsilon = np.dot(self._compliance_matrix, np.array(
            [internal_loads.forces.z, internal_loads.moments.x, internal_loads.moments.y], dtype=dtype)).flatten()

        delta_T = np.cross(-self.shear_center, Vector([internal_loads.forces.x, internal_loads.forces.y]))
        T = internal_loads.moments.z + delta_T
        twisting = T / self._GI_t

        return EulerBernoulliWithTorsionDisplacements(epsilon[0], Vector([epsilon[1], epsilon[2]]), twisting)

    def calc_element_load_state(self, element, displacements, transverse_force=Vector([0, 0])):
        """
       Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        transverse_force: Vector (default: Vector([0,0]))
            The transverse force.

        Returns
        -------
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions

        # Transform transverse force into the principal axis coordinate system
        Q_principal_axis = transform_direction_m(self._transform_cross_section_to_principal_axis_atm, transverse_force)

        l = self._discreet_geometry.element_reference_length_dict[element]
        q_X1 = element.integral_values_0['q_X']
        q_X2 = element.integral_values_l['q_X']
        q_X3 = element.integral_values_l_half['q_X']

        q_Y1 = element.integral_values_0['q_Y']
        q_Y2 = element.integral_values_l['q_Y']
        q_Y3 = element.integral_values_l_half['q_Y']

        def x(s): return node_midsurface_positions[element.node1].x + element.dx_ds(self._discreet_geometry) * s

        def y(s): return node_midsurface_positions[element.node1].y + element.dy_ds(self._discreet_geometry) * s

        def normal_strain(s): return displacements.extension + displacements.curvature.x * y(s) - \
                                     displacements.curvature.y * x(s)

        def normal_flow(s): return normal_strain(s) * element.thickness * element.shell.stiffness.E

        def shear_flow(s):
            return element.q_t_1 * displacements.twisting + \
                                  Q_principal_axis.x * ((q_X1*l**2 - l*s*(3*q_X1 + q_X2 - 4*q_X3) + 2*s**2*(q_X1 + q_X2 - 2*q_X3))/l**2) + \
                                  Q_principal_axis.y * ((q_Y1*l**2 - l*s*(3*q_Y1 + q_Y2 - 4*q_Y3) + 2*s**2*(q_Y1 + q_Y2 - 2*q_Y3))/l**2)

        def shear_strain(s): return shear_flow(s) / element.thickness / element.shell.stiffness.G

        bounds = (0, l)
        return ElementLoadState(
            {'normal_strain': lambda s: get_function_with_bounds(normal_strain, s, bounds),
             'shear_strain': lambda s: get_function_with_bounds(shear_strain, s, bounds)},
            {'normal_flow': lambda s: get_function_with_bounds(normal_flow, s, bounds),
             'shear_flow': lambda s: get_function_with_bounds(shear_flow, s, bounds)})

    def calc_element_load_states(self, displacements, transverse_force=Vector([0, 0])):
        """
       Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        transverse_force: Vector (default: Vector([0,0]))
            The transverse force.

        Returns
        -------
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        return {e: self.calc_element_load_state(e, displacements, transverse_force)
                for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.

        Parameters
        ----------
        internal_loads: ClassicInternalLoads
            Cross section internal loads.

        Returns
        -------
        EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements,\
               self.calc_element_load_states(displacements, Vector([internal_loads.forces.x, internal_loads.forces.y]))


class HybridCrossSectionProcessor(CrossSectionProcessor):
    """
    This class is a two in one cross section processor. The main cross section processor is a composite cross section
    processor, but for the calculation of the warping and therefore the rotation pole (shear center)
    of the cross section, the `IsotropicCrossSectionProcessor` ia used.

    Attributes
    ----------
    _main_processor: BaseCompositeCrossSectionProcessor
        The main cross section processor.
    _isotropic_cs_processor: IsotropicCrossSectionProcessor
        The isotropic cross section processor for the shear center calculation.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """

        super().__init__(cross_section_id, z_beam, **kwargs)
        if 'hybrid_processor' in kwargs:
            self._main_processor = kwargs['hybrid_processor']
        else:
            self._main_processor = 'JungWithoutWarping'
            log.warning(
                'Main cross section processor unknown. '
                'Hybrid processor initialised with "JungWithoutWarping" main cross section processor'
            )

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            # Do the isotropic calculation (for the shear center)
            isotropic_cs_processor = IsotropicCrossSectionProcessor(self.id, self.z_beam, dtype=self._dtype)
            isotropic_cs_processor.discreet_geometry = self.discreet_geometry
            sc_isotropic = isotropic_cs_processor.shear_center
            self._isotropic_cs_processor = isotropic_cs_processor

            # Do the main calculation (for the stiffness matrix and element strains and stresses
            main_cs_processor = get_cross_section_processor_from_name(self._main_processor)(self.id, self.z_beam, dtype=self._dtype)
            main_cs_processor.discreet_geometry = self.discreet_geometry
            main_cs_processor._shear_center = sc_isotropic
            main_cs_processor._update_required = True
            self._main_cs_processor = main_cs_processor

            # Copy data from the two cross section processors in this class
            self._stiffness = main_cs_processor.stiffness
            self._cog, self._inertia = self._calc_inertia()
            self._shear_center = sc_isotropic

            self._elastic_center = main_cs_processor.elastic_center
            self._principal_axis_angle = main_cs_processor.principal_axis_angle

            self._transform_cross_section_to_elastic_atm = main_cs_processor.transform_cross_section_to_elastic_atm
            self._transform_elastic_to_cross_section_atm = main_cs_processor.transform_elastic_to_cross_section_atm
            self._transform_elastic_to_principal_axis_atm = main_cs_processor.transform_elastic_to_principal_axis_atm
            self._transform_principal_axis_to_elastic_atm = main_cs_processor.transform_principal_axis_to_elastic_atm
            self._transform_cross_section_to_principal_axis_atm = main_cs_processor.transform_cross_section_to_principal_axis_atm
            self._transform_principal_axis_to_cross_section_atm = main_cs_processor.transform_principal_axis_to_cross_section_atm

            self._transform_cross_section_to_shear_principal_axis_atm = main_cs_processor.transform_cross_section_to_shear_principal_axis_atm
            self._transform_shear_principal_axis_to_cross_section_atm = main_cs_processor.transform_shear_principal_axis_to_cross_section_atm

    @property
    def transform_cross_section_to_shear_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_shear_principal_axis_atm

    @property
    def transform_shear_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_shear_principal_axis_to_cross_section_atm

    def calc_element_load_states(self, displacements):
        """
        Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        return {e: self.calc_element_load_state(e, displacements) for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements, self.calc_element_load_states(displacements)

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_displacements(internal_loads)

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: CompositeElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_element_load_state(element, displacements)

    def calc_element_min_max_load_state(self, element, displacements):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_element_min_max_load_state(element, displacements)


class SongCrossSectionProcessor(BaseCompositeCrossSectionProcessor):
    """
    Represents an anisotropic cross section analysis for thin-walled composite structures.
    The discreet geometry has to be made of one or multiple closed cells. The contour elements are under
    plate load and transverse shear. Seven displacements(three strains, tree curvatures, derivation of twisting)
    from the internal loads can be determined. The calculations are based of
    [Song1990]_, [Qin2002]_ and [Librescu1991]_.
    
    Coordinate systems:
        * x-y: cross section coordinate system, arbitrary.
        
    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        Timoschenko bending with restrained warping stiffness matrix (7x7).
    _compliance_matrix: numpy.ndarray
        Timoschenko bending with restrained warping complience matrix (7x7).
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
    """
    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        kwargs['open_cs'] = False
        super().__init__(cross_section_id, z_beam, **kwargs)

    def _update_if_required(self):
        """
        Update the cached values and does the cross section calculation for all load cases if required.
        """
        if self._update_required:
            self._update_required = False

            if len(self._discreet_geometry.cells) == 0:
                raise RuntimeError('SongCrossSectionProcessor can only process cross-section with at least one cell.')

            self._cog, self._inertia = self._calc_inertia()
            
            self._set_torsional_function_values(self._discreet_geometry.cells)

            E_3 = np.identity(3)
            pole = self.pole
            node_warpings_true_pole = self._get_warping(pole)
            stiffness_matrix_elastic_true_pole = self._get_stiffness_matrix(True, E_3, pole, node_warpings_true_pole)
            Pi = -stiffness_matrix_elastic_true_pole[idx(37)]/stiffness_matrix_elastic_true_pole[idx(33)]
            node_warpings = {node: value - Pi for (node, value) in node_warpings_true_pole.items()}
            self._set_element_warping(node_warpings)
            
            self._stiffness_matrix = self._get_stiffness_matrix(True, E_3, pole, node_warpings)
            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)
            self._stiffness = TimoschenkoWithRestrainedWarpingStiffness(self._stiffness_matrix)

            self._elastic_center, psma, self._principal_axis_angle = get_elatic_center_and_bending_principal_axis_angle(self._stiffness_matrix[2:5, 2:5])
            self._shear_principal_axis_angle = self._principal_axis_angle
            self._set_augmented_transformation_matrices()

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _get_stiffness_matrix(self, warping_part, atm, pole, node_warpings):
        """
        Returns the stiffness matrix of the cross section.
        
        Parameters
        ----------
        warping_part: bool
            If True, the last row and column (restrained warping) is calculated.
        atm: numpy.ndarray
            Augmented transformation matrix into the coordinate system for the stiffness calculation.
        pole: Vector
            Rotation pole of the rigid body rotation of the cross section. Not yet transformed.
        node_warpings: dict(INode, float)
            Warping for each node.
        
        Returns
        -------
        numpy.ndarray
            7x7 cross section stiffness matrix.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        S_half_py = np.zeros((7, 7), dtype=dtype)
        S_half = cython.declare(cython_dtype[:, :], S_half_py)
        if warping_part:
            pole = transform_location_m(atm, pole)
        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            pos1 = transform_location_m(atm, node_midsurface_positions[element.node1])
            pos2 = transform_location_m(atm, node_midsurface_positions[element.node2])
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y
            dx_ds: cython_dtype = element.dx_ds(self._discreet_geometry)
            dy_ds: cython_dtype = element.dy_ds(self._discreet_geometry)
            psi_e: cython_dtype = element.torsional_function_value
            
            if warping_part:
                a1: cython_dtype = -(y1-pole.y)*dy_ds - (x1-pole.x)*dx_ds
                a2: cython_dtype = -(y2-pole.y)*dy_ds - (x2-pole.x)*dx_ds
                F_w1: cython_dtype = node_warpings[element.node1]
                F_w2: cython_dtype = node_warpings[element.node2]
            
            K_py = element.shell.stiffness.K_Song
            K = cython.declare(cython_dtype[:, :], K_py)
            A_s_py = element.shell.stiffness.A_s
            A_s = cython.declare(cython_dtype[:, :], A_s_py)

            int_const = l
            int_x = l/2*(x1+x2)
            int_y = l/2*(y1+y2)
            int_x_x = l/3*(x1**2+x1*x2+x2**2)
            int_y_y = l/3*(y1**2+y1*y2+y2**2)
            int_x_y = l/6*((2*x1+x2)*y1 + (x1+2*x2)*y2)
            
            if warping_part:
                int_a = l/2*(a1+a2)
                int_x_a = l/6*((2*a1+a2)*x1 + (a1+2*a2)*x2)
                int_y_a = l/6*((2*a1+a2)*y1 + (a1+2*a2)*y2)
                int_a_a = l/3*(a1**2+a1*a2+a2**2)
                int_F_w = l/2*(F_w1+F_w2)
                int_x_F_w = l/6*((2*F_w1+F_w2)*x1 + (F_w1+2*F_w2)*x2)
                int_y_F_w = l/6*((2*F_w1+F_w2)*y1 + (F_w1+2*F_w2)*y2)
                int_F_w_a = l/6*((2*F_w1+F_w2)*a1 + (F_w1+2*F_w2)*a2)
                int_F_w_F_w = l/3*(F_w1**2+F_w1*F_w2+F_w2**2)
            
            S_half[idx(11)] += (K[22]*dx_ds**2 + A_s[44]*dy_ds**2)*int_const
            S_half[idx(12)] += -(A_s[44] - K[22])*dx_ds*dy_ds*int_const
            S_half[idx(13)] += K[21]*dx_ds*int_const
            S_half[idx(14)] += -K[23]*dx_ds**2*int_const + K[21]*dx_ds*int_y
            S_half[idx(15)] += -K[23]*dx_ds*dy_ds*int_const - K[21]*dx_ds*int_x
            S_half[idx(16)] += K[22]*dx_ds*int_const*psi_e
            S_half[idx(22)] += (A_s[44]*dx_ds**2 + K[22]*dy_ds**2)*int_const
            S_half[idx(23)] += K[21]*dy_ds*int_const
            S_half[idx(24)] += -K[23]*dx_ds*dy_ds*int_const + K[21]*dy_ds*int_y
            S_half[idx(25)] += -K[23]*dy_ds**2*int_const - K[21]*dy_ds*int_x
            S_half[idx(26)] += K[22]*dy_ds*int_const*psi_e
            S_half[idx(33)] += K[11]*int_const
            S_half[idx(34)] += -K[13]*dx_ds*int_const + K[11]*int_y
            S_half[idx(35)] += -K[13]*dy_ds*int_const - K[11]*int_x
            S_half[idx(36)] += K[12]*int_const*psi_e
            S_half[idx(44)] += K[43]*dx_ds**2*int_const - (K[13] + K[41])*dx_ds*int_y + K[11]*int_y_y
            S_half[idx(45)] += K[43]*dx_ds*dy_ds*int_const + K[41]*dx_ds*int_x - K[13]*dy_ds*int_y - K[11]*int_x_y
            S_half[idx(46)] += -(K[42]*dx_ds*int_const - K[12]*int_y)*psi_e
            S_half[idx(55)] += K[43]*dy_ds**2*int_const + (K[13] + K[41])*dy_ds*int_x + K[11]*int_x_x
            S_half[idx(56)] += -(K[42]*dy_ds*int_const + K[12]*int_x)*psi_e
            S_half[idx(66)] += K[22]*int_const*psi_e**2

            if warping_part:
                S_half[idx(17)] += -K[21]*dx_ds*int_F_w - K[23]*dx_ds*int_a
                S_half[idx(27)] += -K[21]*dy_ds*int_F_w - K[23]*dy_ds*int_a
                S_half[idx(37)] += -K[11]*int_F_w - K[13]*int_a
                S_half[idx(47)] += K[41]*dx_ds*int_F_w + K[43]*dx_ds*int_a - K[11]*int_y_F_w - K[13]*int_y_a
                S_half[idx(57)] += K[41]*dy_ds*int_F_w + K[43]*dy_ds*int_a + K[11]*int_x_F_w + K[13]*int_x_a
                S_half[idx(67)] += -(K[21]*int_F_w + K[23]*int_a)*psi_e
                S_half[idx(77)] += K[11]*int_F_w_F_w + (K[13] + K[41])*int_F_w_a + K[43]*int_a_a

        return symmetrize(S_half_py)
    
    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.
        
        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.
        
        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()
        displacements = np.dot(self._compliance_matrix, internal_loads.tolist()).flatten()
        return TimoschenkoWithRestrainedWarpingDisplacements.from_list(displacements)

    @staticmethod
    def stress_state_from_strain_state_function(K, A_s, strain_state):
        """
        Calculates the stress state from a given strain state.

        Parameters
        ----------
        strain_state: dict(str, function(float))
            Stain state:
                epsilon_zz_0: function(float)
                    Axial strain from primary warping as function of the contur coordinate.
                gamma_zs: function(float)
                    Membran shear strain as function of the contur coordinate.
                kappa_zz: function(float)
                    Curvature from secondary warping as function of the contur coordinate.
                gamma_zn: function(float)
                    Transverse shear strain as function of the contur coordinate.

        Returns
        -------
        dict(str, function(float))
            Stress state as function of the contur coordinate:
                Resultant forces:    N_zz, N_zs, N_zn, N_sn
                Resultant moments:   M_zz, M_zs
        """
        with_transverse_shear_stiffness = True

        N_zz = lambda s: K[11] * strain_state['epsilon_zz_0'](s) + K[12] * strain_state['gamma_zs'](s) + K[13] * \
                         strain_state['kappa_zz'](s)
        N_zs = lambda s: K[21] * strain_state['epsilon_zz_0'](s) + K[22] * strain_state['gamma_zs'](s) + K[23] * \
                         strain_state['kappa_zz'](s)
        M_zz = lambda s: K[41] * strain_state['epsilon_zz_0'](s) + K[42] * strain_state['gamma_zs'](s) + K[43] * \
                         strain_state['kappa_zz'](s)
        M_zs = lambda s: K[51] * strain_state['epsilon_zz_0'](s) + K[52] * strain_state['gamma_zs'](s) + K[53] * \
                         strain_state['kappa_zz'](s)
        N_zn = lambda s: (A_s[44] * strain_state['gamma_zn'](s)) if with_transverse_shear_stiffness else 0
        N_sn = lambda s: (A_s[45] * strain_state['gamma_zn'](s)) if with_transverse_shear_stiffness else 0

        return {'N_zz': N_zz, 'N_zs': N_zs, 'N_zn': N_zn, 'N_sn': N_sn, 'M_zz': M_zz, 'M_zs': M_zs}

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        l = self._discreet_geometry.element_reference_length_dict[element]

        dx_ds = element.dx_ds(self._discreet_geometry)
        dy_ds = element.dy_ds(self._discreet_geometry)

        def x(s): return node_midsurface_positions[element.node1].x + dx_ds * s

        def y(s): return node_midsurface_positions[element.node1].y + dy_ds * s

        def warping(s): return element.node1_warping + (element.node2_warping - element.node1_warping) * s / l

        # Displacements
        gamma_xz = displacements.strain[0]
        gamma_yz = displacements.strain[1]
        w_0_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = displacements.twisting_derivation

        # Strain state: kinematic
        def epsilon_zz_0(s): return w_0_d + - Theta_y_d * x(s) + Theta_x_d * y(s) - phi_dd * warping(s)

        def kappa_zz(s): return - Theta_y_d * dy_ds - Theta_x_d * dx_ds - phi_dd * element.q_midsurface(self._discreet_geometry, s, self.pole)

        def gamma_zs(s): return gamma_xz * dx_ds + gamma_yz * dy_ds + element.torsional_function_value * phi_d

        def gamma_zn(s): return gamma_xz * dy_ds - gamma_yz * dx_ds

        bounds = (0, l)
        strain_state = {'epsilon_zz_0': lambda s: get_function_with_bounds(epsilon_zz_0, s, bounds),
                        'gamma_zs': lambda s: get_function_with_bounds(gamma_zs, s, bounds),
                        'kappa_zz': lambda s: get_function_with_bounds(kappa_zz, s, bounds),
                        'gamma_zn': lambda s: get_function_with_bounds(gamma_zn, s, bounds)}

        # Stress state: material laws
        stress_state = self.stress_state_from_strain_state_function(element.shell.stiffness.K_Song, element.shell.stiffness.A_s, strain_state)

        # Load state
        return ElementLoadState(strain_state, stress_state)


class JungCrossSectionProcessor(BaseCompositeCrossSectionProcessor):
    """
    Represents a anisotropic cross section analysis for thin-walled composite structures.
    The geometry has to be made of one or multiple closed sections. The contour elements are
    under plate load and transverse shear. Seven displacements(three strains, tree curvatures, derivation of twisting)
    from the internal loads can be determined. The calculations are based of [Jung2002b]_.

    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        Timoschenko bending with restrained warping stiffness matrix (7x7).
    _compliance_matrix: numpy.ndarray
        Timoschenko bending with restrained warping compliance matrix (7x7).
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.

    _Q, _P, _R: numpy.ndarray
        Matrices for the calculation of the cucualting shear flows.
    _b, _B: numpy.ndarray
        Matrices for intermediate calculation.
    _p: numpy.ndarray
        Matrix for the shear correction.
    _K_bb, _K_bv, _K_vv: numpy.ndarray
        Parts of the stiffness matrix.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam, **kwargs)

    @property
    def _ignore_warping(self) -> bool:
        return False

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            dtype = self._dtype

            self._cog, self._inertia = self._calc_inertia()

            cells = self._discreet_geometry.cells
            num_cells = len(cells)

            self._set_torsional_function_values(cells)
            self._cutted_discreet_geometry = self.get_cutted_discreet_geometry_from_discreet_geometry(
                self._discreet_geometry,
            )

            # Clear contur integral values
            for n in self._cutted_discreet_geometry.nodes:
                n.integral_values = dict()
            for e in self._cutted_discreet_geometry.elements:
                e.integral_values_0 = dict()
                e.integral_values_l_half = dict()
                e.integral_values_l = dict()
            for n in self._discreet_geometry.nodes:
                n.integral_values = dict()
            for e in self._discreet_geometry.elements:
                e.integral_values_0 = dict()
                e.integral_values_l_half = dict()
                e.integral_values_l = dict()

            # Calculate warping
            self._set_contur_integral_values_recursive(self._contur_integral_functions_warping, ['omega'])

            # # DEBUG
            # for cell in cells:
            #     int_omega_ds = 0.
            #     int_ds = 0.
            #     element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
            #     for e in cell.elements:
            #         l = element_reference_length_dict[e]
            #         int_omega_ds += (e.integral_values_0['omega'] +\
            #                          e.integral_values_l['omega']) / 2. * l
            #         int_ds += l
            #
            #     omega_offset = - int_omega_ds / int_ds
            #     log.warning(f'omega offset cells: {omega_offset}')

            int_omega_ds = 0.
            int_ds = 0.
            element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
            elements_for_omega_mean = set()
            if len(cells) > 0:
                for cell in cells:
                    elements_for_omega_mean.update(cell.elements)
            else:
                elements_for_omega_mean = self._discreet_geometry.elements
            for e in elements_for_omega_mean:
                l = element_reference_length_dict[e]
                int_omega_ds += (e.integral_values_0['omega'] + e.integral_values_l['omega']) / 2. * l
                int_ds += l

            omega_offset = - int_omega_ds / int_ds
            log.debug(f'omega offset used: {omega_offset}')
            for n in self.discreet_geometry.nodes:
                n.integral_values['omega'] += omega_offset
            for e in self.discreet_geometry.elements:
                e.integral_values_0['omega'] += omega_offset
                e.integral_values_l['omega'] += omega_offset

            self._set_contur_integral_values(
                self._contur_integral_functions,
                [
                    'int_A11_ds',
                    'int_B16_ds',
                    'int_D16_ds',
                    'int_A11_x_ds',
                    'int_A11_y_ds',
                    'int_A11_omega_ds',
                    'int_B16_x_ds',
                    'int_B16_y_ds',
                    'int_B16_omega_ds',
                ]
            )

            self._set_segment_cell_mapping(4, cells)

            # Set H matrices to elements
            for segment, Z in self._Z_dict.items():
                for element in segment.elements:
                    is_in_dir = DiscreetCrossSectionGeometry.is_element_in_direction_of_segment(element, segment)
                    if is_in_dir == True:
                        element.Z = Z
                    elif is_in_dir == False:
                        element.Z = -Z
                    else:
                        # Not in cell
                        if not self._open_cs:
                            raise RuntimeError('Open cross-section part.')
                        else:
                            pass
                        # assert np.all(Z == 0)
                        # element.Z = Z  # Z is zero

            self._set_cell_matrices(cells)

            # Solve is faster than using inverse of Q
            self._b = lgs_solve(self._Q, self._P, dtype=dtype)
            self._B = lgs_solve(self._Q, self._R, dtype=dtype)

            for e in self._discreet_geometry.elements:
                if e.Z is not None:
                    e.b = e.Z @ self._b
                    e.B = e.Z @ self._B
                else:
                    e.b = np.zeros((4, 4*num_cells), dtype=dtype)
                    e.B = np.zeros((4, 4*num_cells), dtype=dtype)
                    if not self._open_cs:
                        raise RuntimeError('Open cross-section part.')

            self._set_cross_section_matrix_K_bb()

            # TODO: nicht invertieren sondern LGS lösen, K_bb ist schlecht konditioniert
            self._K_bb_inv = np.linalg.inv(self._K_bb)

            self._set_element_f_r_matrices()

            self._set_cross_section_matrix_p()

            self._set_cross_section_matrices_K_vv_and_K_bv()

            p1 = self._p[:, 0:5]
            p2 = self._p[:, 5:7]

            K_bb = self._K_bb
            K_vv = self._K_vv
            K_bv = self._K_bv

            K11 = K_bb + 2 * K_bv @ p1 + p1.T @ K_vv @ p1
            K12 = K_bv @ p2 + p1.T @ K_vv @ p2
            K22 = p2.T @ K_vv @ p2

            K = np.vstack((np.hstack((K11, K12)), np.hstack((K12.T, K22))))

            # Rearrange the K matrix: shear stiffness from the back to the front
            V = np.zeros((7, 7), dtype=dtype)
            ones = ((0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 0), (6, 1))
            for r, c in ones:
                V[r, c] = 1.
            K = V.T @ K @ V

            if self._ignore_warping:
                self._stiffness_matrix = K[0:6, 0:6]
                self._stiffness = TimoschenkoStiffness(self._stiffness_matrix)
            else:
                self._stiffness_matrix = K
                self._stiffness = TimoschenkoWithRestrainedWarpingStiffness(self._stiffness_matrix)

            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)

            self._elastic_center, self._principal_axis_stiffness, self._principal_axis_angle = \
                get_elatic_center_and_bending_principal_axis_angle(self._stiffness_matrix[2:5, 2:5])

            # TODO: stimmt das so?
            self._shear_principal_axis_stiffness, self._shear_principal_axis_angle = \
                get_shear_principal_axis_stiffness_and_angle(self._stiffness_matrix[0:3, 0:3])

            self._set_augmented_transformation_matrices()

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _set_cell_matrices(self, cells):
        """
        Set the Q, P and R matrices.

        Parameters
        ----------
        cells: list(Cell)
            List of cells.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        num_cells = len(cells)
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict

        Q: np.ndarray[dtype] = np.zeros((4*num_cells, 4*num_cells), dtype=dtype)
        P: np.ndarray[dtype] = np.zeros((4*num_cells, 5), dtype=dtype)
        R: np.ndarray[dtype] = np.zeros((4*num_cells, 5), dtype=dtype)

        for cell_idx in range(num_cells):
            cell = cells[cell_idx]

            Q_cell: np.ndarray[dtype] = np.zeros((4, 4*num_cells), dtype=dtype)
            P_cell: np.ndarray[dtype] = np.zeros((4, 5), dtype=dtype)
            R_cell: np.ndarray[dtype] = np.zeros((4, 5), dtype=dtype)

            A_i = cell.area
            elements = cell.elements
            for element in elements:
                Q_element_half_py: np.ndarray[dtype] = np.zeros((4, 4), dtype=dtype)
                P_element_py: np.ndarray[dtype] = np.zeros((4, 5), dtype=dtype)
                R_element_py: np.ndarray[dtype] = np.zeros((4, 5), dtype=dtype)
                Q_element_half = cython.declare(cython_dtype[:, :], Q_element_half_py)
                P_element = cython.declare(cython_dtype[:, :], P_element_py)
                R_element = cython.declare(cython_dtype[:, :], R_element_py)

                is_element_in_direction_of_cell = DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(
                    element, cell.elements
                )
                assert is_element_in_direction_of_cell is not None
                direction_factor = 1. if is_element_in_direction_of_cell else -1.
                direction_factor_global = (1. if element.is_in_global_integration_direction else -1.) * direction_factor

                l: cython_dtype = element_reference_length_dict[element]
                C_py: np.ndarray[dtype] = element.shell.stiffness.K_Jung
                C = cython.declare(cython_dtype[:, :], C_py)
                Z_element_py: np.ndarray[dtype] = element.Z
                assert Z_element_py is not None
                Z_element = cython.declare(cython_dtype[:, :], Z_element_py)

                pos1 = node_midsurface_positions[element.node1]
                pos2 = node_midsurface_positions[element.node2]
                x1: cython_dtype = pos1.x
                y1: cython_dtype = pos1.y
                x2: cython_dtype = pos2.x
                y2: cython_dtype = pos2.y

                omega1: cython_dtype = element.node1.integral_values['omega']
                omega2: cython_dtype = element.node2.integral_values['omega']

                int_A11_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_A11_ds']
                int_A11_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_A11_ds']
                int_B16_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_B16_ds']
                int_B16_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_B16_ds']
                int_D16_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_D16_ds']
                int_D16_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_D16_ds']
                int_A11_x_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_A11_x_ds']
                int_A11_x_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_A11_x_ds']
                int_A11_y_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_A11_y_ds']
                int_A11_y_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_A11_y_ds']
                int_A11_omega_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_A11_omega_ds']
                int_A11_omega_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_A11_omega_ds']
                int_B16_x_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_B16_x_ds']
                int_B16_x_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_B16_x_ds']
                int_B16_y_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_B16_y_ds']
                int_B16_y_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_B16_y_ds']
                int_B16_omega_ds1: cython_dtype = direction_factor_global * element.integral_values_0['int_B16_omega_ds']
                int_B16_omega_ds2: cython_dtype = direction_factor_global * element.integral_values_l['int_B16_omega_ds']
                int_A11_x_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_A11_x_ds']
                int_A11_y_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_A11_y_ds']
                int_A11_omega_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_A11_omega_ds']
                int_B16_x_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_B16_x_ds']
                int_B16_y_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_B16_y_ds']
                int_B16_omega_ds3: cython_dtype = direction_factor_global * element.integral_values_l_half['int_B16_omega_ds']

                Q_element_half[0, 0] = C[3, 3] * l
                Q_element_half[0, 1] = C[4, 3] * l
                Q_element_half[0, 2] = (1 / 2) * C[4, 3] * l * x1 + (1 / 2) * C[4, 3] * l * x2
                Q_element_half[0, 3] = (1 / 2) * C[4, 3] * l * y1 + (1 / 2) * C[4, 3] * l * y2
                Q_element_half[1, 1] = C[4, 4] * l
                Q_element_half[1, 2] = (1 / 2) * C[4, 4] * l * x1 + (1 / 2) * C[4, 4] * l * x2
                Q_element_half[1, 3] = (1 / 2) * C[4, 4] * l * y1 + (1 / 2) * C[4, 4] * l * y2
                Q_element_half[2, 2] = (1 / 3) * C[4, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * l * x1 * x2 + (1 / 3) * C[
                    4, 4] * l * x2 ** 2
                Q_element_half[2, 3] = (1 / 3) * C[4, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * l * x1 * y2 + (1 / 6) * C[
                    4, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * l * x2 * y2
                Q_element_half[3, 3] = (1 / 3) * C[4, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * l * y1 * y2 + (1 / 3) * C[
                    4, 4] * l * y2 ** 2

                P_element[0, 0] = C[0, 3] * l
                P_element[0, 1] = (1 / 2) * C[0, 3] * l * y1 + (1 / 2) * C[0, 3] * l * y2 - C[3, 1] * x1 + C[3, 1] * x2
                P_element[0, 2] = (1 / 2) * C[3, 0] * l * x1 + (1 / 2) * C[3, 0] * l * x2 - C[3, 1] * y1 + C[3, 1] * y2
                P_element[0, 3] = 2 * C[2, 3] * l
                P_element[0, 4] = (1 / 2) * C[1, 3] * x1 ** 2 - 1 / 2 * C[1, 3] * x2 ** 2 + (1 / 2) * C[
                    1, 3] * y1 ** 2 - 1 / 2 * C[1, 3] * y2 ** 2 + (1 / 2) * C[3, 0] * l * omega1 + (1 / 2) * C[
                                      3, 0] * l * omega2
                P_element[1, 0] = C[0, 4] * l
                P_element[1, 1] = (1 / 2) * C[0, 4] * l * y1 + (1 / 2) * C[0, 4] * l * y2 - C[4, 1] * x1 + C[4, 1] * x2
                P_element[1, 2] = (1 / 2) * C[4, 0] * l * x1 + (1 / 2) * C[4, 0] * l * x2 - C[4, 1] * y1 + C[4, 1] * y2
                P_element[1, 3] = 2 * C[2, 4] * l
                P_element[1, 4] = (1 / 2) * C[1, 4] * x1 ** 2 - 1 / 2 * C[1, 4] * x2 ** 2 + (1 / 2) * C[
                    1, 4] * y1 ** 2 - 1 / 2 * C[1, 4] * y2 ** 2 + (1 / 2) * C[4, 0] * l * omega1 + (1 / 2) * C[
                                      4, 0] * l * omega2
                P_element[2, 0] = (1 / 2) * C[0, 4] * l * x1 + (1 / 2) * C[0, 4] * l * x2
                P_element[2, 1] = (1 / 3) * C[0, 4] * l * x1 * y1 + (1 / 6) * C[0, 4] * l * x1 * y2 + (1 / 6) * C[
                    0, 4] * l * x2 * y1 + (1 / 3) * C[0, 4] * l * x2 * y2 - 1 / 2 * C[4, 1] * x1 ** 2 + (1 / 2) * C[
                                      4, 1] * x2 ** 2
                P_element[2, 2] = (1 / 3) * C[4, 0] * l * x1 ** 2 + (1 / 3) * C[4, 0] * l * x1 * x2 + (1 / 3) * C[
                    4, 0] * l * x2 ** 2 - 1 / 2 * C[4, 1] * x1 * y1 + (1 / 2) * C[4, 1] * x1 * y2 - 1 / 2 * C[
                                      4, 1] * x2 * y1 + (1 / 2) * C[4, 1] * x2 * y2
                P_element[2, 3] = C[2, 4] * l * x1 + C[2, 4] * l * x2
                P_element[2, 4] = (1 / 3) * C[1, 4] * x1 ** 3 + (1 / 3) * C[1, 4] * x1 * y1 ** 2 - 1 / 6 * C[
                    1, 4] * x1 * y1 * y2 - 1 / 6 * C[1, 4] * x1 * y2 ** 2 - 1 / 3 * C[1, 4] * x2 ** 3 + (1 / 6) * C[
                                      1, 4] * x2 * y1 ** 2 + (1 / 6) * C[1, 4] * x2 * y1 * y2 - 1 / 3 * C[
                                      1, 4] * x2 * y2 ** 2 + (1 / 3) * C[4, 0] * l * omega1 * x1 + (1 / 6) * C[
                                      4, 0] * l * omega1 * x2 + (1 / 6) * C[4, 0] * l * omega2 * x1 + (1 / 3) * C[
                                      4, 0] * l * omega2 * x2
                P_element[3, 0] = (1 / 2) * C[0, 4] * l * y1 + (1 / 2) * C[0, 4] * l * y2
                P_element[3, 1] = (1 / 3) * C[0, 4] * l * y1 ** 2 + (1 / 3) * C[0, 4] * l * y1 * y2 + (1 / 3) * C[
                    0, 4] * l * y2 ** 2 - 1 / 2 * C[4, 1] * x1 * y1 - 1 / 2 * C[4, 1] * x1 * y2 + (1 / 2) * C[
                                      4, 1] * x2 * y1 + (1 / 2) * C[4, 1] * x2 * y2
                P_element[3, 2] = (1 / 3) * C[4, 0] * l * x1 * y1 + (1 / 6) * C[4, 0] * l * x1 * y2 + (1 / 6) * C[
                    4, 0] * l * x2 * y1 + (1 / 3) * C[4, 0] * l * x2 * y2 - 1 / 2 * C[4, 1] * y1 ** 2 + (1 / 2) * C[
                                      4, 1] * y2 ** 2
                P_element[3, 3] = C[2, 4] * l * y1 + C[2, 4] * l * y2
                P_element[3, 4] = (1 / 3) * C[1, 4] * x1 ** 2 * y1 + (1 / 6) * C[1, 4] * x1 ** 2 * y2 - 1 / 6 * C[
                    1, 4] * x1 * x2 * y1 + (1 / 6) * C[1, 4] * x1 * x2 * y2 - 1 / 6 * C[1, 4] * x2 ** 2 * y1 - 1 / 3 * \
                                  C[1, 4] * x2 ** 2 * y2 + (1 / 3) * C[1, 4] * y1 ** 3 - 1 / 3 * C[1, 4] * y2 ** 3 + (
                                              1 / 3) * C[4, 0] * l * omega1 * y1 + (1 / 6) * C[
                                      4, 0] * l * omega1 * y2 + (1 / 6) * C[4, 0] * l * omega2 * y1 + (1 / 3) * C[
                                      4, 0] * l * omega2 * y2

                R_element[0, 0] = (1 / 2) * C[3, 3] * int_A11_ds1 * l + (1 / 2) * C[3, 3] * int_A11_ds2 * l - 1 / 2 * C[
                    4, 3] * int_B16_ds1 * l - 1 / 2 * C[4, 3] * int_B16_ds2 * l
                R_element[0, 1] = (1 / 6) * C[3, 3] * int_A11_y_ds1 * l + (1 / 6) * C[3, 3] * int_A11_y_ds2 * l + (
                            2 / 3) * C[3, 3] * int_A11_y_ds3 * l - 1 / 6 * C[4, 3] * int_B16_y_ds1 * l - 1 / 6 * C[
                                      4, 3] * int_B16_y_ds2 * l - 2 / 3 * C[4, 3] * int_B16_y_ds3 * l
                R_element[0, 2] = -1 / 6 * C[3, 3] * int_A11_x_ds1 * l - 1 / 6 * C[3, 3] * int_A11_x_ds2 * l - 2 / 3 * \
                                  C[3, 3] * int_A11_x_ds3 * l + (1 / 6) * C[4, 3] * int_B16_x_ds1 * l + (1 / 6) * C[
                                      4, 3] * int_B16_x_ds2 * l + (2 / 3) * C[4, 3] * int_B16_x_ds3 * l
                R_element[0, 3] = -C[3, 3] * int_B16_ds1 * l - C[3, 3] * int_B16_ds2 * l + C[4, 3] * int_D16_ds1 * l + \
                                  C[4, 3] * int_D16_ds2 * l
                R_element[0, 4] = -1 / 6 * C[3, 3] * int_A11_omega_ds1 * l - 1 / 6 * C[
                    3, 3] * int_A11_omega_ds2 * l - 2 / 3 * C[3, 3] * int_A11_omega_ds3 * l + (1 / 6) * C[
                                      4, 3] * int_B16_omega_ds1 * l + (1 / 6) * C[4, 3] * int_B16_omega_ds2 * l + (
                                              2 / 3) * C[4, 3] * int_B16_omega_ds3 * l
                R_element[1, 0] = (1 / 2) * C[4, 3] * int_A11_ds1 * l + (1 / 2) * C[4, 3] * int_A11_ds2 * l - 1 / 2 * C[
                    4, 4] * int_B16_ds1 * l - 1 / 2 * C[4, 4] * int_B16_ds2 * l
                R_element[1, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l + (1 / 6) * C[4, 3] * int_A11_y_ds2 * l + (
                            2 / 3) * C[4, 3] * int_A11_y_ds3 * l - 1 / 6 * C[4, 4] * int_B16_y_ds1 * l - 1 / 6 * C[
                                      4, 4] * int_B16_y_ds2 * l - 2 / 3 * C[4, 4] * int_B16_y_ds3 * l
                R_element[1, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l - 1 / 6 * C[4, 3] * int_A11_x_ds2 * l - 2 / 3 * \
                                  C[4, 3] * int_A11_x_ds3 * l + (1 / 6) * C[4, 4] * int_B16_x_ds1 * l + (1 / 6) * C[
                                      4, 4] * int_B16_x_ds2 * l + (2 / 3) * C[4, 4] * int_B16_x_ds3 * l
                R_element[1, 3] = -C[4, 3] * int_B16_ds1 * l - C[4, 3] * int_B16_ds2 * l + C[4, 4] * int_D16_ds1 * l + \
                                  C[4, 4] * int_D16_ds2 * l
                R_element[1, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l - 2 / 3 * C[4, 3] * int_A11_omega_ds3 * l + (1 / 6) * C[
                                      4, 4] * int_B16_omega_ds1 * l + (1 / 6) * C[4, 4] * int_B16_omega_ds2 * l + (
                                              2 / 3) * C[4, 4] * int_B16_omega_ds3 * l
                R_element[2, 0] = (1 / 3) * C[4, 3] * int_A11_ds1 * l * x1 + (1 / 6) * C[
                    4, 3] * int_A11_ds1 * l * x2 + (1 / 6) * C[4, 3] * int_A11_ds2 * l * x1 + (1 / 3) * C[
                                      4, 3] * int_A11_ds2 * l * x2 - 1 / 3 * C[4, 4] * int_B16_ds1 * l * x1 - 1 / 6 * C[
                                      4, 4] * int_B16_ds1 * l * x2 - 1 / 6 * C[4, 4] * int_B16_ds2 * l * x1 - 1 / 3 * C[
                                      4, 4] * int_B16_ds2 * l * x2
                R_element[2, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l * x1 + (1 / 6) * C[
                    4, 3] * int_A11_y_ds2 * l * x2 + (1 / 3) * C[4, 3] * int_A11_y_ds3 * l * x1 + (1 / 3) * C[
                                      4, 3] * int_A11_y_ds3 * l * x2 - 1 / 6 * C[
                                      4, 4] * int_B16_y_ds1 * l * x1 - 1 / 6 * C[
                                      4, 4] * int_B16_y_ds2 * l * x2 - 1 / 3 * C[
                                      4, 4] * int_B16_y_ds3 * l * x1 - 1 / 3 * C[4, 4] * int_B16_y_ds3 * l * x2
                R_element[2, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l * x1 - 1 / 6 * C[
                    4, 3] * int_A11_x_ds2 * l * x2 - 1 / 3 * C[4, 3] * int_A11_x_ds3 * l * x1 - 1 / 3 * C[
                                      4, 3] * int_A11_x_ds3 * l * x2 + (1 / 6) * C[4, 4] * int_B16_x_ds1 * l * x1 + (
                                              1 / 6) * C[4, 4] * int_B16_x_ds2 * l * x2 + (1 / 3) * C[
                                      4, 4] * int_B16_x_ds3 * l * x1 + (1 / 3) * C[4, 4] * int_B16_x_ds3 * l * x2
                R_element[2, 3] = -2 / 3 * C[4, 3] * int_B16_ds1 * l * x1 - 1 / 3 * C[
                    4, 3] * int_B16_ds1 * l * x2 - 1 / 3 * C[4, 3] * int_B16_ds2 * l * x1 - 2 / 3 * C[
                                      4, 3] * int_B16_ds2 * l * x2 + (2 / 3) * C[4, 4] * int_D16_ds1 * l * x1 + (
                                              1 / 3) * C[4, 4] * int_D16_ds1 * l * x2 + (1 / 3) * C[
                                      4, 4] * int_D16_ds2 * l * x1 + (2 / 3) * C[4, 4] * int_D16_ds2 * l * x2
                R_element[2, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l * x1 - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l * x2 - 1 / 3 * C[4, 3] * int_A11_omega_ds3 * l * x1 - 1 / 3 * C[
                                      4, 3] * int_A11_omega_ds3 * l * x2 + (1 / 6) * C[
                                      4, 4] * int_B16_omega_ds1 * l * x1 + (1 / 6) * C[
                                      4, 4] * int_B16_omega_ds2 * l * x2 + (1 / 3) * C[
                                      4, 4] * int_B16_omega_ds3 * l * x1 + (1 / 3) * C[
                                      4, 4] * int_B16_omega_ds3 * l * x2
                R_element[3, 0] = (1 / 3) * C[4, 3] * int_A11_ds1 * l * y1 + (1 / 6) * C[
                    4, 3] * int_A11_ds1 * l * y2 + (1 / 6) * C[4, 3] * int_A11_ds2 * l * y1 + (1 / 3) * C[
                                      4, 3] * int_A11_ds2 * l * y2 - 1 / 3 * C[4, 4] * int_B16_ds1 * l * y1 - 1 / 6 * C[
                                      4, 4] * int_B16_ds1 * l * y2 - 1 / 6 * C[4, 4] * int_B16_ds2 * l * y1 - 1 / 3 * C[
                                      4, 4] * int_B16_ds2 * l * y2
                R_element[3, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l * y1 + (1 / 6) * C[
                    4, 3] * int_A11_y_ds2 * l * y2 + (1 / 3) * C[4, 3] * int_A11_y_ds3 * l * y1 + (1 / 3) * C[
                                      4, 3] * int_A11_y_ds3 * l * y2 - 1 / 6 * C[
                                      4, 4] * int_B16_y_ds1 * l * y1 - 1 / 6 * C[
                                      4, 4] * int_B16_y_ds2 * l * y2 - 1 / 3 * C[
                                      4, 4] * int_B16_y_ds3 * l * y1 - 1 / 3 * C[4, 4] * int_B16_y_ds3 * l * y2
                R_element[3, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l * y1 - 1 / 6 * C[
                    4, 3] * int_A11_x_ds2 * l * y2 - 1 / 3 * C[4, 3] * int_A11_x_ds3 * l * y1 - 1 / 3 * C[
                                      4, 3] * int_A11_x_ds3 * l * y2 + (1 / 6) * C[4, 4] * int_B16_x_ds1 * l * y1 + (
                                              1 / 6) * C[4, 4] * int_B16_x_ds2 * l * y2 + (1 / 3) * C[
                                      4, 4] * int_B16_x_ds3 * l * y1 + (1 / 3) * C[4, 4] * int_B16_x_ds3 * l * y2
                R_element[3, 3] = -2 / 3 * C[4, 3] * int_B16_ds1 * l * y1 - 1 / 3 * C[
                    4, 3] * int_B16_ds1 * l * y2 - 1 / 3 * C[4, 3] * int_B16_ds2 * l * y1 - 2 / 3 * C[
                                      4, 3] * int_B16_ds2 * l * y2 + (2 / 3) * C[4, 4] * int_D16_ds1 * l * y1 + (
                                              1 / 3) * C[4, 4] * int_D16_ds1 * l * y2 + (1 / 3) * C[
                                      4, 4] * int_D16_ds2 * l * y1 + (2 / 3) * C[4, 4] * int_D16_ds2 * l * y2
                R_element[3, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l * y1 - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l * y2 - 1 / 3 * C[4, 3] * int_A11_omega_ds3 * l * y1 - 1 / 3 * C[
                                      4, 3] * int_A11_omega_ds3 * l * y2 + (1 / 6) * C[
                                      4, 4] * int_B16_omega_ds1 * l * y1 + (1 / 6) * C[
                                      4, 4] * int_B16_omega_ds2 * l * y2 + (1 / 3) * C[
                                      4, 4] * int_B16_omega_ds3 * l * y1 + (1 / 3) * C[
                                      4, 4] * int_B16_omega_ds3 * l * y2

                Q_element_py = symmetrize(Q_element_half_py)

                Q_cell += direction_factor * Q_element_py @ Z_element
                P_cell += direction_factor * P_element_py
                R_cell += direction_factor * direction_factor_global * R_element_py

            Q[4 * cell_idx:4 * (cell_idx+1), :] = Q_cell
            P_cell[0, 3] += 2 * A_i
            P[4 * cell_idx:4 * (cell_idx+1), :] = P_cell
            R[4 * cell_idx:4 * (cell_idx+1), :] = R_cell

        self._Q = Q
        self._P = P
        self._R = R

    def _contur_integral_functions_warping(self, element, integration_in_element_direction,
                                           last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the warping contur integral value for one element.

        Parameters
        ----------
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        l = self._cutted_discreet_geometry.element_reference_length_dict[element]
        direction_factor = 1. if integration_in_element_direction else -1.

        r_torsional = direction_factor*(element.r_midsurface(self._cutted_discreet_geometry, self.pole) - element.torsional_function_value)

        l_values = {}
        l_half_values = {}

        l_values['omega'] = last_values['omega'] + l*r_torsional

        return l_values, l_half_values

    def _contur_integral_functions(self, element, integration_in_element_direction,
                                   last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the contur integral values for one element.

        Parameters
        ----------
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        x1 = last_position.x
        x2 = current_position.x
        y1 = last_position.y
        y2 = current_position.y

        l = self._discreet_geometry.element_reference_length_dict[element]

        A_11 = element.shell.stiffness.K_normal[0, 0]
        B_16 = element.shell.stiffness.K_normal[0, 4]
        D_16 = element.shell.stiffness.K_normal[2, 4]

        omega1 = last_node.integral_values['omega']
        omega2 = current_node.integral_values['omega']

        l_values = {}
        l_half_values = {}

        l_values['int_A11_ds'] = last_values['int_A11_ds'] + A_11 * l
        l_values['int_B16_ds'] = last_values['int_B16_ds'] + B_16 * l
        l_values['int_D16_ds'] = last_values['int_D16_ds'] + D_16 * l
        l_values['int_A11_x_ds'] = last_values['int_A11_x_ds'] + A_11 * l * (x1 + x2) / 2
        l_values['int_A11_y_ds'] = last_values['int_A11_y_ds'] + A_11 * l * (y1 + y2) / 2
        l_values['int_A11_omega_ds'] = last_values['int_A11_omega_ds'] + A_11 * l * (omega1 + omega2) / 2
        l_values['int_B16_x_ds'] = last_values['int_B16_x_ds'] + B_16 * l * (x1 + x2) / 2
        l_values['int_B16_y_ds'] = last_values['int_B16_y_ds'] + B_16 * l * (y1 + y2) / 2
        l_values['int_B16_omega_ds'] = last_values['int_B16_omega_ds'] + B_16 * l * (omega1 + omega2) / 2
        l_half_values['int_A11_x_ds'] = last_values['int_A11_x_ds'] + A_11 * l * (3 * x1 + x2) / 8
        l_half_values['int_A11_y_ds'] = last_values['int_A11_y_ds'] + A_11 * l * (3 * y1 + y2) / 8
        l_half_values['int_A11_omega_ds'] = last_values['int_A11_omega_ds'] + A_11 * l * (3 * omega1 + omega2) / 8
        l_half_values['int_B16_x_ds'] = last_values['int_B16_x_ds'] + B_16 * l * (3 * x1 + x2) / 8
        l_half_values['int_B16_y_ds'] = last_values['int_B16_y_ds'] + B_16 * l * (3 * y1 + y2) / 8
        l_half_values['int_B16_omega_ds'] = last_values['int_B16_omega_ds'] + B_16 * l * (3 * omega1 + omega2) / 8

        return l_values, l_half_values

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _set_cross_section_matrix_K_bb(self):
        """
        Set the K_bb matrix.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        K_bb_half_py: np.ndarray[dtype] = np.zeros((5, 5), dtype=dtype)
        K_bb_half = cython.declare(cython_dtype[:, :], K_bb_half_py)

        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            C_py: np.ndarray[dtype] = element.shell.stiffness.K_Jung
            C = cython.declare(cython_dtype[:, :], C_py)
            b_element_py: np.ndarray[dtype] = element.b
            b_element = cython.declare(cython_dtype[:, :], b_element_py)

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            omega1: cython_dtype = element.node1.integral_values['omega']
            omega2: cython_dtype = element.node2.integral_values['omega']

            K_bb_half[0, 0] += C[0, 0] * l + C[3, 3] * b_element[0, 0] ** 2 * l + 2 * C[4, 3] * b_element[0, 0] * \
                               b_element[1, 0] * l + C[4, 3] * b_element[0, 0] * b_element[2, 0] * l * x1 + C[4, 3] * \
                               b_element[0, 0] * b_element[2, 0] * l * x2 + C[4, 3] * b_element[0, 0] * b_element[
                                   3, 0] * l * y1 + C[4, 3] * b_element[0, 0] * b_element[3, 0] * l * y2 + C[4, 4] * \
                               b_element[1, 0] ** 2 * l + C[4, 4] * b_element[1, 0] * b_element[2, 0] * l * x1 + C[
                                   4, 4] * b_element[1, 0] * b_element[2, 0] * l * x2 + C[4, 4] * b_element[1, 0] * \
                               b_element[3, 0] * l * y1 + C[4, 4] * b_element[1, 0] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[2, 0] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 0] ** 2 * l * y2 ** 2
            K_bb_half[0, 1] += (1 / 2) * C[0, 0] * l * y1 + (1 / 2) * C[0, 0] * l * y2 + C[1, 0] * x1 - C[1, 0] * x2 + \
                               C[3, 3] * b_element[0, 0] * b_element[0, 1] * l + C[4, 3] * b_element[0, 0] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 1] * l * y2 + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 0] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 0] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 0] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 0] * l * y2 + C[4, 4] * b_element[1, 0] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 0] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 0] * b_element[3, 1] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[
                                   2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 0] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[3, 0] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 0] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] * b_element[2, 1] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * \
                               b_element[2, 1] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   2, 1] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y2 ** 2
            K_bb_half[0, 2] += -1 / 2 * C[0, 0] * l * x1 - 1 / 2 * C[0, 0] * l * x2 + C[1, 0] * y1 - C[1, 0] * y2 + C[
                3, 3] * b_element[0, 0] * b_element[0, 2] * l + C[4, 3] * b_element[0, 0] * b_element[1, 2] * l + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 2] * l * x1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[
                                   3, 2] * l * y2 + C[4, 3] * b_element[0, 2] * b_element[1, 0] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[3, 0] * l * y2 + C[
                                   4, 4] * b_element[1, 0] * b_element[1, 2] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * \
                               b_element[2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[
                                   2, 2] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 2] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 2] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 2] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y2 ** 2
            K_bb_half[0, 3] += 2 * C[2, 0] * l + C[3, 3] * b_element[0, 0] * b_element[0, 3] * l + C[4, 3] * b_element[
                0, 0] * b_element[1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 3] * l * x1 + (1 / 2) * \
                               C[4, 3] * b_element[0, 0] * b_element[2, 3] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[
                                   3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[1, 0] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[3, 0] * l * y2 + C[
                                   4, 4] * b_element[1, 0] * b_element[1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * \
                               b_element[2, 3] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[
                                   2, 3] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 3] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 3] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 3] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y2 ** 2
            K_bb_half[0, 4] += -1 / 2 * C[0, 0] * l * omega1 - 1 / 2 * C[0, 0] * l * omega2 + (1 / 2) * C[
                1, 0] * x1 ** 2 - 1 / 2 * C[1, 0] * x2 ** 2 + (1 / 2) * C[1, 0] * y1 ** 2 - 1 / 2 * C[1, 0] * y2 ** 2 + \
                               C[3, 3] * b_element[0, 0] * b_element[0, 4] * l + C[4, 3] * b_element[0, 0] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[
                                   1, 0] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 0] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 0] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 0] * l * y2 + C[4, 4] * b_element[1, 0] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 0] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 0] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 0] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 0] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 0] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[1, 1] += (1 / 3) * C[0, 0] * l * y1 ** 2 + (1 / 3) * C[0, 0] * l * y1 * y2 + (1 / 3) * C[
                0, 0] * l * y2 ** 2 + C[1, 0] * x1 * y1 + C[1, 0] * x1 * y2 - C[1, 0] * x2 * y1 - C[1, 0] * x2 * y2 + C[
                                   1, 1] * x1 ** 2 / l - 2 * C[1, 1] * x1 * x2 / l + C[1, 1] * x2 ** 2 / l + C[3, 3] * \
                               b_element[0, 1] ** 2 * l + 2 * C[4, 3] * b_element[0, 1] * b_element[1, 1] * l + C[
                                   4, 3] * b_element[0, 1] * b_element[2, 1] * l * x1 + C[4, 3] * b_element[0, 1] * \
                               b_element[2, 1] * l * x2 + C[4, 3] * b_element[0, 1] * b_element[3, 1] * l * y1 + C[
                                   4, 3] * b_element[0, 1] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[
                                   1, 1] ** 2 * l + C[4, 4] * b_element[1, 1] * b_element[2, 1] * l * x1 + C[4, 4] * \
                               b_element[1, 1] * b_element[2, 1] * l * x2 + C[4, 4] * b_element[1, 1] * b_element[
                                   3, 1] * l * y1 + C[4, 4] * b_element[1, 1] * b_element[3, 1] * l * y2 + (1 / 3) * C[
                                   4, 4] * b_element[2, 1] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] ** 2 * l * x2 ** 2 + (
                                           2 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x1 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x2 * y1 + (
                                           2 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 1] ** 2 * l * y1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 1] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[
                                   3, 1] ** 2 * l * y2 ** 2
            K_bb_half[1, 2] += -1 / 3 * C[0, 0] * l * x1 * y1 - 1 / 6 * C[0, 0] * l * x1 * y2 - 1 / 6 * C[
                0, 0] * l * x2 * y1 - 1 / 3 * C[0, 0] * l * x2 * y2 - 1 / 2 * C[1, 0] * x1 ** 2 + (1 / 2) * C[
                                   1, 0] * x2 ** 2 + (1 / 2) * C[1, 0] * y1 ** 2 - 1 / 2 * C[1, 0] * y2 ** 2 + C[
                                   1, 1] * x1 * y1 / l - C[1, 1] * x1 * y2 / l - C[1, 1] * x2 * y1 / l + C[
                                   1, 1] * x2 * y2 / l + C[3, 3] * b_element[0, 1] * b_element[0, 2] * l + C[4, 3] * \
                               b_element[0, 1] * b_element[1, 2] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[
                                   2, 2] * l * x1 + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 2] * l * x2 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[3, 2] * l * y1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 2] * l * y2 + C[4, 3] * b_element[0, 2] * \
                               b_element[1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 2] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 2] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 2] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 2] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 2] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 2] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 2] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y2 ** 2
            K_bb_half[1, 3] += C[2, 0] * l * y1 + C[2, 0] * l * y2 + 2 * C[2, 1] * x1 - 2 * C[2, 1] * x2 + C[3, 3] * \
                               b_element[0, 1] * b_element[0, 3] * l + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 3] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 3] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 3] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 3] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y2 ** 2
            K_bb_half[1, 4] += -1 / 3 * C[0, 0] * l * omega1 * y1 - 1 / 6 * C[0, 0] * l * omega1 * y2 - 1 / 6 * C[
                0, 0] * l * omega2 * y1 - 1 / 3 * C[0, 0] * l * omega2 * y2 - 1 / 2 * C[1, 0] * omega1 * x1 + (1 / 2) * \
                               C[1, 0] * omega1 * x2 - 1 / 2 * C[1, 0] * omega2 * x1 + (1 / 2) * C[
                                   1, 0] * omega2 * x2 + (1 / 3) * C[1, 0] * x1 ** 2 * y1 + (1 / 6) * C[
                                   1, 0] * x1 ** 2 * y2 - 1 / 6 * C[1, 0] * x1 * x2 * y1 + (1 / 6) * C[
                                   1, 0] * x1 * x2 * y2 - 1 / 6 * C[1, 0] * x2 ** 2 * y1 - 1 / 3 * C[
                                   1, 0] * x2 ** 2 * y2 + (1 / 3) * C[1, 0] * y1 ** 3 - 1 / 3 * C[1, 0] * y2 ** 3 + (
                                           1 / 2) * C[1, 1] * x1 ** 3 / l - 1 / 2 * C[1, 1] * x1 ** 2 * x2 / l - 1 / 2 * \
                               C[1, 1] * x1 * x2 ** 2 / l + (1 / 2) * C[1, 1] * x1 * y1 ** 2 / l - 1 / 2 * C[
                                   1, 1] * x1 * y2 ** 2 / l + (1 / 2) * C[1, 1] * x2 ** 3 / l - 1 / 2 * C[
                                   1, 1] * x2 * y1 ** 2 / l + (1 / 2) * C[1, 1] * x2 * y2 ** 2 / l + C[3, 3] * \
                               b_element[0, 1] * b_element[0, 4] * l + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[2, 2] += (1 / 3) * C[0, 0] * l * x1 ** 2 + (1 / 3) * C[0, 0] * l * x1 * x2 + (1 / 3) * C[
                0, 0] * l * x2 ** 2 - C[1, 0] * x1 * y1 + C[1, 0] * x1 * y2 - C[1, 0] * x2 * y1 + C[1, 0] * x2 * y2 + C[
                                   1, 1] * y1 ** 2 / l - 2 * C[1, 1] * y1 * y2 / l + C[1, 1] * y2 ** 2 / l + C[3, 3] * \
                               b_element[0, 2] ** 2 * l + 2 * C[4, 3] * b_element[0, 2] * b_element[1, 2] * l + C[
                                   4, 3] * b_element[0, 2] * b_element[2, 2] * l * x1 + C[4, 3] * b_element[0, 2] * \
                               b_element[2, 2] * l * x2 + C[4, 3] * b_element[0, 2] * b_element[3, 2] * l * y1 + C[
                                   4, 3] * b_element[0, 2] * b_element[3, 2] * l * y2 + C[4, 4] * b_element[
                                   1, 2] ** 2 * l + C[4, 4] * b_element[1, 2] * b_element[2, 2] * l * x1 + C[4, 4] * \
                               b_element[1, 2] * b_element[2, 2] * l * x2 + C[4, 4] * b_element[1, 2] * b_element[
                                   3, 2] * l * y1 + C[4, 4] * b_element[1, 2] * b_element[3, 2] * l * y2 + (1 / 3) * C[
                                   4, 4] * b_element[2, 2] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 2] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 2] ** 2 * l * x2 ** 2 + (
                                           2 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x2 * y1 + (
                                           2 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] ** 2 * l * y1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 2] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[
                                   3, 2] ** 2 * l * y2 ** 2
            K_bb_half[2, 3] += -C[2, 0] * l * x1 - C[2, 0] * l * x2 + 2 * C[2, 1] * y1 - 2 * C[2, 1] * y2 + C[3, 3] * \
                               b_element[0, 2] * b_element[0, 3] * l + C[4, 3] * b_element[0, 2] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[
                                   1, 2] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 2] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 2] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[3, 2] * l * y2 + C[4, 4] * b_element[1, 2] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 2] * b_element[3, 3] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 2] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 2] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 2] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 2] * b_element[2, 3] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 2] * \
                               b_element[2, 3] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   2, 3] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y2 ** 2
            K_bb_half[2, 4] += (1 / 3) * C[0, 0] * l * omega1 * x1 + (1 / 6) * C[0, 0] * l * omega1 * x2 + (1 / 6) * C[
                0, 0] * l * omega2 * x1 + (1 / 3) * C[0, 0] * l * omega2 * x2 - 1 / 2 * C[1, 0] * omega1 * y1 + (
                                           1 / 2) * C[1, 0] * omega1 * y2 - 1 / 2 * C[1, 0] * omega2 * y1 + (1 / 2) * C[
                                   1, 0] * omega2 * y2 - 1 / 3 * C[1, 0] * x1 ** 3 - 1 / 3 * C[1, 0] * x1 * y1 ** 2 + (
                                           1 / 6) * C[1, 0] * x1 * y1 * y2 + (1 / 6) * C[1, 0] * x1 * y2 ** 2 + (
                                           1 / 3) * C[1, 0] * x2 ** 3 - 1 / 6 * C[1, 0] * x2 * y1 ** 2 - 1 / 6 * C[
                                   1, 0] * x2 * y1 * y2 + (1 / 3) * C[1, 0] * x2 * y2 ** 2 + (1 / 2) * C[
                                   1, 1] * x1 ** 2 * y1 / l - 1 / 2 * C[1, 1] * x1 ** 2 * y2 / l - 1 / 2 * C[
                                   1, 1] * x2 ** 2 * y1 / l + (1 / 2) * C[1, 1] * x2 ** 2 * y2 / l + (1 / 2) * C[
                                   1, 1] * y1 ** 3 / l - 1 / 2 * C[1, 1] * y1 ** 2 * y2 / l - 1 / 2 * C[
                                   1, 1] * y1 * y2 ** 2 / l + (1 / 2) * C[1, 1] * y2 ** 3 / l + C[3, 3] * b_element[
                                   0, 2] * b_element[0, 4] * l + C[4, 3] * b_element[0, 2] * b_element[1, 4] * l + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 4] * l * x1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[2, 4] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[
                                   3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[1, 2] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[2, 2] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[
                                   3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[3, 2] * l * y2 + C[
                                   4, 4] * b_element[1, 2] * b_element[1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 2] * \
                               b_element[2, 4] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   2, 4] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 4] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 4] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 4] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   3, 2] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 2] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y2 ** 2
            K_bb_half[3, 3] += 4 * C[2, 2] * l + C[3, 3] * b_element[0, 3] ** 2 * l + 2 * C[4, 3] * b_element[0, 3] * \
                               b_element[1, 3] * l + C[4, 3] * b_element[0, 3] * b_element[2, 3] * l * x1 + C[4, 3] * \
                               b_element[0, 3] * b_element[2, 3] * l * x2 + C[4, 3] * b_element[0, 3] * b_element[
                                   3, 3] * l * y1 + C[4, 3] * b_element[0, 3] * b_element[3, 3] * l * y2 + C[4, 4] * \
                               b_element[1, 3] ** 2 * l + C[4, 4] * b_element[1, 3] * b_element[2, 3] * l * x1 + C[
                                   4, 4] * b_element[1, 3] * b_element[2, 3] * l * x2 + C[4, 4] * b_element[1, 3] * \
                               b_element[3, 3] * l * y1 + C[4, 4] * b_element[1, 3] * b_element[3, 3] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[2, 3] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 3] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 3] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 3] ** 2 * l * y2 ** 2
            K_bb_half[3, 4] += -C[2, 0] * l * omega1 - C[2, 0] * l * omega2 + C[2, 1] * x1 ** 2 - C[2, 1] * x2 ** 2 + C[
                2, 1] * y1 ** 2 - C[2, 1] * y2 ** 2 + C[3, 3] * b_element[0, 3] * b_element[0, 4] * l + C[4, 3] * \
                               b_element[0, 3] * b_element[1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[
                                   2, 4] * l * x1 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 4] * l * x2 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[3, 4] * l * y1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * \
                               b_element[1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 3] * l * y2 + C[4, 4] * b_element[1, 3] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 3] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 3] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 3] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 3] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 3] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 3] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 3] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[4, 4] += (1 / 3) * C[0, 0] * l * omega1 ** 2 + (1 / 3) * C[0, 0] * l * omega1 * omega2 + (1 / 3) * \
                               C[0, 0] * l * omega2 ** 2 - 2 / 3 * C[1, 0] * omega1 * x1 ** 2 + (1 / 3) * C[
                                   1, 0] * omega1 * x1 * x2 + (1 / 3) * C[1, 0] * omega1 * x2 ** 2 - 2 / 3 * C[
                                   1, 0] * omega1 * y1 ** 2 + (1 / 3) * C[1, 0] * omega1 * y1 * y2 + (1 / 3) * C[
                                   1, 0] * omega1 * y2 ** 2 - 1 / 3 * C[1, 0] * omega2 * x1 ** 2 - 1 / 3 * C[
                                   1, 0] * omega2 * x1 * x2 + (2 / 3) * C[1, 0] * omega2 * x2 ** 2 - 1 / 3 * C[
                                   1, 0] * omega2 * y1 ** 2 - 1 / 3 * C[1, 0] * omega2 * y1 * y2 + (2 / 3) * C[
                                   1, 0] * omega2 * y2 ** 2 + (1 / 3) * C[1, 1] * x1 ** 4 / l - 1 / 3 * C[
                                   1, 1] * x1 ** 3 * x2 / l + (2 / 3) * C[1, 1] * x1 ** 2 * y1 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x1 ** 2 * y1 * y2 / l - 1 / 3 * C[1, 1] * x1 ** 2 * y2 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x1 * x2 ** 3 / l - 1 / 3 * C[1, 1] * x1 * x2 * y1 ** 2 / l + (2 / 3) * C[
                                   1, 1] * x1 * x2 * y1 * y2 / l - 1 / 3 * C[1, 1] * x1 * x2 * y2 ** 2 / l + (1 / 3) * \
                               C[1, 1] * x2 ** 4 / l - 1 / 3 * C[1, 1] * x2 ** 2 * y1 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x2 ** 2 * y1 * y2 / l + (2 / 3) * C[1, 1] * x2 ** 2 * y2 ** 2 / l + (1 / 3) * \
                               C[1, 1] * y1 ** 4 / l - 1 / 3 * C[1, 1] * y1 ** 3 * y2 / l - 1 / 3 * C[
                                   1, 1] * y1 * y2 ** 3 / l + (1 / 3) * C[1, 1] * y2 ** 4 / l + C[3, 3] * b_element[
                                   0, 4] ** 2 * l + 2 * C[4, 3] * b_element[0, 4] * b_element[1, 4] * l + C[4, 3] * \
                               b_element[0, 4] * b_element[2, 4] * l * x1 + C[4, 3] * b_element[0, 4] * b_element[
                                   2, 4] * l * x2 + C[4, 3] * b_element[0, 4] * b_element[3, 4] * l * y1 + C[4, 3] * \
                               b_element[0, 4] * b_element[3, 4] * l * y2 + C[4, 4] * b_element[1, 4] ** 2 * l + C[
                                   4, 4] * b_element[1, 4] * b_element[2, 4] * l * x1 + C[4, 4] * b_element[1, 4] * \
                               b_element[2, 4] * l * x2 + C[4, 4] * b_element[1, 4] * b_element[3, 4] * l * y1 + C[
                                   4, 4] * b_element[1, 4] * b_element[3, 4] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 4] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 4] ** 2 * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * \
                               b_element[2, 4] * b_element[3, 4] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * \
                               b_element[3, 4] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 4] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 4] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 4] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 4] ** 2 * l * y2 ** 2

        self._K_bb = symmetrize(K_bb_half_py)

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _set_cross_section_matrices_K_vv_and_K_bv(self):
        """
        Set the K_vv and K_bv matrices.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        K_vv_py: np.ndarray[dtype] = np.zeros((2, 2), dtype=dtype)
        K_bv_py: np.ndarray[dtype] = np.zeros((5, 2), dtype=dtype)
        K_vv = cython.declare(cython_dtype[:, :], K_vv_py)
        K_bv = cython.declare(cython_dtype[:, :], K_bv_py)

        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            C_py: np.ndarray[dtype] = element.shell.stiffness.K_Jung
            C = cython.declare(cython_dtype[:, :], C_py)
            b_element_py: np.ndarray[dtype] = element.b
            b_element = cython.declare(cython_dtype[:, :], b_element_py)

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            f_r_1_py: np.ndarray[dtype] = element.f_r_1
            f_r_2_py: np.ndarray[dtype] = element.f_r_2
            f_r_3_py: np.ndarray[dtype] = element.f_r_3
            f_r_1 = cython.declare(cython_dtype[:, :], f_r_1_py)
            f_r_2 = cython.declare(cython_dtype[:, :], f_r_2_py)
            f_r_3 = cython.declare(cython_dtype[:, :], f_r_3_py)

            f_r_const_111: cython_dtype = f_r_1[0,0]
            f_r_const_112: cython_dtype = f_r_2[0,0]
            f_r_const_113: cython_dtype = f_r_3[0,0]

            f_r_const_121: cython_dtype = f_r_1[0,1]
            f_r_const_122: cython_dtype = f_r_2[0,1]
            f_r_const_123: cython_dtype = f_r_3[0,1]

            f_r_const_211: cython_dtype = f_r_1[1,0]
            f_r_const_212: cython_dtype = f_r_2[1,0]
            f_r_const_213: cython_dtype = f_r_3[1,0]

            f_r_const_221: cython_dtype = f_r_1[1,1]
            f_r_const_222: cython_dtype = f_r_2[1,1]
            f_r_const_223: cython_dtype = f_r_3[1,1]

            K_bv[0, 0] += (1 / 6) * C[3, 3] * b_element[0, 0] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 0] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 0] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 0] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 0] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 0] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 0] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 0] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 0] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 0] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 0] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 0] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 0] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 0] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_213 * l * y2
            K_bv[0, 1] += (1 / 6) * C[3, 3] * b_element[0, 0] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 0] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 0] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 0] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 0] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 0] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 0] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 0] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 0] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 0] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 0] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 0] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 0] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 0] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_223 * l * y2
            K_bv[1, 0] += (1 / 6) * C[3, 3] * b_element[0, 1] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 1] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 1] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 1] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 1] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 1] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 1] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 1] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 1] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 1] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 1] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 1] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 1] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 1] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_213 * l * y2
            K_bv[1, 1] += (1 / 6) * C[3, 3] * b_element[0, 1] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 1] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 1] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 1] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 1] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 1] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 1] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 1] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 1] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 1] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 1] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 1] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 1] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 1] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_223 * l * y2
            K_bv[2, 0] += (1 / 6) * C[3, 3] * b_element[0, 2] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 2] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 2] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 2] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 2] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 2] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 2] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 2] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 2] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 2] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 2] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 2] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 2] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 2] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_213 * l * y2
            K_bv[2, 1] += (1 / 6) * C[3, 3] * b_element[0, 2] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 2] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 2] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 2] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 2] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 2] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 2] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 2] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 2] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 2] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 2] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 2] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 2] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 2] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_223 * l * y2
            K_bv[3, 0] += (1 / 6) * C[3, 3] * b_element[0, 3] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 3] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 3] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 3] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 3] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 3] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 3] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 3] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 3] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 3] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 3] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 3] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 3] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 3] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_213 * l * y2
            K_bv[3, 1] += (1 / 6) * C[3, 3] * b_element[0, 3] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 3] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 3] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 3] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 3] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 3] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 3] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 3] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 3] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 3] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 3] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 3] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 3] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 3] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_223 * l * y2
            K_bv[4, 0] += (1 / 6) * C[3, 3] * b_element[0, 4] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 4] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 4] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 4] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 4] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 4] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 4] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 4] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 4] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 4] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 4] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 4] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 4] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 4] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_213 * l * y2
            K_bv[4, 1] += (1 / 6) * C[3, 3] * b_element[0, 4] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 4] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 4] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 4] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 4] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 4] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 4] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 4] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 4] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 4] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 4] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 4] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 4] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 4] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_223 * l * y2

            K_vv[0, 0] += (2 / 15) * C[3, 3] * f_r_const_111 ** 2 * l - 1 / 15 * C[
                3, 3] * f_r_const_111 * f_r_const_112 * l + (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_113 * l + (
                                      2 / 15) * C[3, 3] * f_r_const_112 ** 2 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_113 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 ** 2 * l + (4 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_211 * l - 1 / 15 * C[
                              4, 3] * f_r_const_111 * f_r_const_212 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_213 * l - 1 / 15 * C[
                              4, 3] * f_r_const_112 * f_r_const_211 * l + (4 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_212 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_213 * l + (2 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_212 * l + (16 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 ** 2 * l - 1 / 15 * C[4, 4] * f_r_const_211 * f_r_const_212 * l + (
                                      2 / 15) * C[4, 4] * f_r_const_211 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 ** 2 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_213 * l + (8 / 15) * C[4, 4] * f_r_const_213 ** 2 * l
            K_vv[0, 1] += (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 1 / 30 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_111 * f_r_const_123 * l - 1 / 30 * C[
                              3, 3] * f_r_const_112 * f_r_const_121 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_123 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_121 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_122 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_123 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_221 * l - 1 / 30 * C[
                              4, 3] * f_r_const_111 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_223 * l - 1 / 30 * C[
                              4, 3] * f_r_const_112 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_223 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_221 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_222 * l + (8 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_211 * l - 1 / 30 * C[
                              4, 3] * f_r_const_121 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_213 * l - 1 / 30 * C[
                              4, 3] * f_r_const_122 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_213 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_211 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_212 * l + (8 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_221 * l - 1 / 30 * C[
                              4, 4] * f_r_const_211 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_223 * l - 1 / 30 * C[
                              4, 4] * f_r_const_212 * f_r_const_221 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_223 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_221 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_222 * l + (8 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_223 * l
            K_vv[1, 0] += (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 1 / 30 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_111 * f_r_const_123 * l - 1 / 30 * C[
                              3, 3] * f_r_const_112 * f_r_const_121 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_123 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_121 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_122 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_123 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_221 * l - 1 / 30 * C[
                              4, 3] * f_r_const_111 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_223 * l - 1 / 30 * C[
                              4, 3] * f_r_const_112 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_223 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_221 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_222 * l + (8 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_211 * l - 1 / 30 * C[
                              4, 3] * f_r_const_121 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_213 * l - 1 / 30 * C[
                              4, 3] * f_r_const_122 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_213 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_211 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_212 * l + (8 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_221 * l - 1 / 30 * C[
                              4, 4] * f_r_const_211 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_223 * l - 1 / 30 * C[
                              4, 4] * f_r_const_212 * f_r_const_221 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_223 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_221 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_222 * l + (8 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_223 * l
            K_vv[1, 1] += (2 / 15) * C[3, 3] * f_r_const_121 ** 2 * l - 1 / 15 * C[
                3, 3] * f_r_const_121 * f_r_const_122 * l + (2 / 15) * C[3, 3] * f_r_const_121 * f_r_const_123 * l + (
                                      2 / 15) * C[3, 3] * f_r_const_122 ** 2 * l + (2 / 15) * C[
                              3, 3] * f_r_const_122 * f_r_const_123 * l + (8 / 15) * C[
                              3, 3] * f_r_const_123 ** 2 * l + (4 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_221 * l - 1 / 15 * C[
                              4, 3] * f_r_const_121 * f_r_const_222 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_223 * l - 1 / 15 * C[
                              4, 3] * f_r_const_122 * f_r_const_221 * l + (4 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_222 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_222 * l + (16 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_223 * l + (2 / 15) * C[
                              4, 4] * f_r_const_221 ** 2 * l - 1 / 15 * C[4, 4] * f_r_const_221 * f_r_const_222 * l + (
                                      2 / 15) * C[4, 4] * f_r_const_221 * f_r_const_223 * l + (2 / 15) * C[
                              4, 4] * f_r_const_222 ** 2 * l + (2 / 15) * C[
                              4, 4] * f_r_const_222 * f_r_const_223 * l + (8 / 15) * C[4, 4] * f_r_const_223 ** 2 * l

        self._K_vv = K_vv_py
        self._K_bv = K_bv_py

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _set_cross_section_matrix_p(self):
        """
        Set the shear correction matrix p.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        p_v_py: np.ndarray[dtype] = np.zeros((2, 2), dtype=dtype)
        p_q_py: np.ndarray[dtype] = np.zeros((2, 7), dtype=dtype)
        p_v = cython.declare(cython_dtype[:, :], p_v_py)
        p_q = cython.declare(cython_dtype[:, :], p_q_py)

        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict
        for element in elements:
            l: cython_dtype = element_reference_length_dict[element]
            C_py: np.ndarray[dtype] = element.shell.stiffness.K_Jung
            C = cython.declare(cython_dtype[:, :], C_py)
            b_element_py: np.ndarray[dtype] = element.b
            b_element = cython.declare(cython_dtype[:, :], b_element_py)

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            omega1: cython_dtype = element.node1.integral_values['omega']
            omega2: cython_dtype = element.node2.integral_values['omega']

            f_r_1_py: np.ndarray[dtype] = element.f_r_1
            f_r_2_py: np.ndarray[dtype] = element.f_r_2
            f_r_3_py: np.ndarray[dtype] = element.f_r_3
            f_r_1 = cython.declare(cython_dtype[:, :], f_r_1_py)
            f_r_2 = cython.declare(cython_dtype[:, :], f_r_2_py)
            f_r_3 = cython.declare(cython_dtype[:, :], f_r_3_py)

            f_r_const_111: cython_dtype = f_r_1[0, 0]
            f_r_const_112: cython_dtype = f_r_2[0, 0]
            f_r_const_113: cython_dtype = f_r_3[0, 0]

            f_r_const_121: cython_dtype = f_r_1[0, 1]
            f_r_const_122: cython_dtype = f_r_2[0, 1]
            f_r_const_123: cython_dtype = f_r_3[0, 1]

            f_r_const_211: cython_dtype = f_r_1[1, 0]
            f_r_const_212: cython_dtype = f_r_2[1, 0]
            f_r_const_213: cython_dtype = f_r_3[1, 0]

            f_r_const_221: cython_dtype = f_r_1[1, 1]
            f_r_const_222: cython_dtype = f_r_2[1, 1]
            f_r_const_223: cython_dtype = f_r_3[1, 1]

            p_v[0, 0] += 0.0666666666666664 * C[3, 3] * f_r_const_111 ** 2 * l - 0.0333333333333332 * C[
                3, 3] * f_r_const_111 * f_r_const_112 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_111 * f_r_const_113 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 ** 2 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_112 * f_r_const_113 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 ** 2 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_111 * f_r_const_211 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_111 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_111 * f_r_const_213 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_112 * f_r_const_211 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_112 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_112 * f_r_const_213 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_211 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_212 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_113 * f_r_const_213 * l
            p_v[0, 1] += 0.0666666666666664 * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 0.0166666666666666 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_111 * f_r_const_123 * l - 0.0166666666666666 * C[
                             3, 3] * f_r_const_112 * f_r_const_121 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_112 * f_r_const_123 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_121 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_122 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 * f_r_const_123 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_111 * f_r_const_221 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_111 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_111 * f_r_const_223 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_112 * f_r_const_221 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_112 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_112 * f_r_const_223 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_221 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_222 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_113 * f_r_const_223 * l
            p_v[1, 0] += 0.0666666666666664 * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 0.0166666666666666 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_111 * f_r_const_123 * l - 0.0166666666666666 * C[
                             3, 3] * f_r_const_112 * f_r_const_121 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_112 * f_r_const_123 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_121 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_122 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 * f_r_const_123 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_121 * f_r_const_211 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_121 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_121 * f_r_const_213 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_122 * f_r_const_211 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_122 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_122 * f_r_const_213 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_211 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_212 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_123 * f_r_const_213 * l
            p_v[1, 1] += 0.0666666666666664 * C[3, 3] * f_r_const_121 ** 2 * l - 0.0333333333333332 * C[
                3, 3] * f_r_const_121 * f_r_const_122 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_121 * f_r_const_123 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_122 ** 2 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_122 * f_r_const_123 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_123 ** 2 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_121 * f_r_const_221 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_121 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_121 * f_r_const_223 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_122 * f_r_const_221 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_122 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_122 * f_r_const_223 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_221 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_222 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_123 * f_r_const_223 * l

            p_q[0, 0] += 0.0833333333333333 * C[3, 0] * f_r_const_111 * l + 0.0833333333333333 * C[
                3, 0] * f_r_const_112 * l + 0.333333333333333 * C[3, 0] * f_r_const_113 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 0] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 0] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 0] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 0] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 0] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_113 * l * y2
            p_q[0, 1] += -0.0833333333333333 * C[1, 3] * f_r_const_111 * x1 + 0.0833333333333333 * C[
                1, 3] * f_r_const_111 * x2 - 0.0833333333333333 * C[1, 3] * f_r_const_112 * x1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * x2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * x1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * x2 + 0.0833333333333335 * C[
                             3, 0] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[
                             3, 0] * f_r_const_112 * l * y2 + 0.166666666666667 * C[
                             3, 0] * f_r_const_113 * l * y1 + 0.166666666666667 * C[
                             3, 0] * f_r_const_113 * l * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 1] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 1] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 1] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 1] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_113 * l * y2
            p_q[0, 2] += 0.0833333333333334 * C[0, 3] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_112 * l * x2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * x1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * x2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_111 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_111 * y2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * y2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * y1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 2] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 2] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 2] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 2] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_113 * l * y2
            p_q[0, 3] += 0.166666666666667 * C[3, 2] * f_r_const_111 * l + 0.166666666666667 * C[
                3, 2] * f_r_const_112 * l + 0.666666666666667 * C[3, 2] * f_r_const_113 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 3] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 3] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 3] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 3] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 3] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_113 * l * y2 + 0.0833333333333333 * f_r_const_111 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_111 * x1 * y2 + 0.0833333333333333 * f_r_const_111 * x2 * y1 + 0.0833333333333333 * f_r_const_112 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_112 * x1 * y2 + 0.0833333333333333 * f_r_const_112 * x2 * y1 + 0.333333333333333 * f_r_const_113 * l * (
                                     -omega1 / l + omega2 / l) - 0.333333333333333 * f_r_const_113 * x1 * y2 + 0.333333333333333 * f_r_const_113 * x2 * y1
            p_q[0, 4] += 0.0833333333333334 * C[0, 3] * f_r_const_111 * l * omega1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_112 * l * omega2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * omega1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * omega2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_111 * x1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_111 * x1 * x2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_111 * y1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_111 * y1 * y2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_112 * x1 * x2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_112 * x2 ** 2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_112 * y1 * y2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_112 * y2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * x1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * x2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * y1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * y2 ** 2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 4] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 4] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 4] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 4] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_113 * l * y2
            p_q[
                0, 5] += 0.0833333333333333 * f_r_const_111 * x1 - 0.0833333333333333 * f_r_const_111 * x2 + 0.0833333333333333 * f_r_const_112 * x1 - 0.0833333333333333 * f_r_const_112 * x2 + 0.333333333333333 * f_r_const_113 * x1 - 0.333333333333333 * f_r_const_113 * x2
            p_q[
                0, 6] += 0.0833333333333333 * f_r_const_111 * y1 - 0.0833333333333333 * f_r_const_111 * y2 + 0.0833333333333333 * f_r_const_112 * y1 - 0.0833333333333333 * f_r_const_112 * y2 + 0.333333333333333 * f_r_const_113 * y1 - 0.333333333333333 * f_r_const_113 * y2
            p_q[1, 0] += 0.0833333333333333 * C[3, 0] * f_r_const_121 * l + 0.0833333333333333 * C[
                3, 0] * f_r_const_122 * l + 0.333333333333333 * C[3, 0] * f_r_const_123 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 0] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 0] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 0] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 0] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 0] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_123 * l * y2
            p_q[1, 1] += -0.0833333333333333 * C[1, 3] * f_r_const_121 * x1 + 0.0833333333333333 * C[
                1, 3] * f_r_const_121 * x2 - 0.0833333333333333 * C[1, 3] * f_r_const_122 * x1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * x2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * x1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * x2 + 0.0833333333333335 * C[
                             3, 0] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[
                             3, 0] * f_r_const_122 * l * y2 + 0.166666666666667 * C[
                             3, 0] * f_r_const_123 * l * y1 + 0.166666666666667 * C[
                             3, 0] * f_r_const_123 * l * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 1] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 1] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 1] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 1] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_123 * l * y2
            p_q[1, 2] += 0.0833333333333334 * C[0, 3] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_122 * l * x2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * x1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * x2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_121 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_121 * y2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * y2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * y1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 2] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 2] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 2] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 2] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_123 * l * y2
            p_q[1, 3] += 0.166666666666667 * C[3, 2] * f_r_const_121 * l + 0.166666666666667 * C[
                3, 2] * f_r_const_122 * l + 0.666666666666667 * C[3, 2] * f_r_const_123 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 3] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 3] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 3] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 3] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 3] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_123 * l * y2 + 0.0833333333333333 * f_r_const_121 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_121 * x1 * y2 + 0.0833333333333333 * f_r_const_121 * x2 * y1 + 0.0833333333333333 * f_r_const_122 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_122 * x1 * y2 + 0.0833333333333333 * f_r_const_122 * x2 * y1 + 0.333333333333333 * f_r_const_123 * l * (
                                     -omega1 / l + omega2 / l) - 0.333333333333333 * f_r_const_123 * x1 * y2 + 0.333333333333333 * f_r_const_123 * x2 * y1
            p_q[1, 4] += 0.0833333333333334 * C[0, 3] * f_r_const_121 * l * omega1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_122 * l * omega2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * omega1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * omega2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_121 * x1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_121 * x1 * x2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_121 * y1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_121 * y1 * y2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_122 * x1 * x2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_122 * x2 ** 2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_122 * y1 * y2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_122 * y2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * x1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * x2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * y1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * y2 ** 2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 4] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 4] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 4] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 4] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_123 * l * y2
            p_q[
                1, 5] += 0.0833333333333333 * f_r_const_121 * x1 - 0.0833333333333333 * f_r_const_121 * x2 + 0.0833333333333333 * f_r_const_122 * x1 - 0.0833333333333333 * f_r_const_122 * x2 + 0.333333333333333 * f_r_const_123 * x1 - 0.333333333333333 * f_r_const_123 * x2
            p_q[
                1, 6] += 0.0833333333333333 * f_r_const_121 * y1 - 0.0833333333333333 * f_r_const_121 * y2 + 0.0833333333333333 * f_r_const_122 * y1 - 0.0833333333333333 * f_r_const_122 * y2 + 0.333333333333333 * f_r_const_123 * y1 - 0.333333333333333 * f_r_const_123 * y2

        self._p_v = p_v_py
        self._p_q = p_q_py
        self._p = -lgs_solve(p_v_py, p_q_py, dtype=dtype)

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    # @cython.cdivision(True)
    def _set_element_f_r_matrices(self):
        """
        Set the f_r matrices to the elements.
        """
        dtype = self._dtype
        cython_dtype = self._cython_dtype

        K_bb_inv_py: np.ndarray[dtype] = self._K_bb_inv
        K_bb_inv = cython.declare(cython_dtype[:, :], K_bb_inv_py)

        elements = self._discreet_geometry.elements
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        for element in elements:
            f_r_1_py: np.ndarray[dtype] = np.zeros((2, 2), dtype=dtype)
            f_r_2_py: np.ndarray[dtype] = np.zeros((2, 2), dtype=dtype)
            f_r_3_py: np.ndarray[dtype] = np.zeros((2, 2), dtype=dtype)
            f_r_1 = cython.declare(cython_dtype[:, :], f_r_1_py)
            f_r_2 = cython.declare(cython_dtype[:, :], f_r_2_py)
            f_r_3 = cython.declare(cython_dtype[:, :], f_r_3_py)

            B_element_py: np.ndarray[dtype] = element.B
            B_element = cython.declare(cython_dtype[:, :], B_element_py)

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1: cython_dtype = pos1.x
            y1: cython_dtype = pos1.y
            x2: cython_dtype = pos2.x
            y2: cython_dtype = pos2.y

            int_A11_ds1: cython_dtype = element.integral_values_0['int_A11_ds']
            int_A11_ds2: cython_dtype = element.integral_values_l['int_A11_ds']
            int_B16_ds1: cython_dtype = element.integral_values_0['int_B16_ds']
            int_B16_ds2: cython_dtype = element.integral_values_l['int_B16_ds']
            int_D16_ds1: cython_dtype = element.integral_values_0['int_D16_ds']
            int_D16_ds2: cython_dtype = element.integral_values_l['int_D16_ds']
            int_A11_x_ds1: cython_dtype = element.integral_values_0['int_A11_x_ds']
            int_A11_x_ds2: cython_dtype = element.integral_values_l['int_A11_x_ds']
            int_A11_y_ds1: cython_dtype = element.integral_values_0['int_A11_y_ds']
            int_A11_y_ds2: cython_dtype = element.integral_values_l['int_A11_y_ds']
            int_A11_omega_ds1: cython_dtype = element.integral_values_0['int_A11_omega_ds']
            int_A11_omega_ds2: cython_dtype = element.integral_values_l['int_A11_omega_ds']
            int_B16_x_ds1: cython_dtype = element.integral_values_0['int_B16_x_ds']
            int_B16_x_ds2: cython_dtype = element.integral_values_l['int_B16_x_ds']
            int_B16_y_ds1: cython_dtype = element.integral_values_0['int_B16_y_ds']
            int_B16_y_ds2: cython_dtype = element.integral_values_l['int_B16_y_ds']
            int_B16_omega_ds1: cython_dtype = element.integral_values_0['int_B16_omega_ds']
            int_B16_omega_ds2: cython_dtype = element.integral_values_l['int_B16_omega_ds']
            int_A11_x_ds3: cython_dtype = element.integral_values_l_half['int_A11_x_ds']
            int_A11_y_ds3: cython_dtype = element.integral_values_l_half['int_A11_y_ds']
            int_A11_omega_ds3: cython_dtype = element.integral_values_l_half['int_A11_omega_ds']
            int_B16_x_ds3: cython_dtype = element.integral_values_l_half['int_B16_x_ds']
            int_B16_y_ds3: cython_dtype = element.integral_values_l_half['int_B16_y_ds']
            int_B16_omega_ds3: cython_dtype = element.integral_values_l_half['int_B16_omega_ds']

            f_r_1[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - \
                          K_bb_inv[0, 2] * int_A11_ds1 - K_bb_inv[1, 2] * int_A11_y_ds1 + K_bb_inv[
                              2, 2] * int_A11_x_ds1 + 2 * K_bb_inv[3, 2] * int_B16_ds1 + K_bb_inv[
                              4, 2] * int_A11_omega_ds1
            f_r_1[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + \
                          K_bb_inv[0, 1] * int_A11_ds1 + K_bb_inv[1, 1] * int_A11_y_ds1 - K_bb_inv[
                              2, 1] * int_A11_x_ds1 - 2 * K_bb_inv[3, 1] * int_B16_ds1 - K_bb_inv[
                              4, 1] * int_A11_omega_ds1
            f_r_1[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + \
                          B_element[2, 0] * K_bb_inv[0, 2] * x1 + B_element[2, 1] * K_bb_inv[1, 2] * x1 + B_element[
                              2, 2] * K_bb_inv[2, 2] * x1 + B_element[2, 3] * K_bb_inv[3, 2] * x1 + B_element[2, 4] * \
                          K_bb_inv[4, 2] * x1 + B_element[3, 0] * K_bb_inv[0, 2] * y1 + B_element[3, 1] * K_bb_inv[
                              1, 2] * y1 + B_element[3, 2] * K_bb_inv[2, 2] * y1 + B_element[3, 3] * K_bb_inv[
                              3, 2] * y1 + B_element[3, 4] * K_bb_inv[4, 2] * y1 + K_bb_inv[0, 2] * int_B16_ds1 + \
                          K_bb_inv[1, 2] * int_B16_y_ds1 - K_bb_inv[2, 2] * int_B16_x_ds1 - 2 * K_bb_inv[
                              3, 2] * int_D16_ds1 - K_bb_inv[4, 2] * int_B16_omega_ds1
            f_r_1[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - \
                          B_element[2, 0] * K_bb_inv[0, 1] * x1 - B_element[2, 1] * K_bb_inv[1, 1] * x1 - B_element[
                              2, 2] * K_bb_inv[2, 1] * x1 - B_element[2, 3] * K_bb_inv[3, 1] * x1 - B_element[2, 4] * \
                          K_bb_inv[4, 1] * x1 - B_element[3, 0] * K_bb_inv[0, 1] * y1 - B_element[3, 1] * K_bb_inv[
                              1, 1] * y1 - B_element[3, 2] * K_bb_inv[2, 1] * y1 - B_element[3, 3] * K_bb_inv[
                              3, 1] * y1 - B_element[3, 4] * K_bb_inv[4, 1] * y1 - K_bb_inv[0, 1] * int_B16_ds1 - \
                          K_bb_inv[1, 1] * int_B16_y_ds1 + K_bb_inv[2, 1] * int_B16_x_ds1 + 2 * K_bb_inv[
                              3, 1] * int_D16_ds1 + K_bb_inv[4, 1] * int_B16_omega_ds1

            f_r_2[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - \
                          K_bb_inv[0, 2] * int_A11_ds2 - K_bb_inv[1, 2] * int_A11_y_ds2 + K_bb_inv[
                              2, 2] * int_A11_x_ds2 + 2 * K_bb_inv[3, 2] * int_B16_ds2 + K_bb_inv[
                              4, 2] * int_A11_omega_ds2
            f_r_2[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + \
                          K_bb_inv[0, 1] * int_A11_ds2 + K_bb_inv[1, 1] * int_A11_y_ds2 - K_bb_inv[
                              2, 1] * int_A11_x_ds2 - 2 * K_bb_inv[3, 1] * int_B16_ds2 - K_bb_inv[
                              4, 1] * int_A11_omega_ds2
            f_r_2[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + \
                          B_element[2, 0] * K_bb_inv[0, 2] * x2 + B_element[2, 1] * K_bb_inv[1, 2] * x2 + B_element[
                              2, 2] * K_bb_inv[2, 2] * x2 + B_element[2, 3] * K_bb_inv[3, 2] * x2 + B_element[2, 4] * \
                          K_bb_inv[4, 2] * x2 + B_element[3, 0] * K_bb_inv[0, 2] * y2 + B_element[3, 1] * K_bb_inv[
                              1, 2] * y2 + B_element[3, 2] * K_bb_inv[2, 2] * y2 + B_element[3, 3] * K_bb_inv[
                              3, 2] * y2 + B_element[3, 4] * K_bb_inv[4, 2] * y2 + K_bb_inv[0, 2] * int_B16_ds2 + \
                          K_bb_inv[1, 2] * int_B16_y_ds2 - K_bb_inv[2, 2] * int_B16_x_ds2 - 2 * K_bb_inv[
                              3, 2] * int_D16_ds2 - K_bb_inv[4, 2] * int_B16_omega_ds2
            f_r_2[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - \
                          B_element[2, 0] * K_bb_inv[0, 1] * x2 - B_element[2, 1] * K_bb_inv[1, 1] * x2 - B_element[
                              2, 2] * K_bb_inv[2, 1] * x2 - B_element[2, 3] * K_bb_inv[3, 1] * x2 - B_element[2, 4] * \
                          K_bb_inv[4, 1] * x2 - B_element[3, 0] * K_bb_inv[0, 1] * y2 - B_element[3, 1] * K_bb_inv[
                              1, 1] * y2 - B_element[3, 2] * K_bb_inv[2, 1] * y2 - B_element[3, 3] * K_bb_inv[
                              3, 1] * y2 - B_element[3, 4] * K_bb_inv[4, 1] * y2 - K_bb_inv[0, 1] * int_B16_ds2 - \
                          K_bb_inv[1, 1] * int_B16_y_ds2 + K_bb_inv[2, 1] * int_B16_x_ds2 + 2 * K_bb_inv[
                              3, 1] * int_D16_ds2 + K_bb_inv[4, 1] * int_B16_omega_ds2

            f_r_3[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - 1 / 2 * \
                          K_bb_inv[0, 2] * int_A11_ds1 - 1 / 2 * K_bb_inv[0, 2] * int_A11_ds2 - K_bb_inv[
                              1, 2] * int_A11_y_ds3 + K_bb_inv[2, 2] * int_A11_x_ds3 + K_bb_inv[3, 2] * int_B16_ds1 + \
                          K_bb_inv[3, 2] * int_B16_ds2 + K_bb_inv[4, 2] * int_A11_omega_ds3
            f_r_3[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + (
                                      1 / 2) * K_bb_inv[0, 1] * int_A11_ds1 + (1 / 2) * K_bb_inv[0, 1] * int_A11_ds2 + \
                          K_bb_inv[1, 1] * int_A11_y_ds3 - K_bb_inv[2, 1] * int_A11_x_ds3 - K_bb_inv[
                              3, 1] * int_B16_ds1 - K_bb_inv[3, 1] * int_B16_ds2 - K_bb_inv[4, 1] * int_A11_omega_ds3
            f_r_3[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + (
                                      1 / 2) * B_element[2, 0] * K_bb_inv[0, 2] * x1 + (1 / 2) * B_element[2, 0] * \
                          K_bb_inv[0, 2] * x2 + (1 / 2) * B_element[2, 1] * K_bb_inv[1, 2] * x1 + (1 / 2) * B_element[
                              2, 1] * K_bb_inv[1, 2] * x2 + (1 / 2) * B_element[2, 2] * K_bb_inv[2, 2] * x1 + (1 / 2) * \
                          B_element[2, 2] * K_bb_inv[2, 2] * x2 + (1 / 2) * B_element[2, 3] * K_bb_inv[3, 2] * x1 + (
                                      1 / 2) * B_element[2, 3] * K_bb_inv[3, 2] * x2 + (1 / 2) * B_element[2, 4] * \
                          K_bb_inv[4, 2] * x1 + (1 / 2) * B_element[2, 4] * K_bb_inv[4, 2] * x2 + (1 / 2) * B_element[
                              3, 0] * K_bb_inv[0, 2] * y1 + (1 / 2) * B_element[3, 0] * K_bb_inv[0, 2] * y2 + (1 / 2) * \
                          B_element[3, 1] * K_bb_inv[1, 2] * y1 + (1 / 2) * B_element[3, 1] * K_bb_inv[1, 2] * y2 + (
                                      1 / 2) * B_element[3, 2] * K_bb_inv[2, 2] * y1 + (1 / 2) * B_element[3, 2] * \
                          K_bb_inv[2, 2] * y2 + (1 / 2) * B_element[3, 3] * K_bb_inv[3, 2] * y1 + (1 / 2) * B_element[
                              3, 3] * K_bb_inv[3, 2] * y2 + (1 / 2) * B_element[3, 4] * K_bb_inv[4, 2] * y1 + (1 / 2) * \
                          B_element[3, 4] * K_bb_inv[4, 2] * y2 + (1 / 2) * K_bb_inv[0, 2] * int_B16_ds1 + (1 / 2) * \
                          K_bb_inv[0, 2] * int_B16_ds2 + K_bb_inv[1, 2] * int_B16_y_ds3 - K_bb_inv[
                              2, 2] * int_B16_x_ds3 - K_bb_inv[3, 2] * int_D16_ds1 - K_bb_inv[3, 2] * int_D16_ds2 - \
                          K_bb_inv[4, 2] * int_B16_omega_ds3
            f_r_3[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - 1 / 2 * \
                          B_element[2, 0] * K_bb_inv[0, 1] * x1 - 1 / 2 * B_element[2, 0] * K_bb_inv[
                              0, 1] * x2 - 1 / 2 * B_element[2, 1] * K_bb_inv[1, 1] * x1 - 1 / 2 * B_element[2, 1] * \
                          K_bb_inv[1, 1] * x2 - 1 / 2 * B_element[2, 2] * K_bb_inv[2, 1] * x1 - 1 / 2 * B_element[
                              2, 2] * K_bb_inv[2, 1] * x2 - 1 / 2 * B_element[2, 3] * K_bb_inv[3, 1] * x1 - 1 / 2 * \
                          B_element[2, 3] * K_bb_inv[3, 1] * x2 - 1 / 2 * B_element[2, 4] * K_bb_inv[
                              4, 1] * x1 - 1 / 2 * B_element[2, 4] * K_bb_inv[4, 1] * x2 - 1 / 2 * B_element[3, 0] * \
                          K_bb_inv[0, 1] * y1 - 1 / 2 * B_element[3, 0] * K_bb_inv[0, 1] * y2 - 1 / 2 * B_element[
                              3, 1] * K_bb_inv[1, 1] * y1 - 1 / 2 * B_element[3, 1] * K_bb_inv[1, 1] * y2 - 1 / 2 * \
                          B_element[3, 2] * K_bb_inv[2, 1] * y1 - 1 / 2 * B_element[3, 2] * K_bb_inv[
                              2, 1] * y2 - 1 / 2 * B_element[3, 3] * K_bb_inv[3, 1] * y1 - 1 / 2 * B_element[3, 3] * \
                          K_bb_inv[3, 1] * y2 - 1 / 2 * B_element[3, 4] * K_bb_inv[4, 1] * y1 - 1 / 2 * B_element[
                              3, 4] * K_bb_inv[4, 1] * y2 - 1 / 2 * K_bb_inv[0, 1] * int_B16_ds1 - 1 / 2 * K_bb_inv[
                              0, 1] * int_B16_ds2 - K_bb_inv[1, 1] * int_B16_y_ds3 + K_bb_inv[2, 1] * int_B16_x_ds3 + \
                          K_bb_inv[3, 1] * int_D16_ds1 + K_bb_inv[3, 1] * int_D16_ds2 + K_bb_inv[
                              4, 1] * int_B16_omega_ds3

            element.f_r_1 = f_r_1_py
            element.f_r_2 = f_r_2_py
            element.f_r_3 = f_r_3_py

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        dtype = self._dtype

        self._update_if_required()
        displacements = self._compliance_matrix.dot(internal_loads.tolist()).flatten()
        if self._ignore_warping:
            return TimoschenkoDisplacements.from_list(displacements)
        else:
            return TimoschenkoWithRestrainedWarpingDisplacements.from_list(displacements)

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        CompositeLoadState
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        dtype = self._dtype

        self._update_if_required()
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict

        l = element_reference_length_dict[element]
        C = element.shell.stiffness.K_Jung
        b_element = element.b

        pos1 = node_midsurface_positions[element.node1]
        pos2 = node_midsurface_positions[element.node2]
        x1 = pos1.x
        y1 = pos1.y
        x2 = pos2.x
        y2 = pos2.y

        omega1 = element.node1.integral_values['omega']
        omega2 = element.node2.integral_values['omega']

        f_r_1 = element.f_r_1
        f_r_2 = element.f_r_2
        f_r_3 = element.f_r_3

        f_r_const_111 = f_r_1[0, 0]
        f_r_const_112 = f_r_2[0, 0]
        f_r_const_113 = f_r_3[0, 0]

        f_r_const_121 = f_r_1[0, 1]
        f_r_const_122 = f_r_2[0, 1]
        f_r_const_123 = f_r_3[0, 1]

        f_r_const_211 = f_r_1[1, 0]
        f_r_const_212 = f_r_2[1, 0]
        f_r_const_213 = f_r_3[1, 0]

        f_r_const_221 = f_r_1[1, 1]
        f_r_const_222 = f_r_2[1, 1]
        f_r_const_223 = f_r_3[1, 1]

        # Cross section displacements
        gamma_xz = displacements.strain[0]
        gamma_yz = displacements.strain[1]
        w_p_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = 0 if self._ignore_warping else displacements.twisting_derivation

        # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
        q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz], dtype=dtype)
        v_s = self._p @ q_cs

        V_x_additional = v_s[0]
        V_y_additional = v_s[1]

        # Element displacements
        def epsilon_zz(s):
            return (Theta_x_d*(l*y1 - s*(y1 - y2)) - Theta_y_d*(l*x1 - s*(x1 - x2)) + l*w_p_d - phi_dd*(l*omega1 - s*(omega1 - omega2)))/l

        def kappa_zz(s):
            return (l*(Theta_x_d*(x1 - x2) + Theta_y_d*(y1 - y2)) + phi_dd*((x1 - x2)*(l*x1 - s*(x1 - x2)) + (y1 - y2)*(l*y1 + s*(-y1 + y2))))/l**2

        def kappa_zs(s):
            return 2*phi_d

        def N_zs(s):
            return (V_x_additional*(f_r_const_111*l**2 - l*s*(3*f_r_const_111 + f_r_const_112 - 4*f_r_const_113) + 2*s**2*(f_r_const_111 + f_r_const_112 - 2*f_r_const_113)) + V_y_additional*(f_r_const_121*l**2 - l*s*(3*f_r_const_121 + f_r_const_122 - 4*f_r_const_123) + 2*s**2*(f_r_const_121 + f_r_const_122 - 2*f_r_const_123)) + l**2*(Theta_x_d*b_element[0,1] + Theta_y_d*b_element[0,2] + b_element[0,0]*w_p_d + b_element[0,3]*phi_d + b_element[0,4]*phi_dd))/l**2

        def M_ss(s):
            return (V_x_additional*(f_r_const_211*l**2 - l*s*(3*f_r_const_211 + f_r_const_212 - 4*f_r_const_213) + 2*s**2*(f_r_const_211 + f_r_const_212 - 2*f_r_const_213)) + V_y_additional*(f_r_const_221*l**2 - l*s*(3*f_r_const_221 + f_r_const_222 - 4*f_r_const_223) + 2*s**2*(f_r_const_221 + f_r_const_222 - 2*f_r_const_223)) + l*(Theta_x_d*(b_element[1,1]*l + b_element[2,1]*(l*x1 - s*(x1 - x2)) + b_element[3,1]*(l*y1 - s*(y1 - y2))) + Theta_y_d*(b_element[1,2]*l + b_element[2,2]*(l*x1 - s*(x1 - x2)) + b_element[3,2]*(l*y1 - s*(y1 - y2))) + phi_d*(b_element[1,3]*l + b_element[2,3]*(l*x1 - s*(x1 - x2)) + b_element[3,3]*(l*y1 - s*(y1 - y2))) + phi_dd*(b_element[1,4]*l + b_element[2,4]*(l*x1 - s*(x1 - x2)) + b_element[3,4]*(l*y1 - s*(y1 - y2))) + w_p_d*(b_element[1,0]*l + b_element[2,0]*(l*x1 - s*(x1 - x2)) + b_element[3,0]*(l*y1 - s*(y1 - y2)))))/l**2

        def gamma_zn(s):  # Only reactive displacement with first order shear deformation theory
            return (-gamma_xz*(y1 - y2) + gamma_yz*(x1 - x2))/l

        # Stress state: material laws
        def N_zz(s):
            return C[0,0]*epsilon_zz(s) + C[0,3]*N_zs(s) + C[0,4]*M_ss(s) + C[1,0]*kappa_zz(s) + C[2,0]*kappa_zs(s)

        def M_zz(s):
            return C[1,0]*epsilon_zz(s) + C[1,1]*kappa_zz(s) + C[1,3]*N_zs(s) + C[1,4]*M_ss(s) + C[2,1]*kappa_zs(s)

        def M_zs(s):
            return C[2,0]*epsilon_zz(s) + C[2,1]*kappa_zz(s) + C[2,2]*kappa_zs(s) + C[2,3]*N_zs(s) + C[2,4]*M_ss(s)

        def gamma_zs(s):
            return C[3,0]*epsilon_zz(s) + C[3,1]*kappa_zz(s) + C[3,2]*kappa_zs(s) + C[3,3]*N_zs(s) + C[4,3]*M_ss(s)

        def kappa_ss(s):
            return C[4,0]*epsilon_zz(s) + C[4,1]*kappa_zz(s) + C[4,2]*kappa_zs(s) + C[4,3]*N_zs(s) + C[4,4]*M_ss(s)

        def N_zn(s): return C[5,5]*gamma_zn(s)

        def epsilon_ss(s): return C[6,0]*epsilon_zz(s) + C[6,1]*kappa_zz(s) + C[6,2]*kappa_zs(s) + C[6,3]*N_zs(s) + C[6,4]*M_ss(s)

        def gamma_sn(s): return C[7,5]*gamma_zn(s)

        # Load state
        bounds = (0, l)
        strain_state = {
            'epsilon_zz': lambda s: get_function_with_bounds(epsilon_zz, s, bounds),
            'kappa_zz': lambda s: get_function_with_bounds(kappa_zz, s, bounds),
            'kappa_zs': lambda s: get_function_with_bounds(kappa_zs, s, bounds),
            'gamma_zs': lambda s: get_function_with_bounds(gamma_zs, s, bounds),
            'kappa_ss': lambda s: get_function_with_bounds(kappa_ss, s, bounds),
            'gamma_zn': lambda s: get_function_with_bounds(gamma_zn, s, bounds),
            'epsilon_ss': lambda s: get_function_with_bounds(epsilon_ss, s, bounds),
            'gamma_sn': lambda s: get_function_with_bounds(gamma_sn, s, bounds),
        }

        stress_state = {
            'N_zz': lambda s: get_function_with_bounds(N_zz, s, bounds),
            'M_zz': lambda s: get_function_with_bounds(M_zz, s, bounds),
            'M_zs': lambda s: get_function_with_bounds(M_zs, s, bounds),
            'N_zs': lambda s: get_function_with_bounds(N_zs, s, bounds),
            'M_ss': lambda s: get_function_with_bounds(M_ss, s, bounds),
            'N_zn': lambda s: get_function_with_bounds(N_zn, s, bounds),
        }

        return ElementLoadState(strain_state, stress_state)

    def _d(self, element, displacements, v_s, s):
        dtype = self._dtype

        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        l = self._discreet_geometry.element_reference_length_dict[element]
        #C = element.material.stiffness.K_Jung
        b_element = element.b

        pos1 = node_midsurface_positions[element.node1]
        pos2 = node_midsurface_positions[element.node2]
        x1 = pos1.x
        y1 = pos1.y
        x2 = pos2.x
        y2 = pos2.y

        omega1 = element.node1.integral_values['omega']
        omega2 = element.node2.integral_values['omega']

        f_r_1 = element.f_r_1
        f_r_2 = element.f_r_2
        f_r_3 = element.f_r_3

        f_r_const_111 = f_r_1[0, 0]
        f_r_const_112 = f_r_2[0, 0]
        f_r_const_113 = f_r_3[0, 0]

        f_r_const_121 = f_r_1[0, 1]
        f_r_const_122 = f_r_2[0, 1]
        f_r_const_123 = f_r_3[0, 1]

        f_r_const_211 = f_r_1[1, 0]
        f_r_const_212 = f_r_2[1, 0]
        f_r_const_213 = f_r_3[1, 0]

        f_r_const_221 = f_r_1[1, 1]
        f_r_const_222 = f_r_2[1, 1]
        f_r_const_223 = f_r_3[1, 1]

        # Cross section displacements
        #gamma_xz = displacements.strain[0]
        #gamma_yz = displacements.strain[1]
        w_p_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = 0 if self._ignore_warping else displacements.twisting_derivation

        V_x_additional = v_s[0]
        V_y_additional = v_s[1]

        d = np.zeros((5, 1), dtype=dtype)

        d[0, 0] = (Theta_x_d * (l * y1 - s * (y1 - y2)) - Theta_y_d * (l * x1 - s * (x1 - x2)) + l * w_p_d - phi_dd * (
                    l * omega1 - s * (omega1 - omega2))) / l
        d[1, 0] = (l * (Theta_x_d * (x1 - x2) + Theta_y_d * (y1 - y2)) + phi_dd * (
                    (x1 - x2) * (l * x1 - s * (x1 - x2)) + (y1 - y2) * (l * y1 + s * (-y1 + y2)))) / l ** 2
        d[2, 0] = 2 * phi_d
        d[3, 0] = (V_x_additional * (f_r_const_111 * l ** 2 - l * s * (
                    3 * f_r_const_111 + f_r_const_112 - 4 * f_r_const_113) + 2 * s ** 2 * (
                                                 f_r_const_111 + f_r_const_112 - 2 * f_r_const_113)) + V_y_additional * (
                               f_r_const_121 * l ** 2 - l * s * (
                                   3 * f_r_const_121 + f_r_const_122 - 4 * f_r_const_123) + 2 * s ** 2 * (
                                           f_r_const_121 + f_r_const_122 - 2 * f_r_const_123)) + l ** 2 * (
                               Theta_x_d * b_element[0, 1] + Theta_y_d * b_element[0, 2] + b_element[0, 0] * w_p_d +
                               b_element[0, 3] * phi_d + b_element[0, 4] * phi_dd)) / l ** 2
        d[4, 0] = (V_x_additional * (f_r_const_211 * l ** 2 - l * s * (
                    3 * f_r_const_211 + f_r_const_212 - 4 * f_r_const_213) + 2 * s ** 2 * (
                                                 f_r_const_211 + f_r_const_212 - 2 * f_r_const_213)) + V_y_additional * (
                               f_r_const_221 * l ** 2 - l * s * (
                                   3 * f_r_const_221 + f_r_const_222 - 4 * f_r_const_223) + 2 * s ** 2 * (
                                           f_r_const_221 + f_r_const_222 - 2 * f_r_const_223)) + l * (Theta_x_d * (
                    b_element[1, 1] * l + b_element[2, 1] * (l * x1 - s * (x1 - x2)) + b_element[3, 1] * (
                        l * y1 - s * (y1 - y2))) + Theta_y_d * (b_element[1, 2] * l + b_element[2, 2] * (
                    l * x1 - s * (x1 - x2)) + b_element[3, 2] * (l * y1 - s * (y1 - y2))) + phi_d * (b_element[
                                                                                                         1, 3] * l +
                                                                                                     b_element[2, 3] * (
                                                                                                                 l * x1 - s * (
                                                                                                                     x1 - x2)) +
                                                                                                     b_element[3, 3] * (
                                                                                                                 l * y1 - s * (
                                                                                                                     y1 - y2))) + phi_dd * (
                                                                                                                  b_element[
                                                                                                                      1, 4] * l +
                                                                                                                  b_element[
                                                                                                                      2, 4] * (
                                                                                                                              l * x1 - s * (
                                                                                                                                  x1 - x2)) +
                                                                                                                  b_element[
                                                                                                                      3, 4] * (
                                                                                                                              l * y1 - s * (
                                                                                                                                  y1 - y2))) + w_p_d * (
                                                                                                                  b_element[
                                                                                                                      1, 0] * l +
                                                                                                                  b_element[
                                                                                                                      2, 0] * (
                                                                                                                              l * x1 - s * (
                                                                                                                                  x1 - x2)) +
                                                                                                                  b_element[
                                                                                                                      3, 0] * (
                                                                                                                              l * y1 - s * (
                                                                                                                                  y1 - y2))))) / l ** 2

        return d

    @staticmethod
    def _t_from_d(C, d_const):
        return C[0:5, 0:5] @ d_const

    @staticmethod
    def strain_stress_vectors_to_load_state(strain, stress):
        strain_state = {'epsilon_zz': strain[0],
                        'kappa_zz': strain[1],
                        'kappa_zs': strain[2],
                        'gamma_zs': stress[3],
                        'kappa_ss': stress[4]}

        stress_state = {'N_zz': stress[0],
                        'M_zz': stress[1],
                        'M_zs': stress[2],
                        'N_zs': strain[3],
                        'M_ss': strain[4]}

        return ElementLoadState(strain_state, stress_state)

    def calc_element_min_max_load_state(self, element, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        dtype = self._dtype

        self._update_if_required()
        node_midsurface_positions = self._discreet_geometry.node_midsurface_positions
        element_reference_length_dict = self._discreet_geometry.element_reference_length_dict

        # simple method: evaluate load states at s=0, s=l/, s=l
        # extended method: evaluate load states at s=0, s=l and the analytical extrema between [0, l]
        simple_method = True  # TODO: performance?

        if simple_method:
            l = element_reference_length_dict[element]
            C = element.shell.stiffness.K_Jung
            # b_element = element.b

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            # x1 = pos1.x
            # y1 = pos1.y
            # x2 = pos2.x
            # y2 = pos2.y
            #
            # omega1 = element.node1.integral_values['omega']
            # omega2 = element.node2.integral_values['omega']
            #
            # f_r_1 = element.f_r_1
            # f_r_2 = element.f_r_2
            # f_r_3 = element.f_r_3
            #
            # f_r_const_111 = f_r_1[0, 0]
            # f_r_const_112 = f_r_2[0, 0]
            # f_r_const_113 = f_r_3[0, 0]
            #
            # f_r_const_121 = f_r_1[0, 1]
            # f_r_const_122 = f_r_2[0, 1]
            # f_r_const_123 = f_r_3[0, 1]
            #
            # f_r_const_211 = f_r_1[1, 0]
            # f_r_const_212 = f_r_2[1, 0]
            # f_r_const_213 = f_r_3[1, 0]
            #
            # f_r_const_221 = f_r_1[1, 1]
            # f_r_const_222 = f_r_2[1, 1]
            # f_r_const_223 = f_r_3[1, 1]

            # Cross section displacements
            gamma_xz = displacements.strain[0]
            gamma_yz = displacements.strain[1]
            w_p_d = displacements.strain[2]
            Theta_x_d = displacements.curvature[0]
            Theta_y_d = displacements.curvature[1]
            phi_d = displacements.curvature[2]
            phi_dd = 0 if self._ignore_warping else displacements.twisting_derivation

            # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
            q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz], dtype=dtype)
            v_s = self._p @ q_cs

            # V_x_additional = v_s[0]
            # V_y_additional = v_s[1]

            # Element strains
            d_ex_0 = self._d(element, displacements, v_s, 0)
            d_ex_l = self._d(element, displacements, v_s, l)
            d_ex_l2 = self._d(element, displacements, v_s, l/2)

            # Element stresses
            t_ex_0 = self._t_from_d(C, d_ex_0)
            t_ex_l = self._t_from_d(C, d_ex_l)
            t_ex_l2 = self._t_from_d(C, d_ex_l2)

            min_strain = np.nanmin(np.hstack([d_ex_0, d_ex_l, d_ex_l2]), axis=1)
            max_strain = np.nanmax(np.hstack([d_ex_0, d_ex_l, d_ex_l2]), axis=1)

            min_stress = np.nanmin(np.hstack([t_ex_0, t_ex_l, t_ex_l2]), axis=1)
            max_stress = np.nanmax(np.hstack([t_ex_0, t_ex_l, t_ex_l2]), axis=1)


        else:
            # TODO: auf Rand-Extrema checken (an den Element Grenzen)
            l = element_reference_length_dict[element]
            C = element.shell.stiffness.K_Jung
            b_element = element.b

            pos1 = node_midsurface_positions[element.node1]
            pos2 = node_midsurface_positions[element.node2]
            x1 = pos1.x
            y1 = pos1.y
            x2 = pos2.x
            y2 = pos2.y

            omega1 = element.node1.integral_values['omega']
            omega2 = element.node2.integral_values['omega']

            f_r_1 = element.f_r_1
            f_r_2 = element.f_r_2
            f_r_3 = element.f_r_3

            f_r_const_111 = f_r_1[0, 0]
            f_r_const_112 = f_r_2[0, 0]
            f_r_const_113 = f_r_3[0, 0]

            f_r_const_121 = f_r_1[0, 1]
            f_r_const_122 = f_r_2[0, 1]
            f_r_const_123 = f_r_3[0, 1]

            f_r_const_211 = f_r_1[1, 0]
            f_r_const_212 = f_r_2[1, 0]
            f_r_const_213 = f_r_3[1, 0]

            f_r_const_221 = f_r_1[1, 1]
            f_r_const_222 = f_r_2[1, 1]
            f_r_const_223 = f_r_3[1, 1]

            # Cross section displacements
            gamma_xz = displacements.strain[0]
            gamma_yz = displacements.strain[1]
            w_p_d = displacements.strain[2]
            Theta_x_d = displacements.curvature[0]
            Theta_y_d = displacements.curvature[1]
            phi_d = displacements.curvature[2]
            phi_dd = 0 if self._ignore_warping else displacements.twisting_derivation

            # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
            q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz], dtype=dtype)
            v_s = self._p @ q_cs

            V_x_additional = v_s[0]
            V_y_additional = v_s[1]

            # Element strains
            d_ex_0 = self._d(element, displacements, v_s, 0)
            d_ex_l = self._d(element, displacements, v_s, l)
            s_d = np.zeros((5, 1), dtype=dtype)
            # s_d_A = np.zeros((2, 2), dtype=dtype)
            # s_d_b = np.zeros((2, 1), dtype=dtype)
            d_ex_d = np.zeros((5, 1), dtype=dtype)

            s_d[0, 0] = float('nan')
            s_d[1, 0] = float('nan')
            s_d[2, 0] = float('nan')
            s_d[3, 0] = (1 / 4) * l * (
                        3 * V_x_additional * f_r_const_111 + V_x_additional * f_r_const_112 - 4 * V_x_additional * f_r_const_113 + 3 * V_y_additional * f_r_const_121 + V_y_additional * f_r_const_122 - 4 * V_y_additional * f_r_const_123) / (
                                    V_x_additional * f_r_const_111 + V_x_additional * f_r_const_112 - 2 * V_x_additional * f_r_const_113 + V_y_additional * f_r_const_121 + V_y_additional * f_r_const_122 - 2 * V_y_additional * f_r_const_123)
            s_d[4, 0] = (1 / 4) * l * (
                        Theta_x_d * b_element[2, 1] * x1 - Theta_x_d * b_element[2, 1] * x2 + Theta_x_d * b_element[
                    3, 1] * y1 - Theta_x_d * b_element[3, 1] * y2 + Theta_y_d * b_element[2, 2] * x1 - Theta_y_d *
                        b_element[2, 2] * x2 + Theta_y_d * b_element[3, 2] * y1 - Theta_y_d * b_element[
                            3, 2] * y2 + 3 * V_x_additional * f_r_const_211 + V_x_additional * f_r_const_212 - 4 * V_x_additional * f_r_const_213 + 3 * V_y_additional * f_r_const_221 + V_y_additional * f_r_const_222 - 4 * V_y_additional * f_r_const_223 +
                        b_element[2, 0] * w_p_d * x1 - b_element[2, 0] * w_p_d * x2 + b_element[2, 3] * phi_d * x1 -
                        b_element[2, 3] * phi_d * x2 + b_element[2, 4] * phi_dd * x1 - b_element[2, 4] * phi_dd * x2 +
                        b_element[3, 0] * w_p_d * y1 - b_element[3, 0] * w_p_d * y2 + b_element[3, 3] * phi_d * y1 -
                        b_element[3, 3] * phi_d * y2 + b_element[3, 4] * phi_dd * y1 - b_element[
                            3, 4] * phi_dd * y2) / (
                                    V_x_additional * f_r_const_211 + V_x_additional * f_r_const_212 - 2 * V_x_additional * f_r_const_213 + V_y_additional * f_r_const_221 + V_y_additional * f_r_const_222 - 2 * V_y_additional * f_r_const_223)

            # s_d in element bounds
            s_d[np.bitwise_and(~np.isnan(s_d), s_d < 0)] = 0
            s_d[np.bitwise_and(~np.isnan(s_d), s_d > l)] = l


            d_ex_d[0, 0] = float('nan')
            d_ex_d[1, 0] = float('nan')
            d_ex_d[2, 0] = float('nan')
            d_ex_d[3, 0] = (V_x_additional * (f_r_const_111 * l ** 2 - l * s_d[3, 0] * (
                        3 * f_r_const_111 + f_r_const_112 - 4 * f_r_const_113) + 2 * s_d[3, 0] ** 2 * (
                                                          f_r_const_111 + f_r_const_112 - 2 * f_r_const_113)) + V_y_additional * (
                                        f_r_const_121 * l ** 2 - l * s_d[3, 0] * (
                                            3 * f_r_const_121 + f_r_const_122 - 4 * f_r_const_123) + 2 * s_d[
                                            3, 0] ** 2 * (
                                                    f_r_const_121 + f_r_const_122 - 2 * f_r_const_123)) + l ** 2 * (
                                        Theta_x_d * b_element[0, 1] + Theta_y_d * b_element[0, 2] + b_element[
                                    0, 0] * w_p_d + b_element[0, 3] * phi_d + b_element[0, 4] * phi_dd)) / l ** 2
            d_ex_d[4, 0] = (V_x_additional * (f_r_const_211 * l ** 2 - l * s_d[4, 0] * (
                        3 * f_r_const_211 + f_r_const_212 - 4 * f_r_const_213) + 2 * s_d[4, 0] ** 2 * (
                                                          f_r_const_211 + f_r_const_212 - 2 * f_r_const_213)) + V_y_additional * (
                                        f_r_const_221 * l ** 2 - l * s_d[4, 0] * (
                                            3 * f_r_const_221 + f_r_const_222 - 4 * f_r_const_223) + 2 * s_d[
                                            4, 0] ** 2 * (f_r_const_221 + f_r_const_222 - 2 * f_r_const_223)) + l * (
                                        Theta_x_d * (
                                            b_element[1, 1] * l + b_element[2, 1] * (l * x1 - s_d[4, 0] * (x1 - x2)) +
                                            b_element[3, 1] * (l * y1 - s_d[4, 0] * (y1 - y2))) + Theta_y_d * (
                                                    b_element[1, 2] * l + b_element[2, 2] * (
                                                        l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 2] * (
                                                                l * y1 - s_d[4, 0] * (y1 - y2))) + phi_d * (
                                                    b_element[1, 3] * l + b_element[2, 3] * (
                                                        l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 3] * (
                                                                l * y1 - s_d[4, 0] * (y1 - y2))) + phi_dd * (
                                                    b_element[1, 4] * l + b_element[2, 4] * (
                                                        l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 4] * (
                                                                l * y1 - s_d[4, 0] * (y1 - y2))) + w_p_d * (
                                                    b_element[1, 0] * l + b_element[2, 0] * (
                                                        l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 0] * (
                                                                l * y1 - s_d[4, 0] * (y1 - y2))))) / l ** 2

            # Element stresses
            t_ex_0 = self._t_from_d(C, d_ex_0)
            t_ex_l = self._t_from_d(C, d_ex_l)
            # s_t_A = np.zeros((5, 5), dtype=dtype)
            s_t = np.zeros((5, 1), dtype=dtype)

            s_t[0, 0] = (1 / 4) * (
                        C[0, 0] * Theta_x_d * l * y1 - C[0, 0] * Theta_x_d * l * y2 - C[0, 0] * Theta_y_d * l * x1 + C[
                    0, 0] * Theta_y_d * l * x2 - C[0, 0] * l * omega1 * phi_dd + C[0, 0] * l * omega2 * phi_dd + 3 * C[
                            0, 3] * V_x_additional * f_r_const_111 * l + C[
                            0, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            0, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            0, 3] * V_y_additional * f_r_const_121 * l + C[
                            0, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            0, 3] * V_y_additional * f_r_const_123 * l + C[0, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[0, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[0, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[0, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            0, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[0, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[0, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[0, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[0, 4] * V_x_additional * f_r_const_211 * l + C[
                            0, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            0, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            0, 4] * V_y_additional * f_r_const_221 * l + C[
                            0, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            0, 4] * V_y_additional * f_r_const_223 * l + C[0, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            0, 4] * b_element[2, 0] * l * w_p_d * x2 + C[0, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            0, 4] * b_element[2, 3] * l * phi_d * x2 + C[0, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            0, 4] * b_element[2, 4] * l * phi_dd * x2 + C[0, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            0, 4] * b_element[3, 0] * l * w_p_d * y2 + C[0, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            0, 4] * b_element[3, 3] * l * phi_d * y2 + C[0, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            0, 4] * b_element[3, 4] * l * phi_dd * y2 + C[1, 0] * phi_dd * x1 ** 2 - 2 * C[
                            1, 0] * phi_dd * x1 * x2 + C[1, 0] * phi_dd * x2 ** 2 + C[1, 0] * phi_dd * y1 ** 2 - 2 * C[
                            1, 0] * phi_dd * y1 * y2 + C[1, 0] * phi_dd * y2 ** 2) / (
                                    C[0, 3] * V_x_additional * f_r_const_111 + C[
                                0, 3] * V_x_additional * f_r_const_112 - 2 * C[0, 3] * V_x_additional * f_r_const_113 +
                                    C[0, 3] * V_y_additional * f_r_const_121 + C[
                                        0, 3] * V_y_additional * f_r_const_122 - 2 * C[
                                        0, 3] * V_y_additional * f_r_const_123 + C[
                                        0, 4] * V_x_additional * f_r_const_211 + C[
                                        0, 4] * V_x_additional * f_r_const_212 - 2 * C[
                                        0, 4] * V_x_additional * f_r_const_213 + C[
                                        0, 4] * V_y_additional * f_r_const_221 + C[
                                        0, 4] * V_y_additional * f_r_const_222 - 2 * C[
                                        0, 4] * V_y_additional * f_r_const_223)
            s_t[1, 0] = (1 / 4) * (
                        C[1, 0] * Theta_x_d * l * y1 - C[1, 0] * Theta_x_d * l * y2 - C[1, 0] * Theta_y_d * l * x1 + C[
                    1, 0] * Theta_y_d * l * x2 - C[1, 0] * l * omega1 * phi_dd + C[1, 0] * l * omega2 * phi_dd + C[
                            1, 1] * phi_dd * x1 ** 2 - 2 * C[1, 1] * phi_dd * x1 * x2 + C[1, 1] * phi_dd * x2 ** 2 + C[
                            1, 1] * phi_dd * y1 ** 2 - 2 * C[1, 1] * phi_dd * y1 * y2 + C[1, 1] * phi_dd * y2 ** 2 + 3 *
                        C[1, 3] * V_x_additional * f_r_const_111 * l + C[
                            1, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            1, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            1, 3] * V_y_additional * f_r_const_121 * l + C[
                            1, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            1, 3] * V_y_additional * f_r_const_123 * l + C[1, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[1, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[1, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[1, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            1, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[1, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[1, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[1, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[1, 4] * V_x_additional * f_r_const_211 * l + C[
                            1, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            1, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            1, 4] * V_y_additional * f_r_const_221 * l + C[
                            1, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            1, 4] * V_y_additional * f_r_const_223 * l + C[1, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            1, 4] * b_element[2, 0] * l * w_p_d * x2 + C[1, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            1, 4] * b_element[2, 3] * l * phi_d * x2 + C[1, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            1, 4] * b_element[2, 4] * l * phi_dd * x2 + C[1, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            1, 4] * b_element[3, 0] * l * w_p_d * y2 + C[1, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            1, 4] * b_element[3, 3] * l * phi_d * y2 + C[1, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            1, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[1, 3] * V_x_additional * f_r_const_111 + C[
                1, 3] * V_x_additional * f_r_const_112 - 2 * C[1, 3] * V_x_additional * f_r_const_113 + C[
                                                                              1, 3] * V_y_additional * f_r_const_121 +
                                                                          C[1, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[1, 3] * V_y_additional * f_r_const_123 + C[
                                                                              1, 4] * V_x_additional * f_r_const_211 +
                                                                          C[1, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[1, 4] * V_x_additional * f_r_const_213 + C[
                                                                              1, 4] * V_y_additional * f_r_const_221 +
                                                                          C[1, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[1, 4] * V_y_additional * f_r_const_223)
            s_t[2, 0] = (1 / 4) * (
                        C[2, 0] * Theta_x_d * l * y1 - C[2, 0] * Theta_x_d * l * y2 - C[2, 0] * Theta_y_d * l * x1 + C[
                    2, 0] * Theta_y_d * l * x2 - C[2, 0] * l * omega1 * phi_dd + C[2, 0] * l * omega2 * phi_dd + C[
                            2, 1] * phi_dd * x1 ** 2 - 2 * C[2, 1] * phi_dd * x1 * x2 + C[2, 1] * phi_dd * x2 ** 2 + C[
                            2, 1] * phi_dd * y1 ** 2 - 2 * C[2, 1] * phi_dd * y1 * y2 + C[2, 1] * phi_dd * y2 ** 2 + 3 *
                        C[2, 3] * V_x_additional * f_r_const_111 * l + C[
                            2, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            2, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            2, 3] * V_y_additional * f_r_const_121 * l + C[
                            2, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            2, 3] * V_y_additional * f_r_const_123 * l + C[2, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[2, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[2, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[2, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            2, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[2, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[2, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[2, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[2, 4] * V_x_additional * f_r_const_211 * l + C[
                            2, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            2, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            2, 4] * V_y_additional * f_r_const_221 * l + C[
                            2, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            2, 4] * V_y_additional * f_r_const_223 * l + C[2, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            2, 4] * b_element[2, 0] * l * w_p_d * x2 + C[2, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            2, 4] * b_element[2, 3] * l * phi_d * x2 + C[2, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            2, 4] * b_element[2, 4] * l * phi_dd * x2 + C[2, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            2, 4] * b_element[3, 0] * l * w_p_d * y2 + C[2, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            2, 4] * b_element[3, 3] * l * phi_d * y2 + C[2, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            2, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[2, 3] * V_x_additional * f_r_const_111 + C[
                2, 3] * V_x_additional * f_r_const_112 - 2 * C[2, 3] * V_x_additional * f_r_const_113 + C[
                                                                              2, 3] * V_y_additional * f_r_const_121 +
                                                                          C[2, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[2, 3] * V_y_additional * f_r_const_123 + C[
                                                                              2, 4] * V_x_additional * f_r_const_211 +
                                                                          C[2, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[2, 4] * V_x_additional * f_r_const_213 + C[
                                                                              2, 4] * V_y_additional * f_r_const_221 +
                                                                          C[2, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[2, 4] * V_y_additional * f_r_const_223)
            s_t[3, 0] = (1 / 4) * (
                        C[3, 0] * Theta_x_d * l * y1 - C[3, 0] * Theta_x_d * l * y2 - C[3, 0] * Theta_y_d * l * x1 + C[
                    3, 0] * Theta_y_d * l * x2 - C[3, 0] * l * omega1 * phi_dd + C[3, 0] * l * omega2 * phi_dd + C[
                            3, 1] * phi_dd * x1 ** 2 - 2 * C[3, 1] * phi_dd * x1 * x2 + C[3, 1] * phi_dd * x2 ** 2 + C[
                            3, 1] * phi_dd * y1 ** 2 - 2 * C[3, 1] * phi_dd * y1 * y2 + C[3, 1] * phi_dd * y2 ** 2 + 3 *
                        C[3, 3] * V_x_additional * f_r_const_111 * l + C[
                            3, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            3, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            3, 3] * V_y_additional * f_r_const_121 * l + C[
                            3, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            3, 3] * V_y_additional * f_r_const_123 * l + C[4, 3] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[4, 3] * Theta_x_d * b_element[2, 1] * l * x2 + C[4, 3] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[4, 3] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            4, 3] * Theta_y_d * b_element[2, 2] * l * x1 - C[4, 3] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[4, 3] * Theta_y_d * b_element[3, 2] * l * y1 - C[4, 3] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[4, 3] * V_x_additional * f_r_const_211 * l + C[
                            4, 3] * V_x_additional * f_r_const_212 * l - 4 * C[
                            4, 3] * V_x_additional * f_r_const_213 * l + 3 * C[
                            4, 3] * V_y_additional * f_r_const_221 * l + C[
                            4, 3] * V_y_additional * f_r_const_222 * l - 4 * C[
                            4, 3] * V_y_additional * f_r_const_223 * l + C[4, 3] * b_element[2, 0] * l * w_p_d * x1 - C[
                            4, 3] * b_element[2, 0] * l * w_p_d * x2 + C[4, 3] * b_element[2, 3] * l * phi_d * x1 - C[
                            4, 3] * b_element[2, 3] * l * phi_d * x2 + C[4, 3] * b_element[2, 4] * l * phi_dd * x1 - C[
                            4, 3] * b_element[2, 4] * l * phi_dd * x2 + C[4, 3] * b_element[3, 0] * l * w_p_d * y1 - C[
                            4, 3] * b_element[3, 0] * l * w_p_d * y2 + C[4, 3] * b_element[3, 3] * l * phi_d * y1 - C[
                            4, 3] * b_element[3, 3] * l * phi_d * y2 + C[4, 3] * b_element[3, 4] * l * phi_dd * y1 - C[
                            4, 3] * b_element[3, 4] * l * phi_dd * y2) / (C[3, 3] * V_x_additional * f_r_const_111 + C[
                3, 3] * V_x_additional * f_r_const_112 - 2 * C[3, 3] * V_x_additional * f_r_const_113 + C[
                                                                              3, 3] * V_y_additional * f_r_const_121 +
                                                                          C[3, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[3, 3] * V_y_additional * f_r_const_123 + C[
                                                                              4, 3] * V_x_additional * f_r_const_211 +
                                                                          C[4, 3] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[4, 3] * V_x_additional * f_r_const_213 + C[
                                                                              4, 3] * V_y_additional * f_r_const_221 +
                                                                          C[4, 3] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[4, 3] * V_y_additional * f_r_const_223)
            s_t[4, 0] = (1 / 4) * (
                        C[4, 0] * Theta_x_d * l * y1 - C[4, 0] * Theta_x_d * l * y2 - C[4, 0] * Theta_y_d * l * x1 + C[
                    4, 0] * Theta_y_d * l * x2 - C[4, 0] * l * omega1 * phi_dd + C[4, 0] * l * omega2 * phi_dd + C[
                            4, 1] * phi_dd * x1 ** 2 - 2 * C[4, 1] * phi_dd * x1 * x2 + C[4, 1] * phi_dd * x2 ** 2 + C[
                            4, 1] * phi_dd * y1 ** 2 - 2 * C[4, 1] * phi_dd * y1 * y2 + C[4, 1] * phi_dd * y2 ** 2 + 3 *
                        C[4, 3] * V_x_additional * f_r_const_111 * l + C[
                            4, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            4, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            4, 3] * V_y_additional * f_r_const_121 * l + C[
                            4, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            4, 3] * V_y_additional * f_r_const_123 * l + C[4, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[4, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[4, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[4, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            4, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[4, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[4, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[4, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[4, 4] * V_x_additional * f_r_const_211 * l + C[
                            4, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            4, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            4, 4] * V_y_additional * f_r_const_221 * l + C[
                            4, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            4, 4] * V_y_additional * f_r_const_223 * l + C[4, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            4, 4] * b_element[2, 0] * l * w_p_d * x2 + C[4, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            4, 4] * b_element[2, 3] * l * phi_d * x2 + C[4, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            4, 4] * b_element[2, 4] * l * phi_dd * x2 + C[4, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            4, 4] * b_element[3, 0] * l * w_p_d * y2 + C[4, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            4, 4] * b_element[3, 3] * l * phi_d * y2 + C[4, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            4, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[4, 3] * V_x_additional * f_r_const_111 + C[
                4, 3] * V_x_additional * f_r_const_112 - 2 * C[4, 3] * V_x_additional * f_r_const_113 + C[
                                                                              4, 3] * V_y_additional * f_r_const_121 +
                                                                          C[4, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[4, 3] * V_y_additional * f_r_const_123 + C[
                                                                              4, 4] * V_x_additional * f_r_const_211 +
                                                                          C[4, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[4, 4] * V_x_additional * f_r_const_213 + C[
                                                                              4, 4] * V_y_additional * f_r_const_221 +
                                                                          C[4, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[4, 4] * V_y_additional * f_r_const_223)

            #s_t = lgs_solve(s_t_A, s_t_b, dtype=dtype)
            t_ex_d = np.zeros((5, 1), dtype=dtype)
            for i, s_i in enumerate(s_t):
                if not np.isnan(s_i) and 0 < s_i < l:
                    d_i = self._d(element, displacements, v_s, s_i)
                    t_i = self._t_from_d(C, d_i)
                    t_ex_d[i, 0] = t_i[i]

            min_strain = np.nanmin(np.hstack([d_ex_0, d_ex_l, d_ex_d]), axis=1)
            max_strain = np.nanmax(np.hstack([d_ex_0, d_ex_l, d_ex_d]), axis=1)

            min_stress = np.nanmin(np.hstack([t_ex_0, t_ex_l, t_ex_d]), axis=1)
            max_stress = np.nanmax(np.hstack([t_ex_0, t_ex_l, t_ex_d]), axis=1)


        min_load_state = self.strain_stress_vectors_to_load_state(min_strain, min_stress)
        max_load_state = self.strain_stress_vectors_to_load_state(max_strain, max_stress)

        # min_strain = np.hstack([d_ex_0, d_ex_l, d_ex_d]).nanmin(axis=1)
        # max_strain = np.hstack([d_ex_0, d_ex_l, d_ex_d]).nanmax(axis=1)
        #
        # min_stress = np.hstack([t_ex_0, t_ex_l, t_ex_d]).nanmin(axis=1)
        # max_stress = np.hstack([t_ex_0, t_ex_l, t_ex_d]).nanmax(axis=1)

        # Load state
        #STRAIN_NAMES = ['epsilon_zz', 'kappa_zz', 'kappa_zs', 'gamma_zs', 'kappa_ss']
        #STRESS_NAMES = ['N_zz', 'M_zz', 'M_zs', 'N_zs', 'M_ss']

        #
        # # Validation
        # load_state_functions = self.calc_element_load_state(element, displacements)
        #
        # def calc_load_state(load_state_functions, s):
        #     new_strain_state = {key: val(s) for key, val in load_state_functions.strain_state.items()}
        #     new_stress_state = {key: val(s) for key, val in load_state_functions.stress_state.items()}
        #     return ElementLoadState(new_strain_state, new_stress_state)
        #
        # ex_0_ref = calc_load_state(load_state_functions, 0)
        # ex_l_ref = calc_load_state(load_state_functions, l)
        # ex_l2_ref = calc_load_state(load_state_functions, l/2)

        # strain_dict_min = {}
        # for state_key, stress_from_strain_func in load_state_functions.strain_state.items():
        #     stress = min([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     strain_dict_min[state_key] = stress
        # stress_dict_min = {}
        # for state_key, stress_from_strain_func in load_state_functions.stress_state.items():
        #     stress = min([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     stress_dict_min[state_key] = stress
        #
        # strain_dict_max = {}
        # for state_key, stress_from_strain_func in load_state_functions.strain_state.items():
        #     stress = max([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     strain_dict_max[state_key] = stress
        # stress_dict_max = {}
        # for state_key, stress_from_strain_func in load_state_functions.stress_state.items():
        #     stress = max([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     stress_dict_max[state_key] = stress

        # min_strain_ref = np.nanmin(np.vstack([list(ex_0_ref.strain_state.values()), list(ex_l_ref.strain_state.values()), list(ex_l2_ref.strain_state.values())]).T, axis=1)
        # max_strain_ref = np.nanmax(np.vstack([list(ex_0_ref.strain_state.values()), list(ex_l_ref.strain_state.values()), list(ex_l2_ref.strain_state.values())]).T, axis=1)
        #
        # min_stress_ref = np.nanmin(np.vstack([list(ex_0_ref.stress_state.values()), list(ex_l_ref.stress_state.values()), list(ex_l2_ref.stress_state.values())]).T, axis=1)
        # max_stress_ref = np.nanmax(np.vstack([list(ex_0_ref.stress_state.values()), list(ex_l_ref.stress_state.values()), list(ex_l2_ref.stress_state.values())]).T, axis=1)

        # if not np.all(np.isclose(list(min_load_state.strain_state.values()), min_strain_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(max_load_state.strain_state.values()), max_strain_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(min_load_state.stress_state.values()), min_stress_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(max_load_state.stress_state.values()), max_stress_ref, rtol=1e-1)):
        #     log.warning('nich tgut')

        # assert np.all(np.isclose(list(min_load_state.strain_state.values()), min_strain_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(max_load_state.strain_state.values()), max_strain_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(min_load_state.stress_state.values()), min_stress_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(max_load_state.stress_state.values()), max_stress_ref, rtol=1e-2))

        return min_load_state, max_load_state#ElementLoadState(strain_dict_min, stress_dict_min), ElementLoadState(strain_dict_max, stress_dict_max)#min_load_state, max_load_state


class JungWithoutWarpingCrossSectionProcessor(JungCrossSectionProcessor):
    """
    Processor based on the JungCrossSectionProcessor, but ignores the warping part.
    """
    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam, **kwargs)

    @property
    def _ignore_warping(self) -> bool:
        return True
