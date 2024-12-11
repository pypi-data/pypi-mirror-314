"""
This module provides a 1D finite elements beam analysis for PreDoCS.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from abc import abstractmethod, ABC

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sp_la

from PreDoCS.CrossSectionAnalysis.Interfaces import CrossSectionInertia, TimoschenkoDisplacements, \
    ClassicCrossSectionLoads
from PreDoCS.CrossSectionAnalysis.Interfaces import TimoschenkoWithRestrainedWarpingDisplacements, \
    TimoschenkoWithRestrainedWarpingStiffness, ClassicCrossSectionLoadsWithBimoment
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.dtypes import lgs_solve_sparse
from PreDoCS.util.geometry import create_rotation_matrix_from_directions
from PreDoCS.util.util import get_interpolated_stiffness_and_inertia_matrices
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


class LagrangianShapeFunction(object):
    """
    This class provides Lagrangian shape functions with several orders.
    See http://kratos-wiki.cimne.upc.edu/index.php/One-dimensional_Shape_Functions
    """

    @staticmethod
    def _N_i(z, z_nodes, i):
        """
        Returns the i-th Larangian basis polynomial.

        Parameters
        ----------
        z: float, sympy.core.symbol.Symbol
            The interpolation function argument.
        z_nodes: list(float), list(sympy.core.symbol.Symbol)
            The data point positions.
        i: int
            basis polynomial index.

        Returns
        -------
        float, sympy.core.expr.Expr:
            The value or expression of the basis polynomial.
        """
        n_n = len(z_nodes)
        res = 1
        for j in range(n_n):
            if not j == i:
                res *= (z - z_nodes[j]) / (z_nodes[i] - z_nodes[j])
        return res

    @staticmethod
    def N(z, z_nodes):
        """
        Returns the Larangian shape function vector.

        Parameters
        ----------
        z: float, sympy.core.symbol.Symbol
            The interpolation function argument.
        z_nodes: list(float), list(sympy.core.symbol.Symbol)
            The data point positions.

        Returns
        -------
        list(float), list(sympy.core.expr.Expr):
            The values or expressions of the shape function vector.
        """
        n_n = len(z_nodes)
        return [LagrangianShapeFunction._N_i(z, z_nodes, i) for i in range(n_n)]


class HermiteShapeFunction(object):
    """
    This class provides a cubic Hermite shape function.
    See http://infohost.nmt.edu/~es421/ansys/shapefnt.htm
    """

    @staticmethod
    def N(z, z_nodes):
        """
        Returns the cubic Hermite shape function vector.

        Parameters
        ----------
        z: float, sympy.core.symbol.Symbol
            The interpolation function argument.
        z_nodes: list(float), list(sympy.core.symbol.Symbol)
            The data point positions.

        Returns
        -------
        list(float), list(sympy.core.expr.Expr):
            The values or expressions of the shape function vector.
        """
        assert len(z_nodes) == 2
        l = z_nodes[1] - z_nodes[0]
        r = (z - z_nodes[0]) / l
        H1 = 1 - 3 * r ** 2 + 2 * r ** 3
        H3 = 3 * r ** 2 - 2 * r ** 3
        H2 = l * (r - 2 * r ** 2 + r ** 3)
        H4 = l * (-r ** 2 + r ** 3)
        return [H1, H3, H2, H4]


class BeamNode(object):
    """
    A node of the 1D finite elements beam model.

    Attributes
    ----------
    _z2: float
        Postion on the beam axis.
    _pos: Vector
        Position on the beam axis in PreDoCS system.
    """

    def __init__(self, z2, pos):
        """
        Constructor.

        Parameters
        ----------
        z2: float
            Position on the beam axis.
        pos: Vector
            Position on the beam axis in the PreDoCS coordinate system.
        """
        self._pos = pos
        self._z2 = z2

    @property
    def z2(self):
        """float: Position on the beam axis."""
        return self._z2

    @property
    def pos(self):
        """float: Position on the beam axis in the PreDoCS coordinate system."""
        return self._pos


class AbstractBeamElement(ABC):
    """
    A element of the 1D finite elements beam model. The element stiffness is a
    7x7 TimoschenkoWithRestrainedWarpingStiffness matrix.

    Attributes
    ----------
    _node1: BeamNode
        First node of the element.
    _node2: BeamNode
        Second node of the element.
    _cross_section_stiffness_matrix: np.ndarray
        The cross-section stiffness matrix of the element.
    _cross_section_inertia_matrix: np.ndarray
        The cross-section inertia matrix of the element.
    _node_positions: list(float)
        The positions of the nodes (end nodes and integration point nodes) in the beam coordinate system.
    _element_stiffness_matrix: numpy.ndarray
        The FE element stiffness matrix.
    _element_mass_matrix: numpy.ndarray
        The FE element mass matrix.
    _line_load_conversion_matrix: numpy.ndarray
        Matrix for the conversion of line loads at the nodes (end nodes and integration point nodes) to node loads.

    Constants
    ---------
    A_matrix: scipy.sparse.dok_array
        The permutation matrix to convert the displacements of the nodes from the global to the local order.
    """

    def __init__(self, node1, node2, stiffness_matrix, inertia_matrix, dtype=np.float64):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness_matrix: np.ndarray
            The stiffness matrix of the element (6x6 or 7x7).
        inertia_matrix: np.ndarray
            The inertia matrix of the element.
        """
        self._dtype = dtype
        self._node1 = node1
        self._node2 = node2
        self._cross_section_stiffness_matrix = np.array(stiffness_matrix, dtype=dtype)
        if self.ignore_warping():
            assert self._cross_section_stiffness_matrix.shape == (6, 6)
        else:
            assert self._cross_section_stiffness_matrix.shape == (7, 7)
        self._cross_section_inertia_matrix = np.array(inertia_matrix, dtype=dtype)
        assert self._cross_section_inertia_matrix.shape == (6, 6)
        self._T_e_g_c = None
        self._T_e_g = None

    @property
    def node1(self):
        """BeamNode: First node of the element."""
        return self._node1

    @property
    def node2(self):
        """BeamNode: Second node of the element."""
        return self._node2
    
    def get_z_element(self, z2: float) -> float:
        """
        Returns the element coordinate from the global beam coordinate.
        Can be scaled, if the beam element spans over a kink.
        """
        assert self._node1.z2 <= z2 <= self._node2.z2
        z2_diff = self._node2.z2 - self._node1.z2
        return (z2 - self.node1.z2) / z2_diff * self.length


    @property
    def direction(self):
        """Vector: direction of the element in PreDoCS coordinate System"""
        direction = self.node2.pos - self.node1.pos
        return direction.normalised

    @property
    def cross_section_stiffness_matrix(self) :
        """The cross-section stiffness matrix of the element."""
        return self._cross_section_stiffness_matrix

    @property
    def length(self):
        """float: Length of the element in beam direction."""
        return self.node2.pos.dist(self.node1.pos)

    @property
    def node_positions(self) -> list[list[float]]:
        """
        The positions of the nodes (end nodes and integration point nodes) in the element coordinate system for each DOF.
        """
        if not hasattr(self, '_node_positions'):
            pos_1 = self.node1.pos
            direction = self.direction
            l = self.length
            self._node_positions = [
                [z2_norm * l * direction + pos_1 for z2_norm in z2_norm_list]
                for z2_norm_list in self.node_positions_norm()
            ]

        return self._node_positions

    @property
    def T_e_g_c(self):
        """
        Used to transform single node displacements from global coordinate system to the element coordinate system
        :math:`x_e = T_e_g_c * x_g`
        """
        if self._T_e_g_c is None:
            dtype = self._dtype
            mat3 = create_rotation_matrix_from_directions(self.direction, Vector([0, 0, 1]))

            res = sp.dok_array((6, 6), dtype=dtype)
            res[0:3,0:3] = mat3
            res[3:6,3:6] = mat3

            self._T_e_g_c = res
        return self._T_e_g_c

    @property
    def T_e_g(self):
        """
        Transforms element DOF to PreDoCS (global) DOF, such that :math:`\\hat{U_{element}} = T_e_g * \\hat{U_{global}}`.
        """
        if self._T_e_g is None:
            dtype = self._dtype
            num_nodes = self.num_nodes()

            # Rotation of one node
            T_e_g_c = self.T_e_g_c

            # Assemble for all nodes
            A_matrix = self.A_matrix()
            T_e_g_global = sp.dok_array((6*num_nodes, 6*num_nodes), dtype=dtype)
            for i in range(num_nodes):
                T_e_g_global[i*6:i*6+6, i*6:i*6+6] = T_e_g_c
            T_e_g_element = A_matrix @ T_e_g_global.tocsc() @ A_matrix.T
            #assert np.allclose(T_e_g_element.T.todense(), np.linalg.inv(T_e_g_element.todense()))
            self._T_e_g = T_e_g_element
        return self._T_e_g

    def node_loads_from_line_load_function(self, line_load_function):
        """
        Calculates the node loads from a given line load function.

        Parameters
        ----------
        line_load_function: function(dof, z)
            Line load of the node DOF 'dof' at the beam position 'z'.

        Returns
        -------
        numpy.ndarray
            Vector of the node loads.
        """
        dtype = self._dtype
        f_L_hat = []
        z_nodes = self.node_positions
        for i_displacement in range(len(z_nodes)):
            displacement_nodes = z_nodes[i_displacement]
            for i_node in range(len(displacement_nodes)):
                f_L_hat.append(line_load_function(i_displacement, displacement_nodes[i_node]))
        f_L_hat = np.array(f_L_hat, dtype=dtype).T
        R_L_m = self.line_load_conversion_matrix.dot(f_L_hat)
        return R_L_m

    def post_processing(self, element_displacement_vector_global, z2):
        """
        Returns the post processing data for this element from a given global element displacement vector.

        Parameters
        ----------
        element_displacement_vector_global: numpy.array
            The global element displacement vector (20 components).
        z2: float
            The global position where to calculate the displacements. Must be in the range of the element.

        Returns
        -------
        list(float)
            List of the six beam displacements.
        TimoschenkoDisplacements or TimoschenkoWithRestrainedWarpingDisplacements
            The cross section displacements.
        ClassicCrossSectionLoads or ClassicCrossSectionLoadsWithBimoment
            The cross section internal loads.
        """
        dtype = self._dtype
        ignore_warping = self.ignore_warping()
        z2_element = self.get_z_element(z2)
        element_displacement_vector_global = np.array(element_displacement_vector_global, dtype=dtype)
        element_displacement_vector_local = self.A_matrix().dot(element_displacement_vector_global)
        if self.deformation_transformation():
            element_displacement_vector_local_transformed = (self.T_e_g).dot(element_displacement_vector_local)
            beam_displacements = (self.T_e_g_c.T @ self.H_matrix(z2_element)).dot(
                element_displacement_vector_local_transformed).flatten().tolist()
        else:
            element_displacement_vector_local_transformed = element_displacement_vector_local
            beam_displacements = self.H_matrix(z2_element).dot(
                element_displacement_vector_local_transformed).flatten().tolist()
        cross_section_displacements_vector = self.B_matrix(z2_element).dot(element_displacement_vector_local_transformed).flatten()


        if ignore_warping:
            cross_section_displacements = TimoschenkoDisplacements.from_list(cross_section_displacements_vector)
        else:
            cross_section_displacements = TimoschenkoWithRestrainedWarpingDisplacements.from_list(cross_section_displacements_vector)

        cross_section_internal_loads_vector = self.cross_section_stiffness_matrix @ cross_section_displacements_vector

        if ignore_warping:
            cross_section_internal_loads = ClassicCrossSectionLoads.from_list(cross_section_internal_loads_vector)
        else:
            cross_section_internal_loads = ClassicCrossSectionLoadsWithBimoment.from_list(cross_section_internal_loads_vector)

        return beam_displacements, cross_section_displacements, cross_section_internal_loads

    @staticmethod
    @abstractmethod
    def num_nodes() -> int:
        pass

    @staticmethod
    @abstractmethod
    def element_dof() -> int:
        """Number of DOF per element."""
        pass

    @staticmethod
    @abstractmethod
    def dof_increment_per_element() -> int:
        """The increment of global DOF per new element."""
        pass

    @staticmethod
    @abstractmethod
    def deformation_transformation() -> bool:
        """True, if the global beam deformations have to transformed from the global to the element coordinate system."""
        pass

    @staticmethod
    @abstractmethod
    def ignore_warping() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def node_positions_norm() -> list[list[float]]:
        pass

    @classmethod
    @abstractmethod
    def A_matrix(cls) -> sp.csc_array:
        pass

    @property
    @abstractmethod
    def element_stiffness_matrix(self) -> sp.csc_array:
        """numpy.ndarray: The FE element stiffness matrix."""
        pass

    @property
    @abstractmethod
    def element_mass_matrix(self) -> sp.csc_array:
        """numpy.ndarray: The FE element mass matrix."""
        pass

    @property
    @abstractmethod
    def line_load_conversion_matrix(self) -> sp.csc_array:
        """numpy.ndarray: Matrix for the conversion of line loads at the nodes (end nodes and integration point nodes) to node loads."""
        pass

    @abstractmethod
    def H_matrix(self, z: float) -> np.ndarray:
        """
        Returns the H matrix of the element at a given z coordinate. The H matrix is used to calculate
        the beam displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The H matrix.
        """
        pass

    @abstractmethod
    def B_matrix(self, z: float) -> np.ndarray:
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        pass


class BeamElementJung(AbstractBeamElement):
    """
    A element of the 1D finite elements beam model. The elements have two nodes and 20 DOF:
    six DOF per node and eight integration points. The element stiffness is a
    7x7 TimoschenkoWithRestrainedWarpingStiffness matrix.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def num_nodes() -> int:
        raise ValueError('Element has non uniform placement of nodes')

    @staticmethod
    def element_dof() -> int:
        """Number of DOF per element."""
        return 20

    @staticmethod
    def dof_increment_per_element() -> int:
        """The increment of global DOF per new element."""
        return 13

    @staticmethod
    def deformation_transformation() -> bool:
        """True, if the global beam deformations have to transformed from the global to the element coordinate system."""
        return False

    @staticmethod
    def ignore_warping() -> bool:
        return False

    @staticmethod
    def node_positions_norm() -> list[list[float]]:
        return [
            [0, 0.5, 1],
            [0, 0.5, 1],
            [0, 1. / 3., 2. / 3., 1],
            [0, 0.5, 1],
            [0, 0.5, 1],
            [0, 1],
            [0, 1],
        ]

    @classmethod
    def A_matrix(cls) -> sp.csc_array:
        if not hasattr(cls, '_A_matrix'):
            cls._A_matrix = sp.dok_array(
                [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                 ]
            ).tocsc()
        return cls._A_matrix

    @property
    def element_stiffness_matrix(self):
        """numpy.ndarray: The FE element stiffness matrix."""
        if not hasattr(self, '_element_stiffness_matrix'):
            dtype = self._dtype
            l = self.length
            S = self.cross_section_stiffness_matrix
            K_m = sp.dok_array((20, 20), dtype=dtype)

            K_m[0, 0] = (7 / 3) * S[0, 0] / l
            K_m[0, 1] = -8 / 3 * S[0, 0] / l
            K_m[0, 2] = (1 / 3) * S[0, 0] / l
            K_m[0, 3] = (7 / 3) * S[0, 1] / l
            K_m[0, 4] = -8 / 3 * S[0, 1] / l
            K_m[0, 5] = (1 / 3) * S[0, 1] / l
            K_m[0, 6] = (5 / 2) * S[0, 2] / l
            K_m[0, 7] = -3 / 2 * S[0, 2] / l
            K_m[0, 8] = -3 / 2 * S[0, 2] / l
            K_m[0, 9] = (1 / 2) * S[0, 2] / l
            K_m[0, 10] = -1 / 2 * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[0, 11] = -1 / 3 * (2 * S[0, 1] * l + 8 * S[0, 3]) / l
            K_m[0, 12] = (1 / 6) * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[0, 13] = (1 / 2) * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[0, 14] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[0, 15] = -1 / 6 * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[0, 16] = (S[0, 5] * l + 4 * S[0, 6]) / l ** 2
            K_m[0, 17] = -(S[0, 5] * l + 4 * S[0, 6]) / l ** 2
            K_m[0, 18] = -1 / 3 * S[0, 5] + 3 * S[0, 6] / l
            K_m[0, 19] = (1 / 3) * S[0, 5] + S[0, 6] / l
            K_m[1, 0] = -8 / 3 * S[0, 0] / l
            K_m[1, 1] = (16 / 3) * S[0, 0] / l
            K_m[1, 2] = -8 / 3 * S[0, 0] / l
            K_m[1, 3] = -8 / 3 * S[0, 1] / l
            K_m[1, 4] = (16 / 3) * S[0, 1] / l
            K_m[1, 5] = -8 / 3 * S[0, 1] / l
            K_m[1, 6] = -3 * S[0, 2] / l
            K_m[1, 7] = 3 * S[0, 2] / l
            K_m[1, 8] = 3 * S[0, 2] / l
            K_m[1, 9] = -3 * S[0, 2] / l
            K_m[1, 10] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[1, 11] = (16 / 3) * S[0, 3] / l
            K_m[1, 12] = -1 / 3 * (2 * S[0, 1] * l + 8 * S[0, 3]) / l
            K_m[1, 13] = -1 / 3 * (2 * S[0, 0] * l + 8 * S[0, 4]) / l
            K_m[1, 14] = (16 / 3) * S[0, 4] / l
            K_m[1, 15] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[1, 16] = -8 * S[0, 6] / l ** 2
            K_m[1, 17] = 8 * S[0, 6] / l ** 2
            K_m[1, 18] = (2 / 3) * S[0, 5] - 4 * S[0, 6] / l
            K_m[1, 19] = -2 / 3 * S[0, 5] - 4 * S[0, 6] / l
            K_m[2, 0] = (1 / 3) * S[0, 0] / l
            K_m[2, 1] = -8 / 3 * S[0, 0] / l
            K_m[2, 2] = (7 / 3) * S[0, 0] / l
            K_m[2, 3] = (1 / 3) * S[0, 1] / l
            K_m[2, 4] = -8 / 3 * S[0, 1] / l
            K_m[2, 5] = (7 / 3) * S[0, 1] / l
            K_m[2, 6] = (1 / 2) * S[0, 2] / l
            K_m[2, 7] = -3 / 2 * S[0, 2] / l
            K_m[2, 8] = -3 / 2 * S[0, 2] / l
            K_m[2, 9] = (5 / 2) * S[0, 2] / l
            K_m[2, 10] = -1 / 6 * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[2, 11] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[2, 12] = (1 / 2) * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[2, 13] = (1 / 6) * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[2, 14] = -1 / 3 * (2 * S[0, 0] * l + 8 * S[0, 4]) / l
            K_m[2, 15] = -1 / 2 * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[2, 16] = (-S[0, 5] * l + 4 * S[0, 6]) / l ** 2
            K_m[2, 17] = (S[0, 5] * l - 4 * S[0, 6]) / l ** 2
            K_m[2, 18] = -1 / 3 * S[0, 5] + S[0, 6] / l
            K_m[2, 19] = (1 / 3) * S[0, 5] + 3 * S[0, 6] / l
            K_m[3, 0] = (7 / 3) * S[1, 0] / l
            K_m[3, 1] = -8 / 3 * S[1, 0] / l
            K_m[3, 2] = (1 / 3) * S[1, 0] / l
            K_m[3, 3] = (7 / 3) * S[1, 1] / l
            K_m[3, 4] = -8 / 3 * S[1, 1] / l
            K_m[3, 5] = (1 / 3) * S[1, 1] / l
            K_m[3, 6] = (5 / 2) * S[1, 2] / l
            K_m[3, 7] = -3 / 2 * S[1, 2] / l
            K_m[3, 8] = -3 / 2 * S[1, 2] / l
            K_m[3, 9] = (1 / 2) * S[1, 2] / l
            K_m[3, 10] = -1 / 2 * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[3, 11] = -1 / 3 * (2 * S[1, 1] * l + 8 * S[1, 3]) / l
            K_m[3, 12] = (1 / 6) * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[3, 13] = (1 / 2) * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[3, 14] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[3, 15] = -1 / 6 * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[3, 16] = (S[1, 5] * l + 4 * S[1, 6]) / l ** 2
            K_m[3, 17] = -(S[1, 5] * l + 4 * S[1, 6]) / l ** 2
            K_m[3, 18] = -1 / 3 * S[1, 5] + 3 * S[1, 6] / l
            K_m[3, 19] = (1 / 3) * S[1, 5] + S[1, 6] / l
            K_m[4, 0] = -8 / 3 * S[1, 0] / l
            K_m[4, 1] = (16 / 3) * S[1, 0] / l
            K_m[4, 2] = -8 / 3 * S[1, 0] / l
            K_m[4, 3] = -8 / 3 * S[1, 1] / l
            K_m[4, 4] = (16 / 3) * S[1, 1] / l
            K_m[4, 5] = -8 / 3 * S[1, 1] / l
            K_m[4, 6] = -3 * S[1, 2] / l
            K_m[4, 7] = 3 * S[1, 2] / l
            K_m[4, 8] = 3 * S[1, 2] / l
            K_m[4, 9] = -3 * S[1, 2] / l
            K_m[4, 10] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[4, 11] = (16 / 3) * S[1, 3] / l
            K_m[4, 12] = -1 / 3 * (2 * S[1, 1] * l + 8 * S[1, 3]) / l
            K_m[4, 13] = -1 / 3 * (2 * S[1, 0] * l + 8 * S[1, 4]) / l
            K_m[4, 14] = (16 / 3) * S[1, 4] / l
            K_m[4, 15] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[4, 16] = -8 * S[1, 6] / l ** 2
            K_m[4, 17] = 8 * S[1, 6] / l ** 2
            K_m[4, 18] = (2 / 3) * S[1, 5] - 4 * S[1, 6] / l
            K_m[4, 19] = -2 / 3 * S[1, 5] - 4 * S[1, 6] / l
            K_m[5, 0] = (1 / 3) * S[1, 0] / l
            K_m[5, 1] = -8 / 3 * S[1, 0] / l
            K_m[5, 2] = (7 / 3) * S[1, 0] / l
            K_m[5, 3] = (1 / 3) * S[1, 1] / l
            K_m[5, 4] = -8 / 3 * S[1, 1] / l
            K_m[5, 5] = (7 / 3) * S[1, 1] / l
            K_m[5, 6] = (1 / 2) * S[1, 2] / l
            K_m[5, 7] = -3 / 2 * S[1, 2] / l
            K_m[5, 8] = -3 / 2 * S[1, 2] / l
            K_m[5, 9] = (5 / 2) * S[1, 2] / l
            K_m[5, 10] = -1 / 6 * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[5, 11] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[5, 12] = (1 / 2) * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[5, 13] = (1 / 6) * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[5, 14] = -1 / 3 * (2 * S[1, 0] * l + 8 * S[1, 4]) / l
            K_m[5, 15] = -1 / 2 * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[5, 16] = (-S[1, 5] * l + 4 * S[1, 6]) / l ** 2
            K_m[5, 17] = (S[1, 5] * l - 4 * S[1, 6]) / l ** 2
            K_m[5, 18] = -1 / 3 * S[1, 5] + S[1, 6] / l
            K_m[5, 19] = (1 / 3) * S[1, 5] + 3 * S[1, 6] / l
            K_m[6, 0] = (5 / 2) * S[2, 0] / l
            K_m[6, 1] = -3 * S[2, 0] / l
            K_m[6, 2] = (1 / 2) * S[2, 0] / l
            K_m[6, 3] = (5 / 2) * S[2, 1] / l
            K_m[6, 4] = -3 * S[2, 1] / l
            K_m[6, 5] = (1 / 2) * S[2, 1] / l
            K_m[6, 6] = (37 / 10) * S[2, 2] / l
            K_m[6, 7] = -189 / 40 * S[2, 2] / l
            K_m[6, 8] = (27 / 20) * S[2, 2] / l
            K_m[6, 9] = -13 / 40 * S[2, 2] / l
            K_m[6, 10] = (1 / 120) * (-83 * S[2, 1] * l + 300 * S[2, 3]) / l
            K_m[6, 11] = -11 / 30 * S[2, 1] - 3 * S[2, 3] / l
            K_m[6, 12] = (7 / 120) * S[2, 1] + (1 / 2) * S[2, 3] / l
            K_m[6, 13] = (1 / 120) * (83 * S[2, 0] * l + 300 * S[2, 4]) / l
            K_m[6, 14] = (11 / 30) * S[2, 0] - 3 * S[2, 4] / l
            K_m[6, 15] = -7 / 120 * S[2, 0] + (1 / 2) * S[2, 4] / l
            K_m[6, 16] = (1 / 20) * (11 * S[2, 5] * l + 90 * S[2, 6]) / l ** 2
            K_m[6, 17] = -1 / 20 * (11 * S[2, 5] * l + 90 * S[2, 6]) / l ** 2
            K_m[6, 18] = (1 / 20) * (-12 * S[2, 5] * l + 65 * S[2, 6]) / l
            K_m[6, 19] = (1 / 20) * (3 * S[2, 5] * l + 25 * S[2, 6]) / l
            K_m[7, 0] = -3 / 2 * S[2, 0] / l
            K_m[7, 1] = 3 * S[2, 0] / l
            K_m[7, 2] = -3 / 2 * S[2, 0] / l
            K_m[7, 3] = -3 / 2 * S[2, 1] / l
            K_m[7, 4] = 3 * S[2, 1] / l
            K_m[7, 5] = -3 / 2 * S[2, 1] / l
            K_m[7, 6] = -189 / 40 * S[2, 2] / l
            K_m[7, 7] = (54 / 5) * S[2, 2] / l
            K_m[7, 8] = -297 / 40 * S[2, 2] / l
            K_m[7, 9] = (27 / 20) * S[2, 2] / l
            K_m[7, 10] = (3 / 40) * (11 * S[2, 1] * l - 20 * S[2, 3]) / l
            K_m[7, 11] = -9 / 10 * S[2, 1] + 3 * S[2, 3] / l
            K_m[7, 12] = (3 / 40) * (S[2, 1] * l - 20 * S[2, 3]) / l
            K_m[7, 13] = -1 / 40 * (33 * S[2, 0] * l + 60 * S[2, 4]) / l
            K_m[7, 14] = (9 / 10) * S[2, 0] + 3 * S[2, 4] / l
            K_m[7, 15] = -1 / 40 * (3 * S[2, 0] * l + 60 * S[2, 4]) / l
            K_m[7, 16] = (9 / 20) * (3 * S[2, 5] * l - 10 * S[2, 6]) / l ** 2
            K_m[7, 17] = (9 / 20) * (-3 * S[2, 5] * l + 10 * S[2, 6]) / l ** 2
            K_m[7, 18] = (3 / 20) * (7 * S[2, 5] * l - 15 * S[2, 6]) / l
            K_m[7, 19] = (3 / 20) * (2 * S[2, 5] * l - 15 * S[2, 6]) / l
            K_m[8, 0] = -3 / 2 * S[2, 0] / l
            K_m[8, 1] = 3 * S[2, 0] / l
            K_m[8, 2] = -3 / 2 * S[2, 0] / l
            K_m[8, 3] = -3 / 2 * S[2, 1] / l
            K_m[8, 4] = 3 * S[2, 1] / l
            K_m[8, 5] = -3 / 2 * S[2, 1] / l
            K_m[8, 6] = (27 / 20) * S[2, 2] / l
            K_m[8, 7] = -297 / 40 * S[2, 2] / l
            K_m[8, 8] = (54 / 5) * S[2, 2] / l
            K_m[8, 9] = -189 / 40 * S[2, 2] / l
            K_m[8, 10] = -1 / 40 * (3 * S[2, 1] * l + 60 * S[2, 3]) / l
            K_m[8, 11] = (9 / 10) * S[2, 1] + 3 * S[2, 3] / l
            K_m[8, 12] = -1 / 40 * (33 * S[2, 1] * l + 60 * S[2, 3]) / l
            K_m[8, 13] = (3 / 40) * (S[2, 0] * l - 20 * S[2, 4]) / l
            K_m[8, 14] = -9 / 10 * S[2, 0] + 3 * S[2, 4] / l
            K_m[8, 15] = (3 / 40) * (11 * S[2, 0] * l - 20 * S[2, 4]) / l
            K_m[8, 16] = -1 / 20 * (27 * S[2, 5] * l + 90 * S[2, 6]) / l ** 2
            K_m[8, 17] = (9 / 20) * (3 * S[2, 5] * l + 10 * S[2, 6]) / l ** 2
            K_m[8, 18] = -1 / 20 * (6 * S[2, 5] * l + 45 * S[2, 6]) / l
            K_m[8, 19] = -1 / 20 * (21 * S[2, 5] * l + 45 * S[2, 6]) / l
            K_m[9, 0] = (1 / 2) * S[2, 0] / l
            K_m[9, 1] = -3 * S[2, 0] / l
            K_m[9, 2] = (5 / 2) * S[2, 0] / l
            K_m[9, 3] = (1 / 2) * S[2, 1] / l
            K_m[9, 4] = -3 * S[2, 1] / l
            K_m[9, 5] = (5 / 2) * S[2, 1] / l
            K_m[9, 6] = -13 / 40 * S[2, 2] / l
            K_m[9, 7] = (27 / 20) * S[2, 2] / l
            K_m[9, 8] = -189 / 40 * S[2, 2] / l
            K_m[9, 9] = (37 / 10) * S[2, 2] / l
            K_m[9, 10] = -7 / 120 * S[2, 1] + (1 / 2) * S[2, 3] / l
            K_m[9, 11] = (11 / 30) * S[2, 1] - 3 * S[2, 3] / l
            K_m[9, 12] = (1 / 120) * (83 * S[2, 1] * l + 300 * S[2, 3]) / l
            K_m[9, 13] = (7 / 120) * S[2, 0] + (1 / 2) * S[2, 4] / l
            K_m[9, 14] = -11 / 30 * S[2, 0] - 3 * S[2, 4] / l
            K_m[9, 15] = (1 / 120) * (-83 * S[2, 0] * l + 300 * S[2, 4]) / l
            K_m[9, 16] = (1 / 20) * (-11 * S[2, 5] * l + 90 * S[2, 6]) / l ** 2
            K_m[9, 17] = (1 / 20) * (11 * S[2, 5] * l - 90 * S[2, 6]) / l ** 2
            K_m[9, 18] = (1 / 20) * (-3 * S[2, 5] * l + 25 * S[2, 6]) / l
            K_m[9, 19] = (1 / 20) * (12 * S[2, 5] * l + 65 * S[2, 6]) / l
            K_m[10, 0] = -1 / 2 * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[10, 1] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[10, 2] = -1 / 6 * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[10, 3] = -1 / 2 * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[10, 4] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[10, 5] = -1 / 6 * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[10, 6] = (1 / 120) * (-83 * S[1, 2] * l + 300 * S[3, 2]) / l
            K_m[10, 7] = (3 / 40) * (11 * S[1, 2] * l - 20 * S[3, 2]) / l
            K_m[10, 8] = -1 / 40 * (3 * S[1, 2] * l + 60 * S[3, 2]) / l
            K_m[10, 9] = -7 / 120 * S[1, 2] + (1 / 2) * S[3, 2] / l
            K_m[10, 10] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l - 15 * S[1, 3] - 15 * S[3, 1])) / l
            K_m[10, 11] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[10, 12] = -1 / 30 * S[1, 1] * l - 1 / 6 * S[1, 3] + (1 / 6) * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[10, 13] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l - 15 * S[1, 4] + 15 * S[3, 0])) / l
            K_m[10, 14] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[10, 15] = (1 / 30) * S[1, 0] * l - 1 / 6 * S[1, 4] - 1 / 6 * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[10, 16] = -1 / 10 * S[1, 5] - S[1, 6] / l + S[3, 5] / l + 4 * S[3, 6] / l ** 2
            K_m[10, 17] = (1 / 10) * S[1, 5] + S[1, 6] / l - S[3, 5] / l - 4 * S[3, 6] / l ** 2
            K_m[10, 18] = (1 / 60) * (180 * S[3, 6] + l * (7 * S[1, 5] * l - 40 * S[1, 6] - 20 * S[3, 5])) / l
            K_m[10, 19] = -1 / 20 * S[1, 5] * l - 1 / 3 * S[1, 6] + (1 / 3) * S[3, 5] + S[3, 6] / l
            K_m[11, 0] = -1 / 3 * (2 * S[1, 0] * l + 8 * S[3, 0]) / l
            K_m[11, 1] = (16 / 3) * S[3, 0] / l
            K_m[11, 2] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[11, 3] = -1 / 3 * (2 * S[1, 1] * l + 8 * S[3, 1]) / l
            K_m[11, 4] = (16 / 3) * S[3, 1] / l
            K_m[11, 5] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[11, 6] = -11 / 30 * S[1, 2] - 3 * S[3, 2] / l
            K_m[11, 7] = -9 / 10 * S[1, 2] + 3 * S[3, 2] / l
            K_m[11, 8] = (9 / 10) * S[1, 2] + 3 * S[3, 2] / l
            K_m[11, 9] = (11 / 30) * S[1, 2] - 3 * S[3, 2] / l
            K_m[11, 10] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[11, 11] = (8 / 15) * (S[1, 1] * l ** 2 + 10 * S[3, 3]) / l
            K_m[11, 12] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[11, 13] = -1 / 15 * (40 * S[3, 4] + l * (S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[11, 14] = (8 / 15) * (-S[1, 0] * l ** 2 + 10 * S[3, 4]) / l
            K_m[11, 15] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[11, 16] = -4 / 5 * S[1, 5] - 8 * S[3, 6] / l ** 2
            K_m[11, 17] = (4 / 5) * S[1, 5] + 8 * S[3, 6] / l ** 2
            K_m[11, 18] = (1 / 15) * (-60 * S[3, 6] + l * (-S[1, 5] * l - 10 * S[1, 6] + 10 * S[3, 5])) / l
            K_m[11, 19] = (1 / 15) * (-60 * S[3, 6] + l * (-S[1, 5] * l + 10 * S[1, 6] - 10 * S[3, 5])) / l
            K_m[12, 0] = (1 / 6) * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[12, 1] = -1 / 3 * (2 * S[1, 0] * l + 8 * S[3, 0]) / l
            K_m[12, 2] = (1 / 2) * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[12, 3] = (1 / 6) * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[12, 4] = -1 / 3 * (2 * S[1, 1] * l + 8 * S[3, 1]) / l
            K_m[12, 5] = (1 / 2) * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[12, 6] = (7 / 120) * S[1, 2] + (1 / 2) * S[3, 2] / l
            K_m[12, 7] = (3 / 40) * (S[1, 2] * l - 20 * S[3, 2]) / l
            K_m[12, 8] = -1 / 40 * (33 * S[1, 2] * l + 60 * S[3, 2]) / l
            K_m[12, 9] = (1 / 120) * (83 * S[1, 2] * l + 300 * S[3, 2]) / l
            K_m[12, 10] = -1 / 30 * S[1, 1] * l + (1 / 6) * S[1, 3] - 1 / 6 * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[12, 11] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[12, 12] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l + 15 * S[1, 3] + 15 * S[3, 1])) / l
            K_m[12, 13] = (1 / 30) * S[1, 0] * l + (1 / 6) * S[1, 4] + (1 / 6) * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[12, 14] = -1 / 15 * (40 * S[3, 4] + l * (S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[12, 15] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l + 15 * S[1, 4] - 15 * S[3, 0])) / l
            K_m[12, 16] = -1 / 10 * S[1, 5] + S[1, 6] / l - S[3, 5] / l + 4 * S[3, 6] / l ** 2
            K_m[12, 17] = (1 / 10) * S[1, 5] - S[1, 6] / l + S[3, 5] / l - 4 * S[3, 6] / l ** 2
            K_m[12, 18] = -1 / 20 * S[1, 5] * l + (1 / 3) * S[1, 6] - 1 / 3 * S[3, 5] + S[3, 6] / l
            K_m[12, 19] = (1 / 60) * (180 * S[3, 6] + l * (7 * S[1, 5] * l + 40 * S[1, 6] + 20 * S[3, 5])) / l
            K_m[13, 0] = (1 / 2) * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[13, 1] = -1 / 3 * (2 * S[0, 0] * l + 8 * S[4, 0]) / l
            K_m[13, 2] = (1 / 6) * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[13, 3] = (1 / 2) * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[13, 4] = -1 / 3 * (2 * S[0, 1] * l + 8 * S[4, 1]) / l
            K_m[13, 5] = (1 / 6) * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[13, 6] = (1 / 120) * (83 * S[0, 2] * l + 300 * S[4, 2]) / l
            K_m[13, 7] = -1 / 40 * (33 * S[0, 2] * l + 60 * S[4, 2]) / l
            K_m[13, 8] = (3 / 40) * (S[0, 2] * l - 20 * S[4, 2]) / l
            K_m[13, 9] = (7 / 120) * S[0, 2] + (1 / 2) * S[4, 2] / l
            K_m[13, 10] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l + 15 * S[0, 3] - 15 * S[4, 1])) / l
            K_m[13, 11] = -1 / 15 * (40 * S[4, 3] + l * (S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[13, 12] = (1 / 30) * S[0, 1] * l + (1 / 6) * S[0, 3] + (1 / 6) * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[13, 13] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l + 15 * S[0, 4] + 15 * S[4, 0])) / l
            K_m[13, 14] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[13, 15] = -1 / 30 * S[0, 0] * l + (1 / 6) * S[0, 4] - 1 / 6 * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[13, 16] = (1 / 10) * S[0, 5] + S[0, 6] / l + S[4, 5] / l + 4 * S[4, 6] / l ** 2
            K_m[13, 17] = -1 / 10 * S[0, 5] - S[0, 6] / l - S[4, 5] / l - 4 * S[4, 6] / l ** 2
            K_m[13, 18] = (1 / 60) * (180 * S[4, 6] + l * (-7 * S[0, 5] * l + 40 * S[0, 6] - 20 * S[4, 5])) / l
            K_m[13, 19] = (1 / 20) * S[0, 5] * l + (1 / 3) * S[0, 6] + (1 / 3) * S[4, 5] + S[4, 6] / l
            K_m[14, 0] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[14, 1] = (16 / 3) * S[4, 0] / l
            K_m[14, 2] = -1 / 3 * (2 * S[0, 0] * l + 8 * S[4, 0]) / l
            K_m[14, 3] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[14, 4] = (16 / 3) * S[4, 1] / l
            K_m[14, 5] = -1 / 3 * (2 * S[0, 1] * l + 8 * S[4, 1]) / l
            K_m[14, 6] = (11 / 30) * S[0, 2] - 3 * S[4, 2] / l
            K_m[14, 7] = (9 / 10) * S[0, 2] + 3 * S[4, 2] / l
            K_m[14, 8] = -9 / 10 * S[0, 2] + 3 * S[4, 2] / l
            K_m[14, 9] = -11 / 30 * S[0, 2] - 3 * S[4, 2] / l
            K_m[14, 10] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[14, 11] = (8 / 15) * (-S[0, 1] * l ** 2 + 10 * S[4, 3]) / l
            K_m[14, 12] = -1 / 15 * (40 * S[4, 3] + l * (S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[14, 13] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[14, 14] = (8 / 15) * (S[0, 0] * l ** 2 + 10 * S[4, 4]) / l
            K_m[14, 15] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[14, 16] = (4 / 5) * S[0, 5] - 8 * S[4, 6] / l ** 2
            K_m[14, 17] = -4 / 5 * S[0, 5] + 8 * S[4, 6] / l ** 2
            K_m[14, 18] = (1 / 15) * (-60 * S[4, 6] + l * (S[0, 5] * l + 10 * S[0, 6] + 10 * S[4, 5])) / l
            K_m[14, 19] = (1 / 15) * (-60 * S[4, 6] + l * (S[0, 5] * l - 10 * S[0, 6] - 10 * S[4, 5])) / l
            K_m[15, 0] = -1 / 6 * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[15, 1] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[15, 2] = -1 / 2 * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[15, 3] = -1 / 6 * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[15, 4] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[15, 5] = -1 / 2 * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[15, 6] = -7 / 120 * S[0, 2] + (1 / 2) * S[4, 2] / l
            K_m[15, 7] = -1 / 40 * (3 * S[0, 2] * l + 60 * S[4, 2]) / l
            K_m[15, 8] = (3 / 40) * (11 * S[0, 2] * l - 20 * S[4, 2]) / l
            K_m[15, 9] = (1 / 120) * (-83 * S[0, 2] * l + 300 * S[4, 2]) / l
            K_m[15, 10] = (1 / 30) * S[0, 1] * l - 1 / 6 * S[0, 3] - 1 / 6 * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[15, 11] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[15, 12] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l - 15 * S[0, 3] + 15 * S[4, 1])) / l
            K_m[15, 13] = -1 / 30 * S[0, 0] * l - 1 / 6 * S[0, 4] + (1 / 6) * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[15, 14] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[15, 15] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l - 15 * S[0, 4] - 15 * S[4, 0])) / l
            K_m[15, 16] = (1 / 10) * S[0, 5] - S[0, 6] / l - S[4, 5] / l + 4 * S[4, 6] / l ** 2
            K_m[15, 17] = -1 / 10 * S[0, 5] + S[0, 6] / l + S[4, 5] / l - 4 * S[4, 6] / l ** 2
            K_m[15, 18] = (1 / 20) * S[0, 5] * l - 1 / 3 * S[0, 6] - 1 / 3 * S[4, 5] + S[4, 6] / l
            K_m[15, 19] = (1 / 60) * (180 * S[4, 6] + l * (-7 * S[0, 5] * l - 40 * S[0, 6] + 20 * S[4, 5])) / l
            K_m[16, 0] = (S[5, 0] * l + 4 * S[6, 0]) / l ** 2
            K_m[16, 1] = -8 * S[6, 0] / l ** 2
            K_m[16, 2] = (-S[5, 0] * l + 4 * S[6, 0]) / l ** 2
            K_m[16, 3] = (S[5, 1] * l + 4 * S[6, 1]) / l ** 2
            K_m[16, 4] = -8 * S[6, 1] / l ** 2
            K_m[16, 5] = (-S[5, 1] * l + 4 * S[6, 1]) / l ** 2
            K_m[16, 6] = (1 / 20) * (11 * S[5, 2] * l + 90 * S[6, 2]) / l ** 2
            K_m[16, 7] = (9 / 20) * (3 * S[5, 2] * l - 10 * S[6, 2]) / l ** 2
            K_m[16, 8] = -1 / 20 * (27 * S[5, 2] * l + 90 * S[6, 2]) / l ** 2
            K_m[16, 9] = (1 / 20) * (-11 * S[5, 2] * l + 90 * S[6, 2]) / l ** 2
            K_m[16, 10] = -1 / 10 * S[5, 1] + S[5, 3] / l - S[6, 1] / l + 4 * S[6, 3] / l ** 2
            K_m[16, 11] = -4 / 5 * S[5, 1] - 8 * S[6, 3] / l ** 2
            K_m[16, 12] = -1 / 10 * S[5, 1] - S[5, 3] / l + S[6, 1] / l + 4 * S[6, 3] / l ** 2
            K_m[16, 13] = (1 / 10) * S[5, 0] + S[5, 4] / l + S[6, 0] / l + 4 * S[6, 4] / l ** 2
            K_m[16, 14] = (4 / 5) * S[5, 0] - 8 * S[6, 4] / l ** 2
            K_m[16, 15] = (1 / 10) * S[5, 0] - S[5, 4] / l - S[6, 0] / l + 4 * S[6, 4] / l ** 2
            K_m[16, 16] = (6 / 5) * S[5, 5] / l + 12 * S[6, 6] / l ** 3
            K_m[16, 17] = -6 / 5 * S[5, 5] / l - 12 * S[6, 6] / l ** 3
            K_m[16, 18] = (1 / 10) * S[5, 5] + S[5, 6] / l - S[6, 5] / l + 6 * S[6, 6] / l ** 2
            K_m[16, 19] = (1 / 10) * S[5, 5] - S[5, 6] / l + S[6, 5] / l + 6 * S[6, 6] / l ** 2
            K_m[17, 0] = -(S[5, 0] * l + 4 * S[6, 0]) / l ** 2
            K_m[17, 1] = 8 * S[6, 0] / l ** 2
            K_m[17, 2] = (S[5, 0] * l - 4 * S[6, 0]) / l ** 2
            K_m[17, 3] = -(S[5, 1] * l + 4 * S[6, 1]) / l ** 2
            K_m[17, 4] = 8 * S[6, 1] / l ** 2
            K_m[17, 5] = (S[5, 1] * l - 4 * S[6, 1]) / l ** 2
            K_m[17, 6] = -1 / 20 * (11 * S[5, 2] * l + 90 * S[6, 2]) / l ** 2
            K_m[17, 7] = (9 / 20) * (-3 * S[5, 2] * l + 10 * S[6, 2]) / l ** 2
            K_m[17, 8] = (9 / 20) * (3 * S[5, 2] * l + 10 * S[6, 2]) / l ** 2
            K_m[17, 9] = (1 / 20) * (11 * S[5, 2] * l - 90 * S[6, 2]) / l ** 2
            K_m[17, 10] = (1 / 10) * S[5, 1] - S[5, 3] / l + S[6, 1] / l - 4 * S[6, 3] / l ** 2
            K_m[17, 11] = (4 / 5) * S[5, 1] + 8 * S[6, 3] / l ** 2
            K_m[17, 12] = (1 / 10) * S[5, 1] + S[5, 3] / l - S[6, 1] / l - 4 * S[6, 3] / l ** 2
            K_m[17, 13] = -1 / 10 * S[5, 0] - S[5, 4] / l - S[6, 0] / l - 4 * S[6, 4] / l ** 2
            K_m[17, 14] = -4 / 5 * S[5, 0] + 8 * S[6, 4] / l ** 2
            K_m[17, 15] = -1 / 10 * S[5, 0] + S[5, 4] / l + S[6, 0] / l - 4 * S[6, 4] / l ** 2
            K_m[17, 16] = -6 / 5 * S[5, 5] / l - 12 * S[6, 6] / l ** 3
            K_m[17, 17] = (6 / 5) * S[5, 5] / l + 12 * S[6, 6] / l ** 3
            K_m[17, 18] = -1 / 10 * S[5, 5] - S[5, 6] / l + S[6, 5] / l - 6 * S[6, 6] / l ** 2
            K_m[17, 19] = -1 / 10 * S[5, 5] + S[5, 6] / l - S[6, 5] / l - 6 * S[6, 6] / l ** 2
            K_m[18, 0] = -1 / 3 * S[5, 0] + 3 * S[6, 0] / l
            K_m[18, 1] = (2 / 3) * S[5, 0] - 4 * S[6, 0] / l
            K_m[18, 2] = -1 / 3 * S[5, 0] + S[6, 0] / l
            K_m[18, 3] = -1 / 3 * S[5, 1] + 3 * S[6, 1] / l
            K_m[18, 4] = (2 / 3) * S[5, 1] - 4 * S[6, 1] / l
            K_m[18, 5] = -1 / 3 * S[5, 1] + S[6, 1] / l
            K_m[18, 6] = (1 / 20) * (-12 * S[5, 2] * l + 65 * S[6, 2]) / l
            K_m[18, 7] = (3 / 20) * (7 * S[5, 2] * l - 15 * S[6, 2]) / l
            K_m[18, 8] = -1 / 20 * (6 * S[5, 2] * l + 45 * S[6, 2]) / l
            K_m[18, 9] = (1 / 20) * (-3 * S[5, 2] * l + 25 * S[6, 2]) / l
            K_m[18, 10] = (1 / 60) * (180 * S[6, 3] + l * (7 * S[5, 1] * l - 20 * S[5, 3] - 40 * S[6, 1])) / l
            K_m[18, 11] = (1 / 15) * (-60 * S[6, 3] + l * (-S[5, 1] * l + 10 * S[5, 3] - 10 * S[6, 1])) / l
            K_m[18, 12] = -1 / 20 * S[5, 1] * l - 1 / 3 * S[5, 3] + (1 / 3) * S[6, 1] + S[6, 3] / l
            K_m[18, 13] = (1 / 60) * (180 * S[6, 4] + l * (-7 * S[5, 0] * l - 20 * S[5, 4] + 40 * S[6, 0])) / l
            K_m[18, 14] = (1 / 15) * (-60 * S[6, 4] + l * (S[5, 0] * l + 10 * S[5, 4] + 10 * S[6, 0])) / l
            K_m[18, 15] = (1 / 20) * S[5, 0] * l - 1 / 3 * S[5, 4] - 1 / 3 * S[6, 0] + S[6, 4] / l
            K_m[18, 16] = (1 / 10) * S[5, 5] - S[5, 6] / l + S[6, 5] / l + 6 * S[6, 6] / l ** 2
            K_m[18, 17] = -1 / 10 * S[5, 5] + S[5, 6] / l - S[6, 5] / l - 6 * S[6, 6] / l ** 2
            K_m[18, 18] = (2 / 15) * S[5, 5] * l - 1 / 2 * S[5, 6] - 1 / 2 * S[6, 5] + 4 * S[6, 6] / l
            K_m[18, 19] = -1 / 30 * S[5, 5] * l - 1 / 2 * S[5, 6] + (1 / 2) * S[6, 5] + 2 * S[6, 6] / l
            K_m[19, 0] = (1 / 3) * S[5, 0] + S[6, 0] / l
            K_m[19, 1] = -2 / 3 * S[5, 0] - 4 * S[6, 0] / l
            K_m[19, 2] = (1 / 3) * S[5, 0] + 3 * S[6, 0] / l
            K_m[19, 3] = (1 / 3) * S[5, 1] + S[6, 1] / l
            K_m[19, 4] = -2 / 3 * S[5, 1] - 4 * S[6, 1] / l
            K_m[19, 5] = (1 / 3) * S[5, 1] + 3 * S[6, 1] / l
            K_m[19, 6] = (1 / 20) * (3 * S[5, 2] * l + 25 * S[6, 2]) / l
            K_m[19, 7] = (3 / 20) * (2 * S[5, 2] * l - 15 * S[6, 2]) / l
            K_m[19, 8] = -1 / 20 * (21 * S[5, 2] * l + 45 * S[6, 2]) / l
            K_m[19, 9] = (1 / 20) * (12 * S[5, 2] * l + 65 * S[6, 2]) / l
            K_m[19, 10] = -1 / 20 * S[5, 1] * l + (1 / 3) * S[5, 3] - 1 / 3 * S[6, 1] + S[6, 3] / l
            K_m[19, 11] = (1 / 15) * (-60 * S[6, 3] + l * (-S[5, 1] * l - 10 * S[5, 3] + 10 * S[6, 1])) / l
            K_m[19, 12] = (1 / 60) * (180 * S[6, 3] + l * (7 * S[5, 1] * l + 20 * S[5, 3] + 40 * S[6, 1])) / l
            K_m[19, 13] = (1 / 20) * S[5, 0] * l + (1 / 3) * S[5, 4] + (1 / 3) * S[6, 0] + S[6, 4] / l
            K_m[19, 14] = (1 / 15) * (-60 * S[6, 4] + l * (S[5, 0] * l - 10 * S[5, 4] - 10 * S[6, 0])) / l
            K_m[19, 15] = (1 / 60) * (180 * S[6, 4] + l * (-7 * S[5, 0] * l + 20 * S[5, 4] - 40 * S[6, 0])) / l
            K_m[19, 16] = (1 / 10) * S[5, 5] + S[5, 6] / l - S[6, 5] / l + 6 * S[6, 6] / l ** 2
            K_m[19, 17] = -1 / 10 * S[5, 5] - S[5, 6] / l + S[6, 5] / l - 6 * S[6, 6] / l ** 2
            K_m[19, 18] = -1 / 30 * S[5, 5] * l + (1 / 2) * S[5, 6] - 1 / 2 * S[6, 5] + 2 * S[6, 6] / l
            K_m[19, 19] = (2 / 15) * S[5, 5] * l + (1 / 2) * S[5, 6] + (1 / 2) * S[6, 5] + 4 * S[6, 6] / l

            self._element_stiffness_matrix = K_m.tocsc()

        return self._element_stiffness_matrix

    @property
    def element_mass_matrix(self):
        """numpy.ndarray: The FE element mass matrix."""
        if not hasattr(self, '_element_mass_matrix'):
            dtype = self._dtype
            l = self.length
            M_cs = self._cross_section_inertia_matrix
            M_m = sp.dok_array((20, 20), dtype=dtype)

            M_m[0, 0] = (2 / 15) * M_cs[0, 0] * l
            M_m[0, 1] = (1 / 15) * M_cs[0, 0] * l
            M_m[0, 2] = -1 / 30 * M_cs[0, 0] * l
            # M_m[03] = 0
            # M_m[04] = 0
            # M_m[05] = 0
            # M_m[06] = 0
            # M_m[07] = 0
            # M_m[08] = 0
            # M_m[09] = 0
            # M_m[010] = 0
            # M_m[011] = 0
            # M_m[012] = 0
            # M_m[013] = 0
            # M_m[014] = 0
            # M_m[015] = 0
            M_m[0, 16] = (11 / 60) * M_cs[0, 5] * l
            M_m[0, 17] = -1 / 60 * M_cs[0, 5] * l
            M_m[0, 18] = (1 / 60) * M_cs[0, 5] * l ** 2
            # M_m[019] = 0
            M_m[1, 0] = (1 / 15) * M_cs[0, 0] * l
            M_m[1, 1] = (8 / 15) * M_cs[0, 0] * l
            M_m[1, 2] = (1 / 15) * M_cs[0, 0] * l
            # M_m[13] = 0
            # M_m[14] = 0
            # M_m[15] = 0
            # M_m[16] = 0
            # M_m[17] = 0
            # M_m[18] = 0
            # M_m[19] = 0
            # M_m[110] = 0
            # M_m[111] = 0
            # M_m[112] = 0
            # M_m[113] = 0
            # M_m[114] = 0
            # M_m[115] = 0
            M_m[1, 16] = (1 / 3) * M_cs[0, 5] * l
            M_m[1, 17] = (1 / 3) * M_cs[0, 5] * l
            M_m[1, 18] = (1 / 15) * M_cs[0, 5] * l ** 2
            M_m[1, 19] = -1 / 15 * M_cs[0, 5] * l ** 2
            M_m[2, 0] = -1 / 30 * M_cs[0, 0] * l
            M_m[2, 1] = (1 / 15) * M_cs[0, 0] * l
            M_m[2, 2] = (2 / 15) * M_cs[0, 0] * l
            # M_m[23] = 0
            # M_m[24] = 0
            # M_m[25] = 0
            # M_m[26] = 0
            # M_m[27] = 0
            # M_m[28] = 0
            # M_m[29] = 0
            # M_m[210] = 0
            # M_m[211] = 0
            # M_m[212] = 0
            # M_m[213] = 0
            # M_m[214] = 0
            # M_m[215] = 0
            M_m[2, 16] = -1 / 60 * M_cs[0, 5] * l
            M_m[2, 17] = (11 / 60) * M_cs[0, 5] * l
            # M_m[218] = 0
            M_m[2, 19] = -1 / 60 * M_cs[0, 5] * l ** 2
            # M_m[30] = 0
            # M_m[31] = 0
            # M_m[32] = 0
            M_m[3, 3] = (2 / 15) * M_cs[1, 1] * l
            M_m[3, 4] = (1 / 15) * M_cs[1, 1] * l
            M_m[3, 5] = -1 / 30 * M_cs[1, 1] * l
            # M_m[36] = 0
            # M_m[37] = 0
            # M_m[38] = 0
            # M_m[39] = 0
            # M_m[310] = 0
            # M_m[311] = 0
            # M_m[312] = 0
            # M_m[313] = 0
            # M_m[314] = 0
            # M_m[315] = 0
            M_m[3, 16] = (11 / 60) * M_cs[1, 5] * l
            M_m[3, 17] = -1 / 60 * M_cs[1, 5] * l
            M_m[3, 18] = (1 / 60) * M_cs[1, 5] * l ** 2
            # M_m[319] = 0
            # M_m[40] = 0
            # M_m[41] = 0
            # M_m[42] = 0
            M_m[4, 3] = (1 / 15) * M_cs[1, 1] * l
            M_m[4, 4] = (8 / 15) * M_cs[1, 1] * l
            M_m[4, 5] = (1 / 15) * M_cs[1, 1] * l
            # M_m[46] = 0
            # M_m[47] = 0
            # M_m[48] = 0
            # M_m[49] = 0
            # M_m[410] = 0
            # M_m[411] = 0
            # M_m[412] = 0
            # M_m[413] = 0
            # M_m[414] = 0
            # M_m[415] = 0
            M_m[4, 16] = (1 / 3) * M_cs[1, 5] * l
            M_m[4, 17] = (1 / 3) * M_cs[1, 5] * l
            M_m[4, 18] = (1 / 15) * M_cs[1, 5] * l ** 2
            M_m[4, 19] = -1 / 15 * M_cs[1, 5] * l ** 2
            # M_m[50] = 0
            # M_m[51] = 0
            # M_m[52] = 0
            M_m[5, 3] = -1 / 30 * M_cs[1, 1] * l
            M_m[5, 4] = (1 / 15) * M_cs[1, 1] * l
            M_m[5, 5] = (2 / 15) * M_cs[1, 1] * l
            # M_m[56] = 0
            # M_m[57] = 0
            # M_m[58] = 0
            # M_m[59] = 0
            # M_m[510] = 0
            # M_m[511] = 0
            # M_m[512] = 0
            # M_m[513] = 0
            # M_m[514] = 0
            # M_m[515] = 0
            M_m[5, 16] = -1 / 60 * M_cs[1, 5] * l
            M_m[5, 17] = (11 / 60) * M_cs[1, 5] * l
            # M_m[518] = 0
            M_m[5, 19] = -1 / 60 * M_cs[1, 5] * l ** 2
            # M_m[60] = 0
            # M_m[61] = 0
            # M_m[62] = 0
            # M_m[63] = 0
            # M_m[64] = 0
            # M_m[65] = 0
            M_m[6, 6] = (8 / 105) * M_cs[2, 2] * l
            M_m[6, 7] = (33 / 560) * M_cs[2, 2] * l
            M_m[6, 8] = -3 / 140 * M_cs[2, 2] * l
            M_m[6, 9] = (19 / 1680) * M_cs[2, 2] * l
            M_m[6, 10] = (11 / 120) * M_cs[2, 3] * l
            M_m[6, 11] = (1 / 30) * M_cs[2, 3] * l
            # M_m[612] = 0
            M_m[6, 13] = (11 / 120) * M_cs[2, 4] * l
            M_m[6, 14] = (1 / 30) * M_cs[2, 4] * l
            # M_m[615] = 0
            # M_m[616] = 0
            # M_m[617] = 0
            # M_m[618] = 0
            # M_m[619] = 0
            # M_m[70] = 0
            # M_m[71] = 0
            # M_m[72] = 0
            # M_m[73] = 0
            # M_m[74] = 0
            # M_m[75] = 0
            M_m[7, 6] = (33 / 560) * M_cs[2, 2] * l
            M_m[7, 7] = (27 / 70) * M_cs[2, 2] * l
            M_m[7, 8] = -27 / 560 * M_cs[2, 2] * l
            M_m[7, 9] = -3 / 140 * M_cs[2, 2] * l
            M_m[7, 10] = (3 / 20) * M_cs[2, 3] * l
            M_m[7, 11] = (3 / 10) * M_cs[2, 3] * l
            M_m[7, 12] = -3 / 40 * M_cs[2, 3] * l
            M_m[7, 13] = (3 / 20) * M_cs[2, 4] * l
            M_m[7, 14] = (3 / 10) * M_cs[2, 4] * l
            M_m[7, 15] = -3 / 40 * M_cs[2, 4] * l
            # M_m[716] = 0
            # M_m[717] = 0
            # M_m[718] = 0
            # M_m[719] = 0
            # M_m[80] = 0
            # M_m[81] = 0
            # M_m[82] = 0
            # M_m[83] = 0
            # M_m[84] = 0
            # M_m[85] = 0
            M_m[8, 6] = -3 / 140 * M_cs[2, 2] * l
            M_m[8, 7] = -27 / 560 * M_cs[2, 2] * l
            M_m[8, 8] = (27 / 70) * M_cs[2, 2] * l
            M_m[8, 9] = (33 / 560) * M_cs[2, 2] * l
            M_m[8, 10] = -3 / 40 * M_cs[2, 3] * l
            M_m[8, 11] = (3 / 10) * M_cs[2, 3] * l
            M_m[8, 12] = (3 / 20) * M_cs[2, 3] * l
            M_m[8, 13] = -3 / 40 * M_cs[2, 4] * l
            M_m[8, 14] = (3 / 10) * M_cs[2, 4] * l
            M_m[8, 15] = (3 / 20) * M_cs[2, 4] * l
            # M_m[816] = 0
            # M_m[817] = 0
            # M_m[818] = 0
            # M_m[819] = 0
            # M_m[90] = 0
            # M_m[91] = 0
            # M_m[92] = 0
            # M_m[93] = 0
            # M_m[94] = 0
            # M_m[95] = 0
            M_m[9, 6] = (19 / 1680) * M_cs[2, 2] * l
            M_m[9, 7] = -3 / 140 * M_cs[2, 2] * l
            M_m[9, 8] = (33 / 560) * M_cs[2, 2] * l
            M_m[9, 9] = (8 / 105) * M_cs[2, 2] * l
            # M_m[910] = 0
            M_m[9, 11] = (1 / 30) * M_cs[2, 3] * l
            M_m[9, 12] = (11 / 120) * M_cs[2, 3] * l
            # M_m[913] = 0
            M_m[9, 14] = (1 / 30) * M_cs[2, 4] * l
            M_m[9, 15] = (11 / 120) * M_cs[2, 4] * l
            # M_m[916] = 0
            # M_m[917] = 0
            # M_m[918] = 0
            # M_m[919] = 0
            # M_m[100] = 0
            # M_m[101] = 0
            # M_m[102] = 0
            # M_m[103] = 0
            # M_m[104] = 0
            # M_m[105] = 0
            M_m[10, 6] = (11 / 120) * M_cs[2, 3] * l
            M_m[10, 7] = (3 / 20) * M_cs[2, 3] * l
            M_m[10, 8] = -3 / 40 * M_cs[2, 3] * l
            # M_m[109] = 0
            M_m[10, 10] = (2 / 15) * M_cs[3, 3] * l
            M_m[10, 11] = (1 / 15) * M_cs[3, 3] * l
            M_m[10, 12] = -1 / 30 * M_cs[3, 3] * l
            M_m[10, 13] = (2 / 15) * M_cs[3, 4] * l
            M_m[10, 14] = (1 / 15) * M_cs[3, 4] * l
            M_m[10, 15] = -1 / 30 * M_cs[3, 4] * l
            # M_m[1016] = 0
            # M_m[1017] = 0
            # M_m[1018] = 0
            # M_m[1019] = 0
            # M_m[110] = 0
            # M_m[111] = 0
            # M_m[112] = 0
            # M_m[113] = 0
            # M_m[114] = 0
            # M_m[115] = 0
            M_m[11, 6] = (1 / 30) * M_cs[2, 3] * l
            M_m[11, 7] = (3 / 10) * M_cs[2, 3] * l
            M_m[11, 8] = (3 / 10) * M_cs[2, 3] * l
            M_m[11, 9] = (1 / 30) * M_cs[2, 3] * l
            M_m[11, 10] = (1 / 15) * M_cs[3, 3] * l
            M_m[11, 11] = (8 / 15) * M_cs[3, 3] * l
            M_m[11, 12] = (1 / 15) * M_cs[3, 3] * l
            M_m[11, 13] = (1 / 15) * M_cs[3, 4] * l
            M_m[11, 14] = (8 / 15) * M_cs[3, 4] * l
            M_m[11, 15] = (1 / 15) * M_cs[3, 4] * l
            # M_m[1116] = 0
            # M_m[1117] = 0
            # M_m[1118] = 0
            # M_m[1119] = 0
            # M_m[120] = 0
            # M_m[121] = 0
            # M_m[122] = 0
            # M_m[123] = 0
            # M_m[124] = 0
            # M_m[125] = 0
            # M_m[126] = 0
            M_m[12, 7] = -3 / 40 * M_cs[2, 3] * l
            M_m[12, 8] = (3 / 20) * M_cs[2, 3] * l
            M_m[12, 9] = (11 / 120) * M_cs[2, 3] * l
            M_m[12, 10] = -1 / 30 * M_cs[3, 3] * l
            M_m[12, 11] = (1 / 15) * M_cs[3, 3] * l
            M_m[12, 12] = (2 / 15) * M_cs[3, 3] * l
            M_m[12, 13] = -1 / 30 * M_cs[3, 4] * l
            M_m[12, 14] = (1 / 15) * M_cs[3, 4] * l
            M_m[12, 15] = (2 / 15) * M_cs[3, 4] * l
            # M_m[1216] = 0
            # M_m[1217] = 0
            # M_m[1218] = 0
            # M_m[1219] = 0
            # M_m[130] = 0
            # M_m[131] = 0
            # M_m[132] = 0
            # M_m[133] = 0
            # M_m[134] = 0
            # M_m[135] = 0
            M_m[13, 6] = (11 / 120) * M_cs[2, 4] * l
            M_m[13, 7] = (3 / 20) * M_cs[2, 4] * l
            M_m[13, 8] = -3 / 40 * M_cs[2, 4] * l
            # M_m[139] = 0
            M_m[13, 10] = (2 / 15) * M_cs[3, 4] * l
            M_m[13, 11] = (1 / 15) * M_cs[3, 4] * l
            M_m[13, 12] = -1 / 30 * M_cs[3, 4] * l
            M_m[13, 13] = (2 / 15) * M_cs[4, 4] * l
            M_m[13, 14] = (1 / 15) * M_cs[4, 4] * l
            M_m[13, 15] = -1 / 30 * M_cs[4, 4] * l
            # M_m[1316] = 0
            # M_m[1317] = 0
            # M_m[1318] = 0
            # M_m[1319] = 0
            # M_m[140] = 0
            # M_m[141] = 0
            # M_m[142] = 0
            # M_m[143] = 0
            # M_m[144] = 0
            # M_m[145] = 0
            M_m[14, 6] = (1 / 30) * M_cs[2, 4] * l
            M_m[14, 7] = (3 / 10) * M_cs[2, 4] * l
            M_m[14, 8] = (3 / 10) * M_cs[2, 4] * l
            M_m[14, 9] = (1 / 30) * M_cs[2, 4] * l
            M_m[14, 10] = (1 / 15) * M_cs[3, 4] * l
            M_m[14, 11] = (8 / 15) * M_cs[3, 4] * l
            M_m[14, 12] = (1 / 15) * M_cs[3, 4] * l
            M_m[14, 13] = (1 / 15) * M_cs[4, 4] * l
            M_m[14, 14] = (8 / 15) * M_cs[4, 4] * l
            M_m[14, 15] = (1 / 15) * M_cs[4, 4] * l
            # M_m[1416] = 0
            # M_m[1417] = 0
            # M_m[1418] = 0
            # M_m[1419] = 0
            # M_m[150] = 0
            # M_m[151] = 0
            # M_m[152] = 0
            # M_m[153] = 0
            # M_m[154] = 0
            # M_m[155] = 0
            # M_m[156] = 0
            M_m[15, 7] = -3 / 40 * M_cs[2, 4] * l
            M_m[15, 8] = (3 / 20) * M_cs[2, 4] * l
            M_m[15, 9] = (11 / 120) * M_cs[2, 4] * l
            M_m[15, 10] = -1 / 30 * M_cs[3, 4] * l
            M_m[15, 11] = (1 / 15) * M_cs[3, 4] * l
            M_m[15, 12] = (2 / 15) * M_cs[3, 4] * l
            M_m[15, 13] = -1 / 30 * M_cs[4, 4] * l
            M_m[15, 14] = (1 / 15) * M_cs[4, 4] * l
            M_m[15, 15] = (2 / 15) * M_cs[4, 4] * l
            # M_m[1516] = 0
            # M_m[1517] = 0
            # M_m[1518] = 0
            # M_m[1519] = 0
            M_m[16, 0] = (11 / 60) * M_cs[0, 5] * l
            M_m[16, 1] = (1 / 3) * M_cs[0, 5] * l
            M_m[16, 2] = -1 / 60 * M_cs[0, 5] * l
            M_m[16, 3] = (11 / 60) * M_cs[1, 5] * l
            M_m[16, 4] = (1 / 3) * M_cs[1, 5] * l
            M_m[16, 5] = -1 / 60 * M_cs[1, 5] * l
            # M_m[166] = 0
            # M_m[167] = 0
            # M_m[168] = 0
            # M_m[169] = 0
            # M_m[1610] = 0
            # M_m[1611] = 0
            # M_m[1612] = 0
            # M_m[1613] = 0
            # M_m[1614] = 0
            # M_m[1615] = 0
            M_m[16, 16] = (13 / 35) * M_cs[5, 5] * l
            M_m[16, 17] = (9 / 70) * M_cs[5, 5] * l
            M_m[16, 18] = (11 / 210) * M_cs[5, 5] * l ** 2
            M_m[16, 19] = -13 / 420 * M_cs[5, 5] * l ** 2
            M_m[17, 0] = -1 / 60 * M_cs[0, 5] * l
            M_m[17, 1] = (1 / 3) * M_cs[0, 5] * l
            M_m[17, 2] = (11 / 60) * M_cs[0, 5] * l
            M_m[17, 3] = -1 / 60 * M_cs[1, 5] * l
            M_m[17, 4] = (1 / 3) * M_cs[1, 5] * l
            M_m[17, 5] = (11 / 60) * M_cs[1, 5] * l
            # M_m[176] = 0
            # M_m[177] = 0
            # M_m[178] = 0
            # M_m[179] = 0
            # M_m[1710] = 0
            # M_m[1711] = 0
            # M_m[1712] = 0
            # M_m[1713] = 0
            # M_m[1714] = 0
            # M_m[1715] = 0
            M_m[17, 16] = (9 / 70) * M_cs[5, 5] * l
            M_m[17, 17] = (13 / 35) * M_cs[5, 5] * l
            M_m[17, 18] = (13 / 420) * M_cs[5, 5] * l ** 2
            M_m[17, 19] = -11 / 210 * M_cs[5, 5] * l ** 2
            M_m[18, 0] = (1 / 60) * M_cs[0, 5] * l ** 2
            M_m[18, 1] = (1 / 15) * M_cs[0, 5] * l ** 2
            # M_m[182] = 0
            M_m[18, 3] = (1 / 60) * M_cs[1, 5] * l ** 2
            M_m[18, 4] = (1 / 15) * M_cs[1, 5] * l ** 2
            # M_m[185] = 0
            # M_m[186] = 0
            # M_m[187] = 0
            # M_m[188] = 0
            # M_m[189] = 0
            # M_m[1810] = 0
            # M_m[1811] = 0
            # M_m[1812] = 0
            # M_m[1813] = 0
            # M_m[1814] = 0
            # M_m[1815] = 0
            M_m[18, 16] = (11 / 210) * M_cs[5, 5] * l ** 2
            M_m[18, 17] = (13 / 420) * M_cs[5, 5] * l ** 2
            M_m[18, 18] = (1 / 105) * M_cs[5, 5] * l ** 3
            M_m[18, 19] = -1 / 140 * M_cs[5, 5] * l ** 3
            # M_m[190] = 0
            M_m[19, 1] = -1 / 15 * M_cs[0, 5] * l ** 2
            M_m[19, 2] = -1 / 60 * M_cs[0, 5] * l ** 2
            # M_m[193] = 0
            M_m[19, 4] = -1 / 15 * M_cs[1, 5] * l ** 2
            M_m[19, 5] = -1 / 60 * M_cs[1, 5] * l ** 2
            # M_m[196] = 0
            # M_m[197] = 0
            # M_m[198] = 0
            # M_m[199] = 0
            # M_m[1910] = 0
            # M_m[1911] = 0
            # M_m[1912] = 0
            # M_m[1913] = 0
            # M_m[1914] = 0
            # M_m[1915] = 0
            M_m[19, 16] = -13 / 420 * M_cs[5, 5] * l ** 2
            M_m[19, 17] = -11 / 210 * M_cs[5, 5] * l ** 2
            M_m[19, 18] = -1 / 140 * M_cs[5, 5] * l ** 3
            M_m[19, 19] = (1 / 105) * M_cs[5, 5] * l ** 3

            self._element_mass_matrix = M_m.tocsc()

        return self._element_mass_matrix

    @property
    def line_load_conversion_matrix(self):
        """numpy.ndarray: Matrix for the conversion of line loads at the nodes (end nodes and integration point nodes) to node loads."""
        if not hasattr(self, '_line_load_conversion_matrix'):
            dtype = self._dtype
            l = self.length
            F_L_m = sp.dok_array((20, 20), dtype=dtype)

            F_L_m[0, 0] = (2 / 15) * l
            F_L_m[0, 1] = (1 / 15) * l
            F_L_m[0, 2] = -1 / 30 * l
            # F_L_m[03] = 0
            # F_L_m[04] = 0
            # F_L_m[05] = 0
            # F_L_m[06] = 0
            # F_L_m[07] = 0
            # F_L_m[08] = 0
            # F_L_m[09] = 0
            # F_L_m[010] = 0
            # F_L_m[011] = 0
            # F_L_m[012] = 0
            # F_L_m[013] = 0
            # F_L_m[014] = 0
            # F_L_m[015] = 0
            # F_L_m[016] = 0
            # F_L_m[017] = 0
            # F_L_m[018] = 0
            # F_L_m[019] = 0
            F_L_m[1, 0] = (1 / 15) * l
            F_L_m[1, 1] = (8 / 15) * l
            F_L_m[1, 2] = (1 / 15) * l
            # F_L_m[13] = 0
            # F_L_m[14] = 0
            # F_L_m[15] = 0
            # F_L_m[16] = 0
            # F_L_m[17] = 0
            # F_L_m[18] = 0
            # F_L_m[19] = 0
            # F_L_m[110] = 0
            # F_L_m[111] = 0
            # F_L_m[112] = 0
            # F_L_m[113] = 0
            # F_L_m[114] = 0
            # F_L_m[115] = 0
            # F_L_m[116] = 0
            # F_L_m[117] = 0
            # F_L_m[118] = 0
            # F_L_m[119] = 0
            F_L_m[2, 0] = -1 / 30 * l
            F_L_m[2, 1] = (1 / 15) * l
            F_L_m[2, 2] = (2 / 15) * l
            # F_L_m[23] = 0
            # F_L_m[24] = 0
            # F_L_m[25] = 0
            # F_L_m[26] = 0
            # F_L_m[27] = 0
            # F_L_m[28] = 0
            # F_L_m[29] = 0
            # F_L_m[210] = 0
            # F_L_m[211] = 0
            # F_L_m[212] = 0
            # F_L_m[213] = 0
            # F_L_m[214] = 0
            # F_L_m[215] = 0
            # F_L_m[216] = 0
            # F_L_m[217] = 0
            # F_L_m[218] = 0
            # F_L_m[219] = 0
            # F_L_m[30] = 0
            # F_L_m[31] = 0
            # F_L_m[32] = 0
            F_L_m[3, 3] = (2 / 15) * l
            F_L_m[3, 4] = (1 / 15) * l
            F_L_m[3, 5] = -1 / 30 * l
            # F_L_m[36] = 0
            # F_L_m[37] = 0
            # F_L_m[38] = 0
            # F_L_m[39] = 0
            # F_L_m[310] = 0
            # F_L_m[311] = 0
            # F_L_m[312] = 0
            # F_L_m[313] = 0
            # F_L_m[314] = 0
            # F_L_m[315] = 0
            # F_L_m[316] = 0
            # F_L_m[317] = 0
            # F_L_m[318] = 0
            # F_L_m[319] = 0
            # F_L_m[40] = 0
            # F_L_m[41] = 0
            # F_L_m[42] = 0
            F_L_m[4, 3] = (1 / 15) * l
            F_L_m[4, 4] = (8 / 15) * l
            F_L_m[4, 5] = (1 / 15) * l
            # F_L_m[46] = 0
            # F_L_m[47] = 0
            # F_L_m[48] = 0
            # F_L_m[49] = 0
            # F_L_m[410] = 0
            # F_L_m[411] = 0
            # F_L_m[412] = 0
            # F_L_m[413] = 0
            # F_L_m[414] = 0
            # F_L_m[415] = 0
            # F_L_m[416] = 0
            # F_L_m[417] = 0
            # F_L_m[418] = 0
            # F_L_m[419] = 0
            # F_L_m[50] = 0
            # F_L_m[51] = 0
            # F_L_m[52] = 0
            F_L_m[5, 3] = -1 / 30 * l
            F_L_m[5, 4] = (1 / 15) * l
            F_L_m[5, 5] = (2 / 15) * l
            # F_L_m[56] = 0
            # F_L_m[57] = 0
            # F_L_m[58] = 0
            # F_L_m[59] = 0
            # F_L_m[510] = 0
            # F_L_m[511] = 0
            # F_L_m[512] = 0
            # F_L_m[513] = 0
            # F_L_m[514] = 0
            # F_L_m[515] = 0
            # F_L_m[516] = 0
            # F_L_m[517] = 0
            # F_L_m[518] = 0
            # F_L_m[519] = 0
            # F_L_m[60] = 0
            # F_L_m[61] = 0
            # F_L_m[62] = 0
            # F_L_m[63] = 0
            # F_L_m[64] = 0
            # F_L_m[65] = 0
            F_L_m[6, 6] = (8 / 105) * l
            F_L_m[6, 7] = (33 / 560) * l
            F_L_m[6, 8] = -3 / 140 * l
            F_L_m[6, 9] = (19 / 1680) * l
            # F_L_m[610] = 0
            # F_L_m[611] = 0
            # F_L_m[612] = 0
            # F_L_m[613] = 0
            # F_L_m[614] = 0
            # F_L_m[615] = 0
            # F_L_m[616] = 0
            # F_L_m[617] = 0
            # F_L_m[618] = 0
            # F_L_m[619] = 0
            # F_L_m[70] = 0
            # F_L_m[71] = 0
            # F_L_m[72] = 0
            # F_L_m[73] = 0
            # F_L_m[74] = 0
            # F_L_m[75] = 0
            F_L_m[7, 6] = (33 / 560) * l
            F_L_m[7, 7] = (27 / 70) * l
            F_L_m[7, 8] = -27 / 560 * l
            F_L_m[7, 9] = -3 / 140 * l
            # F_L_m[710] = 0
            # F_L_m[711] = 0
            # F_L_m[712] = 0
            # F_L_m[713] = 0
            # F_L_m[714] = 0
            # F_L_m[715] = 0
            # F_L_m[716] = 0
            # F_L_m[717] = 0
            # F_L_m[718] = 0
            # F_L_m[719] = 0
            # F_L_m[80] = 0
            # F_L_m[81] = 0
            # F_L_m[82] = 0
            # F_L_m[83] = 0
            # F_L_m[84] = 0
            # F_L_m[85] = 0
            F_L_m[8, 6] = -3 / 140 * l
            F_L_m[8, 7] = -27 / 560 * l
            F_L_m[8, 8] = (27 / 70) * l
            F_L_m[8, 9] = (33 / 560) * l
            # F_L_m[810] = 0
            # F_L_m[811] = 0
            # F_L_m[812] = 0
            # F_L_m[813] = 0
            # F_L_m[814] = 0
            # F_L_m[815] = 0
            # F_L_m[816] = 0
            # F_L_m[817] = 0
            # F_L_m[818] = 0
            # F_L_m[819] = 0
            # F_L_m[90] = 0
            # F_L_m[91] = 0
            # F_L_m[92] = 0
            # F_L_m[93] = 0
            # F_L_m[94] = 0
            # F_L_m[95] = 0
            F_L_m[9, 6] = (19 / 1680) * l
            F_L_m[9, 7] = -3 / 140 * l
            F_L_m[9, 8] = (33 / 560) * l
            F_L_m[9, 9] = (8 / 105) * l
            # F_L_m[910] = 0
            # F_L_m[911] = 0
            # F_L_m[912] = 0
            # F_L_m[913] = 0
            # F_L_m[914] = 0
            # F_L_m[915] = 0
            # F_L_m[916] = 0
            # F_L_m[917] = 0
            # F_L_m[918] = 0
            # F_L_m[919] = 0
            # F_L_m[100] = 0
            # F_L_m[101] = 0
            # F_L_m[102] = 0
            # F_L_m[103] = 0
            # F_L_m[104] = 0
            # F_L_m[105] = 0
            # F_L_m[106] = 0
            # F_L_m[107] = 0
            # F_L_m[108] = 0
            # F_L_m[109] = 0
            F_L_m[10, 10] = (2 / 15) * l
            F_L_m[10, 11] = (1 / 15) * l
            F_L_m[10, 12] = -1 / 30 * l
            # F_L_m[1013] = 0
            # F_L_m[1014] = 0
            # F_L_m[1015] = 0
            # F_L_m[1016] = 0
            # F_L_m[1017] = 0
            # F_L_m[1018] = 0
            # F_L_m[1019] = 0
            # F_L_m[110] = 0
            # F_L_m[111] = 0
            # F_L_m[112] = 0
            # F_L_m[113] = 0
            # F_L_m[114] = 0
            # F_L_m[115] = 0
            # F_L_m[116] = 0
            # F_L_m[117] = 0
            # F_L_m[118] = 0
            # F_L_m[119] = 0
            F_L_m[11, 10] = (1 / 15) * l
            F_L_m[11, 11] = (8 / 15) * l
            F_L_m[11, 12] = (1 / 15) * l
            # F_L_m[1113] = 0
            # F_L_m[1114] = 0
            # F_L_m[1115] = 0
            # F_L_m[1116] = 0
            # F_L_m[1117] = 0
            # F_L_m[1118] = 0
            # F_L_m[1119] = 0
            # F_L_m[120] = 0
            # F_L_m[121] = 0
            # F_L_m[122] = 0
            # F_L_m[123] = 0
            # F_L_m[124] = 0
            # F_L_m[125] = 0
            # F_L_m[126] = 0
            # F_L_m[127] = 0
            # F_L_m[128] = 0
            # F_L_m[129] = 0
            F_L_m[12, 10] = -1 / 30 * l
            F_L_m[12, 11] = (1 / 15) * l
            F_L_m[12, 12] = (2 / 15) * l
            # F_L_m[1213] = 0
            # F_L_m[1214] = 0
            # F_L_m[1215] = 0
            # F_L_m[1216] = 0
            # F_L_m[1217] = 0
            # F_L_m[1218] = 0
            # F_L_m[1219] = 0
            # F_L_m[130] = 0
            # F_L_m[131] = 0
            # F_L_m[132] = 0
            # F_L_m[133] = 0
            # F_L_m[134] = 0
            # F_L_m[135] = 0
            # F_L_m[136] = 0
            # F_L_m[137] = 0
            # F_L_m[138] = 0
            # F_L_m[139] = 0
            # F_L_m[1310] = 0
            # F_L_m[1311] = 0
            # F_L_m[1312] = 0
            F_L_m[13, 13] = (2 / 15) * l
            F_L_m[13, 14] = (1 / 15) * l
            F_L_m[13, 15] = -1 / 30 * l
            # F_L_m[1316] = 0
            # F_L_m[1317] = 0
            # F_L_m[1318] = 0
            # F_L_m[1319] = 0
            # F_L_m[140] = 0
            # F_L_m[141] = 0
            # F_L_m[142] = 0
            # F_L_m[143] = 0
            # F_L_m[144] = 0
            # F_L_m[145] = 0
            # F_L_m[146] = 0
            # F_L_m[147] = 0
            # F_L_m[148] = 0
            # F_L_m[149] = 0
            # F_L_m[1410] = 0
            # F_L_m[1411] = 0
            # F_L_m[1412] = 0
            F_L_m[14, 13] = (1 / 15) * l
            F_L_m[14, 14] = (8 / 15) * l
            F_L_m[14, 15] = (1 / 15) * l
            # F_L_m[1416] = 0
            # F_L_m[1417] = 0
            # F_L_m[1418] = 0
            # F_L_m[1419] = 0
            # F_L_m[150] = 0
            # F_L_m[151] = 0
            # F_L_m[152] = 0
            # F_L_m[153] = 0
            # F_L_m[154] = 0
            # F_L_m[155] = 0
            # F_L_m[156] = 0
            # F_L_m[157] = 0
            # F_L_m[158] = 0
            # F_L_m[159] = 0
            # F_L_m[1510] = 0
            # F_L_m[1511] = 0
            # F_L_m[1512] = 0
            F_L_m[15, 13] = -1 / 30 * l
            F_L_m[15, 14] = (1 / 15) * l
            F_L_m[15, 15] = (2 / 15) * l
            # F_L_m[1516] = 0
            # F_L_m[1517] = 0
            # F_L_m[1518] = 0
            # F_L_m[1519] = 0
            # F_L_m[160] = 0
            # F_L_m[161] = 0
            # F_L_m[162] = 0
            # F_L_m[163] = 0
            # F_L_m[164] = 0
            # F_L_m[165] = 0
            # F_L_m[166] = 0
            # F_L_m[167] = 0
            # F_L_m[168] = 0
            # F_L_m[169] = 0
            # F_L_m[1610] = 0
            # F_L_m[1611] = 0
            # F_L_m[1612] = 0
            # F_L_m[1613] = 0
            # F_L_m[1614] = 0
            # F_L_m[1615] = 0
            F_L_m[16, 16] = (13 / 35) * l
            F_L_m[16, 17] = (9 / 70) * l
            F_L_m[16, 18] = (11 / 210) * l ** 2
            F_L_m[16, 19] = -13 / 420 * l ** 2
            # F_L_m[170] = 0
            # F_L_m[171] = 0
            # F_L_m[172] = 0
            # F_L_m[173] = 0
            # F_L_m[174] = 0
            # F_L_m[175] = 0
            # F_L_m[176] = 0
            # F_L_m[177] = 0
            # F_L_m[178] = 0
            # F_L_m[179] = 0
            # F_L_m[1710] = 0
            # F_L_m[1711] = 0
            # F_L_m[1712] = 0
            # F_L_m[1713] = 0
            # F_L_m[1714] = 0
            # F_L_m[1715] = 0
            F_L_m[17, 16] = (9 / 70) * l
            F_L_m[17, 17] = (13 / 35) * l
            F_L_m[17, 18] = (13 / 420) * l ** 2
            F_L_m[17, 19] = -11 / 210 * l ** 2
            # F_L_m[180] = 0
            # F_L_m[181] = 0
            # F_L_m[182] = 0
            # F_L_m[183] = 0
            # F_L_m[184] = 0
            # F_L_m[185] = 0
            # F_L_m[186] = 0
            # F_L_m[187] = 0
            # F_L_m[188] = 0
            # F_L_m[189] = 0
            # F_L_m[1810] = 0
            # F_L_m[1811] = 0
            # F_L_m[1812] = 0
            # F_L_m[1813] = 0
            # F_L_m[1814] = 0
            # F_L_m[1815] = 0
            F_L_m[18, 16] = (11 / 210) * l ** 2
            F_L_m[18, 17] = (13 / 420) * l ** 2
            F_L_m[18, 18] = (1 / 105) * l ** 3
            F_L_m[18, 19] = -1 / 140 * l ** 3
            # F_L_m[190] = 0
            # F_L_m[191] = 0
            # F_L_m[192] = 0
            # F_L_m[193] = 0
            # F_L_m[194] = 0
            # F_L_m[195] = 0
            # F_L_m[196] = 0
            # F_L_m[197] = 0
            # F_L_m[198] = 0
            # F_L_m[199] = 0
            # F_L_m[1910] = 0
            # F_L_m[1911] = 0
            # F_L_m[1912] = 0
            # F_L_m[1913] = 0
            # F_L_m[1914] = 0
            # F_L_m[1915] = 0
            F_L_m[19, 16] = -13 / 420 * l ** 2
            F_L_m[19, 17] = -11 / 210 * l ** 2
            F_L_m[19, 18] = -1 / 140 * l ** 3
            F_L_m[19, 19] = (1 / 105) * l ** 3

            self._line_load_conversion_matrix = F_L_m.tocsc()

        return self._line_load_conversion_matrix

    def H_matrix(self, z):
        """
        Returns the H matrix of the element at a given z coordinate. The H matrix is used to calculate
        the beam displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The H matrix.
        """
        dtype = self._dtype
        l = self.length
        H = sp.dok_array((6, 20), dtype=dtype)

        H[0, 0] = (l - 2 * z) * (l - z) / l ** 2
        H[0, 1] = 4 * z * (l - z) / l ** 2
        H[0, 2] = z * (-l + 2 * z) / l ** 2
        # H[03] = 0
        # H[04] = 0
        # H[05] = 0
        # H[06] = 0
        # H[07] = 0
        # H[08] = 0
        # H[09] = 0
        # H[010] = 0
        # H[011] = 0
        # H[012] = 0
        # H[013] = 0
        # H[014] = 0
        # H[015] = 0
        # H[016] = 0
        # H[017] = 0
        # H[018] = 0
        # H[019] = 0
        # H[10] = 0
        # H[11] = 0
        # H[12] = 0
        H[1, 3] = (l - 2 * z) * (l - z) / l ** 2
        H[1, 4] = 4 * z * (l - z) / l ** 2
        H[1, 5] = z * (-l + 2 * z) / l ** 2
        # H[16] = 0
        # H[17] = 0
        # H[18] = 0
        # H[19] = 0
        # H[110] = 0
        # H[111] = 0
        # H[112] = 0
        # H[113] = 0
        # H[114] = 0
        # H[115] = 0
        # H[116] = 0
        # H[117] = 0
        # H[118] = 0
        # H[119] = 0
        # H[20] = 0
        # H[21] = 0
        # H[22] = 0
        # H[23] = 0
        # H[24] = 0
        # H[25] = 0
        H[2, 6] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[2, 7] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[2, 8] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[2, 9] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        # H[210] = 0
        # H[211] = 0
        # H[212] = 0
        # H[213] = 0
        # H[214] = 0
        # H[215] = 0
        # H[216] = 0
        # H[217] = 0
        # H[218] = 0
        # H[219] = 0
        # H[30] = 0
        # H[31] = 0
        # H[32] = 0
        # H[33] = 0
        # H[34] = 0
        # H[35] = 0
        # H[36] = 0
        # H[37] = 0
        # H[38] = 0
        # H[39] = 0
        H[3, 10] = (l - 2 * z) * (l - z) / l ** 2
        H[3, 11] = 4 * z * (l - z) / l ** 2
        H[3, 12] = z * (-l + 2 * z) / l ** 2
        # H[313] = 0
        # H[314] = 0
        # H[315] = 0
        # H[316] = 0
        # H[317] = 0
        # H[318] = 0
        # H[319] = 0
        # H[40] = 0
        # H[41] = 0
        # H[42] = 0
        # H[43] = 0
        # H[44] = 0
        # H[45] = 0
        # H[46] = 0
        # H[47] = 0
        # H[48] = 0
        # H[49] = 0
        # H[410] = 0
        # H[411] = 0
        # H[412] = 0
        H[4, 13] = (l - 2 * z) * (l - z) / l ** 2
        H[4, 14] = 4 * z * (l - z) / l ** 2
        H[4, 15] = z * (-l + 2 * z) / l ** 2
        # H[416] = 0
        # H[417] = 0
        # H[418] = 0
        # H[419] = 0
        # H[50] = 0
        # H[51] = 0
        # H[52] = 0
        # H[53] = 0
        # H[54] = 0
        # H[55] = 0
        # H[56] = 0
        # H[57] = 0
        # H[58] = 0
        # H[59] = 0
        # H[510] = 0
        # H[511] = 0
        # H[512] = 0
        # H[513] = 0
        # H[514] = 0
        # H[515] = 0
        H[5, 16] = (l ** 3 - 3 * l * z ** 2 + 2 * z ** 3) / l ** 3
        H[5, 17] = z ** 2 * (3 * l - 2 * z) / l ** 3
        H[5, 18] = z - 2 * z ** 2 / l + z ** 3 / l ** 2
        H[5, 19] = z ** 2 * (-l + z) / l ** 2

        return H

    def B_matrix(self, z):
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        dtype = self._dtype
        l = self.length
        B = sp.dok_array((7, 20), dtype=dtype)

        B[0, 0] = (-3 * l + 4 * z) / l ** 2
        B[0, 1] = 4 * (l - 2 * z) / l ** 2
        B[0, 2] = (-l + 4 * z) / l ** 2
        # B[03] = 0
        # B[04] = 0
        # B[05] = 0
        # B[06] = 0
        # B[07] = 0
        # B[08] = 0
        # B[09] = 0
        # B[010] = 0
        # B[011] = 0
        # B[012] = 0
        B[0, 13] = -1 + 3 * z / l - 2 * z ** 2 / l ** 2
        B[0, 14] = 4 * z * (-l + z) / l ** 2
        B[0, 15] = z * (l - 2 * z) / l ** 2
        # B[016] = 0
        # B[017] = 0
        # B[018] = 0
        # B[019] = 0
        # B[10] = 0
        # B[11] = 0
        # B[12] = 0
        B[1, 3] = (-3 * l + 4 * z) / l ** 2
        B[1, 4] = 4 * (l - 2 * z) / l ** 2
        B[1, 5] = (-l + 4 * z) / l ** 2
        # B[16] = 0
        # B[17] = 0
        # B[18] = 0
        # B[19] = 0
        B[1, 10] = 1 - 3 * z / l + 2 * z ** 2 / l ** 2
        B[1, 11] = 4 * z * (l - z) / l ** 2
        B[1, 12] = z * (-l + 2 * z) / l ** 2
        # B[113] = 0
        # B[114] = 0
        # B[115] = 0
        # B[116] = 0
        # B[117] = 0
        # B[118] = 0
        # B[119] = 0
        # B[20] = 0
        # B[21] = 0
        # B[22] = 0
        # B[23] = 0
        # B[24] = 0
        # B[25] = 0
        B[2, 6] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[2, 7] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[2, 8] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[2, 9] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        # B[210] = 0
        # B[211] = 0
        # B[212] = 0
        # B[213] = 0
        # B[214] = 0
        # B[215] = 0
        # B[216] = 0
        # B[217] = 0
        # B[218] = 0
        # B[219] = 0
        # B[30] = 0
        # B[31] = 0
        # B[32] = 0
        # B[33] = 0
        # B[34] = 0
        # B[35] = 0
        # B[36] = 0
        # B[37] = 0
        # B[38] = 0
        # B[39] = 0
        B[3, 10] = (-3 * l + 4 * z) / l ** 2
        B[3, 11] = 4 * (l - 2 * z) / l ** 2
        B[3, 12] = (-l + 4 * z) / l ** 2
        # B[313] = 0
        # B[314] = 0
        # B[315] = 0
        # B[316] = 0
        # B[317] = 0
        # B[318] = 0
        # B[319] = 0
        # B[40] = 0
        # B[41] = 0
        # B[42] = 0
        # B[43] = 0
        # B[44] = 0
        # B[45] = 0
        # B[46] = 0
        # B[47] = 0
        # B[48] = 0
        # B[49] = 0
        # B[410] = 0
        # B[411] = 0
        # B[412] = 0
        B[4, 13] = (-3 * l + 4 * z) / l ** 2
        B[4, 14] = 4 * (l - 2 * z) / l ** 2
        B[4, 15] = (-l + 4 * z) / l ** 2
        # B[416] = 0
        # B[417] = 0
        # B[418] = 0
        # B[419] = 0
        # B[50] = 0
        # B[51] = 0
        # B[52] = 0
        # B[53] = 0
        # B[54] = 0
        # B[55] = 0
        # B[56] = 0
        # B[57] = 0
        # B[58] = 0
        # B[59] = 0
        # B[510] = 0
        # B[511] = 0
        # B[512] = 0
        # B[513] = 0
        # B[514] = 0
        # B[515] = 0
        B[5, 16] = 6 * z * (-l + z) / l ** 3
        B[5, 17] = 6 * z * (l - z) / l ** 3
        B[5, 18] = 1 - 4 * z / l + 3 * z ** 2 / l ** 2
        B[5, 19] = z * (-2 * l + 3 * z) / l ** 2
        # B[60] = 0
        # B[61] = 0
        # B[62] = 0
        # B[63] = 0
        # B[64] = 0
        # B[65] = 0
        # B[66] = 0
        # B[67] = 0
        # B[68] = 0
        # B[69] = 0
        # B[610] = 0
        # B[611] = 0
        # B[612] = 0
        # B[613] = 0
        # B[614] = 0
        # B[615] = 0
        B[6, 16] = 6 * (-l + 2 * z) / l ** 3
        B[6, 17] = 6 * (l - 2 * z) / l ** 3
        B[6, 18] = 2 * (-2 * l + 3 * z) / l ** 2
        B[6, 19] = 2 * (-l + 3 * z) / l ** 2

        return B


class BeamElement3Node(AbstractBeamElement):
    """
    A element of the 1D finite elements beam model. The elements have three nodes and 18 DOF.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def num_nodes() -> int:
        return 3

    @staticmethod
    def element_dof() -> int:
        """Number of DOF per element."""
        return 18

    @staticmethod
    def dof_increment_per_element() -> int:
        """The increment of global DOF per new element."""
        return 12

    @staticmethod
    def deformation_transformation() -> bool:
        """True, if the global beam deformations have to transformed from the global to the element coordinate system."""
        return True

    @staticmethod
    def node_positions_norm() -> list[list[float]]:
        return [[0, 0.5, 1] for i in range(6)]

    @classmethod
    def A_matrix(cls) -> sp.csc_array:
        if not hasattr(cls, '_A_matrix'):
            cls._A_matrix = sp.dok_array(
                [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                 ]
            ).tocsc()
        return cls._A_matrix

    @property
    def element_mass_matrix(self):
        """numpy.ndarray: The FE element mass matrix."""
        if not hasattr(self, '_element_mass_matrix'):
            dtype = self._dtype
            l = self.length
            M_cs = self._cross_section_inertia_matrix
            M_m = sp.dok_array((18, 18), dtype=dtype)

            M_m[0, 0] = (2 / 15) * M_cs[0, 0] * l
            M_m[0, 1] = (1 / 15) * M_cs[0, 0] * l
            M_m[0, 2] = -1 / 30 * M_cs[0, 0] * l
            # M_m[0,3] = 0
            # M_m[0,4] = 0
            # M_m[0,5] = 0
            # M_m[0,6] = 0
            # M_m[0,7] = 0
            # M_m[0,8] = 0
            # M_m[0,9] = 0
            # M_m[0,10] = 0
            # M_m[0,11] = 0
            # M_m[0,12] = 0
            # M_m[0,13] = 0
            # M_m[0,14] = 0
            M_m[0, 15] = (2 / 15) * M_cs[0, 5] * l
            M_m[0, 16] = (1 / 15) * M_cs[0, 5] * l
            M_m[0, 17] = -1 / 30 * M_cs[0, 5] * l
            M_m[1, 0] = (1 / 15) * M_cs[0, 0] * l
            M_m[1, 1] = (8 / 15) * M_cs[0, 0] * l
            M_m[1, 2] = (1 / 15) * M_cs[0, 0] * l
            # M_m[1,3] = 0
            # M_m[1,4] = 0
            # M_m[1,5] = 0
            # M_m[1,6] = 0
            # M_m[1,7] = 0
            # M_m[1,8] = 0
            # M_m[1,9] = 0
            # M_m[1,10] = 0
            # M_m[1,11] = 0
            # M_m[1,12] = 0
            # M_m[1,13] = 0
            # M_m[1,14] = 0
            M_m[1, 15] = (1 / 15) * M_cs[0, 5] * l
            M_m[1, 16] = (8 / 15) * M_cs[0, 5] * l
            M_m[1, 17] = (1 / 15) * M_cs[0, 5] * l
            M_m[2, 0] = -1 / 30 * M_cs[0, 0] * l
            M_m[2, 1] = (1 / 15) * M_cs[0, 0] * l
            M_m[2, 2] = (2 / 15) * M_cs[0, 0] * l
            # M_m[2,3] = 0
            # M_m[2,4] = 0
            # M_m[2,5] = 0
            # M_m[2,6] = 0
            # M_m[2,7] = 0
            # M_m[2,8] = 0
            # M_m[2,9] = 0
            # M_m[2,10] = 0
            # M_m[2,11] = 0
            # M_m[2,12] = 0
            # M_m[2,13] = 0
            # M_m[2,14] = 0
            M_m[2, 15] = -1 / 30 * M_cs[0, 5] * l
            M_m[2, 16] = (1 / 15) * M_cs[0, 5] * l
            M_m[2, 17] = (2 / 15) * M_cs[0, 5] * l
            # M_m[3,0] = 0
            # M_m[3,1] = 0
            # M_m[3,2] = 0
            M_m[3, 3] = (2 / 15) * M_cs[1, 1] * l
            M_m[3, 4] = (1 / 15) * M_cs[1, 1] * l
            M_m[3, 5] = -1 / 30 * M_cs[1, 1] * l
            # M_m[3,6] = 0
            # M_m[3,7] = 0
            # M_m[3,8] = 0
            # M_m[3,9] = 0
            # M_m[3,10] = 0
            # M_m[3,11] = 0
            # M_m[3,12] = 0
            # M_m[3,13] = 0
            # M_m[3,14] = 0
            M_m[3, 15] = (2 / 15) * M_cs[1, 5] * l
            M_m[3, 16] = (1 / 15) * M_cs[1, 5] * l
            M_m[3, 17] = -1 / 30 * M_cs[1, 5] * l
            # M_m[4,0] = 0
            # M_m[4,1] = 0
            # M_m[4,2] = 0
            M_m[4, 3] = (1 / 15) * M_cs[1, 1] * l
            M_m[4, 4] = (8 / 15) * M_cs[1, 1] * l
            M_m[4, 5] = (1 / 15) * M_cs[1, 1] * l
            # M_m[4,6] = 0
            # M_m[4,7] = 0
            # M_m[4,8] = 0
            # M_m[4,9] = 0
            # M_m[4,10] = 0
            # M_m[4,11] = 0
            # M_m[4,12] = 0
            # M_m[4,13] = 0
            # M_m[4,14] = 0
            M_m[4, 15] = (1 / 15) * M_cs[1, 5] * l
            M_m[4, 16] = (8 / 15) * M_cs[1, 5] * l
            M_m[4, 17] = (1 / 15) * M_cs[1, 5] * l
            # M_m[5,0] = 0
            # M_m[5,1] = 0
            # M_m[5,2] = 0
            M_m[5, 3] = -1 / 30 * M_cs[1, 1] * l
            M_m[5, 4] = (1 / 15) * M_cs[1, 1] * l
            M_m[5, 5] = (2 / 15) * M_cs[1, 1] * l
            # M_m[5,6] = 0
            # M_m[5,7] = 0
            # M_m[5,8] = 0
            # M_m[5,9] = 0
            # M_m[5,10] = 0
            # M_m[5,11] = 0
            # M_m[5,12] = 0
            # M_m[5,13] = 0
            # M_m[5,14] = 0
            M_m[5, 15] = -1 / 30 * M_cs[1, 5] * l
            M_m[5, 16] = (1 / 15) * M_cs[1, 5] * l
            M_m[5, 17] = (2 / 15) * M_cs[1, 5] * l
            # M_m[6,0] = 0
            # M_m[6,1] = 0
            # M_m[6,2] = 0
            # M_m[6,3] = 0
            # M_m[6,4] = 0
            # M_m[6,5] = 0
            M_m[6, 6] = (2 / 15) * M_cs[2, 2] * l
            M_m[6, 7] = (1 / 15) * M_cs[2, 2] * l
            M_m[6, 8] = -1 / 30 * M_cs[2, 2] * l
            M_m[6, 9] = (2 / 15) * M_cs[2, 3] * l
            M_m[6, 10] = (1 / 15) * M_cs[2, 3] * l
            M_m[6, 11] = -1 / 30 * M_cs[2, 3] * l
            M_m[6, 12] = (2 / 15) * M_cs[2, 4] * l
            M_m[6, 13] = (1 / 15) * M_cs[2, 4] * l
            M_m[6, 14] = -1 / 30 * M_cs[2, 4] * l
            # M_m[6,15] = 0
            # M_m[6,16] = 0
            # M_m[6,17] = 0
            # M_m[7,0] = 0
            # M_m[7,1] = 0
            # M_m[7,2] = 0
            # M_m[7,3] = 0
            # M_m[7,4] = 0
            # M_m[7,5] = 0
            M_m[7, 6] = (1 / 15) * M_cs[2, 2] * l
            M_m[7, 7] = (8 / 15) * M_cs[2, 2] * l
            M_m[7, 8] = (1 / 15) * M_cs[2, 2] * l
            M_m[7, 9] = (1 / 15) * M_cs[2, 3] * l
            M_m[7, 10] = (8 / 15) * M_cs[2, 3] * l
            M_m[7, 11] = (1 / 15) * M_cs[2, 3] * l
            M_m[7, 12] = (1 / 15) * M_cs[2, 4] * l
            M_m[7, 13] = (8 / 15) * M_cs[2, 4] * l
            M_m[7, 14] = (1 / 15) * M_cs[2, 4] * l
            # M_m[7,15] = 0
            # M_m[7,16] = 0
            # M_m[7,17] = 0
            # M_m[8,0] = 0
            # M_m[8,1] = 0
            # M_m[8,2] = 0
            # M_m[8,3] = 0
            # M_m[8,4] = 0
            # M_m[8,5] = 0
            M_m[8, 6] = -1 / 30 * M_cs[2, 2] * l
            M_m[8, 7] = (1 / 15) * M_cs[2, 2] * l
            M_m[8, 8] = (2 / 15) * M_cs[2, 2] * l
            M_m[8, 9] = -1 / 30 * M_cs[2, 3] * l
            M_m[8, 10] = (1 / 15) * M_cs[2, 3] * l
            M_m[8, 11] = (2 / 15) * M_cs[2, 3] * l
            M_m[8, 12] = -1 / 30 * M_cs[2, 4] * l
            M_m[8, 13] = (1 / 15) * M_cs[2, 4] * l
            M_m[8, 14] = (2 / 15) * M_cs[2, 4] * l
            # M_m[8,15] = 0
            # M_m[8,16] = 0
            # M_m[8,17] = 0
            # M_m[9,0] = 0
            # M_m[9,1] = 0
            # M_m[9,2] = 0
            # M_m[9,3] = 0
            # M_m[9,4] = 0
            # M_m[9,5] = 0
            M_m[9, 6] = (2 / 15) * M_cs[2, 3] * l
            M_m[9, 7] = (1 / 15) * M_cs[2, 3] * l
            M_m[9, 8] = -1 / 30 * M_cs[2, 3] * l
            M_m[9, 9] = (2 / 15) * M_cs[3, 3] * l
            M_m[9, 10] = (1 / 15) * M_cs[3, 3] * l
            M_m[9, 11] = -1 / 30 * M_cs[3, 3] * l
            M_m[9, 12] = (2 / 15) * M_cs[3, 4] * l
            M_m[9, 13] = (1 / 15) * M_cs[3, 4] * l
            M_m[9, 14] = -1 / 30 * M_cs[3, 4] * l
            # M_m[9,15] = 0
            # M_m[9,16] = 0
            # M_m[9,17] = 0
            # M_m[10,0] = 0
            # M_m[10,1] = 0
            # M_m[10,2] = 0
            # M_m[10,3] = 0
            # M_m[10,4] = 0
            # M_m[10,5] = 0
            M_m[10, 6] = (1 / 15) * M_cs[2, 3] * l
            M_m[10, 7] = (8 / 15) * M_cs[2, 3] * l
            M_m[10, 8] = (1 / 15) * M_cs[2, 3] * l
            M_m[10, 9] = (1 / 15) * M_cs[3, 3] * l
            M_m[10, 10] = (8 / 15) * M_cs[3, 3] * l
            M_m[10, 11] = (1 / 15) * M_cs[3, 3] * l
            M_m[10, 12] = (1 / 15) * M_cs[3, 4] * l
            M_m[10, 13] = (8 / 15) * M_cs[3, 4] * l
            M_m[10, 14] = (1 / 15) * M_cs[3, 4] * l
            # M_m[10,15] = 0
            # M_m[10,16] = 0
            # M_m[10,17] = 0
            # M_m[11,0] = 0
            # M_m[11,1] = 0
            # M_m[11,2] = 0
            # M_m[11,3] = 0
            # M_m[11,4] = 0
            # M_m[11,5] = 0
            M_m[11, 6] = -1 / 30 * M_cs[2, 3] * l
            M_m[11, 7] = (1 / 15) * M_cs[2, 3] * l
            M_m[11, 8] = (2 / 15) * M_cs[2, 3] * l
            M_m[11, 9] = -1 / 30 * M_cs[3, 3] * l
            M_m[11, 10] = (1 / 15) * M_cs[3, 3] * l
            M_m[11, 11] = (2 / 15) * M_cs[3, 3] * l
            M_m[11, 12] = -1 / 30 * M_cs[3, 4] * l
            M_m[11, 13] = (1 / 15) * M_cs[3, 4] * l
            M_m[11, 14] = (2 / 15) * M_cs[3, 4] * l
            # M_m[11,15] = 0
            # M_m[11,16] = 0
            # M_m[11,17] = 0
            # M_m[12,0] = 0
            # M_m[12,1] = 0
            # M_m[12,2] = 0
            # M_m[12,3] = 0
            # M_m[12,4] = 0
            # M_m[12,5] = 0
            M_m[12, 6] = (2 / 15) * M_cs[2, 4] * l
            M_m[12, 7] = (1 / 15) * M_cs[2, 4] * l
            M_m[12, 8] = -1 / 30 * M_cs[2, 4] * l
            M_m[12, 9] = (2 / 15) * M_cs[3, 4] * l
            M_m[12, 10] = (1 / 15) * M_cs[3, 4] * l
            M_m[12, 11] = -1 / 30 * M_cs[3, 4] * l
            M_m[12, 12] = (2 / 15) * M_cs[4, 4] * l
            M_m[12, 13] = (1 / 15) * M_cs[4, 4] * l
            M_m[12, 14] = -1 / 30 * M_cs[4, 4] * l
            # M_m[12,15] = 0
            # M_m[12,16] = 0
            # M_m[12,17] = 0
            # M_m[13,0] = 0
            # M_m[13,1] = 0
            # M_m[13,2] = 0
            # M_m[13,3] = 0
            # M_m[13,4] = 0
            # M_m[13,5] = 0
            M_m[13, 6] = (1 / 15) * M_cs[2, 4] * l
            M_m[13, 7] = (8 / 15) * M_cs[2, 4] * l
            M_m[13, 8] = (1 / 15) * M_cs[2, 4] * l
            M_m[13, 9] = (1 / 15) * M_cs[3, 4] * l
            M_m[13, 10] = (8 / 15) * M_cs[3, 4] * l
            M_m[13, 11] = (1 / 15) * M_cs[3, 4] * l
            M_m[13, 12] = (1 / 15) * M_cs[4, 4] * l
            M_m[13, 13] = (8 / 15) * M_cs[4, 4] * l
            M_m[13, 14] = (1 / 15) * M_cs[4, 4] * l
            # M_m[13,15] = 0
            # M_m[13,16] = 0
            # M_m[13,17] = 0
            # M_m[14,0] = 0
            # M_m[14,1] = 0
            # M_m[14,2] = 0
            # M_m[14,3] = 0
            # M_m[14,4] = 0
            # M_m[14,5] = 0
            M_m[14, 6] = -1 / 30 * M_cs[2, 4] * l
            M_m[14, 7] = (1 / 15) * M_cs[2, 4] * l
            M_m[14, 8] = (2 / 15) * M_cs[2, 4] * l
            M_m[14, 9] = -1 / 30 * M_cs[3, 4] * l
            M_m[14, 10] = (1 / 15) * M_cs[3, 4] * l
            M_m[14, 11] = (2 / 15) * M_cs[3, 4] * l
            M_m[14, 12] = -1 / 30 * M_cs[4, 4] * l
            M_m[14, 13] = (1 / 15) * M_cs[4, 4] * l
            M_m[14, 14] = (2 / 15) * M_cs[4, 4] * l
            # M_m[14,15] = 0
            # M_m[14,16] = 0
            # M_m[14,17] = 0
            M_m[15, 0] = (2 / 15) * M_cs[0, 5] * l
            M_m[15, 1] = (1 / 15) * M_cs[0, 5] * l
            M_m[15, 2] = -1 / 30 * M_cs[0, 5] * l
            M_m[15, 3] = (2 / 15) * M_cs[1, 5] * l
            M_m[15, 4] = (1 / 15) * M_cs[1, 5] * l
            M_m[15, 5] = -1 / 30 * M_cs[1, 5] * l
            # M_m[15,6] = 0
            # M_m[15,7] = 0
            # M_m[15,8] = 0
            # M_m[15,9] = 0
            # M_m[15,10] = 0
            # M_m[15,11] = 0
            # M_m[15,12] = 0
            # M_m[15,13] = 0
            # M_m[15,14] = 0
            M_m[15, 15] = (2 / 15) * M_cs[5, 5] * l
            M_m[15, 16] = (1 / 15) * M_cs[5, 5] * l
            M_m[15, 17] = -1 / 30 * M_cs[5, 5] * l
            M_m[16, 0] = (1 / 15) * M_cs[0, 5] * l
            M_m[16, 1] = (8 / 15) * M_cs[0, 5] * l
            M_m[16, 2] = (1 / 15) * M_cs[0, 5] * l
            M_m[16, 3] = (1 / 15) * M_cs[1, 5] * l
            M_m[16, 4] = (8 / 15) * M_cs[1, 5] * l
            M_m[16, 5] = (1 / 15) * M_cs[1, 5] * l
            # M_m[16,6] = 0
            # M_m[16,7] = 0
            # M_m[16,8] = 0
            # M_m[16,9] = 0
            # M_m[16,10] = 0
            # M_m[16,11] = 0
            # M_m[16,12] = 0
            # M_m[16,13] = 0
            # M_m[16,14] = 0
            M_m[16, 15] = (1 / 15) * M_cs[5, 5] * l
            M_m[16, 16] = (8 / 15) * M_cs[5, 5] * l
            M_m[16, 17] = (1 / 15) * M_cs[5, 5] * l
            M_m[17, 0] = -1 / 30 * M_cs[0, 5] * l
            M_m[17, 1] = (1 / 15) * M_cs[0, 5] * l
            M_m[17, 2] = (2 / 15) * M_cs[0, 5] * l
            M_m[17, 3] = -1 / 30 * M_cs[1, 5] * l
            M_m[17, 4] = (1 / 15) * M_cs[1, 5] * l
            M_m[17, 5] = (2 / 15) * M_cs[1, 5] * l
            # M_m[17,6] = 0
            # M_m[17,7] = 0
            # M_m[17,8] = 0
            # M_m[17,9] = 0
            # M_m[17,10] = 0
            # M_m[17,11] = 0
            # M_m[17,12] = 0
            # M_m[17,13] = 0
            # M_m[17,14] = 0
            M_m[17, 15] = -1 / 30 * M_cs[5, 5] * l
            M_m[17, 16] = (1 / 15) * M_cs[5, 5] * l
            M_m[17, 17] = (2 / 15) * M_cs[5, 5] * l

            self._element_mass_matrix = M_m.tocsc()

        return self._element_mass_matrix

    @property
    def line_load_conversion_matrix(self):
        """numpy.ndarray: Matrix for the conversion of line loads at the nodes (end nodes and integration point nodes) to node loads."""
        if not hasattr(self, '_line_load_conversion_matrix'):
            dtype = self._dtype
            l = self.length
            F_L_m = sp.dok_array((18, 18), dtype=dtype)

            F_L_m[0, 0] = (2 / 15) * l
            F_L_m[0, 1] = (1 / 15) * l
            F_L_m[0, 2] = -1 / 30 * l
            # F_L_m[0,3] = 0
            # F_L_m[0,4] = 0
            # F_L_m[0,5] = 0
            # F_L_m[0,6] = 0
            # F_L_m[0,7] = 0
            # F_L_m[0,8] = 0
            # F_L_m[0,9] = 0
            # F_L_m[0,10] = 0
            # F_L_m[0,11] = 0
            # F_L_m[0,12] = 0
            # F_L_m[0,13] = 0
            # F_L_m[0,14] = 0
            # F_L_m[0,15] = 0
            # F_L_m[0,16] = 0
            # F_L_m[0,17] = 0
            F_L_m[1, 0] = (1 / 15) * l
            F_L_m[1, 1] = (8 / 15) * l
            F_L_m[1, 2] = (1 / 15) * l
            # F_L_m[1,3] = 0
            # F_L_m[1,4] = 0
            # F_L_m[1,5] = 0
            # F_L_m[1,6] = 0
            # F_L_m[1,7] = 0
            # F_L_m[1,8] = 0
            # F_L_m[1,9] = 0
            # F_L_m[1,10] = 0
            # F_L_m[1,11] = 0
            # F_L_m[1,12] = 0
            # F_L_m[1,13] = 0
            # F_L_m[1,14] = 0
            # F_L_m[1,15] = 0
            # F_L_m[1,16] = 0
            # F_L_m[1,17] = 0
            F_L_m[2, 0] = -1 / 30 * l
            F_L_m[2, 1] = (1 / 15) * l
            F_L_m[2, 2] = (2 / 15) * l
            # F_L_m[2,3] = 0
            # F_L_m[2,4] = 0
            # F_L_m[2,5] = 0
            # F_L_m[2,6] = 0
            # F_L_m[2,7] = 0
            # F_L_m[2,8] = 0
            # F_L_m[2,9] = 0
            # F_L_m[2,10] = 0
            # F_L_m[2,11] = 0
            # F_L_m[2,12] = 0
            # F_L_m[2,13] = 0
            # F_L_m[2,14] = 0
            # F_L_m[2,15] = 0
            # F_L_m[2,16] = 0
            # F_L_m[2,17] = 0
            # F_L_m[3,0] = 0
            # F_L_m[3,1] = 0
            # F_L_m[3,2] = 0
            F_L_m[3, 3] = (2 / 15) * l
            F_L_m[3, 4] = (1 / 15) * l
            F_L_m[3, 5] = -1 / 30 * l
            # F_L_m[3,6] = 0
            # F_L_m[3,7] = 0
            # F_L_m[3,8] = 0
            # F_L_m[3,9] = 0
            # F_L_m[3,10] = 0
            # F_L_m[3,11] = 0
            # F_L_m[3,12] = 0
            # F_L_m[3,13] = 0
            # F_L_m[3,14] = 0
            # F_L_m[3,15] = 0
            # F_L_m[3,16] = 0
            # F_L_m[3,17] = 0
            # F_L_m[4,0] = 0
            # F_L_m[4,1] = 0
            # F_L_m[4,2] = 0
            F_L_m[4, 3] = (1 / 15) * l
            F_L_m[4, 4] = (8 / 15) * l
            F_L_m[4, 5] = (1 / 15) * l
            # F_L_m[4,6] = 0
            # F_L_m[4,7] = 0
            # F_L_m[4,8] = 0
            # F_L_m[4,9] = 0
            # F_L_m[4,10] = 0
            # F_L_m[4,11] = 0
            # F_L_m[4,12] = 0
            # F_L_m[4,13] = 0
            # F_L_m[4,14] = 0
            # F_L_m[4,15] = 0
            # F_L_m[4,16] = 0
            # F_L_m[4,17] = 0
            # F_L_m[5,0] = 0
            # F_L_m[5,1] = 0
            # F_L_m[5,2] = 0
            F_L_m[5, 3] = -1 / 30 * l
            F_L_m[5, 4] = (1 / 15) * l
            F_L_m[5, 5] = (2 / 15) * l
            # F_L_m[5,6] = 0
            # F_L_m[5,7] = 0
            # F_L_m[5,8] = 0
            # F_L_m[5,9] = 0
            # F_L_m[5,10] = 0
            # F_L_m[5,11] = 0
            # F_L_m[5,12] = 0
            # F_L_m[5,13] = 0
            # F_L_m[5,14] = 0
            # F_L_m[5,15] = 0
            # F_L_m[5,16] = 0
            # F_L_m[5,17] = 0
            # F_L_m[6,0] = 0
            # F_L_m[6,1] = 0
            # F_L_m[6,2] = 0
            # F_L_m[6,3] = 0
            # F_L_m[6,4] = 0
            # F_L_m[6,5] = 0
            F_L_m[6, 6] = (2 / 15) * l
            F_L_m[6, 7] = (1 / 15) * l
            F_L_m[6, 8] = -1 / 30 * l
            # F_L_m[6,9] = 0
            # F_L_m[6,10] = 0
            # F_L_m[6,11] = 0
            # F_L_m[6,12] = 0
            # F_L_m[6,13] = 0
            # F_L_m[6,14] = 0
            # F_L_m[6,15] = 0
            # F_L_m[6,16] = 0
            # F_L_m[6,17] = 0
            # F_L_m[7,0] = 0
            # F_L_m[7,1] = 0
            # F_L_m[7,2] = 0
            # F_L_m[7,3] = 0
            # F_L_m[7,4] = 0
            # F_L_m[7,5] = 0
            F_L_m[7, 6] = (1 / 15) * l
            F_L_m[7, 7] = (8 / 15) * l
            F_L_m[7, 8] = (1 / 15) * l
            # F_L_m[7,9] = 0
            # F_L_m[7,10] = 0
            # F_L_m[7,11] = 0
            # F_L_m[7,12] = 0
            # F_L_m[7,13] = 0
            # F_L_m[7,14] = 0
            # F_L_m[7,15] = 0
            # F_L_m[7,16] = 0
            # F_L_m[7,17] = 0
            # F_L_m[8,0] = 0
            # F_L_m[8,1] = 0
            # F_L_m[8,2] = 0
            # F_L_m[8,3] = 0
            # F_L_m[8,4] = 0
            # F_L_m[8,5] = 0
            F_L_m[8, 6] = -1 / 30 * l
            F_L_m[8, 7] = (1 / 15) * l
            F_L_m[8, 8] = (2 / 15) * l
            # F_L_m[8,9] = 0
            # F_L_m[8,10] = 0
            # F_L_m[8,11] = 0
            # F_L_m[8,12] = 0
            # F_L_m[8,13] = 0
            # F_L_m[8,14] = 0
            # F_L_m[8,15] = 0
            # F_L_m[8,16] = 0
            # F_L_m[8,17] = 0
            # F_L_m[9,0] = 0
            # F_L_m[9,1] = 0
            # F_L_m[9,2] = 0
            # F_L_m[9,3] = 0
            # F_L_m[9,4] = 0
            # F_L_m[9,5] = 0
            # F_L_m[9,6] = 0
            # F_L_m[9,7] = 0
            # F_L_m[9,8] = 0
            F_L_m[9, 9] = (2 / 15) * l
            F_L_m[9, 10] = (1 / 15) * l
            F_L_m[9, 11] = -1 / 30 * l
            # F_L_m[9,12] = 0
            # F_L_m[9,13] = 0
            # F_L_m[9,14] = 0
            # F_L_m[9,15] = 0
            # F_L_m[9,16] = 0
            # F_L_m[9,17] = 0
            # F_L_m[10,0] = 0
            # F_L_m[10,1] = 0
            # F_L_m[10,2] = 0
            # F_L_m[10,3] = 0
            # F_L_m[10,4] = 0
            # F_L_m[10,5] = 0
            # F_L_m[10,6] = 0
            # F_L_m[10,7] = 0
            # F_L_m[10,8] = 0
            F_L_m[10, 9] = (1 / 15) * l
            F_L_m[10, 10] = (8 / 15) * l
            F_L_m[10, 11] = (1 / 15) * l
            # F_L_m[10,12] = 0
            # F_L_m[10,13] = 0
            # F_L_m[10,14] = 0
            # F_L_m[10,15] = 0
            # F_L_m[10,16] = 0
            # F_L_m[10,17] = 0
            # F_L_m[11,0] = 0
            # F_L_m[11,1] = 0
            # F_L_m[11,2] = 0
            # F_L_m[11,3] = 0
            # F_L_m[11,4] = 0
            # F_L_m[11,5] = 0
            # F_L_m[11,6] = 0
            # F_L_m[11,7] = 0
            # F_L_m[11,8] = 0
            F_L_m[11, 9] = -1 / 30 * l
            F_L_m[11, 10] = (1 / 15) * l
            F_L_m[11, 11] = (2 / 15) * l
            # F_L_m[11,12] = 0
            # F_L_m[11,13] = 0
            # F_L_m[11,14] = 0
            # F_L_m[11,15] = 0
            # F_L_m[11,16] = 0
            # F_L_m[11,17] = 0
            # F_L_m[12,0] = 0
            # F_L_m[12,1] = 0
            # F_L_m[12,2] = 0
            # F_L_m[12,3] = 0
            # F_L_m[12,4] = 0
            # F_L_m[12,5] = 0
            # F_L_m[12,6] = 0
            # F_L_m[12,7] = 0
            # F_L_m[12,8] = 0
            # F_L_m[12,9] = 0
            # F_L_m[12,10] = 0
            # F_L_m[12,11] = 0
            F_L_m[12, 12] = (2 / 15) * l
            F_L_m[12, 13] = (1 / 15) * l
            F_L_m[12, 14] = -1 / 30 * l
            # F_L_m[12,15] = 0
            # F_L_m[12,16] = 0
            # F_L_m[12,17] = 0
            # F_L_m[13,0] = 0
            # F_L_m[13,1] = 0
            # F_L_m[13,2] = 0
            # F_L_m[13,3] = 0
            # F_L_m[13,4] = 0
            # F_L_m[13,5] = 0
            # F_L_m[13,6] = 0
            # F_L_m[13,7] = 0
            # F_L_m[13,8] = 0
            # F_L_m[13,9] = 0
            # F_L_m[13,10] = 0
            # F_L_m[13,11] = 0
            F_L_m[13, 12] = (1 / 15) * l
            F_L_m[13, 13] = (8 / 15) * l
            F_L_m[13, 14] = (1 / 15) * l
            # F_L_m[13,15] = 0
            # F_L_m[13,16] = 0
            # F_L_m[13,17] = 0
            # F_L_m[14,0] = 0
            # F_L_m[14,1] = 0
            # F_L_m[14,2] = 0
            # F_L_m[14,3] = 0
            # F_L_m[14,4] = 0
            # F_L_m[14,5] = 0
            # F_L_m[14,6] = 0
            # F_L_m[14,7] = 0
            # F_L_m[14,8] = 0
            # F_L_m[14,9] = 0
            # F_L_m[14,10] = 0
            # F_L_m[14,11] = 0
            F_L_m[14, 12] = -1 / 30 * l
            F_L_m[14, 13] = (1 / 15) * l
            F_L_m[14, 14] = (2 / 15) * l
            # F_L_m[14,15] = 0
            # F_L_m[14,16] = 0
            # F_L_m[14,17] = 0
            # F_L_m[15,0] = 0
            # F_L_m[15,1] = 0
            # F_L_m[15,2] = 0
            # F_L_m[15,3] = 0
            # F_L_m[15,4] = 0
            # F_L_m[15,5] = 0
            # F_L_m[15,6] = 0
            # F_L_m[15,7] = 0
            # F_L_m[15,8] = 0
            # F_L_m[15,9] = 0
            # F_L_m[15,10] = 0
            # F_L_m[15,11] = 0
            # F_L_m[15,12] = 0
            # F_L_m[15,13] = 0
            # F_L_m[15,14] = 0
            F_L_m[15, 15] = (2 / 15) * l
            F_L_m[15, 16] = (1 / 15) * l
            F_L_m[15, 17] = -1 / 30 * l
            # F_L_m[16,0] = 0
            # F_L_m[16,1] = 0
            # F_L_m[16,2] = 0
            # F_L_m[16,3] = 0
            # F_L_m[16,4] = 0
            # F_L_m[16,5] = 0
            # F_L_m[16,6] = 0
            # F_L_m[16,7] = 0
            # F_L_m[16,8] = 0
            # F_L_m[16,9] = 0
            # F_L_m[16,10] = 0
            # F_L_m[16,11] = 0
            # F_L_m[16,12] = 0
            # F_L_m[16,13] = 0
            # F_L_m[16,14] = 0
            F_L_m[16, 15] = (1 / 15) * l
            F_L_m[16, 16] = (8 / 15) * l
            F_L_m[16, 17] = (1 / 15) * l
            # F_L_m[17,0] = 0
            # F_L_m[17,1] = 0
            # F_L_m[17,2] = 0
            # F_L_m[17,3] = 0
            # F_L_m[17,4] = 0
            # F_L_m[17,5] = 0
            # F_L_m[17,6] = 0
            # F_L_m[17,7] = 0
            # F_L_m[17,8] = 0
            # F_L_m[17,9] = 0
            # F_L_m[17,10] = 0
            # F_L_m[17,11] = 0
            # F_L_m[17,12] = 0
            # F_L_m[17,13] = 0
            # F_L_m[17,14] = 0
            F_L_m[17, 15] = -1 / 30 * l
            F_L_m[17, 16] = (1 / 15) * l
            F_L_m[17, 17] = (2 / 15) * l

            self._line_load_conversion_matrix = F_L_m.tocsc()

        return self._line_load_conversion_matrix

    def H_matrix(self, z):
        """
        Returns the H matrix of the element at a given z coordinate. The H matrix is used to calculate
        the beam displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The H matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        H = sp.dok_array((6, 18), dtype=dtype)

        H[0, 0] = (l - 2 * z) * (l - z) / l ** 2
        H[0, 1] = 4 * z * (l - z) / l ** 2
        H[0, 2] = z * (-l + 2 * z) / l ** 2
        # H[0,3] = 0
        # H[0,4] = 0
        # H[0,5] = 0
        # H[0,6] = 0
        # H[0,7] = 0
        # H[0,8] = 0
        # H[0,9] = 0
        # H[0,10] = 0
        # H[0,11] = 0
        # H[0,12] = 0
        # H[0,13] = 0
        # H[0,14] = 0
        # H[0,15] = 0
        # H[0,16] = 0
        # H[0,17] = 0
        # H[1,0] = 0
        # H[1,1] = 0
        # H[1,2] = 0
        H[1, 3] = (l - 2 * z) * (l - z) / l ** 2
        H[1, 4] = 4 * z * (l - z) / l ** 2
        H[1, 5] = z * (-l + 2 * z) / l ** 2
        # H[1,6] = 0
        # H[1,7] = 0
        # H[1,8] = 0
        # H[1,9] = 0
        # H[1,10] = 0
        # H[1,11] = 0
        # H[1,12] = 0
        # H[1,13] = 0
        # H[1,14] = 0
        # H[1,15] = 0
        # H[1,16] = 0
        # H[1,17] = 0
        # H[2,0] = 0
        # H[2,1] = 0
        # H[2,2] = 0
        # H[2,3] = 0
        # H[2,4] = 0
        # H[2,5] = 0
        H[2, 6] = (l - 2 * z) * (l - z) / l ** 2
        H[2, 7] = 4 * z * (l - z) / l ** 2
        H[2, 8] = z * (-l + 2 * z) / l ** 2
        # H[2,9] = 0
        # H[2,10] = 0
        # H[2,11] = 0
        # H[2,12] = 0
        # H[2,13] = 0
        # H[2,14] = 0
        # H[2,15] = 0
        # H[2,16] = 0
        # H[2,17] = 0
        # H[3,0] = 0
        # H[3,1] = 0
        # H[3,2] = 0
        # H[3,3] = 0
        # H[3,4] = 0
        # H[3,5] = 0
        # H[3,6] = 0
        # H[3,7] = 0
        # H[3,8] = 0
        H[3, 9] = (l - 2 * z) * (l - z) / l ** 2
        H[3, 10] = 4 * z * (l - z) / l ** 2
        H[3, 11] = z * (-l + 2 * z) / l ** 2
        # H[3,12] = 0
        # H[3,13] = 0
        # H[3,14] = 0
        # H[3,15] = 0
        # H[3,16] = 0
        # H[3,17] = 0
        # H[4,0] = 0
        # H[4,1] = 0
        # H[4,2] = 0
        # H[4,3] = 0
        # H[4,4] = 0
        # H[4,5] = 0
        # H[4,6] = 0
        # H[4,7] = 0
        # H[4,8] = 0
        # H[4,9] = 0
        # H[4,10] = 0
        # H[4,11] = 0
        H[4, 12] = (l - 2 * z) * (l - z) / l ** 2
        H[4, 13] = 4 * z * (l - z) / l ** 2
        H[4, 14] = z * (-l + 2 * z) / l ** 2
        # H[4,15] = 0
        # H[4,16] = 0
        # H[4,17] = 0
        # H[5,0] = 0
        # H[5,1] = 0
        # H[5,2] = 0
        # H[5,3] = 0
        # H[5,4] = 0
        # H[5,5] = 0
        # H[5,6] = 0
        # H[5,7] = 0
        # H[5,8] = 0
        # H[5,9] = 0
        # H[5,10] = 0
        # H[5,11] = 0
        # H[5,12] = 0
        # H[5,13] = 0
        # H[5,14] = 0
        H[5, 15] = (l - 2 * z) * (l - z) / l ** 2
        H[5, 16] = 4 * z * (l - z) / l ** 2
        H[5, 17] = z * (-l + 2 * z) / l ** 2

        return H


class BeamElement3NodeWithWarping(BeamElement3Node):
    """
    A element of the 1D finite elements beam model. The elements have three nodes and 18 DOF.
    The warping part of the stiffness cross-section matrices is taken into account.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def ignore_warping() -> bool:
        return False

    @property
    def element_stiffness_matrix(self):
        """numpy.ndarray: The FE element stiffness matrix."""
        if not hasattr(self, '_element_stiffness_matrix'):
            dtype = self._dtype
            l = self.length
            S = self.cross_section_stiffness_matrix
            K_m = sp.dok_array((18, 18), dtype=dtype)

            K_m[0, 0] = (7 / 3) * S[0, 0] / l
            K_m[0, 1] = -8 / 3 * S[0, 0] / l
            K_m[0, 2] = (1 / 3) * S[0, 0] / l
            K_m[0, 3] = (7 / 3) * S[0, 1] / l
            K_m[0, 4] = -8 / 3 * S[0, 1] / l
            K_m[0, 5] = (1 / 3) * S[0, 1] / l
            K_m[0, 6] = (7 / 3) * S[0, 2] / l
            K_m[0, 7] = -8 / 3 * S[0, 2] / l
            K_m[0, 8] = (1 / 3) * S[0, 2] / l
            K_m[0, 9] = -1 / 2 * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[0, 10] = (2 / 3) * (-S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[0, 11] = (1 / 6) * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[0, 12] = (1 / 2) * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[0, 13] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[0, 14] = -1 / 6 * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[0, 15] = (1 / 3) * (7 * S[0, 5] * l - 12 * S[0, 6]) / l ** 2
            K_m[0, 16] = (8 / 3) * (-S[0, 5] * l + 3 * S[0, 6]) / l ** 2
            K_m[0, 17] = (1 / 3) * (S[0, 5] * l - 12 * S[0, 6]) / l ** 2
            K_m[1, 0] = -8 / 3 * S[0, 0] / l
            K_m[1, 1] = (16 / 3) * S[0, 0] / l
            K_m[1, 2] = -8 / 3 * S[0, 0] / l
            K_m[1, 3] = -8 / 3 * S[0, 1] / l
            K_m[1, 4] = (16 / 3) * S[0, 1] / l
            K_m[1, 5] = -8 / 3 * S[0, 1] / l
            K_m[1, 6] = -8 / 3 * S[0, 2] / l
            K_m[1, 7] = (16 / 3) * S[0, 2] / l
            K_m[1, 8] = -8 / 3 * S[0, 2] / l
            K_m[1, 9] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[1, 10] = (16 / 3) * S[0, 3] / l
            K_m[1, 11] = (2 / 3) * (-S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[1, 12] = (2 / 3) * (-S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[1, 13] = (16 / 3) * S[0, 4] / l
            K_m[1, 14] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[1, 15] = -8 / 3 * S[0, 5] / l
            K_m[1, 16] = (16 / 3) * S[0, 5] / l
            K_m[1, 17] = -8 / 3 * S[0, 5] / l
            K_m[2, 0] = (1 / 3) * S[0, 0] / l
            K_m[2, 1] = -8 / 3 * S[0, 0] / l
            K_m[2, 2] = (7 / 3) * S[0, 0] / l
            K_m[2, 3] = (1 / 3) * S[0, 1] / l
            K_m[2, 4] = -8 / 3 * S[0, 1] / l
            K_m[2, 5] = (7 / 3) * S[0, 1] / l
            K_m[2, 6] = (1 / 3) * S[0, 2] / l
            K_m[2, 7] = -8 / 3 * S[0, 2] / l
            K_m[2, 8] = (7 / 3) * S[0, 2] / l
            K_m[2, 9] = -1 / 6 * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[2, 10] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[2, 11] = (1 / 2) * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[2, 12] = (1 / 6) * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[2, 13] = (2 / 3) * (-S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[2, 14] = -1 / 2 * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[2, 15] = (1 / 3) * (S[0, 5] * l + 12 * S[0, 6]) / l ** 2
            K_m[2, 16] = (8 / 3) * (-S[0, 5] * l - 3 * S[0, 6]) / l ** 2
            K_m[2, 17] = (1 / 3) * (7 * S[0, 5] * l + 12 * S[0, 6]) / l ** 2
            K_m[3, 0] = (7 / 3) * S[1, 0] / l
            K_m[3, 1] = -8 / 3 * S[1, 0] / l
            K_m[3, 2] = (1 / 3) * S[1, 0] / l
            K_m[3, 3] = (7 / 3) * S[1, 1] / l
            K_m[3, 4] = -8 / 3 * S[1, 1] / l
            K_m[3, 5] = (1 / 3) * S[1, 1] / l
            K_m[3, 6] = (7 / 3) * S[1, 2] / l
            K_m[3, 7] = -8 / 3 * S[1, 2] / l
            K_m[3, 8] = (1 / 3) * S[1, 2] / l
            K_m[3, 9] = -1 / 2 * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[3, 10] = (2 / 3) * (-S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[3, 11] = (1 / 6) * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[3, 12] = (1 / 2) * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[3, 13] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[3, 14] = -1 / 6 * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[3, 15] = (1 / 3) * (7 * S[1, 5] * l - 12 * S[1, 6]) / l ** 2
            K_m[3, 16] = (8 / 3) * (-S[1, 5] * l + 3 * S[1, 6]) / l ** 2
            K_m[3, 17] = (1 / 3) * (S[1, 5] * l - 12 * S[1, 6]) / l ** 2
            K_m[4, 0] = -8 / 3 * S[1, 0] / l
            K_m[4, 1] = (16 / 3) * S[1, 0] / l
            K_m[4, 2] = -8 / 3 * S[1, 0] / l
            K_m[4, 3] = -8 / 3 * S[1, 1] / l
            K_m[4, 4] = (16 / 3) * S[1, 1] / l
            K_m[4, 5] = -8 / 3 * S[1, 1] / l
            K_m[4, 6] = -8 / 3 * S[1, 2] / l
            K_m[4, 7] = (16 / 3) * S[1, 2] / l
            K_m[4, 8] = -8 / 3 * S[1, 2] / l
            K_m[4, 9] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[4, 10] = (16 / 3) * S[1, 3] / l
            K_m[4, 11] = (2 / 3) * (-S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[4, 12] = (2 / 3) * (-S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[4, 13] = (16 / 3) * S[1, 4] / l
            K_m[4, 14] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[4, 15] = -8 / 3 * S[1, 5] / l
            K_m[4, 16] = (16 / 3) * S[1, 5] / l
            K_m[4, 17] = -8 / 3 * S[1, 5] / l
            K_m[5, 0] = (1 / 3) * S[1, 0] / l
            K_m[5, 1] = -8 / 3 * S[1, 0] / l
            K_m[5, 2] = (7 / 3) * S[1, 0] / l
            K_m[5, 3] = (1 / 3) * S[1, 1] / l
            K_m[5, 4] = -8 / 3 * S[1, 1] / l
            K_m[5, 5] = (7 / 3) * S[1, 1] / l
            K_m[5, 6] = (1 / 3) * S[1, 2] / l
            K_m[5, 7] = -8 / 3 * S[1, 2] / l
            K_m[5, 8] = (7 / 3) * S[1, 2] / l
            K_m[5, 9] = -1 / 6 * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[5, 10] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[5, 11] = (1 / 2) * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[5, 12] = (1 / 6) * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[5, 13] = (2 / 3) * (-S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[5, 14] = -1 / 2 * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[5, 15] = (1 / 3) * (S[1, 5] * l + 12 * S[1, 6]) / l ** 2
            K_m[5, 16] = (8 / 3) * (-S[1, 5] * l - 3 * S[1, 6]) / l ** 2
            K_m[5, 17] = (1 / 3) * (7 * S[1, 5] * l + 12 * S[1, 6]) / l ** 2
            K_m[6, 0] = (7 / 3) * S[2, 0] / l
            K_m[6, 1] = -8 / 3 * S[2, 0] / l
            K_m[6, 2] = (1 / 3) * S[2, 0] / l
            K_m[6, 3] = (7 / 3) * S[2, 1] / l
            K_m[6, 4] = -8 / 3 * S[2, 1] / l
            K_m[6, 5] = (1 / 3) * S[2, 1] / l
            K_m[6, 6] = (7 / 3) * S[2, 2] / l
            K_m[6, 7] = -8 / 3 * S[2, 2] / l
            K_m[6, 8] = (1 / 3) * S[2, 2] / l
            K_m[6, 9] = -1 / 2 * S[2, 1] + (7 / 3) * S[2, 3] / l
            K_m[6, 10] = (2 / 3) * (-S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[6, 11] = (1 / 6) * S[2, 1] + (1 / 3) * S[2, 3] / l
            K_m[6, 12] = (1 / 2) * S[2, 0] + (7 / 3) * S[2, 4] / l
            K_m[6, 13] = (2 / 3) * (S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[6, 14] = -1 / 6 * S[2, 0] + (1 / 3) * S[2, 4] / l
            K_m[6, 15] = (1 / 3) * (7 * S[2, 5] * l - 12 * S[2, 6]) / l ** 2
            K_m[6, 16] = (8 / 3) * (-S[2, 5] * l + 3 * S[2, 6]) / l ** 2
            K_m[6, 17] = (1 / 3) * (S[2, 5] * l - 12 * S[2, 6]) / l ** 2
            K_m[7, 0] = -8 / 3 * S[2, 0] / l
            K_m[7, 1] = (16 / 3) * S[2, 0] / l
            K_m[7, 2] = -8 / 3 * S[2, 0] / l
            K_m[7, 3] = -8 / 3 * S[2, 1] / l
            K_m[7, 4] = (16 / 3) * S[2, 1] / l
            K_m[7, 5] = -8 / 3 * S[2, 1] / l
            K_m[7, 6] = -8 / 3 * S[2, 2] / l
            K_m[7, 7] = (16 / 3) * S[2, 2] / l
            K_m[7, 8] = -8 / 3 * S[2, 2] / l
            K_m[7, 9] = (2 / 3) * (S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[7, 10] = (16 / 3) * S[2, 3] / l
            K_m[7, 11] = (2 / 3) * (-S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[7, 12] = (2 / 3) * (-S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[7, 13] = (16 / 3) * S[2, 4] / l
            K_m[7, 14] = (2 / 3) * (S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[7, 15] = -8 / 3 * S[2, 5] / l
            K_m[7, 16] = (16 / 3) * S[2, 5] / l
            K_m[7, 17] = -8 / 3 * S[2, 5] / l
            K_m[8, 0] = (1 / 3) * S[2, 0] / l
            K_m[8, 1] = -8 / 3 * S[2, 0] / l
            K_m[8, 2] = (7 / 3) * S[2, 0] / l
            K_m[8, 3] = (1 / 3) * S[2, 1] / l
            K_m[8, 4] = -8 / 3 * S[2, 1] / l
            K_m[8, 5] = (7 / 3) * S[2, 1] / l
            K_m[8, 6] = (1 / 3) * S[2, 2] / l
            K_m[8, 7] = -8 / 3 * S[2, 2] / l
            K_m[8, 8] = (7 / 3) * S[2, 2] / l
            K_m[8, 9] = -1 / 6 * S[2, 1] + (1 / 3) * S[2, 3] / l
            K_m[8, 10] = (2 / 3) * (S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[8, 11] = (1 / 2) * S[2, 1] + (7 / 3) * S[2, 3] / l
            K_m[8, 12] = (1 / 6) * S[2, 0] + (1 / 3) * S[2, 4] / l
            K_m[8, 13] = (2 / 3) * (-S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[8, 14] = -1 / 2 * S[2, 0] + (7 / 3) * S[2, 4] / l
            K_m[8, 15] = (1 / 3) * (S[2, 5] * l + 12 * S[2, 6]) / l ** 2
            K_m[8, 16] = (8 / 3) * (-S[2, 5] * l - 3 * S[2, 6]) / l ** 2
            K_m[8, 17] = (1 / 3) * (7 * S[2, 5] * l + 12 * S[2, 6]) / l ** 2
            K_m[9, 0] = -1 / 2 * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[9, 1] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[9, 2] = -1 / 6 * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[9, 3] = -1 / 2 * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[9, 4] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[9, 5] = -1 / 6 * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[9, 6] = -1 / 2 * S[1, 2] + (7 / 3) * S[3, 2] / l
            K_m[9, 7] = (2 / 3) * (S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[9, 8] = -1 / 6 * S[1, 2] + (1 / 3) * S[3, 2] / l
            K_m[9, 9] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l - 15 * S[1, 3] - 15 * S[3, 1])) / l
            K_m[9, 10] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[9, 11] = -1 / 30 * S[1, 1] * l - 1 / 6 * S[1, 3] + (1 / 6) * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[9, 12] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l - 15 * S[1, 4] + 15 * S[3, 0])) / l
            K_m[9, 13] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[9, 14] = (1 / 30) * S[1, 0] * l - 1 / 6 * S[1, 4] - 1 / 6 * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[9, 15] = (-1 / 2 * S[1, 5] * l ** 2 - 4 * S[3, 6] + (1 / 3) * l * (
                        2 * S[1, 6] + 7 * S[3, 5])) / l ** 2
            K_m[9, 16] = (2 / 3) * (S[1, 5] * l ** 2 + 12 * S[3, 6] - 2 * l * (S[1, 6] + 2 * S[3, 5])) / l ** 2
            K_m[9, 17] = (1 / 6) * (-S[1, 5] * l ** 2 - 24 * S[3, 6] + 2 * l * (2 * S[1, 6] + S[3, 5])) / l ** 2
            K_m[10, 0] = (2 / 3) * (-S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[10, 1] = (16 / 3) * S[3, 0] / l
            K_m[10, 2] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[10, 3] = (2 / 3) * (-S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[10, 4] = (16 / 3) * S[3, 1] / l
            K_m[10, 5] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[10, 6] = (2 / 3) * (-S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[10, 7] = (16 / 3) * S[3, 2] / l
            K_m[10, 8] = (2 / 3) * (S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[10, 9] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[10, 10] = (8 / 15) * (S[1, 1] * l ** 2 + 10 * S[3, 3]) / l
            K_m[10, 11] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[10, 12] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l - 10 * S[1, 4] - 10 * S[3, 0])) / l
            K_m[10, 13] = (8 / 15) * (-S[1, 0] * l ** 2 + 10 * S[3, 4]) / l
            K_m[10, 14] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[10, 15] = (2 / 3) * (-S[1, 5] * l + 4 * S[1, 6] - 4 * S[3, 5]) / l
            K_m[10, 16] = (16 / 3) * (-S[1, 6] + S[3, 5]) / l
            K_m[10, 17] = (2 / 3) * (S[1, 5] * l + 4 * S[1, 6] - 4 * S[3, 5]) / l
            K_m[11, 0] = (1 / 6) * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[11, 1] = (2 / 3) * (-S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[11, 2] = (1 / 2) * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[11, 3] = (1 / 6) * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[11, 4] = (2 / 3) * (-S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[11, 5] = (1 / 2) * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[11, 6] = (1 / 6) * S[1, 2] + (1 / 3) * S[3, 2] / l
            K_m[11, 7] = (2 / 3) * (-S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[11, 8] = (1 / 2) * S[1, 2] + (7 / 3) * S[3, 2] / l
            K_m[11, 9] = -1 / 30 * S[1, 1] * l + (1 / 6) * S[1, 3] - 1 / 6 * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[11, 10] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[11, 11] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l + 15 * S[1, 3] + 15 * S[3, 1])) / l
            K_m[11, 12] = (1 / 30) * S[1, 0] * l + (1 / 6) * S[1, 4] + (1 / 6) * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[11, 13] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l - 10 * S[1, 4] - 10 * S[3, 0])) / l
            K_m[11, 14] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l + 15 * S[1, 4] - 15 * S[3, 0])) / l
            K_m[11, 15] = (1 / 6) * (S[1, 5] * l ** 2 + 24 * S[3, 6] + 2 * l * (2 * S[1, 6] + S[3, 5])) / l ** 2
            K_m[11, 16] = (2 / 3) * (-S[1, 5] * l ** 2 - 12 * S[3, 6] + 2 * l * (-S[1, 6] - 2 * S[3, 5])) / l ** 2
            K_m[11, 17] = ((1 / 2) * S[1, 5] * l ** 2 + 4 * S[3, 6] + (1 / 3) * l * (
                        2 * S[1, 6] + 7 * S[3, 5])) / l ** 2
            K_m[12, 0] = (1 / 2) * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[12, 1] = (2 / 3) * (-S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[12, 2] = (1 / 6) * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[12, 3] = (1 / 2) * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[12, 4] = (2 / 3) * (-S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[12, 5] = (1 / 6) * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[12, 6] = (1 / 2) * S[0, 2] + (7 / 3) * S[4, 2] / l
            K_m[12, 7] = (2 / 3) * (-S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[12, 8] = (1 / 6) * S[0, 2] + (1 / 3) * S[4, 2] / l
            K_m[12, 9] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l + 15 * S[0, 3] - 15 * S[4, 1])) / l
            K_m[12, 10] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l - 10 * S[0, 3] - 10 * S[4, 1])) / l
            K_m[12, 11] = (1 / 30) * S[0, 1] * l + (1 / 6) * S[0, 3] + (1 / 6) * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[12, 12] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l + 15 * S[0, 4] + 15 * S[4, 0])) / l
            K_m[12, 13] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[12, 14] = -1 / 30 * S[0, 0] * l + (1 / 6) * S[0, 4] - 1 / 6 * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[12, 15] = ((1 / 2) * S[0, 5] * l ** 2 - 4 * S[4, 6] + (1 / 3) * l * (
                        -2 * S[0, 6] + 7 * S[4, 5])) / l ** 2
            K_m[12, 16] = (2 / 3) * (-S[0, 5] * l ** 2 + 12 * S[4, 6] + 2 * l * (S[0, 6] - 2 * S[4, 5])) / l ** 2
            K_m[12, 17] = (1 / 6) * (S[0, 5] * l ** 2 - 24 * S[4, 6] + 2 * l * (-2 * S[0, 6] + S[4, 5])) / l ** 2
            K_m[13, 0] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[13, 1] = (16 / 3) * S[4, 0] / l
            K_m[13, 2] = (2 / 3) * (-S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[13, 3] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[13, 4] = (16 / 3) * S[4, 1] / l
            K_m[13, 5] = (2 / 3) * (-S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[13, 6] = (2 / 3) * (S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[13, 7] = (16 / 3) * S[4, 2] / l
            K_m[13, 8] = (2 / 3) * (-S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[13, 9] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[13, 10] = (8 / 15) * (-S[0, 1] * l ** 2 + 10 * S[4, 3]) / l
            K_m[13, 11] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l - 10 * S[0, 3] - 10 * S[4, 1])) / l
            K_m[13, 12] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[13, 13] = (8 / 15) * (S[0, 0] * l ** 2 + 10 * S[4, 4]) / l
            K_m[13, 14] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[13, 15] = (2 / 3) * (S[0, 5] * l - 4 * S[0, 6] - 4 * S[4, 5]) / l
            K_m[13, 16] = (16 / 3) * (S[0, 6] + S[4, 5]) / l
            K_m[13, 17] = (2 / 3) * (-S[0, 5] * l - 4 * S[0, 6] - 4 * S[4, 5]) / l
            K_m[14, 0] = -1 / 6 * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[14, 1] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[14, 2] = -1 / 2 * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[14, 3] = -1 / 6 * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[14, 4] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[14, 5] = -1 / 2 * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[14, 6] = -1 / 6 * S[0, 2] + (1 / 3) * S[4, 2] / l
            K_m[14, 7] = (2 / 3) * (S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[14, 8] = -1 / 2 * S[0, 2] + (7 / 3) * S[4, 2] / l
            K_m[14, 9] = (1 / 30) * S[0, 1] * l - 1 / 6 * S[0, 3] - 1 / 6 * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[14, 10] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[14, 11] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l - 15 * S[0, 3] + 15 * S[4, 1])) / l
            K_m[14, 12] = -1 / 30 * S[0, 0] * l - 1 / 6 * S[0, 4] + (1 / 6) * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[14, 13] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[14, 14] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l - 15 * S[0, 4] - 15 * S[4, 0])) / l
            K_m[14, 15] = (1 / 6) * (-S[0, 5] * l ** 2 + 24 * S[4, 6] + 2 * l * (-2 * S[0, 6] + S[4, 5])) / l ** 2
            K_m[14, 16] = (2 / 3) * (S[0, 5] * l ** 2 - 12 * S[4, 6] + 2 * l * (S[0, 6] - 2 * S[4, 5])) / l ** 2
            K_m[14, 17] = (-1 / 2 * S[0, 5] * l ** 2 + 4 * S[4, 6] + (1 / 3) * l * (
                        -2 * S[0, 6] + 7 * S[4, 5])) / l ** 2
            K_m[15, 0] = (1 / 3) * (7 * S[5, 0] * l - 12 * S[6, 0]) / l ** 2
            K_m[15, 1] = -8 / 3 * S[5, 0] / l
            K_m[15, 2] = (1 / 3) * (S[5, 0] * l + 12 * S[6, 0]) / l ** 2
            K_m[15, 3] = (1 / 3) * (7 * S[5, 1] * l - 12 * S[6, 1]) / l ** 2
            K_m[15, 4] = -8 / 3 * S[5, 1] / l
            K_m[15, 5] = (1 / 3) * (S[5, 1] * l + 12 * S[6, 1]) / l ** 2
            K_m[15, 6] = (1 / 3) * (7 * S[5, 2] * l - 12 * S[6, 2]) / l ** 2
            K_m[15, 7] = -8 / 3 * S[5, 2] / l
            K_m[15, 8] = (1 / 3) * (S[5, 2] * l + 12 * S[6, 2]) / l ** 2
            K_m[15, 9] = (-1 / 2 * S[5, 1] * l ** 2 - 4 * S[6, 3] + (1 / 3) * l * (
                        7 * S[5, 3] + 2 * S[6, 1])) / l ** 2
            K_m[15, 10] = (2 / 3) * (-S[5, 1] * l - 4 * S[5, 3] + 4 * S[6, 1]) / l
            K_m[15, 11] = (1 / 6) * (S[5, 1] * l ** 2 + 24 * S[6, 3] + 2 * l * (S[5, 3] + 2 * S[6, 1])) / l ** 2
            K_m[15, 12] = ((1 / 2) * S[5, 0] * l ** 2 - 4 * S[6, 4] + (1 / 3) * l * (
                        7 * S[5, 4] - 2 * S[6, 0])) / l ** 2
            K_m[15, 13] = (2 / 3) * (S[5, 0] * l - 4 * S[5, 4] - 4 * S[6, 0]) / l
            K_m[15, 14] = (1 / 6) * (-S[5, 0] * l ** 2 + 24 * S[6, 4] + 2 * l * (S[5, 4] - 2 * S[6, 0])) / l ** 2
            K_m[15, 15] = (1 / 3) * (7 * S[5, 5] * l ** 2 + 48 * S[6, 6] - 12 * l * (S[5, 6] + S[6, 5])) / l ** 3
            K_m[15, 16] = (8 / 3) * (-S[5, 5] * l ** 2 + 3 * S[5, 6] * l - 12 * S[6, 6]) / l ** 3
            K_m[15, 17] = (1 / 3) * (S[5, 5] * l ** 2 + 48 * S[6, 6] + 12 * l * (-S[5, 6] + S[6, 5])) / l ** 3
            K_m[16, 0] = (8 / 3) * (-S[5, 0] * l + 3 * S[6, 0]) / l ** 2
            K_m[16, 1] = (16 / 3) * S[5, 0] / l
            K_m[16, 2] = (8 / 3) * (-S[5, 0] * l - 3 * S[6, 0]) / l ** 2
            K_m[16, 3] = (8 / 3) * (-S[5, 1] * l + 3 * S[6, 1]) / l ** 2
            K_m[16, 4] = (16 / 3) * S[5, 1] / l
            K_m[16, 5] = (8 / 3) * (-S[5, 1] * l - 3 * S[6, 1]) / l ** 2
            K_m[16, 6] = (8 / 3) * (-S[5, 2] * l + 3 * S[6, 2]) / l ** 2
            K_m[16, 7] = (16 / 3) * S[5, 2] / l
            K_m[16, 8] = (8 / 3) * (-S[5, 2] * l - 3 * S[6, 2]) / l ** 2
            K_m[16, 9] = (2 / 3) * (S[5, 1] * l ** 2 + 12 * S[6, 3] - 2 * l * (2 * S[5, 3] + S[6, 1])) / l ** 2
            K_m[16, 10] = (16 / 3) * (S[5, 3] - S[6, 1]) / l
            K_m[16, 11] = (2 / 3) * (-S[5, 1] * l ** 2 - 12 * S[6, 3] + 2 * l * (-2 * S[5, 3] - S[6, 1])) / l ** 2
            K_m[16, 12] = (2 / 3) * (-S[5, 0] * l ** 2 + 12 * S[6, 4] + 2 * l * (-2 * S[5, 4] + S[6, 0])) / l ** 2
            K_m[16, 13] = (16 / 3) * (S[5, 4] + S[6, 0]) / l
            K_m[16, 14] = (2 / 3) * (S[5, 0] * l ** 2 - 12 * S[6, 4] + 2 * l * (-2 * S[5, 4] + S[6, 0])) / l ** 2
            K_m[16, 15] = (8 / 3) * (-S[5, 5] * l ** 2 + 3 * S[6, 5] * l - 12 * S[6, 6]) / l ** 3
            K_m[16, 16] = (16 / 3) * S[5, 5] / l + 64 * S[6, 6] / l ** 3
            K_m[16, 17] = (8 / 3) * (-S[5, 5] * l ** 2 - 3 * S[6, 5] * l - 12 * S[6, 6]) / l ** 3
            K_m[17, 0] = (1 / 3) * (S[5, 0] * l - 12 * S[6, 0]) / l ** 2
            K_m[17, 1] = -8 / 3 * S[5, 0] / l
            K_m[17, 2] = (1 / 3) * (7 * S[5, 0] * l + 12 * S[6, 0]) / l ** 2
            K_m[17, 3] = (1 / 3) * (S[5, 1] * l - 12 * S[6, 1]) / l ** 2
            K_m[17, 4] = -8 / 3 * S[5, 1] / l
            K_m[17, 5] = (1 / 3) * (7 * S[5, 1] * l + 12 * S[6, 1]) / l ** 2
            K_m[17, 6] = (1 / 3) * (S[5, 2] * l - 12 * S[6, 2]) / l ** 2
            K_m[17, 7] = -8 / 3 * S[5, 2] / l
            K_m[17, 8] = (1 / 3) * (7 * S[5, 2] * l + 12 * S[6, 2]) / l ** 2
            K_m[17, 9] = (1 / 6) * (-S[5, 1] * l ** 2 - 24 * S[6, 3] + 2 * l * (S[5, 3] + 2 * S[6, 1])) / l ** 2
            K_m[17, 10] = (2 / 3) * (S[5, 1] * l - 4 * S[5, 3] + 4 * S[6, 1]) / l
            K_m[17, 11] = ((1 / 2) * S[5, 1] * l ** 2 + 4 * S[6, 3] + (1 / 3) * l * (
                        7 * S[5, 3] + 2 * S[6, 1])) / l ** 2
            K_m[17, 12] = (1 / 6) * (S[5, 0] * l ** 2 - 24 * S[6, 4] + 2 * l * (S[5, 4] - 2 * S[6, 0])) / l ** 2
            K_m[17, 13] = (2 / 3) * (-S[5, 0] * l - 4 * S[5, 4] - 4 * S[6, 0]) / l
            K_m[17, 14] = (-1 / 2 * S[5, 0] * l ** 2 + 4 * S[6, 4] + (1 / 3) * l * (
                        7 * S[5, 4] - 2 * S[6, 0])) / l ** 2
            K_m[17, 15] = (1 / 3) * (S[5, 5] * l ** 2 + 48 * S[6, 6] + 12 * l * (S[5, 6] - S[6, 5])) / l ** 3
            K_m[17, 16] = (8 / 3) * (-S[5, 5] * l ** 2 - 3 * S[5, 6] * l - 12 * S[6, 6]) / l ** 3
            K_m[17, 17] = (1 / 3) * (7 * S[5, 5] * l ** 2 + 48 * S[6, 6] + 12 * l * (S[5, 6] + S[6, 5])) / l ** 3

            self._element_stiffness_matrix = K_m.tocsc()

        return self._element_stiffness_matrix

    def B_matrix(self, z):
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        B = sp.dok_array((7, 18), dtype=dtype)

        B[0, 0] = (-3 * l + 4 * z) / l ** 2
        B[0, 1] = 4 * (l - 2 * z) / l ** 2
        B[0, 2] = (-l + 4 * z) / l ** 2
        # B[0,3] = 0
        # B[0,4] = 0
        # B[0,5] = 0
        # B[0,6] = 0
        # B[0,7] = 0
        # B[0,8] = 0
        # B[0,9] = 0
        # B[0,10] = 0
        # B[0,11] = 0
        B[0, 12] = -1 + 3 * z / l - 2 * z ** 2 / l ** 2
        B[0, 13] = 4 * z * (-l + z) / l ** 2
        B[0, 14] = z * (l - 2 * z) / l ** 2
        # B[0,15] = 0
        # B[0,16] = 0
        # B[0,17] = 0
        # B[1,0] = 0
        # B[1,1] = 0
        # B[1,2] = 0
        B[1, 3] = (-3 * l + 4 * z) / l ** 2
        B[1, 4] = 4 * (l - 2 * z) / l ** 2
        B[1, 5] = (-l + 4 * z) / l ** 2
        # B[1,6] = 0
        # B[1,7] = 0
        # B[1,8] = 0
        B[1, 9] = 1 - 3 * z / l + 2 * z ** 2 / l ** 2
        B[1, 10] = 4 * z * (l - z) / l ** 2
        B[1, 11] = z * (-l + 2 * z) / l ** 2
        # B[1,12] = 0
        # B[1,13] = 0
        # B[1,14] = 0
        # B[1,15] = 0
        # B[1,16] = 0
        # B[1,17] = 0
        # B[2,0] = 0
        # B[2,1] = 0
        # B[2,2] = 0
        # B[2,3] = 0
        # B[2,4] = 0
        # B[2,5] = 0
        B[2, 6] = (-3 * l + 4 * z) / l ** 2
        B[2, 7] = 4 * (l - 2 * z) / l ** 2
        B[2, 8] = (-l + 4 * z) / l ** 2
        # B[2,9] = 0
        # B[2,10] = 0
        # B[2,11] = 0
        # B[2,12] = 0
        # B[2,13] = 0
        # B[2,14] = 0
        # B[2,15] = 0
        # B[2,16] = 0
        # B[2,17] = 0
        # B[3,0] = 0
        # B[3,1] = 0
        # B[3,2] = 0
        # B[3,3] = 0
        # B[3,4] = 0
        # B[3,5] = 0
        # B[3,6] = 0
        # B[3,7] = 0
        # B[3,8] = 0
        B[3, 9] = (-3 * l + 4 * z) / l ** 2
        B[3, 10] = 4 * (l - 2 * z) / l ** 2
        B[3, 11] = (-l + 4 * z) / l ** 2
        # B[3,12] = 0
        # B[3,13] = 0
        # B[3,14] = 0
        # B[3,15] = 0
        # B[3,16] = 0
        # B[3,17] = 0
        # B[4,0] = 0
        # B[4,1] = 0
        # B[4,2] = 0
        # B[4,3] = 0
        # B[4,4] = 0
        # B[4,5] = 0
        # B[4,6] = 0
        # B[4,7] = 0
        # B[4,8] = 0
        # B[4,9] = 0
        # B[4,10] = 0
        # B[4,11] = 0
        B[4, 12] = (-3 * l + 4 * z) / l ** 2
        B[4, 13] = 4 * (l - 2 * z) / l ** 2
        B[4, 14] = (-l + 4 * z) / l ** 2
        # B[4,15] = 0
        # B[4,16] = 0
        # B[4,17] = 0
        # B[5,0] = 0
        # B[5,1] = 0
        # B[5,2] = 0
        # B[5,3] = 0
        # B[5,4] = 0
        # B[5,5] = 0
        # B[5,6] = 0
        # B[5,7] = 0
        # B[5,8] = 0
        # B[5,9] = 0
        # B[5,10] = 0
        # B[5,11] = 0
        # B[5,12] = 0
        # B[5,13] = 0
        # B[5,14] = 0
        B[5, 15] = (-3 * l + 4 * z) / l ** 2
        B[5, 16] = 4 * (l - 2 * z) / l ** 2
        B[5, 17] = (-l + 4 * z) / l ** 2
        # B[6,0] = 0
        # B[6,1] = 0
        # B[6,2] = 0
        # B[6,3] = 0
        # B[6,4] = 0
        # B[6,5] = 0
        # B[6,6] = 0
        # B[6,7] = 0
        # B[6,8] = 0
        # B[6,9] = 0
        # B[6,10] = 0
        # B[6,11] = 0
        # B[6,12] = 0
        # B[6,13] = 0
        # B[6,14] = 0
        B[6, 15] = 4 / l ** 2
        B[6, 16] = -8 / l ** 2
        B[6, 17] = 4 / l ** 2

        return B


class BeamElement3NodeWithoutWarping(BeamElement3Node):
    """
    A element of the 1D finite elements beam model. The elements have three nodes and 18 DOF.
    The warping part of the stiffness cross-section matrices is ignored.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def ignore_warping() -> bool:
        return True

    @property
    def element_stiffness_matrix(self):
        """numpy.ndarray: The FE element stiffness matrix."""
        if not hasattr(self, '_element_stiffness_matrix'):
            dtype = self._dtype
            l = self.length
            S = self.cross_section_stiffness_matrix
            K_m = sp.dok_array((18, 18), dtype=dtype)

            K_m[0, 0] = (7 / 3) * S[0, 0] / l
            K_m[0, 1] = -8 / 3 * S[0, 0] / l
            K_m[0, 2] = (1 / 3) * S[0, 0] / l
            K_m[0, 3] = (7 / 3) * S[0, 1] / l
            K_m[0, 4] = -8 / 3 * S[0, 1] / l
            K_m[0, 5] = (1 / 3) * S[0, 1] / l
            K_m[0, 6] = (7 / 3) * S[0, 2] / l
            K_m[0, 7] = -8 / 3 * S[0, 2] / l
            K_m[0, 8] = (1 / 3) * S[0, 2] / l
            K_m[0, 9] = -1 / 2 * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[0, 10] = (2 / 3) * (-S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[0, 11] = (1 / 6) * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[0, 12] = (1 / 2) * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[0, 13] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[0, 14] = -1 / 6 * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[0, 15] = (7 / 3) * S[0, 5] / l
            K_m[0, 16] = -8 / 3 * S[0, 5] / l
            K_m[0, 17] = (1 / 3) * S[0, 5] / l
            K_m[1, 0] = -8 / 3 * S[0, 0] / l
            K_m[1, 1] = (16 / 3) * S[0, 0] / l
            K_m[1, 2] = -8 / 3 * S[0, 0] / l
            K_m[1, 3] = -8 / 3 * S[0, 1] / l
            K_m[1, 4] = (16 / 3) * S[0, 1] / l
            K_m[1, 5] = -8 / 3 * S[0, 1] / l
            K_m[1, 6] = -8 / 3 * S[0, 2] / l
            K_m[1, 7] = (16 / 3) * S[0, 2] / l
            K_m[1, 8] = -8 / 3 * S[0, 2] / l
            K_m[1, 9] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[1, 10] = (16 / 3) * S[0, 3] / l
            K_m[1, 11] = (2 / 3) * (-S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[1, 12] = (2 / 3) * (-S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[1, 13] = (16 / 3) * S[0, 4] / l
            K_m[1, 14] = (2 / 3) * (S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[1, 15] = -8 / 3 * S[0, 5] / l
            K_m[1, 16] = (16 / 3) * S[0, 5] / l
            K_m[1, 17] = -8 / 3 * S[0, 5] / l
            K_m[2, 0] = (1 / 3) * S[0, 0] / l
            K_m[2, 1] = -8 / 3 * S[0, 0] / l
            K_m[2, 2] = (7 / 3) * S[0, 0] / l
            K_m[2, 3] = (1 / 3) * S[0, 1] / l
            K_m[2, 4] = -8 / 3 * S[0, 1] / l
            K_m[2, 5] = (7 / 3) * S[0, 1] / l
            K_m[2, 6] = (1 / 3) * S[0, 2] / l
            K_m[2, 7] = -8 / 3 * S[0, 2] / l
            K_m[2, 8] = (7 / 3) * S[0, 2] / l
            K_m[2, 9] = -1 / 6 * S[0, 1] + (1 / 3) * S[0, 3] / l
            K_m[2, 10] = (2 / 3) * (S[0, 1] * l - 4 * S[0, 3]) / l
            K_m[2, 11] = (1 / 2) * S[0, 1] + (7 / 3) * S[0, 3] / l
            K_m[2, 12] = (1 / 6) * S[0, 0] + (1 / 3) * S[0, 4] / l
            K_m[2, 13] = (2 / 3) * (-S[0, 0] * l - 4 * S[0, 4]) / l
            K_m[2, 14] = -1 / 2 * S[0, 0] + (7 / 3) * S[0, 4] / l
            K_m[2, 15] = (1 / 3) * S[0, 5] / l
            K_m[2, 16] = -8 / 3 * S[0, 5] / l
            K_m[2, 17] = (7 / 3) * S[0, 5] / l
            K_m[3, 0] = (7 / 3) * S[1, 0] / l
            K_m[3, 1] = -8 / 3 * S[1, 0] / l
            K_m[3, 2] = (1 / 3) * S[1, 0] / l
            K_m[3, 3] = (7 / 3) * S[1, 1] / l
            K_m[3, 4] = -8 / 3 * S[1, 1] / l
            K_m[3, 5] = (1 / 3) * S[1, 1] / l
            K_m[3, 6] = (7 / 3) * S[1, 2] / l
            K_m[3, 7] = -8 / 3 * S[1, 2] / l
            K_m[3, 8] = (1 / 3) * S[1, 2] / l
            K_m[3, 9] = -1 / 2 * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[3, 10] = (2 / 3) * (-S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[3, 11] = (1 / 6) * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[3, 12] = (1 / 2) * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[3, 13] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[3, 14] = -1 / 6 * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[3, 15] = (7 / 3) * S[1, 5] / l
            K_m[3, 16] = -8 / 3 * S[1, 5] / l
            K_m[3, 17] = (1 / 3) * S[1, 5] / l
            K_m[4, 0] = -8 / 3 * S[1, 0] / l
            K_m[4, 1] = (16 / 3) * S[1, 0] / l
            K_m[4, 2] = -8 / 3 * S[1, 0] / l
            K_m[4, 3] = -8 / 3 * S[1, 1] / l
            K_m[4, 4] = (16 / 3) * S[1, 1] / l
            K_m[4, 5] = -8 / 3 * S[1, 1] / l
            K_m[4, 6] = -8 / 3 * S[1, 2] / l
            K_m[4, 7] = (16 / 3) * S[1, 2] / l
            K_m[4, 8] = -8 / 3 * S[1, 2] / l
            K_m[4, 9] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[4, 10] = (16 / 3) * S[1, 3] / l
            K_m[4, 11] = (2 / 3) * (-S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[4, 12] = (2 / 3) * (-S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[4, 13] = (16 / 3) * S[1, 4] / l
            K_m[4, 14] = (2 / 3) * (S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[4, 15] = -8 / 3 * S[1, 5] / l
            K_m[4, 16] = (16 / 3) * S[1, 5] / l
            K_m[4, 17] = -8 / 3 * S[1, 5] / l
            K_m[5, 0] = (1 / 3) * S[1, 0] / l
            K_m[5, 1] = -8 / 3 * S[1, 0] / l
            K_m[5, 2] = (7 / 3) * S[1, 0] / l
            K_m[5, 3] = (1 / 3) * S[1, 1] / l
            K_m[5, 4] = -8 / 3 * S[1, 1] / l
            K_m[5, 5] = (7 / 3) * S[1, 1] / l
            K_m[5, 6] = (1 / 3) * S[1, 2] / l
            K_m[5, 7] = -8 / 3 * S[1, 2] / l
            K_m[5, 8] = (7 / 3) * S[1, 2] / l
            K_m[5, 9] = -1 / 6 * S[1, 1] + (1 / 3) * S[1, 3] / l
            K_m[5, 10] = (2 / 3) * (S[1, 1] * l - 4 * S[1, 3]) / l
            K_m[5, 11] = (1 / 2) * S[1, 1] + (7 / 3) * S[1, 3] / l
            K_m[5, 12] = (1 / 6) * S[1, 0] + (1 / 3) * S[1, 4] / l
            K_m[5, 13] = (2 / 3) * (-S[1, 0] * l - 4 * S[1, 4]) / l
            K_m[5, 14] = -1 / 2 * S[1, 0] + (7 / 3) * S[1, 4] / l
            K_m[5, 15] = (1 / 3) * S[1, 5] / l
            K_m[5, 16] = -8 / 3 * S[1, 5] / l
            K_m[5, 17] = (7 / 3) * S[1, 5] / l
            K_m[6, 0] = (7 / 3) * S[2, 0] / l
            K_m[6, 1] = -8 / 3 * S[2, 0] / l
            K_m[6, 2] = (1 / 3) * S[2, 0] / l
            K_m[6, 3] = (7 / 3) * S[2, 1] / l
            K_m[6, 4] = -8 / 3 * S[2, 1] / l
            K_m[6, 5] = (1 / 3) * S[2, 1] / l
            K_m[6, 6] = (7 / 3) * S[2, 2] / l
            K_m[6, 7] = -8 / 3 * S[2, 2] / l
            K_m[6, 8] = (1 / 3) * S[2, 2] / l
            K_m[6, 9] = -1 / 2 * S[2, 1] + (7 / 3) * S[2, 3] / l
            K_m[6, 10] = (2 / 3) * (-S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[6, 11] = (1 / 6) * S[2, 1] + (1 / 3) * S[2, 3] / l
            K_m[6, 12] = (1 / 2) * S[2, 0] + (7 / 3) * S[2, 4] / l
            K_m[6, 13] = (2 / 3) * (S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[6, 14] = -1 / 6 * S[2, 0] + (1 / 3) * S[2, 4] / l
            K_m[6, 15] = (7 / 3) * S[2, 5] / l
            K_m[6, 16] = -8 / 3 * S[2, 5] / l
            K_m[6, 17] = (1 / 3) * S[2, 5] / l
            K_m[7, 0] = -8 / 3 * S[2, 0] / l
            K_m[7, 1] = (16 / 3) * S[2, 0] / l
            K_m[7, 2] = -8 / 3 * S[2, 0] / l
            K_m[7, 3] = -8 / 3 * S[2, 1] / l
            K_m[7, 4] = (16 / 3) * S[2, 1] / l
            K_m[7, 5] = -8 / 3 * S[2, 1] / l
            K_m[7, 6] = -8 / 3 * S[2, 2] / l
            K_m[7, 7] = (16 / 3) * S[2, 2] / l
            K_m[7, 8] = -8 / 3 * S[2, 2] / l
            K_m[7, 9] = (2 / 3) * (S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[7, 10] = (16 / 3) * S[2, 3] / l
            K_m[7, 11] = (2 / 3) * (-S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[7, 12] = (2 / 3) * (-S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[7, 13] = (16 / 3) * S[2, 4] / l
            K_m[7, 14] = (2 / 3) * (S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[7, 15] = -8 / 3 * S[2, 5] / l
            K_m[7, 16] = (16 / 3) * S[2, 5] / l
            K_m[7, 17] = -8 / 3 * S[2, 5] / l
            K_m[8, 0] = (1 / 3) * S[2, 0] / l
            K_m[8, 1] = -8 / 3 * S[2, 0] / l
            K_m[8, 2] = (7 / 3) * S[2, 0] / l
            K_m[8, 3] = (1 / 3) * S[2, 1] / l
            K_m[8, 4] = -8 / 3 * S[2, 1] / l
            K_m[8, 5] = (7 / 3) * S[2, 1] / l
            K_m[8, 6] = (1 / 3) * S[2, 2] / l
            K_m[8, 7] = -8 / 3 * S[2, 2] / l
            K_m[8, 8] = (7 / 3) * S[2, 2] / l
            K_m[8, 9] = -1 / 6 * S[2, 1] + (1 / 3) * S[2, 3] / l
            K_m[8, 10] = (2 / 3) * (S[2, 1] * l - 4 * S[2, 3]) / l
            K_m[8, 11] = (1 / 2) * S[2, 1] + (7 / 3) * S[2, 3] / l
            K_m[8, 12] = (1 / 6) * S[2, 0] + (1 / 3) * S[2, 4] / l
            K_m[8, 13] = (2 / 3) * (-S[2, 0] * l - 4 * S[2, 4]) / l
            K_m[8, 14] = -1 / 2 * S[2, 0] + (7 / 3) * S[2, 4] / l
            K_m[8, 15] = (1 / 3) * S[2, 5] / l
            K_m[8, 16] = -8 / 3 * S[2, 5] / l
            K_m[8, 17] = (7 / 3) * S[2, 5] / l
            K_m[9, 0] = -1 / 2 * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[9, 1] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[9, 2] = -1 / 6 * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[9, 3] = -1 / 2 * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[9, 4] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[9, 5] = -1 / 6 * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[9, 6] = -1 / 2 * S[1, 2] + (7 / 3) * S[3, 2] / l
            K_m[9, 7] = (2 / 3) * (S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[9, 8] = -1 / 6 * S[1, 2] + (1 / 3) * S[3, 2] / l
            K_m[9, 9] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l - 15 * S[1, 3] - 15 * S[3, 1])) / l
            K_m[9, 10] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[9, 11] = -1 / 30 * S[1, 1] * l - 1 / 6 * S[1, 3] + (1 / 6) * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[9, 12] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l - 15 * S[1, 4] + 15 * S[3, 0])) / l
            K_m[9, 13] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[9, 14] = (1 / 30) * S[1, 0] * l - 1 / 6 * S[1, 4] - 1 / 6 * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[9, 15] = -1 / 2 * S[1, 5] + (7 / 3) * S[3, 5] / l
            K_m[9, 16] = (2 / 3) * (S[1, 5] * l - 4 * S[3, 5]) / l
            K_m[9, 17] = -1 / 6 * S[1, 5] + (1 / 3) * S[3, 5] / l
            K_m[10, 0] = (2 / 3) * (-S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[10, 1] = (16 / 3) * S[3, 0] / l
            K_m[10, 2] = (2 / 3) * (S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[10, 3] = (2 / 3) * (-S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[10, 4] = (16 / 3) * S[3, 1] / l
            K_m[10, 5] = (2 / 3) * (S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[10, 6] = (2 / 3) * (-S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[10, 7] = (16 / 3) * S[3, 2] / l
            K_m[10, 8] = (2 / 3) * (S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[10, 9] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[10, 10] = (8 / 15) * (S[1, 1] * l ** 2 + 10 * S[3, 3]) / l
            K_m[10, 11] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l + 10 * S[1, 3] - 10 * S[3, 1])) / l
            K_m[10, 12] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l - 10 * S[1, 4] - 10 * S[3, 0])) / l
            K_m[10, 13] = (8 / 15) * (-S[1, 0] * l ** 2 + 10 * S[3, 4]) / l
            K_m[10, 14] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l + 10 * S[1, 4] + 10 * S[3, 0])) / l
            K_m[10, 15] = (2 / 3) * (-S[1, 5] * l - 4 * S[3, 5]) / l
            K_m[10, 16] = (16 / 3) * S[3, 5] / l
            K_m[10, 17] = (2 / 3) * (S[1, 5] * l - 4 * S[3, 5]) / l
            K_m[11, 0] = (1 / 6) * S[1, 0] + (1 / 3) * S[3, 0] / l
            K_m[11, 1] = (2 / 3) * (-S[1, 0] * l - 4 * S[3, 0]) / l
            K_m[11, 2] = (1 / 2) * S[1, 0] + (7 / 3) * S[3, 0] / l
            K_m[11, 3] = (1 / 6) * S[1, 1] + (1 / 3) * S[3, 1] / l
            K_m[11, 4] = (2 / 3) * (-S[1, 1] * l - 4 * S[3, 1]) / l
            K_m[11, 5] = (1 / 2) * S[1, 1] + (7 / 3) * S[3, 1] / l
            K_m[11, 6] = (1 / 6) * S[1, 2] + (1 / 3) * S[3, 2] / l
            K_m[11, 7] = (2 / 3) * (-S[1, 2] * l - 4 * S[3, 2]) / l
            K_m[11, 8] = (1 / 2) * S[1, 2] + (7 / 3) * S[3, 2] / l
            K_m[11, 9] = -1 / 30 * S[1, 1] * l + (1 / 6) * S[1, 3] - 1 / 6 * S[3, 1] + (1 / 3) * S[3, 3] / l
            K_m[11, 10] = (1 / 15) * (-40 * S[3, 3] + l * (S[1, 1] * l - 10 * S[1, 3] + 10 * S[3, 1])) / l
            K_m[11, 11] = (1 / 30) * (70 * S[3, 3] + l * (4 * S[1, 1] * l + 15 * S[1, 3] + 15 * S[3, 1])) / l
            K_m[11, 12] = (1 / 30) * S[1, 0] * l + (1 / 6) * S[1, 4] + (1 / 6) * S[3, 0] + (1 / 3) * S[3, 4] / l
            K_m[11, 13] = (1 / 15) * (-40 * S[3, 4] + l * (-S[1, 0] * l - 10 * S[1, 4] - 10 * S[3, 0])) / l
            K_m[11, 14] = (1 / 30) * (70 * S[3, 4] + l * (-4 * S[1, 0] * l + 15 * S[1, 4] - 15 * S[3, 0])) / l
            K_m[11, 15] = (1 / 6) * S[1, 5] + (1 / 3) * S[3, 5] / l
            K_m[11, 16] = (2 / 3) * (-S[1, 5] * l - 4 * S[3, 5]) / l
            K_m[11, 17] = (1 / 2) * S[1, 5] + (7 / 3) * S[3, 5] / l
            K_m[12, 0] = (1 / 2) * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[12, 1] = (2 / 3) * (-S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[12, 2] = (1 / 6) * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[12, 3] = (1 / 2) * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[12, 4] = (2 / 3) * (-S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[12, 5] = (1 / 6) * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[12, 6] = (1 / 2) * S[0, 2] + (7 / 3) * S[4, 2] / l
            K_m[12, 7] = (2 / 3) * (-S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[12, 8] = (1 / 6) * S[0, 2] + (1 / 3) * S[4, 2] / l
            K_m[12, 9] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l + 15 * S[0, 3] - 15 * S[4, 1])) / l
            K_m[12, 10] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l - 10 * S[0, 3] - 10 * S[4, 1])) / l
            K_m[12, 11] = (1 / 30) * S[0, 1] * l + (1 / 6) * S[0, 3] + (1 / 6) * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[12, 12] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l + 15 * S[0, 4] + 15 * S[4, 0])) / l
            K_m[12, 13] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[12, 14] = -1 / 30 * S[0, 0] * l + (1 / 6) * S[0, 4] - 1 / 6 * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[12, 15] = (1 / 2) * S[0, 5] + (7 / 3) * S[4, 5] / l
            K_m[12, 16] = (2 / 3) * (-S[0, 5] * l - 4 * S[4, 5]) / l
            K_m[12, 17] = (1 / 6) * S[0, 5] + (1 / 3) * S[4, 5] / l
            K_m[13, 0] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[13, 1] = (16 / 3) * S[4, 0] / l
            K_m[13, 2] = (2 / 3) * (-S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[13, 3] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[13, 4] = (16 / 3) * S[4, 1] / l
            K_m[13, 5] = (2 / 3) * (-S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[13, 6] = (2 / 3) * (S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[13, 7] = (16 / 3) * S[4, 2] / l
            K_m[13, 8] = (2 / 3) * (-S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[13, 9] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[13, 10] = (8 / 15) * (-S[0, 1] * l ** 2 + 10 * S[4, 3]) / l
            K_m[13, 11] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l - 10 * S[0, 3] - 10 * S[4, 1])) / l
            K_m[13, 12] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[13, 13] = (8 / 15) * (S[0, 0] * l ** 2 + 10 * S[4, 4]) / l
            K_m[13, 14] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l - 10 * S[0, 4] + 10 * S[4, 0])) / l
            K_m[13, 15] = (2 / 3) * (S[0, 5] * l - 4 * S[4, 5]) / l
            K_m[13, 16] = (16 / 3) * S[4, 5] / l
            K_m[13, 17] = (2 / 3) * (-S[0, 5] * l - 4 * S[4, 5]) / l
            K_m[14, 0] = -1 / 6 * S[0, 0] + (1 / 3) * S[4, 0] / l
            K_m[14, 1] = (2 / 3) * (S[0, 0] * l - 4 * S[4, 0]) / l
            K_m[14, 2] = -1 / 2 * S[0, 0] + (7 / 3) * S[4, 0] / l
            K_m[14, 3] = -1 / 6 * S[0, 1] + (1 / 3) * S[4, 1] / l
            K_m[14, 4] = (2 / 3) * (S[0, 1] * l - 4 * S[4, 1]) / l
            K_m[14, 5] = -1 / 2 * S[0, 1] + (7 / 3) * S[4, 1] / l
            K_m[14, 6] = -1 / 6 * S[0, 2] + (1 / 3) * S[4, 2] / l
            K_m[14, 7] = (2 / 3) * (S[0, 2] * l - 4 * S[4, 2]) / l
            K_m[14, 8] = -1 / 2 * S[0, 2] + (7 / 3) * S[4, 2] / l
            K_m[14, 9] = (1 / 30) * S[0, 1] * l - 1 / 6 * S[0, 3] - 1 / 6 * S[4, 1] + (1 / 3) * S[4, 3] / l
            K_m[14, 10] = (1 / 15) * (-40 * S[4, 3] + l * (-S[0, 1] * l + 10 * S[0, 3] + 10 * S[4, 1])) / l
            K_m[14, 11] = (1 / 30) * (70 * S[4, 3] + l * (-4 * S[0, 1] * l - 15 * S[0, 3] + 15 * S[4, 1])) / l
            K_m[14, 12] = -1 / 30 * S[0, 0] * l - 1 / 6 * S[0, 4] + (1 / 6) * S[4, 0] + (1 / 3) * S[4, 4] / l
            K_m[14, 13] = (1 / 15) * (-40 * S[4, 4] + l * (S[0, 0] * l + 10 * S[0, 4] - 10 * S[4, 0])) / l
            K_m[14, 14] = (1 / 30) * (70 * S[4, 4] + l * (4 * S[0, 0] * l - 15 * S[0, 4] - 15 * S[4, 0])) / l
            K_m[14, 15] = -1 / 6 * S[0, 5] + (1 / 3) * S[4, 5] / l
            K_m[14, 16] = (2 / 3) * (S[0, 5] * l - 4 * S[4, 5]) / l
            K_m[14, 17] = -1 / 2 * S[0, 5] + (7 / 3) * S[4, 5] / l
            K_m[15, 0] = (7 / 3) * S[5, 0] / l
            K_m[15, 1] = -8 / 3 * S[5, 0] / l
            K_m[15, 2] = (1 / 3) * S[5, 0] / l
            K_m[15, 3] = (7 / 3) * S[5, 1] / l
            K_m[15, 4] = -8 / 3 * S[5, 1] / l
            K_m[15, 5] = (1 / 3) * S[5, 1] / l
            K_m[15, 6] = (7 / 3) * S[5, 2] / l
            K_m[15, 7] = -8 / 3 * S[5, 2] / l
            K_m[15, 8] = (1 / 3) * S[5, 2] / l
            K_m[15, 9] = -1 / 2 * S[5, 1] + (7 / 3) * S[5, 3] / l
            K_m[15, 10] = (2 / 3) * (-S[5, 1] * l - 4 * S[5, 3]) / l
            K_m[15, 11] = (1 / 6) * S[5, 1] + (1 / 3) * S[5, 3] / l
            K_m[15, 12] = (1 / 2) * S[5, 0] + (7 / 3) * S[5, 4] / l
            K_m[15, 13] = (2 / 3) * (S[5, 0] * l - 4 * S[5, 4]) / l
            K_m[15, 14] = -1 / 6 * S[5, 0] + (1 / 3) * S[5, 4] / l
            K_m[15, 15] = (7 / 3) * S[5, 5] / l
            K_m[15, 16] = -8 / 3 * S[5, 5] / l
            K_m[15, 17] = (1 / 3) * S[5, 5] / l
            K_m[16, 0] = -8 / 3 * S[5, 0] / l
            K_m[16, 1] = (16 / 3) * S[5, 0] / l
            K_m[16, 2] = -8 / 3 * S[5, 0] / l
            K_m[16, 3] = -8 / 3 * S[5, 1] / l
            K_m[16, 4] = (16 / 3) * S[5, 1] / l
            K_m[16, 5] = -8 / 3 * S[5, 1] / l
            K_m[16, 6] = -8 / 3 * S[5, 2] / l
            K_m[16, 7] = (16 / 3) * S[5, 2] / l
            K_m[16, 8] = -8 / 3 * S[5, 2] / l
            K_m[16, 9] = (2 / 3) * (S[5, 1] * l - 4 * S[5, 3]) / l
            K_m[16, 10] = (16 / 3) * S[5, 3] / l
            K_m[16, 11] = (2 / 3) * (-S[5, 1] * l - 4 * S[5, 3]) / l
            K_m[16, 12] = (2 / 3) * (-S[5, 0] * l - 4 * S[5, 4]) / l
            K_m[16, 13] = (16 / 3) * S[5, 4] / l
            K_m[16, 14] = (2 / 3) * (S[5, 0] * l - 4 * S[5, 4]) / l
            K_m[16, 15] = -8 / 3 * S[5, 5] / l
            K_m[16, 16] = (16 / 3) * S[5, 5] / l
            K_m[16, 17] = -8 / 3 * S[5, 5] / l
            K_m[17, 0] = (1 / 3) * S[5, 0] / l
            K_m[17, 1] = -8 / 3 * S[5, 0] / l
            K_m[17, 2] = (7 / 3) * S[5, 0] / l
            K_m[17, 3] = (1 / 3) * S[5, 1] / l
            K_m[17, 4] = -8 / 3 * S[5, 1] / l
            K_m[17, 5] = (7 / 3) * S[5, 1] / l
            K_m[17, 6] = (1 / 3) * S[5, 2] / l
            K_m[17, 7] = -8 / 3 * S[5, 2] / l
            K_m[17, 8] = (7 / 3) * S[5, 2] / l
            K_m[17, 9] = -1 / 6 * S[5, 1] + (1 / 3) * S[5, 3] / l
            K_m[17, 10] = (2 / 3) * (S[5, 1] * l - 4 * S[5, 3]) / l
            K_m[17, 11] = (1 / 2) * S[5, 1] + (7 / 3) * S[5, 3] / l
            K_m[17, 12] = (1 / 6) * S[5, 0] + (1 / 3) * S[5, 4] / l
            K_m[17, 13] = (2 / 3) * (-S[5, 0] * l - 4 * S[5, 4]) / l
            K_m[17, 14] = -1 / 2 * S[5, 0] + (7 / 3) * S[5, 4] / l
            K_m[17, 15] = (1 / 3) * S[5, 5] / l
            K_m[17, 16] = -8 / 3 * S[5, 5] / l
            K_m[17, 17] = (7 / 3) * S[5, 5] / l

            self._element_stiffness_matrix = K_m.tocsc()

        return self._element_stiffness_matrix

    def B_matrix(self, z):
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        B = sp.dok_array((6, 18), dtype=dtype)

        B[0, 0] = (-3 * l + 4 * z) / l ** 2
        B[0, 1] = 4 * (l - 2 * z) / l ** 2
        B[0, 2] = (-l + 4 * z) / l ** 2
        # B[0,3] = 0
        # B[0,4] = 0
        # B[0,5] = 0
        # B[0,6] = 0
        # B[0,7] = 0
        # B[0,8] = 0
        # B[0,9] = 0
        # B[0,10] = 0
        # B[0,11] = 0
        B[0, 12] = -1 + 3 * z / l - 2 * z ** 2 / l ** 2
        B[0, 13] = 4 * z * (-l + z) / l ** 2
        B[0, 14] = z * (l - 2 * z) / l ** 2
        # B[0,15] = 0
        # B[0,16] = 0
        # B[0,17] = 0
        # B[1,0] = 0
        # B[1,1] = 0
        # B[1,2] = 0
        B[1, 3] = (-3 * l + 4 * z) / l ** 2
        B[1, 4] = 4 * (l - 2 * z) / l ** 2
        B[1, 5] = (-l + 4 * z) / l ** 2
        # B[1,6] = 0
        # B[1,7] = 0
        # B[1,8] = 0
        B[1, 9] = 1 - 3 * z / l + 2 * z ** 2 / l ** 2
        B[1, 10] = 4 * z * (l - z) / l ** 2
        B[1, 11] = z * (-l + 2 * z) / l ** 2
        # B[1,12] = 0
        # B[1,13] = 0
        # B[1,14] = 0
        # B[1,15] = 0
        # B[1,16] = 0
        # B[1,17] = 0
        # B[2,0] = 0
        # B[2,1] = 0
        # B[2,2] = 0
        # B[2,3] = 0
        # B[2,4] = 0
        # B[2,5] = 0
        B[2, 6] = (-3 * l + 4 * z) / l ** 2
        B[2, 7] = 4 * (l - 2 * z) / l ** 2
        B[2, 8] = (-l + 4 * z) / l ** 2
        # B[2,9] = 0
        # B[2,10] = 0
        # B[2,11] = 0
        # B[2,12] = 0
        # B[2,13] = 0
        # B[2,14] = 0
        # B[2,15] = 0
        # B[2,16] = 0
        # B[2,17] = 0
        # B[3,0] = 0
        # B[3,1] = 0
        # B[3,2] = 0
        # B[3,3] = 0
        # B[3,4] = 0
        # B[3,5] = 0
        # B[3,6] = 0
        # B[3,7] = 0
        # B[3,8] = 0
        B[3, 9] = (-3 * l + 4 * z) / l ** 2
        B[3, 10] = 4 * (l - 2 * z) / l ** 2
        B[3, 11] = (-l + 4 * z) / l ** 2
        # B[3,12] = 0
        # B[3,13] = 0
        # B[3,14] = 0
        # B[3,15] = 0
        # B[3,16] = 0
        # B[3,17] = 0
        # B[4,0] = 0
        # B[4,1] = 0
        # B[4,2] = 0
        # B[4,3] = 0
        # B[4,4] = 0
        # B[4,5] = 0
        # B[4,6] = 0
        # B[4,7] = 0
        # B[4,8] = 0
        # B[4,9] = 0
        # B[4,10] = 0
        # B[4,11] = 0
        B[4, 12] = (-3 * l + 4 * z) / l ** 2
        B[4, 13] = 4 * (l - 2 * z) / l ** 2
        B[4, 14] = (-l + 4 * z) / l ** 2
        # B[4,15] = 0
        # B[4,16] = 0
        # B[4,17] = 0
        # B[5,0] = 0
        # B[5,1] = 0
        # B[5,2] = 0
        # B[5,3] = 0
        # B[5,4] = 0
        # B[5,5] = 0
        # B[5,6] = 0
        # B[5,7] = 0
        # B[5,8] = 0
        # B[5,9] = 0
        # B[5,10] = 0
        # B[5,11] = 0
        # B[5,12] = 0
        # B[5,13] = 0
        # B[5,14] = 0
        B[5, 15] = (-3 * l + 4 * z) / l ** 2
        B[5, 16] = 4 * (l - 2 * z) / l ** 2
        B[5, 17] = (-l + 4 * z) / l ** 2

        return B



class BeamElement4Node(AbstractBeamElement):
    """
    A element of the 1D finite elements beam model. The elements have four nodes and 24 DOF.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def num_nodes() -> int:
        return 4

    @staticmethod
    def element_dof() -> int:
        """Number of DOF per element."""
        return 24

    @staticmethod
    def dof_increment_per_element() -> int:
        """The increment of global DOF per new element."""
        return 18

    @staticmethod
    def deformation_transformation() -> bool:
        """True, if the global beam deformations have to transformed from the global to the element coordinate system."""
        return True

    @staticmethod
    def node_positions_norm() -> list[list[float]]:
        return [[0, 1/3, 2/3, 1] for i in range(6)]

    @classmethod
    def A_matrix(cls) -> sp.csc_array:
        if not hasattr(cls, '_A_matrix'):
            dtype = np.float64
            A = sp.dok_array((24, 24), dtype=dtype)

            A[0, 0] = 1.00000000000000
            A[1, 6] = 1.00000000000000
            A[2, 12] = 1.00000000000000
            A[3, 18] = 1.00000000000000
            A[4, 1] = 1.00000000000000
            A[5, 7] = 1.00000000000000
            A[6, 13] = 1.00000000000000
            A[7, 19] = 1.00000000000000
            A[8, 2] = 1.00000000000000
            A[9, 8] = 1.00000000000000
            A[10, 14] = 1.00000000000000
            A[11, 20] = 1.00000000000000
            A[12, 3] = 1.00000000000000
            A[13, 9] = 1.00000000000000
            A[14, 15] = 1.00000000000000
            A[15, 21] = 1.00000000000000
            A[16, 4] = 1.00000000000000
            A[17, 10] = 1.00000000000000
            A[18, 16] = 1.00000000000000
            A[19, 22] = 1.00000000000000
            A[20, 5] = 1.00000000000000
            A[21, 11] = 1.00000000000000
            A[22, 17] = 1.00000000000000
            A[23, 23] = 1.00000000000000

            cls._A_matrix = sp.dok_array(A, dtype=dtype).tocsc()
        return cls._A_matrix

    @property
    def element_mass_matrix(self):
        """numpy.ndarray: The FE element mass matrix."""
        if not hasattr(self, '_element_mass_matrix'):
            dtype = self._dtype
            l = self.length
            M_cs = self._cross_section_inertia_matrix
            M_m = sp.dok_array((24, 24), dtype=dtype)

            M_m[0,0] = (8/105)*M_cs[0,0]*l
            M_m[0,1] = (33/560)*M_cs[0,0]*l
            M_m[0,2] = -3/140*M_cs[0,0]*l
            M_m[0,3] = (19/1680)*M_cs[0,0]*l
            M_m[0,20] = (8/105)*M_cs[0,5]*l
            M_m[0,21] = (33/560)*M_cs[0,5]*l
            M_m[0,22] = -3/140*M_cs[0,5]*l
            M_m[0,23] = (19/1680)*M_cs[0,5]*l
            M_m[1,0] = (33/560)*M_cs[0,0]*l
            M_m[1,1] = (27/70)*M_cs[0,0]*l
            M_m[1,2] = -27/560*M_cs[0,0]*l
            M_m[1,3] = -3/140*M_cs[0,0]*l
            M_m[1,20] = (33/560)*M_cs[0,5]*l
            M_m[1,21] = (27/70)*M_cs[0,5]*l
            M_m[1,22] = -27/560*M_cs[0,5]*l
            M_m[1,23] = -3/140*M_cs[0,5]*l
            M_m[2,0] = -3/140*M_cs[0,0]*l
            M_m[2,1] = -27/560*M_cs[0,0]*l
            M_m[2,2] = (27/70)*M_cs[0,0]*l
            M_m[2,3] = (33/560)*M_cs[0,0]*l
            M_m[2,20] = -3/140*M_cs[0,5]*l
            M_m[2,21] = -27/560*M_cs[0,5]*l
            M_m[2,22] = (27/70)*M_cs[0,5]*l
            M_m[2,23] = (33/560)*M_cs[0,5]*l
            M_m[3,0] = (19/1680)*M_cs[0,0]*l
            M_m[3,1] = -3/140*M_cs[0,0]*l
            M_m[3,2] = (33/560)*M_cs[0,0]*l
            M_m[3,3] = (8/105)*M_cs[0,0]*l
            M_m[3,20] = (19/1680)*M_cs[0,5]*l
            M_m[3,21] = -3/140*M_cs[0,5]*l
            M_m[3,22] = (33/560)*M_cs[0,5]*l
            M_m[3,23] = (8/105)*M_cs[0,5]*l
            M_m[4,4] = (8/105)*M_cs[1,1]*l
            M_m[4,5] = (33/560)*M_cs[1,1]*l
            M_m[4,6] = -3/140*M_cs[1,1]*l
            M_m[4,7] = (19/1680)*M_cs[1,1]*l
            M_m[4,20] = (8/105)*M_cs[1,5]*l
            M_m[4,21] = (33/560)*M_cs[1,5]*l
            M_m[4,22] = -3/140*M_cs[1,5]*l
            M_m[4,23] = (19/1680)*M_cs[1,5]*l
            M_m[5,4] = (33/560)*M_cs[1,1]*l
            M_m[5,5] = (27/70)*M_cs[1,1]*l
            M_m[5,6] = -27/560*M_cs[1,1]*l
            M_m[5,7] = -3/140*M_cs[1,1]*l
            M_m[5,20] = (33/560)*M_cs[1,5]*l
            M_m[5,21] = (27/70)*M_cs[1,5]*l
            M_m[5,22] = -27/560*M_cs[1,5]*l
            M_m[5,23] = -3/140*M_cs[1,5]*l
            M_m[6,4] = -3/140*M_cs[1,1]*l
            M_m[6,5] = -27/560*M_cs[1,1]*l
            M_m[6,6] = (27/70)*M_cs[1,1]*l
            M_m[6,7] = (33/560)*M_cs[1,1]*l
            M_m[6,20] = -3/140*M_cs[1,5]*l
            M_m[6,21] = -27/560*M_cs[1,5]*l
            M_m[6,22] = (27/70)*M_cs[1,5]*l
            M_m[6,23] = (33/560)*M_cs[1,5]*l
            M_m[7,4] = (19/1680)*M_cs[1,1]*l
            M_m[7,5] = -3/140*M_cs[1,1]*l
            M_m[7,6] = (33/560)*M_cs[1,1]*l
            M_m[7,7] = (8/105)*M_cs[1,1]*l
            M_m[7,20] = (19/1680)*M_cs[1,5]*l
            M_m[7,21] = -3/140*M_cs[1,5]*l
            M_m[7,22] = (33/560)*M_cs[1,5]*l
            M_m[7,23] = (8/105)*M_cs[1,5]*l
            M_m[8,8] = (8/105)*M_cs[2,2]*l
            M_m[8,9] = (33/560)*M_cs[2,2]*l
            M_m[8,10] = -3/140*M_cs[2,2]*l
            M_m[8,11] = (19/1680)*M_cs[2,2]*l
            M_m[8,12] = (8/105)*M_cs[2,3]*l
            M_m[8,13] = (33/560)*M_cs[2,3]*l
            M_m[8,14] = -3/140*M_cs[2,3]*l
            M_m[8,15] = (19/1680)*M_cs[2,3]*l
            M_m[8,16] = (8/105)*M_cs[2,4]*l
            M_m[8,17] = (33/560)*M_cs[2,4]*l
            M_m[8,18] = -3/140*M_cs[2,4]*l
            M_m[8,19] = (19/1680)*M_cs[2,4]*l
            M_m[9,8] = (33/560)*M_cs[2,2]*l
            M_m[9,9] = (27/70)*M_cs[2,2]*l
            M_m[9,10] = -27/560*M_cs[2,2]*l
            M_m[9,11] = -3/140*M_cs[2,2]*l
            M_m[9,12] = (33/560)*M_cs[2,3]*l
            M_m[9,13] = (27/70)*M_cs[2,3]*l
            M_m[9,14] = -27/560*M_cs[2,3]*l
            M_m[9,15] = -3/140*M_cs[2,3]*l
            M_m[9,16] = (33/560)*M_cs[2,4]*l
            M_m[9,17] = (27/70)*M_cs[2,4]*l
            M_m[9,18] = -27/560*M_cs[2,4]*l
            M_m[9,19] = -3/140*M_cs[2,4]*l
            M_m[10,8] = -3/140*M_cs[2,2]*l
            M_m[10,9] = -27/560*M_cs[2,2]*l
            M_m[10,10] = (27/70)*M_cs[2,2]*l
            M_m[10,11] = (33/560)*M_cs[2,2]*l
            M_m[10,12] = -3/140*M_cs[2,3]*l
            M_m[10,13] = -27/560*M_cs[2,3]*l
            M_m[10,14] = (27/70)*M_cs[2,3]*l
            M_m[10,15] = (33/560)*M_cs[2,3]*l
            M_m[10,16] = -3/140*M_cs[2,4]*l
            M_m[10,17] = -27/560*M_cs[2,4]*l
            M_m[10,18] = (27/70)*M_cs[2,4]*l
            M_m[10,19] = (33/560)*M_cs[2,4]*l
            M_m[11,8] = (19/1680)*M_cs[2,2]*l
            M_m[11,9] = -3/140*M_cs[2,2]*l
            M_m[11,10] = (33/560)*M_cs[2,2]*l
            M_m[11,11] = (8/105)*M_cs[2,2]*l
            M_m[11,12] = (19/1680)*M_cs[2,3]*l
            M_m[11,13] = -3/140*M_cs[2,3]*l
            M_m[11,14] = (33/560)*M_cs[2,3]*l
            M_m[11,15] = (8/105)*M_cs[2,3]*l
            M_m[11,16] = (19/1680)*M_cs[2,4]*l
            M_m[11,17] = -3/140*M_cs[2,4]*l
            M_m[11,18] = (33/560)*M_cs[2,4]*l
            M_m[11,19] = (8/105)*M_cs[2,4]*l
            M_m[12,8] = (8/105)*M_cs[2,3]*l
            M_m[12,9] = (33/560)*M_cs[2,3]*l
            M_m[12,10] = -3/140*M_cs[2,3]*l
            M_m[12,11] = (19/1680)*M_cs[2,3]*l
            M_m[12,12] = (8/105)*M_cs[3,3]*l
            M_m[12,13] = (33/560)*M_cs[3,3]*l
            M_m[12,14] = -3/140*M_cs[3,3]*l
            M_m[12,15] = (19/1680)*M_cs[3,3]*l
            M_m[12,16] = (8/105)*M_cs[3,4]*l
            M_m[12,17] = (33/560)*M_cs[3,4]*l
            M_m[12,18] = -3/140*M_cs[3,4]*l
            M_m[12,19] = (19/1680)*M_cs[3,4]*l
            M_m[13,8] = (33/560)*M_cs[2,3]*l
            M_m[13,9] = (27/70)*M_cs[2,3]*l
            M_m[13,10] = -27/560*M_cs[2,3]*l
            M_m[13,11] = -3/140*M_cs[2,3]*l
            M_m[13,12] = (33/560)*M_cs[3,3]*l
            M_m[13,13] = (27/70)*M_cs[3,3]*l
            M_m[13,14] = -27/560*M_cs[3,3]*l
            M_m[13,15] = -3/140*M_cs[3,3]*l
            M_m[13,16] = (33/560)*M_cs[3,4]*l
            M_m[13,17] = (27/70)*M_cs[3,4]*l
            M_m[13,18] = -27/560*M_cs[3,4]*l
            M_m[13,19] = -3/140*M_cs[3,4]*l
            M_m[14,8] = -3/140*M_cs[2,3]*l
            M_m[14,9] = -27/560*M_cs[2,3]*l
            M_m[14,10] = (27/70)*M_cs[2,3]*l
            M_m[14,11] = (33/560)*M_cs[2,3]*l
            M_m[14,12] = -3/140*M_cs[3,3]*l
            M_m[14,13] = -27/560*M_cs[3,3]*l
            M_m[14,14] = (27/70)*M_cs[3,3]*l
            M_m[14,15] = (33/560)*M_cs[3,3]*l
            M_m[14,16] = -3/140*M_cs[3,4]*l
            M_m[14,17] = -27/560*M_cs[3,4]*l
            M_m[14,18] = (27/70)*M_cs[3,4]*l
            M_m[14,19] = (33/560)*M_cs[3,4]*l
            M_m[15,8] = (19/1680)*M_cs[2,3]*l
            M_m[15,9] = -3/140*M_cs[2,3]*l
            M_m[15,10] = (33/560)*M_cs[2,3]*l
            M_m[15,11] = (8/105)*M_cs[2,3]*l
            M_m[15,12] = (19/1680)*M_cs[3,3]*l
            M_m[15,13] = -3/140*M_cs[3,3]*l
            M_m[15,14] = (33/560)*M_cs[3,3]*l
            M_m[15,15] = (8/105)*M_cs[3,3]*l
            M_m[15,16] = (19/1680)*M_cs[3,4]*l
            M_m[15,17] = -3/140*M_cs[3,4]*l
            M_m[15,18] = (33/560)*M_cs[3,4]*l
            M_m[15,19] = (8/105)*M_cs[3,4]*l
            M_m[16,8] = (8/105)*M_cs[2,4]*l
            M_m[16,9] = (33/560)*M_cs[2,4]*l
            M_m[16,10] = -3/140*M_cs[2,4]*l
            M_m[16,11] = (19/1680)*M_cs[2,4]*l
            M_m[16,12] = (8/105)*M_cs[3,4]*l
            M_m[16,13] = (33/560)*M_cs[3,4]*l
            M_m[16,14] = -3/140*M_cs[3,4]*l
            M_m[16,15] = (19/1680)*M_cs[3,4]*l
            M_m[16,16] = (8/105)*M_cs[4,4]*l
            M_m[16,17] = (33/560)*M_cs[4,4]*l
            M_m[16,18] = -3/140*M_cs[4,4]*l
            M_m[16,19] = (19/1680)*M_cs[4,4]*l
            M_m[17,8] = (33/560)*M_cs[2,4]*l
            M_m[17,9] = (27/70)*M_cs[2,4]*l
            M_m[17,10] = -27/560*M_cs[2,4]*l
            M_m[17,11] = -3/140*M_cs[2,4]*l
            M_m[17,12] = (33/560)*M_cs[3,4]*l
            M_m[17,13] = (27/70)*M_cs[3,4]*l
            M_m[17,14] = -27/560*M_cs[3,4]*l
            M_m[17,15] = -3/140*M_cs[3,4]*l
            M_m[17,16] = (33/560)*M_cs[4,4]*l
            M_m[17,17] = (27/70)*M_cs[4,4]*l
            M_m[17,18] = -27/560*M_cs[4,4]*l
            M_m[17,19] = -3/140*M_cs[4,4]*l
            M_m[18,8] = -3/140*M_cs[2,4]*l
            M_m[18,9] = -27/560*M_cs[2,4]*l
            M_m[18,10] = (27/70)*M_cs[2,4]*l
            M_m[18,11] = (33/560)*M_cs[2,4]*l
            M_m[18,12] = -3/140*M_cs[3,4]*l
            M_m[18,13] = -27/560*M_cs[3,4]*l
            M_m[18,14] = (27/70)*M_cs[3,4]*l
            M_m[18,15] = (33/560)*M_cs[3,4]*l
            M_m[18,16] = -3/140*M_cs[4,4]*l
            M_m[18,17] = -27/560*M_cs[4,4]*l
            M_m[18,18] = (27/70)*M_cs[4,4]*l
            M_m[18,19] = (33/560)*M_cs[4,4]*l
            M_m[19,8] = (19/1680)*M_cs[2,4]*l
            M_m[19,9] = -3/140*M_cs[2,4]*l
            M_m[19,10] = (33/560)*M_cs[2,4]*l
            M_m[19,11] = (8/105)*M_cs[2,4]*l
            M_m[19,12] = (19/1680)*M_cs[3,4]*l
            M_m[19,13] = -3/140*M_cs[3,4]*l
            M_m[19,14] = (33/560)*M_cs[3,4]*l
            M_m[19,15] = (8/105)*M_cs[3,4]*l
            M_m[19,16] = (19/1680)*M_cs[4,4]*l
            M_m[19,17] = -3/140*M_cs[4,4]*l
            M_m[19,18] = (33/560)*M_cs[4,4]*l
            M_m[19,19] = (8/105)*M_cs[4,4]*l
            M_m[20,0] = (8/105)*M_cs[0,5]*l
            M_m[20,1] = (33/560)*M_cs[0,5]*l
            M_m[20,2] = -3/140*M_cs[0,5]*l
            M_m[20,3] = (19/1680)*M_cs[0,5]*l
            M_m[20,4] = (8/105)*M_cs[1,5]*l
            M_m[20,5] = (33/560)*M_cs[1,5]*l
            M_m[20,6] = -3/140*M_cs[1,5]*l
            M_m[20,7] = (19/1680)*M_cs[1,5]*l
            M_m[20,20] = (8/105)*M_cs[5,5]*l
            M_m[20,21] = (33/560)*M_cs[5,5]*l
            M_m[20,22] = -3/140*M_cs[5,5]*l
            M_m[20,23] = (19/1680)*M_cs[5,5]*l
            M_m[21,0] = (33/560)*M_cs[0,5]*l
            M_m[21,1] = (27/70)*M_cs[0,5]*l
            M_m[21,2] = -27/560*M_cs[0,5]*l
            M_m[21,3] = -3/140*M_cs[0,5]*l
            M_m[21,4] = (33/560)*M_cs[1,5]*l
            M_m[21,5] = (27/70)*M_cs[1,5]*l
            M_m[21,6] = -27/560*M_cs[1,5]*l
            M_m[21,7] = -3/140*M_cs[1,5]*l
            M_m[21,20] = (33/560)*M_cs[5,5]*l
            M_m[21,21] = (27/70)*M_cs[5,5]*l
            M_m[21,22] = -27/560*M_cs[5,5]*l
            M_m[21,23] = -3/140*M_cs[5,5]*l
            M_m[22,0] = -3/140*M_cs[0,5]*l
            M_m[22,1] = -27/560*M_cs[0,5]*l
            M_m[22,2] = (27/70)*M_cs[0,5]*l
            M_m[22,3] = (33/560)*M_cs[0,5]*l
            M_m[22,4] = -3/140*M_cs[1,5]*l
            M_m[22,5] = -27/560*M_cs[1,5]*l
            M_m[22,6] = (27/70)*M_cs[1,5]*l
            M_m[22,7] = (33/560)*M_cs[1,5]*l
            M_m[22,20] = -3/140*M_cs[5,5]*l
            M_m[22,21] = -27/560*M_cs[5,5]*l
            M_m[22,22] = (27/70)*M_cs[5,5]*l
            M_m[22,23] = (33/560)*M_cs[5,5]*l
            M_m[23,0] = (19/1680)*M_cs[0,5]*l
            M_m[23,1] = -3/140*M_cs[0,5]*l
            M_m[23,2] = (33/560)*M_cs[0,5]*l
            M_m[23,3] = (8/105)*M_cs[0,5]*l
            M_m[23,4] = (19/1680)*M_cs[1,5]*l
            M_m[23,5] = -3/140*M_cs[1,5]*l
            M_m[23,6] = (33/560)*M_cs[1,5]*l
            M_m[23,7] = (8/105)*M_cs[1,5]*l
            M_m[23,20] = (19/1680)*M_cs[5,5]*l
            M_m[23,21] = -3/140*M_cs[5,5]*l
            M_m[23,22] = (33/560)*M_cs[5,5]*l
            M_m[23,23] = (8/105)*M_cs[5,5]*l

            self._element_mass_matrix = M_m.tocsc()

        return self._element_mass_matrix

    @property
    def line_load_conversion_matrix(self):
        """numpy.ndarray: Matrix for the conversion of line loads at the nodes (end nodes and integration point nodes) to node loads."""
        if not hasattr(self, '_line_load_conversion_matrix'):
            dtype = self._dtype
            l = self.length
            F_L_m = sp.dok_array((24, 24), dtype=dtype)

            F_L_m[0,0] = (8/105)*l
            F_L_m[0,1] = (33/560)*l
            F_L_m[0,2] = -3/140*l
            F_L_m[0,3] = (19/1680)*l
            F_L_m[1,0] = (33/560)*l
            F_L_m[1,1] = (27/70)*l
            F_L_m[1,2] = -27/560*l
            F_L_m[1,3] = -3/140*l
            F_L_m[2,0] = -3/140*l
            F_L_m[2,1] = -27/560*l
            F_L_m[2,2] = (27/70)*l
            F_L_m[2,3] = (33/560)*l
            F_L_m[3,0] = (19/1680)*l
            F_L_m[3,1] = -3/140*l
            F_L_m[3,2] = (33/560)*l
            F_L_m[3,3] = (8/105)*l
            F_L_m[4,4] = (8/105)*l
            F_L_m[4,5] = (33/560)*l
            F_L_m[4,6] = -3/140*l
            F_L_m[4,7] = (19/1680)*l
            F_L_m[5,4] = (33/560)*l
            F_L_m[5,5] = (27/70)*l
            F_L_m[5,6] = -27/560*l
            F_L_m[5,7] = -3/140*l
            F_L_m[6,4] = -3/140*l
            F_L_m[6,5] = -27/560*l
            F_L_m[6,6] = (27/70)*l
            F_L_m[6,7] = (33/560)*l
            F_L_m[7,4] = (19/1680)*l
            F_L_m[7,5] = -3/140*l
            F_L_m[7,6] = (33/560)*l
            F_L_m[7,7] = (8/105)*l
            F_L_m[8,8] = (8/105)*l
            F_L_m[8,9] = (33/560)*l
            F_L_m[8,10] = -3/140*l
            F_L_m[8,11] = (19/1680)*l
            F_L_m[9,8] = (33/560)*l
            F_L_m[9,9] = (27/70)*l
            F_L_m[9,10] = -27/560*l
            F_L_m[9,11] = -3/140*l
            F_L_m[10,8] = -3/140*l
            F_L_m[10,9] = -27/560*l
            F_L_m[10,10] = (27/70)*l
            F_L_m[10,11] = (33/560)*l
            F_L_m[11,8] = (19/1680)*l
            F_L_m[11,9] = -3/140*l
            F_L_m[11,10] = (33/560)*l
            F_L_m[11,11] = (8/105)*l
            F_L_m[12,12] = (8/105)*l
            F_L_m[12,13] = (33/560)*l
            F_L_m[12,14] = -3/140*l
            F_L_m[12,15] = (19/1680)*l
            F_L_m[13,12] = (33/560)*l
            F_L_m[13,13] = (27/70)*l
            F_L_m[13,14] = -27/560*l
            F_L_m[13,15] = -3/140*l
            F_L_m[14,12] = -3/140*l
            F_L_m[14,13] = -27/560*l
            F_L_m[14,14] = (27/70)*l
            F_L_m[14,15] = (33/560)*l
            F_L_m[15,12] = (19/1680)*l
            F_L_m[15,13] = -3/140*l
            F_L_m[15,14] = (33/560)*l
            F_L_m[15,15] = (8/105)*l
            F_L_m[16,16] = (8/105)*l
            F_L_m[16,17] = (33/560)*l
            F_L_m[16,18] = -3/140*l
            F_L_m[16,19] = (19/1680)*l
            F_L_m[17,16] = (33/560)*l
            F_L_m[17,17] = (27/70)*l
            F_L_m[17,18] = -27/560*l
            F_L_m[17,19] = -3/140*l
            F_L_m[18,16] = -3/140*l
            F_L_m[18,17] = -27/560*l
            F_L_m[18,18] = (27/70)*l
            F_L_m[18,19] = (33/560)*l
            F_L_m[19,16] = (19/1680)*l
            F_L_m[19,17] = -3/140*l
            F_L_m[19,18] = (33/560)*l
            F_L_m[19,19] = (8/105)*l
            F_L_m[20,20] = (8/105)*l
            F_L_m[20,21] = (33/560)*l
            F_L_m[20,22] = -3/140*l
            F_L_m[20,23] = (19/1680)*l
            F_L_m[21,20] = (33/560)*l
            F_L_m[21,21] = (27/70)*l
            F_L_m[21,22] = -27/560*l
            F_L_m[21,23] = -3/140*l
            F_L_m[22,20] = -3/140*l
            F_L_m[22,21] = -27/560*l
            F_L_m[22,22] = (27/70)*l
            F_L_m[22,23] = (33/560)*l
            F_L_m[23,20] = (19/1680)*l
            F_L_m[23,21] = -3/140*l
            F_L_m[23,22] = (33/560)*l
            F_L_m[23,23] = (8/105)*l

            self._line_load_conversion_matrix = F_L_m.tocsc()

        return self._line_load_conversion_matrix

    def H_matrix(self, z):
        """
        Returns the H matrix of the element at a given z coordinate. The H matrix is used to calculate
        the beam displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The H matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        H = sp.dok_array((6, 24), dtype=dtype)

        H[0, 0] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[0, 1] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[0, 2] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[0, 3] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        H[1, 4] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[1, 5] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[1, 6] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[1, 7] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        H[2, 8] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[2, 9] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[2, 10] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[2, 11] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        H[3, 12] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[3, 13] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[3, 14] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[3, 15] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        H[4, 16] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[4, 17] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[4, 18] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[4, 19] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3
        H[5, 20] = (1 / 2) * (l - 3 * z) * (l - z) * (2 * l - 3 * z) / l ** 3
        H[5, 21] = (9 / 2) * z * (l - z) * (2 * l - 3 * z) / l ** 3
        H[5, 22] = -9 / 2 * z * (l - 3 * z) * (l - z) / l ** 3
        H[5, 23] = (1 / 2) * z * (l - 3 * z) * (2 * l - 3 * z) / l ** 3

        return H


class BeamElement4NodeWithWarping(BeamElement4Node):
    """
    A element of the 1D finite elements beam model. The elements have four nodes and 24 DOF.
    The warping part of the stiffness cross-section matrices is taken into account.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def ignore_warping() -> bool:
        return False

    @property
    def element_stiffness_matrix(self):
        """numpy.ndarray: The FE element stiffness matrix."""
        if not hasattr(self, '_element_stiffness_matrix'):
            dtype = self._dtype
            l = self.length
            S = self.cross_section_stiffness_matrix
            K_m = sp.dok_array((24, 24), dtype=dtype)

            K_m[0, 0] = (37 / 10) * S[0, 0] / l
            K_m[0, 1] = -189 / 40 * S[0, 0] / l
            K_m[0, 2] = (27 / 20) * S[0, 0] / l
            K_m[0, 3] = -13 / 40 * S[0, 0] / l
            K_m[0, 4] = (37 / 10) * S[0, 1] / l
            K_m[0, 5] = -189 / 40 * S[0, 1] / l
            K_m[0, 6] = (27 / 20) * S[0, 1] / l
            K_m[0, 7] = -13 / 40 * S[0, 1] / l
            K_m[0, 8] = (37 / 10) * S[0, 2] / l
            K_m[0, 9] = -189 / 40 * S[0, 2] / l
            K_m[0, 10] = (27 / 20) * S[0, 2] / l
            K_m[0, 11] = -13 / 40 * S[0, 2] / l
            K_m[0, 12] = -1 / 2 * S[0, 1] + (37 / 10) * S[0, 3] / l
            K_m[0, 13] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[0, 14] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[0, 15] = (1 / 80) * (-7 * S[0, 1] * l - 26 * S[0, 3]) / l
            K_m[0, 16] = (1 / 2) * S[0, 0] + (37 / 10) * S[0, 4] / l
            K_m[0, 17] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[0, 18] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[0, 19] = (1 / 80) * (7 * S[0, 0] * l - 26 * S[0, 4]) / l
            K_m[0, 20] = (1 / 40) * (148 * S[0, 5] * l - 585 * S[0, 6]) / l ** 2
            K_m[0, 21] = (9 / 40) * (-21 * S[0, 5] * l + 155 * S[0, 6]) / l ** 2
            K_m[0, 22] = (9 / 40) * (6 * S[0, 5] * l - 115 * S[0, 6]) / l ** 2
            K_m[0, 23] = (1 / 40) * (-13 * S[0, 5] * l + 225 * S[0, 6]) / l ** 2
            K_m[1, 0] = -189 / 40 * S[0, 0] / l
            K_m[1, 1] = (54 / 5) * S[0, 0] / l
            K_m[1, 2] = -297 / 40 * S[0, 0] / l
            K_m[1, 3] = (27 / 20) * S[0, 0] / l
            K_m[1, 4] = -189 / 40 * S[0, 1] / l
            K_m[1, 5] = (54 / 5) * S[0, 1] / l
            K_m[1, 6] = -297 / 40 * S[0, 1] / l
            K_m[1, 7] = (27 / 20) * S[0, 1] / l
            K_m[1, 8] = -189 / 40 * S[0, 2] / l
            K_m[1, 9] = (54 / 5) * S[0, 2] / l
            K_m[1, 10] = -297 / 40 * S[0, 2] / l
            K_m[1, 11] = (27 / 20) * S[0, 2] / l
            K_m[1, 12] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[1, 13] = (54 / 5) * S[0, 3] / l
            K_m[1, 14] = (27 / 80) * (-3 * S[0, 1] * l - 22 * S[0, 3]) / l
            K_m[1, 15] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[1, 16] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[1, 17] = (54 / 5) * S[0, 4] / l
            K_m[1, 18] = (27 / 80) * (3 * S[0, 0] * l - 22 * S[0, 4]) / l
            K_m[1, 19] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[1, 20] = (27 / 40) * (-7 * S[0, 5] * l + 15 * S[0, 6]) / l ** 2
            K_m[1, 21] = (27 / 40) * (16 * S[0, 5] * l - 45 * S[0, 6]) / l ** 2
            K_m[1, 22] = (27 / 40) * (-11 * S[0, 5] * l + 45 * S[0, 6]) / l ** 2
            K_m[1, 23] = (27 / 40) * (2 * S[0, 5] * l - 15 * S[0, 6]) / l ** 2
            K_m[2, 0] = (27 / 20) * S[0, 0] / l
            K_m[2, 1] = -297 / 40 * S[0, 0] / l
            K_m[2, 2] = (54 / 5) * S[0, 0] / l
            K_m[2, 3] = -189 / 40 * S[0, 0] / l
            K_m[2, 4] = (27 / 20) * S[0, 1] / l
            K_m[2, 5] = -297 / 40 * S[0, 1] / l
            K_m[2, 6] = (54 / 5) * S[0, 1] / l
            K_m[2, 7] = -189 / 40 * S[0, 1] / l
            K_m[2, 8] = (27 / 20) * S[0, 2] / l
            K_m[2, 9] = -297 / 40 * S[0, 2] / l
            K_m[2, 10] = (54 / 5) * S[0, 2] / l
            K_m[2, 11] = -189 / 40 * S[0, 2] / l
            K_m[2, 12] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[2, 13] = (27 / 80) * (3 * S[0, 1] * l - 22 * S[0, 3]) / l
            K_m[2, 14] = (54 / 5) * S[0, 3] / l
            K_m[2, 15] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[2, 16] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[2, 17] = (27 / 80) * (-3 * S[0, 0] * l - 22 * S[0, 4]) / l
            K_m[2, 18] = (54 / 5) * S[0, 4] / l
            K_m[2, 19] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[2, 20] = (27 / 40) * (2 * S[0, 5] * l + 15 * S[0, 6]) / l ** 2
            K_m[2, 21] = (27 / 40) * (-11 * S[0, 5] * l - 45 * S[0, 6]) / l ** 2
            K_m[2, 22] = (27 / 40) * (16 * S[0, 5] * l + 45 * S[0, 6]) / l ** 2
            K_m[2, 23] = (27 / 40) * (-7 * S[0, 5] * l - 15 * S[0, 6]) / l ** 2
            K_m[3, 0] = -13 / 40 * S[0, 0] / l
            K_m[3, 1] = (27 / 20) * S[0, 0] / l
            K_m[3, 2] = -189 / 40 * S[0, 0] / l
            K_m[3, 3] = (37 / 10) * S[0, 0] / l
            K_m[3, 4] = -13 / 40 * S[0, 1] / l
            K_m[3, 5] = (27 / 20) * S[0, 1] / l
            K_m[3, 6] = -189 / 40 * S[0, 1] / l
            K_m[3, 7] = (37 / 10) * S[0, 1] / l
            K_m[3, 8] = -13 / 40 * S[0, 2] / l
            K_m[3, 9] = (27 / 20) * S[0, 2] / l
            K_m[3, 10] = -189 / 40 * S[0, 2] / l
            K_m[3, 11] = (37 / 10) * S[0, 2] / l
            K_m[3, 12] = (1 / 80) * (7 * S[0, 1] * l - 26 * S[0, 3]) / l
            K_m[3, 13] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[3, 14] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[3, 15] = (1 / 2) * S[0, 1] + (37 / 10) * S[0, 3] / l
            K_m[3, 16] = (1 / 80) * (-7 * S[0, 0] * l - 26 * S[0, 4]) / l
            K_m[3, 17] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[3, 18] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[3, 19] = -1 / 2 * S[0, 0] + (37 / 10) * S[0, 4] / l
            K_m[3, 20] = (1 / 40) * (-13 * S[0, 5] * l - 225 * S[0, 6]) / l ** 2
            K_m[3, 21] = (9 / 40) * (6 * S[0, 5] * l + 115 * S[0, 6]) / l ** 2
            K_m[3, 22] = (9 / 40) * (-21 * S[0, 5] * l - 155 * S[0, 6]) / l ** 2
            K_m[3, 23] = (1 / 40) * (148 * S[0, 5] * l + 585 * S[0, 6]) / l ** 2
            K_m[4, 0] = (37 / 10) * S[1, 0] / l
            K_m[4, 1] = -189 / 40 * S[1, 0] / l
            K_m[4, 2] = (27 / 20) * S[1, 0] / l
            K_m[4, 3] = -13 / 40 * S[1, 0] / l
            K_m[4, 4] = (37 / 10) * S[1, 1] / l
            K_m[4, 5] = -189 / 40 * S[1, 1] / l
            K_m[4, 6] = (27 / 20) * S[1, 1] / l
            K_m[4, 7] = -13 / 40 * S[1, 1] / l
            K_m[4, 8] = (37 / 10) * S[1, 2] / l
            K_m[4, 9] = -189 / 40 * S[1, 2] / l
            K_m[4, 10] = (27 / 20) * S[1, 2] / l
            K_m[4, 11] = -13 / 40 * S[1, 2] / l
            K_m[4, 12] = -1 / 2 * S[1, 1] + (37 / 10) * S[1, 3] / l
            K_m[4, 13] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[4, 14] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[4, 15] = (1 / 80) * (-7 * S[1, 1] * l - 26 * S[1, 3]) / l
            K_m[4, 16] = (1 / 2) * S[1, 0] + (37 / 10) * S[1, 4] / l
            K_m[4, 17] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[4, 18] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[4, 19] = (1 / 80) * (7 * S[1, 0] * l - 26 * S[1, 4]) / l
            K_m[4, 20] = (1 / 40) * (148 * S[1, 5] * l - 585 * S[1, 6]) / l ** 2
            K_m[4, 21] = (9 / 40) * (-21 * S[1, 5] * l + 155 * S[1, 6]) / l ** 2
            K_m[4, 22] = (9 / 40) * (6 * S[1, 5] * l - 115 * S[1, 6]) / l ** 2
            K_m[4, 23] = (1 / 40) * (-13 * S[1, 5] * l + 225 * S[1, 6]) / l ** 2
            K_m[5, 0] = -189 / 40 * S[1, 0] / l
            K_m[5, 1] = (54 / 5) * S[1, 0] / l
            K_m[5, 2] = -297 / 40 * S[1, 0] / l
            K_m[5, 3] = (27 / 20) * S[1, 0] / l
            K_m[5, 4] = -189 / 40 * S[1, 1] / l
            K_m[5, 5] = (54 / 5) * S[1, 1] / l
            K_m[5, 6] = -297 / 40 * S[1, 1] / l
            K_m[5, 7] = (27 / 20) * S[1, 1] / l
            K_m[5, 8] = -189 / 40 * S[1, 2] / l
            K_m[5, 9] = (54 / 5) * S[1, 2] / l
            K_m[5, 10] = -297 / 40 * S[1, 2] / l
            K_m[5, 11] = (27 / 20) * S[1, 2] / l
            K_m[5, 12] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[5, 13] = (54 / 5) * S[1, 3] / l
            K_m[5, 14] = (27 / 80) * (-3 * S[1, 1] * l - 22 * S[1, 3]) / l
            K_m[5, 15] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[5, 16] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[5, 17] = (54 / 5) * S[1, 4] / l
            K_m[5, 18] = (27 / 80) * (3 * S[1, 0] * l - 22 * S[1, 4]) / l
            K_m[5, 19] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[5, 20] = (27 / 40) * (-7 * S[1, 5] * l + 15 * S[1, 6]) / l ** 2
            K_m[5, 21] = (27 / 40) * (16 * S[1, 5] * l - 45 * S[1, 6]) / l ** 2
            K_m[5, 22] = (27 / 40) * (-11 * S[1, 5] * l + 45 * S[1, 6]) / l ** 2
            K_m[5, 23] = (27 / 40) * (2 * S[1, 5] * l - 15 * S[1, 6]) / l ** 2
            K_m[6, 0] = (27 / 20) * S[1, 0] / l
            K_m[6, 1] = -297 / 40 * S[1, 0] / l
            K_m[6, 2] = (54 / 5) * S[1, 0] / l
            K_m[6, 3] = -189 / 40 * S[1, 0] / l
            K_m[6, 4] = (27 / 20) * S[1, 1] / l
            K_m[6, 5] = -297 / 40 * S[1, 1] / l
            K_m[6, 6] = (54 / 5) * S[1, 1] / l
            K_m[6, 7] = -189 / 40 * S[1, 1] / l
            K_m[6, 8] = (27 / 20) * S[1, 2] / l
            K_m[6, 9] = -297 / 40 * S[1, 2] / l
            K_m[6, 10] = (54 / 5) * S[1, 2] / l
            K_m[6, 11] = -189 / 40 * S[1, 2] / l
            K_m[6, 12] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[6, 13] = (27 / 80) * (3 * S[1, 1] * l - 22 * S[1, 3]) / l
            K_m[6, 14] = (54 / 5) * S[1, 3] / l
            K_m[6, 15] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[6, 16] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[6, 17] = (27 / 80) * (-3 * S[1, 0] * l - 22 * S[1, 4]) / l
            K_m[6, 18] = (54 / 5) * S[1, 4] / l
            K_m[6, 19] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[6, 20] = (27 / 40) * (2 * S[1, 5] * l + 15 * S[1, 6]) / l ** 2
            K_m[6, 21] = (27 / 40) * (-11 * S[1, 5] * l - 45 * S[1, 6]) / l ** 2
            K_m[6, 22] = (27 / 40) * (16 * S[1, 5] * l + 45 * S[1, 6]) / l ** 2
            K_m[6, 23] = (27 / 40) * (-7 * S[1, 5] * l - 15 * S[1, 6]) / l ** 2
            K_m[7, 0] = -13 / 40 * S[1, 0] / l
            K_m[7, 1] = (27 / 20) * S[1, 0] / l
            K_m[7, 2] = -189 / 40 * S[1, 0] / l
            K_m[7, 3] = (37 / 10) * S[1, 0] / l
            K_m[7, 4] = -13 / 40 * S[1, 1] / l
            K_m[7, 5] = (27 / 20) * S[1, 1] / l
            K_m[7, 6] = -189 / 40 * S[1, 1] / l
            K_m[7, 7] = (37 / 10) * S[1, 1] / l
            K_m[7, 8] = -13 / 40 * S[1, 2] / l
            K_m[7, 9] = (27 / 20) * S[1, 2] / l
            K_m[7, 10] = -189 / 40 * S[1, 2] / l
            K_m[7, 11] = (37 / 10) * S[1, 2] / l
            K_m[7, 12] = (1 / 80) * (7 * S[1, 1] * l - 26 * S[1, 3]) / l
            K_m[7, 13] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[7, 14] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[7, 15] = (1 / 2) * S[1, 1] + (37 / 10) * S[1, 3] / l
            K_m[7, 16] = (1 / 80) * (-7 * S[1, 0] * l - 26 * S[1, 4]) / l
            K_m[7, 17] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[7, 18] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[7, 19] = -1 / 2 * S[1, 0] + (37 / 10) * S[1, 4] / l
            K_m[7, 20] = (1 / 40) * (-13 * S[1, 5] * l - 225 * S[1, 6]) / l ** 2
            K_m[7, 21] = (9 / 40) * (6 * S[1, 5] * l + 115 * S[1, 6]) / l ** 2
            K_m[7, 22] = (9 / 40) * (-21 * S[1, 5] * l - 155 * S[1, 6]) / l ** 2
            K_m[7, 23] = (1 / 40) * (148 * S[1, 5] * l + 585 * S[1, 6]) / l ** 2
            K_m[8, 0] = (37 / 10) * S[2, 0] / l
            K_m[8, 1] = -189 / 40 * S[2, 0] / l
            K_m[8, 2] = (27 / 20) * S[2, 0] / l
            K_m[8, 3] = -13 / 40 * S[2, 0] / l
            K_m[8, 4] = (37 / 10) * S[2, 1] / l
            K_m[8, 5] = -189 / 40 * S[2, 1] / l
            K_m[8, 6] = (27 / 20) * S[2, 1] / l
            K_m[8, 7] = -13 / 40 * S[2, 1] / l
            K_m[8, 8] = (37 / 10) * S[2, 2] / l
            K_m[8, 9] = -189 / 40 * S[2, 2] / l
            K_m[8, 10] = (27 / 20) * S[2, 2] / l
            K_m[8, 11] = -13 / 40 * S[2, 2] / l
            K_m[8, 12] = -1 / 2 * S[2, 1] + (37 / 10) * S[2, 3] / l
            K_m[8, 13] = (3 / 80) * (-19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[8, 14] = (3 / 20) * (2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[8, 15] = (1 / 80) * (-7 * S[2, 1] * l - 26 * S[2, 3]) / l
            K_m[8, 16] = (1 / 2) * S[2, 0] + (37 / 10) * S[2, 4] / l
            K_m[8, 17] = (3 / 80) * (19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[8, 18] = (3 / 20) * (-2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[8, 19] = (1 / 80) * (7 * S[2, 0] * l - 26 * S[2, 4]) / l
            K_m[8, 20] = (1 / 40) * (148 * S[2, 5] * l - 585 * S[2, 6]) / l ** 2
            K_m[8, 21] = (9 / 40) * (-21 * S[2, 5] * l + 155 * S[2, 6]) / l ** 2
            K_m[8, 22] = (9 / 40) * (6 * S[2, 5] * l - 115 * S[2, 6]) / l ** 2
            K_m[8, 23] = (1 / 40) * (-13 * S[2, 5] * l + 225 * S[2, 6]) / l ** 2
            K_m[9, 0] = -189 / 40 * S[2, 0] / l
            K_m[9, 1] = (54 / 5) * S[2, 0] / l
            K_m[9, 2] = -297 / 40 * S[2, 0] / l
            K_m[9, 3] = (27 / 20) * S[2, 0] / l
            K_m[9, 4] = -189 / 40 * S[2, 1] / l
            K_m[9, 5] = (54 / 5) * S[2, 1] / l
            K_m[9, 6] = -297 / 40 * S[2, 1] / l
            K_m[9, 7] = (27 / 20) * S[2, 1] / l
            K_m[9, 8] = -189 / 40 * S[2, 2] / l
            K_m[9, 9] = (54 / 5) * S[2, 2] / l
            K_m[9, 10] = -297 / 40 * S[2, 2] / l
            K_m[9, 11] = (27 / 20) * S[2, 2] / l
            K_m[9, 12] = (3 / 80) * (19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[9, 13] = (54 / 5) * S[2, 3] / l
            K_m[9, 14] = (27 / 80) * (-3 * S[2, 1] * l - 22 * S[2, 3]) / l
            K_m[9, 15] = (3 / 20) * (2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[9, 16] = (3 / 80) * (-19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[9, 17] = (54 / 5) * S[2, 4] / l
            K_m[9, 18] = (27 / 80) * (3 * S[2, 0] * l - 22 * S[2, 4]) / l
            K_m[9, 19] = (3 / 20) * (-2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[9, 20] = (27 / 40) * (-7 * S[2, 5] * l + 15 * S[2, 6]) / l ** 2
            K_m[9, 21] = (27 / 40) * (16 * S[2, 5] * l - 45 * S[2, 6]) / l ** 2
            K_m[9, 22] = (27 / 40) * (-11 * S[2, 5] * l + 45 * S[2, 6]) / l ** 2
            K_m[9, 23] = (27 / 40) * (2 * S[2, 5] * l - 15 * S[2, 6]) / l ** 2
            K_m[10, 0] = (27 / 20) * S[2, 0] / l
            K_m[10, 1] = -297 / 40 * S[2, 0] / l
            K_m[10, 2] = (54 / 5) * S[2, 0] / l
            K_m[10, 3] = -189 / 40 * S[2, 0] / l
            K_m[10, 4] = (27 / 20) * S[2, 1] / l
            K_m[10, 5] = -297 / 40 * S[2, 1] / l
            K_m[10, 6] = (54 / 5) * S[2, 1] / l
            K_m[10, 7] = -189 / 40 * S[2, 1] / l
            K_m[10, 8] = (27 / 20) * S[2, 2] / l
            K_m[10, 9] = -297 / 40 * S[2, 2] / l
            K_m[10, 10] = (54 / 5) * S[2, 2] / l
            K_m[10, 11] = -189 / 40 * S[2, 2] / l
            K_m[10, 12] = (3 / 20) * (-2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[10, 13] = (27 / 80) * (3 * S[2, 1] * l - 22 * S[2, 3]) / l
            K_m[10, 14] = (54 / 5) * S[2, 3] / l
            K_m[10, 15] = (3 / 80) * (-19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[10, 16] = (3 / 20) * (2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[10, 17] = (27 / 80) * (-3 * S[2, 0] * l - 22 * S[2, 4]) / l
            K_m[10, 18] = (54 / 5) * S[2, 4] / l
            K_m[10, 19] = (3 / 80) * (19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[10, 20] = (27 / 40) * (2 * S[2, 5] * l + 15 * S[2, 6]) / l ** 2
            K_m[10, 21] = (27 / 40) * (-11 * S[2, 5] * l - 45 * S[2, 6]) / l ** 2
            K_m[10, 22] = (27 / 40) * (16 * S[2, 5] * l + 45 * S[2, 6]) / l ** 2
            K_m[10, 23] = (27 / 40) * (-7 * S[2, 5] * l - 15 * S[2, 6]) / l ** 2
            K_m[11, 0] = -13 / 40 * S[2, 0] / l
            K_m[11, 1] = (27 / 20) * S[2, 0] / l
            K_m[11, 2] = -189 / 40 * S[2, 0] / l
            K_m[11, 3] = (37 / 10) * S[2, 0] / l
            K_m[11, 4] = -13 / 40 * S[2, 1] / l
            K_m[11, 5] = (27 / 20) * S[2, 1] / l
            K_m[11, 6] = -189 / 40 * S[2, 1] / l
            K_m[11, 7] = (37 / 10) * S[2, 1] / l
            K_m[11, 8] = -13 / 40 * S[2, 2] / l
            K_m[11, 9] = (27 / 20) * S[2, 2] / l
            K_m[11, 10] = -189 / 40 * S[2, 2] / l
            K_m[11, 11] = (37 / 10) * S[2, 2] / l
            K_m[11, 12] = (1 / 80) * (7 * S[2, 1] * l - 26 * S[2, 3]) / l
            K_m[11, 13] = (3 / 20) * (-2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[11, 14] = (3 / 80) * (19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[11, 15] = (1 / 2) * S[2, 1] + (37 / 10) * S[2, 3] / l
            K_m[11, 16] = (1 / 80) * (-7 * S[2, 0] * l - 26 * S[2, 4]) / l
            K_m[11, 17] = (3 / 20) * (2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[11, 18] = (3 / 80) * (-19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[11, 19] = -1 / 2 * S[2, 0] + (37 / 10) * S[2, 4] / l
            K_m[11, 20] = (1 / 40) * (-13 * S[2, 5] * l - 225 * S[2, 6]) / l ** 2
            K_m[11, 21] = (9 / 40) * (6 * S[2, 5] * l + 115 * S[2, 6]) / l ** 2
            K_m[11, 22] = (9 / 40) * (-21 * S[2, 5] * l - 155 * S[2, 6]) / l ** 2
            K_m[11, 23] = (1 / 40) * (148 * S[2, 5] * l + 585 * S[2, 6]) / l ** 2
            K_m[12, 0] = -1 / 2 * S[1, 0] + (37 / 10) * S[3, 0] / l
            K_m[12, 1] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[12, 2] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[12, 3] = (1 / 80) * (7 * S[1, 0] * l - 26 * S[3, 0]) / l
            K_m[12, 4] = -1 / 2 * S[1, 1] + (37 / 10) * S[3, 1] / l
            K_m[12, 5] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[12, 6] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[12, 7] = (1 / 80) * (7 * S[1, 1] * l - 26 * S[3, 1]) / l
            K_m[12, 8] = -1 / 2 * S[1, 2] + (37 / 10) * S[3, 2] / l
            K_m[12, 9] = (3 / 80) * (19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[12, 10] = (3 / 20) * (-2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[12, 11] = (1 / 80) * (7 * S[1, 2] * l - 26 * S[3, 2]) / l
            K_m[12, 12] = (1 / 210) * (777 * S[3, 3] + l * (16 * S[1, 1] * l - 105 * S[1, 3] - 105 * S[3, 1])) / l
            K_m[12, 13] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l + 133 * S[1, 3] - 133 * S[3, 1])) / l
            K_m[12, 14] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l - 14 * S[1, 3] + 14 * S[3, 1])) / l
            K_m[12, 15] = (1 / 1680) * (-546 * S[3, 3] + l * (19 * S[1, 1] * l + 147 * S[1, 3] - 147 * S[3, 1])) / l
            K_m[12, 16] = (1 / 210) * (777 * S[3, 4] + l * (-16 * S[1, 0] * l - 105 * S[1, 4] + 105 * S[3, 0])) / l
            K_m[12, 17] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l + 133 * S[1, 4] + 133 * S[3, 0])) / l
            K_m[12, 18] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l - 14 * S[1, 4] - 14 * S[3, 0])) / l
            K_m[12, 19] = (1 / 1680) * (-546 * S[3, 4] + l * (-19 * S[1, 0] * l + 147 * S[1, 4] + 147 * S[3, 0])) / l
            K_m[12, 20] = (1 / 40) * (
                        -20 * S[1, 5] * l ** 2 - 585 * S[3, 6] + 4 * l * (18 * S[1, 6] + 37 * S[3, 5])) / l ** 2
            K_m[12, 21] = (3 / 80) * (
                        19 * S[1, 5] * l ** 2 - 114 * S[1, 6] * l - 126 * S[3, 5] * l + 930 * S[3, 6]) / l ** 2
            K_m[12, 22] = (3 / 40) * (
                        -4 * S[1, 5] * l ** 2 - 345 * S[3, 6] + 6 * l * (7 * S[1, 6] + 3 * S[3, 5])) / l ** 2
            K_m[12, 23] = (1 / 80) * (
                        7 * S[1, 5] * l ** 2 - 54 * S[1, 6] * l - 26 * S[3, 5] * l + 450 * S[3, 6]) / l ** 2
            K_m[13, 0] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[13, 1] = (54 / 5) * S[3, 0] / l
            K_m[13, 2] = (27 / 80) * (3 * S[1, 0] * l - 22 * S[3, 0]) / l
            K_m[13, 3] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[13, 4] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[13, 5] = (54 / 5) * S[3, 1] / l
            K_m[13, 6] = (27 / 80) * (3 * S[1, 1] * l - 22 * S[3, 1]) / l
            K_m[13, 7] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[13, 8] = (3 / 80) * (-19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[13, 9] = (54 / 5) * S[3, 2] / l
            K_m[13, 10] = (27 / 80) * (3 * S[1, 2] * l - 22 * S[3, 2]) / l
            K_m[13, 11] = (3 / 20) * (-2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[13, 12] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l - 133 * S[1, 3] + 133 * S[3, 1])) / l
            K_m[13, 13] = (27 / 70) * (S[1, 1] * l ** 2 + 28 * S[3, 3]) / l
            K_m[13, 14] = (27 / 560) * (-154 * S[3, 3] + l * (-S[1, 1] * l + 21 * S[1, 3] - 21 * S[3, 1])) / l
            K_m[13, 15] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l - 14 * S[1, 3] + 14 * S[3, 1])) / l
            K_m[13, 16] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l - 133 * S[1, 4] - 133 * S[3, 0])) / l
            K_m[13, 17] = (27 / 70) * (-S[1, 0] * l ** 2 + 28 * S[3, 4]) / l
            K_m[13, 18] = (27 / 560) * (-154 * S[3, 4] + l * (S[1, 0] * l + 21 * S[1, 4] + 21 * S[3, 0])) / l
            K_m[13, 19] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l - 14 * S[1, 4] - 14 * S[3, 0])) / l
            K_m[13, 20] = (3 / 80) * (-19 * S[1, 5] * l ** 2 + 270 * S[3, 6] + 126 * l * (S[1, 6] - S[3, 5])) / l ** 2
            K_m[13, 21] = (27 / 40) * (-45 * S[3, 6] + 16 * l * (-S[1, 6] + S[3, 5])) / l ** 2
            K_m[13, 22] = (27 / 80) * (3 * S[1, 5] * l ** 2 + 90 * S[3, 6] + 22 * l * (S[1, 6] - S[3, 5])) / l ** 2
            K_m[13, 23] = (3 / 40) * (-4 * S[1, 5] * l ** 2 - 135 * S[3, 6] + 18 * l * (-S[1, 6] + S[3, 5])) / l ** 2
            K_m[14, 0] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[14, 1] = (27 / 80) * (-3 * S[1, 0] * l - 22 * S[3, 0]) / l
            K_m[14, 2] = (54 / 5) * S[3, 0] / l
            K_m[14, 3] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[14, 4] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[14, 5] = (27 / 80) * (-3 * S[1, 1] * l - 22 * S[3, 1]) / l
            K_m[14, 6] = (54 / 5) * S[3, 1] / l
            K_m[14, 7] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[14, 8] = (3 / 20) * (2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[14, 9] = (27 / 80) * (-3 * S[1, 2] * l - 22 * S[3, 2]) / l
            K_m[14, 10] = (54 / 5) * S[3, 2] / l
            K_m[14, 11] = (3 / 80) * (19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[14, 12] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l + 14 * S[1, 3] - 14 * S[3, 1])) / l
            K_m[14, 13] = (27 / 560) * (-154 * S[3, 3] + l * (-S[1, 1] * l - 21 * S[1, 3] + 21 * S[3, 1])) / l
            K_m[14, 14] = (27 / 70) * (S[1, 1] * l ** 2 + 28 * S[3, 3]) / l
            K_m[14, 15] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l + 133 * S[1, 3] - 133 * S[3, 1])) / l
            K_m[14, 16] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l + 14 * S[1, 4] + 14 * S[3, 0])) / l
            K_m[14, 17] = (27 / 560) * (-154 * S[3, 4] + l * (S[1, 0] * l - 21 * S[1, 4] - 21 * S[3, 0])) / l
            K_m[14, 18] = (27 / 70) * (-S[1, 0] * l ** 2 + 28 * S[3, 4]) / l
            K_m[14, 19] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l + 133 * S[1, 4] + 133 * S[3, 0])) / l
            K_m[14, 20] = (3 / 40) * (4 * S[1, 5] * l ** 2 + 135 * S[3, 6] + 18 * l * (-S[1, 6] + S[3, 5])) / l ** 2
            K_m[14, 21] = (27 / 80) * (-3 * S[1, 5] * l ** 2 - 90 * S[3, 6] + 22 * l * (S[1, 6] - S[3, 5])) / l ** 2
            K_m[14, 22] = (27 / 40) * (45 * S[3, 6] + 16 * l * (-S[1, 6] + S[3, 5])) / l ** 2
            K_m[14, 23] = (3 / 80) * (19 * S[1, 5] * l ** 2 - 270 * S[3, 6] + 126 * l * (S[1, 6] - S[3, 5])) / l ** 2
            K_m[15, 0] = (1 / 80) * (-7 * S[1, 0] * l - 26 * S[3, 0]) / l
            K_m[15, 1] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[15, 2] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[15, 3] = (1 / 2) * S[1, 0] + (37 / 10) * S[3, 0] / l
            K_m[15, 4] = (1 / 80) * (-7 * S[1, 1] * l - 26 * S[3, 1]) / l
            K_m[15, 5] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[15, 6] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[15, 7] = (1 / 2) * S[1, 1] + (37 / 10) * S[3, 1] / l
            K_m[15, 8] = (1 / 80) * (-7 * S[1, 2] * l - 26 * S[3, 2]) / l
            K_m[15, 9] = (3 / 20) * (2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[15, 10] = (3 / 80) * (-19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[15, 11] = (1 / 2) * S[1, 2] + (37 / 10) * S[3, 2] / l
            K_m[15, 12] = (1 / 1680) * (-546 * S[3, 3] + l * (19 * S[1, 1] * l - 147 * S[1, 3] + 147 * S[3, 1])) / l
            K_m[15, 13] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l + 14 * S[1, 3] - 14 * S[3, 1])) / l
            K_m[15, 14] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l - 133 * S[1, 3] + 133 * S[3, 1])) / l
            K_m[15, 15] = (1 / 210) * (777 * S[3, 3] + l * (16 * S[1, 1] * l + 105 * S[1, 3] + 105 * S[3, 1])) / l
            K_m[15, 16] = (1 / 1680) * (-546 * S[3, 4] + l * (-19 * S[1, 0] * l - 147 * S[1, 4] - 147 * S[3, 0])) / l
            K_m[15, 17] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l + 14 * S[1, 4] + 14 * S[3, 0])) / l
            K_m[15, 18] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l - 133 * S[1, 4] - 133 * S[3, 0])) / l
            K_m[15, 19] = (1 / 210) * (777 * S[3, 4] + l * (-16 * S[1, 0] * l + 105 * S[1, 4] - 105 * S[3, 0])) / l
            K_m[15, 20] = (1 / 80) * (
                        -7 * S[1, 5] * l ** 2 - 450 * S[3, 6] + 2 * l * (-27 * S[1, 6] - 13 * S[3, 5])) / l ** 2
            K_m[15, 21] = (3 / 40) * (
                        4 * S[1, 5] * l ** 2 + 345 * S[3, 6] + 6 * l * (7 * S[1, 6] + 3 * S[3, 5])) / l ** 2
            K_m[15, 22] = (3 / 80) * (
                        -19 * S[1, 5] * l ** 2 - 930 * S[3, 6] + 6 * l * (-19 * S[1, 6] - 21 * S[3, 5])) / l ** 2
            K_m[15, 23] = (1 / 40) * (
                        20 * S[1, 5] * l ** 2 + 585 * S[3, 6] + 4 * l * (18 * S[1, 6] + 37 * S[3, 5])) / l ** 2
            K_m[16, 0] = (1 / 2) * S[0, 0] + (37 / 10) * S[4, 0] / l
            K_m[16, 1] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[16, 2] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[16, 3] = (1 / 80) * (-7 * S[0, 0] * l - 26 * S[4, 0]) / l
            K_m[16, 4] = (1 / 2) * S[0, 1] + (37 / 10) * S[4, 1] / l
            K_m[16, 5] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[16, 6] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[16, 7] = (1 / 80) * (-7 * S[0, 1] * l - 26 * S[4, 1]) / l
            K_m[16, 8] = (1 / 2) * S[0, 2] + (37 / 10) * S[4, 2] / l
            K_m[16, 9] = (3 / 80) * (-19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[16, 10] = (3 / 20) * (2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[16, 11] = (1 / 80) * (-7 * S[0, 2] * l - 26 * S[4, 2]) / l
            K_m[16, 12] = (1 / 210) * (777 * S[4, 3] + l * (-16 * S[0, 1] * l + 105 * S[0, 3] - 105 * S[4, 1])) / l
            K_m[16, 13] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l - 133 * S[0, 3] - 133 * S[4, 1])) / l
            K_m[16, 14] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l + 14 * S[0, 3] + 14 * S[4, 1])) / l
            K_m[16, 15] = (1 / 1680) * (-546 * S[4, 3] + l * (-19 * S[0, 1] * l - 147 * S[0, 3] - 147 * S[4, 1])) / l
            K_m[16, 16] = (1 / 210) * (777 * S[4, 4] + l * (16 * S[0, 0] * l + 105 * S[0, 4] + 105 * S[4, 0])) / l
            K_m[16, 17] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l - 133 * S[0, 4] + 133 * S[4, 0])) / l
            K_m[16, 18] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l + 14 * S[0, 4] - 14 * S[4, 0])) / l
            K_m[16, 19] = (1 / 1680) * (-546 * S[4, 4] + l * (19 * S[0, 0] * l - 147 * S[0, 4] + 147 * S[4, 0])) / l
            K_m[16, 20] = (1 / 40) * (
                        20 * S[0, 5] * l ** 2 - 585 * S[4, 6] + 4 * l * (-18 * S[0, 6] + 37 * S[4, 5])) / l ** 2
            K_m[16, 21] = (3 / 80) * (
                        -19 * S[0, 5] * l ** 2 + 930 * S[4, 6] + 6 * l * (19 * S[0, 6] - 21 * S[4, 5])) / l ** 2
            K_m[16, 22] = (3 / 40) * (
                        4 * S[0, 5] * l ** 2 - 345 * S[4, 6] + 6 * l * (-7 * S[0, 6] + 3 * S[4, 5])) / l ** 2
            K_m[16, 23] = (1 / 80) * (
                        -7 * S[0, 5] * l ** 2 + 450 * S[4, 6] + 2 * l * (27 * S[0, 6] - 13 * S[4, 5])) / l ** 2
            K_m[17, 0] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[17, 1] = (54 / 5) * S[4, 0] / l
            K_m[17, 2] = (27 / 80) * (-3 * S[0, 0] * l - 22 * S[4, 0]) / l
            K_m[17, 3] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[17, 4] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[17, 5] = (54 / 5) * S[4, 1] / l
            K_m[17, 6] = (27 / 80) * (-3 * S[0, 1] * l - 22 * S[4, 1]) / l
            K_m[17, 7] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[17, 8] = (3 / 80) * (19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[17, 9] = (54 / 5) * S[4, 2] / l
            K_m[17, 10] = (27 / 80) * (-3 * S[0, 2] * l - 22 * S[4, 2]) / l
            K_m[17, 11] = (3 / 20) * (2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[17, 12] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l + 133 * S[0, 3] + 133 * S[4, 1])) / l
            K_m[17, 13] = (27 / 70) * (-S[0, 1] * l ** 2 + 28 * S[4, 3]) / l
            K_m[17, 14] = (27 / 560) * (-154 * S[4, 3] + l * (S[0, 1] * l - 21 * S[0, 3] - 21 * S[4, 1])) / l
            K_m[17, 15] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l + 14 * S[0, 3] + 14 * S[4, 1])) / l
            K_m[17, 16] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l + 133 * S[0, 4] - 133 * S[4, 0])) / l
            K_m[17, 17] = (27 / 70) * (S[0, 0] * l ** 2 + 28 * S[4, 4]) / l
            K_m[17, 18] = (27 / 560) * (-154 * S[4, 4] + l * (-S[0, 0] * l - 21 * S[0, 4] + 21 * S[4, 0])) / l
            K_m[17, 19] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l + 14 * S[0, 4] - 14 * S[4, 0])) / l
            K_m[17, 20] = (3 / 80) * (19 * S[0, 5] * l ** 2 + 270 * S[4, 6] - 126 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[17, 21] = (27 / 40) * (-45 * S[4, 6] + 16 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[17, 22] = (27 / 80) * (-3 * S[0, 5] * l ** 2 + 90 * S[4, 6] - 22 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[17, 23] = (3 / 40) * (4 * S[0, 5] * l ** 2 - 135 * S[4, 6] + 18 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[18, 0] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[18, 1] = (27 / 80) * (3 * S[0, 0] * l - 22 * S[4, 0]) / l
            K_m[18, 2] = (54 / 5) * S[4, 0] / l
            K_m[18, 3] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[18, 4] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[18, 5] = (27 / 80) * (3 * S[0, 1] * l - 22 * S[4, 1]) / l
            K_m[18, 6] = (54 / 5) * S[4, 1] / l
            K_m[18, 7] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[18, 8] = (3 / 20) * (-2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[18, 9] = (27 / 80) * (3 * S[0, 2] * l - 22 * S[4, 2]) / l
            K_m[18, 10] = (54 / 5) * S[4, 2] / l
            K_m[18, 11] = (3 / 80) * (-19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[18, 12] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l - 14 * S[0, 3] - 14 * S[4, 1])) / l
            K_m[18, 13] = (27 / 560) * (-154 * S[4, 3] + l * (S[0, 1] * l + 21 * S[0, 3] + 21 * S[4, 1])) / l
            K_m[18, 14] = (27 / 70) * (-S[0, 1] * l ** 2 + 28 * S[4, 3]) / l
            K_m[18, 15] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l - 133 * S[0, 3] - 133 * S[4, 1])) / l
            K_m[18, 16] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l - 14 * S[0, 4] + 14 * S[4, 0])) / l
            K_m[18, 17] = (27 / 560) * (-154 * S[4, 4] + l * (-S[0, 0] * l + 21 * S[0, 4] - 21 * S[4, 0])) / l
            K_m[18, 18] = (27 / 70) * (S[0, 0] * l ** 2 + 28 * S[4, 4]) / l
            K_m[18, 19] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l - 133 * S[0, 4] + 133 * S[4, 0])) / l
            K_m[18, 20] = (3 / 40) * (-4 * S[0, 5] * l ** 2 + 135 * S[4, 6] + 18 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[18, 21] = (27 / 80) * (3 * S[0, 5] * l ** 2 - 90 * S[4, 6] - 22 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[18, 22] = (27 / 40) * (45 * S[4, 6] + 16 * l * (S[0, 6] + S[4, 5])) / l ** 2
            K_m[18, 23] = (3 / 80) * (-19 * S[0, 5] * l ** 2 - 270 * S[4, 6] + 126 * l * (-S[0, 6] - S[4, 5])) / l ** 2
            K_m[19, 0] = (1 / 80) * (7 * S[0, 0] * l - 26 * S[4, 0]) / l
            K_m[19, 1] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[19, 2] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[19, 3] = -1 / 2 * S[0, 0] + (37 / 10) * S[4, 0] / l
            K_m[19, 4] = (1 / 80) * (7 * S[0, 1] * l - 26 * S[4, 1]) / l
            K_m[19, 5] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[19, 6] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[19, 7] = -1 / 2 * S[0, 1] + (37 / 10) * S[4, 1] / l
            K_m[19, 8] = (1 / 80) * (7 * S[0, 2] * l - 26 * S[4, 2]) / l
            K_m[19, 9] = (3 / 20) * (-2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[19, 10] = (3 / 80) * (19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[19, 11] = -1 / 2 * S[0, 2] + (37 / 10) * S[4, 2] / l
            K_m[19, 12] = (1 / 1680) * (-546 * S[4, 3] + l * (-19 * S[0, 1] * l + 147 * S[0, 3] + 147 * S[4, 1])) / l
            K_m[19, 13] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l - 14 * S[0, 3] - 14 * S[4, 1])) / l
            K_m[19, 14] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l + 133 * S[0, 3] + 133 * S[4, 1])) / l
            K_m[19, 15] = (1 / 210) * (777 * S[4, 3] + l * (-16 * S[0, 1] * l - 105 * S[0, 3] + 105 * S[4, 1])) / l
            K_m[19, 16] = (1 / 1680) * (-546 * S[4, 4] + l * (19 * S[0, 0] * l + 147 * S[0, 4] - 147 * S[4, 0])) / l
            K_m[19, 17] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l - 14 * S[0, 4] + 14 * S[4, 0])) / l
            K_m[19, 18] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l + 133 * S[0, 4] - 133 * S[4, 0])) / l
            K_m[19, 19] = (1 / 210) * (777 * S[4, 4] + l * (16 * S[0, 0] * l - 105 * S[0, 4] - 105 * S[4, 0])) / l
            K_m[19, 20] = (1 / 80) * (
                        7 * S[0, 5] * l ** 2 - 450 * S[4, 6] + 2 * l * (27 * S[0, 6] - 13 * S[4, 5])) / l ** 2
            K_m[19, 21] = (3 / 40) * (
                        -4 * S[0, 5] * l ** 2 + 345 * S[4, 6] + 6 * l * (-7 * S[0, 6] + 3 * S[4, 5])) / l ** 2
            K_m[19, 22] = (3 / 80) * (
                        19 * S[0, 5] * l ** 2 - 930 * S[4, 6] + 6 * l * (19 * S[0, 6] - 21 * S[4, 5])) / l ** 2
            K_m[19, 23] = (1 / 40) * (
                        -20 * S[0, 5] * l ** 2 + 585 * S[4, 6] + 4 * l * (-18 * S[0, 6] + 37 * S[4, 5])) / l ** 2
            K_m[20, 0] = (1 / 40) * (148 * S[5, 0] * l - 585 * S[6, 0]) / l ** 2
            K_m[20, 1] = (27 / 40) * (-7 * S[5, 0] * l + 15 * S[6, 0]) / l ** 2
            K_m[20, 2] = (27 / 40) * (2 * S[5, 0] * l + 15 * S[6, 0]) / l ** 2
            K_m[20, 3] = (1 / 40) * (-13 * S[5, 0] * l - 225 * S[6, 0]) / l ** 2
            K_m[20, 4] = (1 / 40) * (148 * S[5, 1] * l - 585 * S[6, 1]) / l ** 2
            K_m[20, 5] = (27 / 40) * (-7 * S[5, 1] * l + 15 * S[6, 1]) / l ** 2
            K_m[20, 6] = (27 / 40) * (2 * S[5, 1] * l + 15 * S[6, 1]) / l ** 2
            K_m[20, 7] = (1 / 40) * (-13 * S[5, 1] * l - 225 * S[6, 1]) / l ** 2
            K_m[20, 8] = (1 / 40) * (148 * S[5, 2] * l - 585 * S[6, 2]) / l ** 2
            K_m[20, 9] = (27 / 40) * (-7 * S[5, 2] * l + 15 * S[6, 2]) / l ** 2
            K_m[20, 10] = (27 / 40) * (2 * S[5, 2] * l + 15 * S[6, 2]) / l ** 2
            K_m[20, 11] = (1 / 40) * (-13 * S[5, 2] * l - 225 * S[6, 2]) / l ** 2
            K_m[20, 12] = (1 / 40) * (
                        -20 * S[5, 1] * l ** 2 - 585 * S[6, 3] + 4 * l * (37 * S[5, 3] + 18 * S[6, 1])) / l ** 2
            K_m[20, 13] = (3 / 80) * (-19 * S[5, 1] * l ** 2 + 270 * S[6, 3] + 126 * l * (-S[5, 3] + S[6, 1])) / l ** 2
            K_m[20, 14] = (3 / 40) * (4 * S[5, 1] * l ** 2 + 135 * S[6, 3] + 18 * l * (S[5, 3] - S[6, 1])) / l ** 2
            K_m[20, 15] = (1 / 80) * (
                        -7 * S[5, 1] * l ** 2 - 450 * S[6, 3] + 2 * l * (-13 * S[5, 3] - 27 * S[6, 1])) / l ** 2
            K_m[20, 16] = (1 / 40) * (
                        20 * S[5, 0] * l ** 2 - 585 * S[6, 4] + 4 * l * (37 * S[5, 4] - 18 * S[6, 0])) / l ** 2
            K_m[20, 17] = (3 / 80) * (19 * S[5, 0] * l ** 2 + 270 * S[6, 4] - 126 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[20, 18] = (3 / 40) * (-4 * S[5, 0] * l ** 2 + 135 * S[6, 4] + 18 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[20, 19] = (1 / 80) * (
                        7 * S[5, 0] * l ** 2 - 450 * S[6, 4] + 2 * l * (-13 * S[5, 4] + 27 * S[6, 0])) / l ** 2
            K_m[20, 20] = (1 / 40) * (148 * S[5, 5] * l ** 2 + 3240 * S[6, 6] - 585 * l * (S[5, 6] + S[6, 5])) / l ** 3
            K_m[20, 21] = (9 / 40) * (
                        -21 * S[5, 5] * l ** 2 - 900 * S[6, 6] + 5 * l * (31 * S[5, 6] + 9 * S[6, 5])) / l ** 3
            K_m[20, 22] = (9 / 40) * (
                        6 * S[5, 5] * l ** 2 + 720 * S[6, 6] + 5 * l * (-23 * S[5, 6] + 9 * S[6, 5])) / l ** 3
            K_m[20, 23] = (1 / 40) * (-13 * S[5, 5] * l ** 2 - 1620 * S[6, 6] + 225 * l * (S[5, 6] - S[6, 5])) / l ** 3
            K_m[21, 0] = (9 / 40) * (-21 * S[5, 0] * l + 155 * S[6, 0]) / l ** 2
            K_m[21, 1] = (27 / 40) * (16 * S[5, 0] * l - 45 * S[6, 0]) / l ** 2
            K_m[21, 2] = (27 / 40) * (-11 * S[5, 0] * l - 45 * S[6, 0]) / l ** 2
            K_m[21, 3] = (9 / 40) * (6 * S[5, 0] * l + 115 * S[6, 0]) / l ** 2
            K_m[21, 4] = (9 / 40) * (-21 * S[5, 1] * l + 155 * S[6, 1]) / l ** 2
            K_m[21, 5] = (27 / 40) * (16 * S[5, 1] * l - 45 * S[6, 1]) / l ** 2
            K_m[21, 6] = (27 / 40) * (-11 * S[5, 1] * l - 45 * S[6, 1]) / l ** 2
            K_m[21, 7] = (9 / 40) * (6 * S[5, 1] * l + 115 * S[6, 1]) / l ** 2
            K_m[21, 8] = (9 / 40) * (-21 * S[5, 2] * l + 155 * S[6, 2]) / l ** 2
            K_m[21, 9] = (27 / 40) * (16 * S[5, 2] * l - 45 * S[6, 2]) / l ** 2
            K_m[21, 10] = (27 / 40) * (-11 * S[5, 2] * l - 45 * S[6, 2]) / l ** 2
            K_m[21, 11] = (9 / 40) * (6 * S[5, 2] * l + 115 * S[6, 2]) / l ** 2
            K_m[21, 12] = (3 / 80) * (
                        19 * S[5, 1] * l ** 2 - 126 * S[5, 3] * l - 114 * S[6, 1] * l + 930 * S[6, 3]) / l ** 2
            K_m[21, 13] = (27 / 40) * (-45 * S[6, 3] + 16 * l * (S[5, 3] - S[6, 1])) / l ** 2
            K_m[21, 14] = (27 / 80) * (-3 * S[5, 1] * l ** 2 - 90 * S[6, 3] + 22 * l * (-S[5, 3] + S[6, 1])) / l ** 2
            K_m[21, 15] = (3 / 40) * (
                        4 * S[5, 1] * l ** 2 + 345 * S[6, 3] + 6 * l * (3 * S[5, 3] + 7 * S[6, 1])) / l ** 2
            K_m[21, 16] = (3 / 80) * (
                        -19 * S[5, 0] * l ** 2 + 930 * S[6, 4] + 6 * l * (-21 * S[5, 4] + 19 * S[6, 0])) / l ** 2
            K_m[21, 17] = (27 / 40) * (-45 * S[6, 4] + 16 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[21, 18] = (27 / 80) * (3 * S[5, 0] * l ** 2 - 90 * S[6, 4] - 22 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[21, 19] = (3 / 40) * (
                        -4 * S[5, 0] * l ** 2 + 345 * S[6, 4] + 6 * l * (3 * S[5, 4] - 7 * S[6, 0])) / l ** 2
            K_m[21, 20] = (9 / 40) * (
                        -21 * S[5, 5] * l ** 2 - 900 * S[6, 6] + 5 * l * (9 * S[5, 6] + 31 * S[6, 5])) / l ** 3
            K_m[21, 21] = (27 / 40) * (16 * S[5, 5] * l ** 2 + 840 * S[6, 6] - 45 * l * (S[5, 6] + S[6, 5])) / l ** 3
            K_m[21, 22] = (27 / 40) * (-11 * S[5, 5] * l ** 2 - 780 * S[6, 6] + 45 * l * (S[5, 6] - S[6, 5])) / l ** 3
            K_m[21, 23] = (9 / 40) * (
                        6 * S[5, 5] * l ** 2 + 720 * S[6, 6] + 5 * l * (-9 * S[5, 6] + 23 * S[6, 5])) / l ** 3
            K_m[22, 0] = (9 / 40) * (6 * S[5, 0] * l - 115 * S[6, 0]) / l ** 2
            K_m[22, 1] = (27 / 40) * (-11 * S[5, 0] * l + 45 * S[6, 0]) / l ** 2
            K_m[22, 2] = (27 / 40) * (16 * S[5, 0] * l + 45 * S[6, 0]) / l ** 2
            K_m[22, 3] = (9 / 40) * (-21 * S[5, 0] * l - 155 * S[6, 0]) / l ** 2
            K_m[22, 4] = (9 / 40) * (6 * S[5, 1] * l - 115 * S[6, 1]) / l ** 2
            K_m[22, 5] = (27 / 40) * (-11 * S[5, 1] * l + 45 * S[6, 1]) / l ** 2
            K_m[22, 6] = (27 / 40) * (16 * S[5, 1] * l + 45 * S[6, 1]) / l ** 2
            K_m[22, 7] = (9 / 40) * (-21 * S[5, 1] * l - 155 * S[6, 1]) / l ** 2
            K_m[22, 8] = (9 / 40) * (6 * S[5, 2] * l - 115 * S[6, 2]) / l ** 2
            K_m[22, 9] = (27 / 40) * (-11 * S[5, 2] * l + 45 * S[6, 2]) / l ** 2
            K_m[22, 10] = (27 / 40) * (16 * S[5, 2] * l + 45 * S[6, 2]) / l ** 2
            K_m[22, 11] = (9 / 40) * (-21 * S[5, 2] * l - 155 * S[6, 2]) / l ** 2
            K_m[22, 12] = (3 / 40) * (
                        -4 * S[5, 1] * l ** 2 - 345 * S[6, 3] + 6 * l * (3 * S[5, 3] + 7 * S[6, 1])) / l ** 2
            K_m[22, 13] = (27 / 80) * (3 * S[5, 1] * l ** 2 + 90 * S[6, 3] + 22 * l * (-S[5, 3] + S[6, 1])) / l ** 2
            K_m[22, 14] = (27 / 40) * (45 * S[6, 3] + 16 * l * (S[5, 3] - S[6, 1])) / l ** 2
            K_m[22, 15] = (3 / 80) * (
                        -19 * S[5, 1] * l ** 2 - 930 * S[6, 3] + 6 * l * (-21 * S[5, 3] - 19 * S[6, 1])) / l ** 2
            K_m[22, 16] = (3 / 40) * (
                        4 * S[5, 0] * l ** 2 - 345 * S[6, 4] + 6 * l * (3 * S[5, 4] - 7 * S[6, 0])) / l ** 2
            K_m[22, 17] = (27 / 80) * (-3 * S[5, 0] * l ** 2 + 90 * S[6, 4] - 22 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[22, 18] = (27 / 40) * (45 * S[6, 4] + 16 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[22, 19] = (3 / 80) * (
                        19 * S[5, 0] * l ** 2 - 930 * S[6, 4] + 6 * l * (-21 * S[5, 4] + 19 * S[6, 0])) / l ** 2
            K_m[22, 20] = (9 / 40) * (
                        6 * S[5, 5] * l ** 2 + 720 * S[6, 6] + 5 * l * (9 * S[5, 6] - 23 * S[6, 5])) / l ** 3
            K_m[22, 21] = (27 / 40) * (-11 * S[5, 5] * l ** 2 - 780 * S[6, 6] + 45 * l * (-S[5, 6] + S[6, 5])) / l ** 3
            K_m[22, 22] = (27 / 40) * (16 * S[5, 5] * l ** 2 + 840 * S[6, 6] + 45 * l * (S[5, 6] + S[6, 5])) / l ** 3
            K_m[22, 23] = (9 / 40) * (
                        -21 * S[5, 5] * l ** 2 - 900 * S[6, 6] + 5 * l * (-9 * S[5, 6] - 31 * S[6, 5])) / l ** 3
            K_m[23, 0] = (1 / 40) * (-13 * S[5, 0] * l + 225 * S[6, 0]) / l ** 2
            K_m[23, 1] = (27 / 40) * (2 * S[5, 0] * l - 15 * S[6, 0]) / l ** 2
            K_m[23, 2] = (27 / 40) * (-7 * S[5, 0] * l - 15 * S[6, 0]) / l ** 2
            K_m[23, 3] = (1 / 40) * (148 * S[5, 0] * l + 585 * S[6, 0]) / l ** 2
            K_m[23, 4] = (1 / 40) * (-13 * S[5, 1] * l + 225 * S[6, 1]) / l ** 2
            K_m[23, 5] = (27 / 40) * (2 * S[5, 1] * l - 15 * S[6, 1]) / l ** 2
            K_m[23, 6] = (27 / 40) * (-7 * S[5, 1] * l - 15 * S[6, 1]) / l ** 2
            K_m[23, 7] = (1 / 40) * (148 * S[5, 1] * l + 585 * S[6, 1]) / l ** 2
            K_m[23, 8] = (1 / 40) * (-13 * S[5, 2] * l + 225 * S[6, 2]) / l ** 2
            K_m[23, 9] = (27 / 40) * (2 * S[5, 2] * l - 15 * S[6, 2]) / l ** 2
            K_m[23, 10] = (27 / 40) * (-7 * S[5, 2] * l - 15 * S[6, 2]) / l ** 2
            K_m[23, 11] = (1 / 40) * (148 * S[5, 2] * l + 585 * S[6, 2]) / l ** 2
            K_m[23, 12] = (1 / 80) * (
                        7 * S[5, 1] * l ** 2 - 26 * S[5, 3] * l - 54 * S[6, 1] * l + 450 * S[6, 3]) / l ** 2
            K_m[23, 13] = (3 / 40) * (-4 * S[5, 1] * l ** 2 - 135 * S[6, 3] + 18 * l * (S[5, 3] - S[6, 1])) / l ** 2
            K_m[23, 14] = (3 / 80) * (19 * S[5, 1] * l ** 2 - 270 * S[6, 3] + 126 * l * (-S[5, 3] + S[6, 1])) / l ** 2
            K_m[23, 15] = (1 / 40) * (
                        20 * S[5, 1] * l ** 2 + 585 * S[6, 3] + 4 * l * (37 * S[5, 3] + 18 * S[6, 1])) / l ** 2
            K_m[23, 16] = (1 / 80) * (
                        -7 * S[5, 0] * l ** 2 + 450 * S[6, 4] + 2 * l * (-13 * S[5, 4] + 27 * S[6, 0])) / l ** 2
            K_m[23, 17] = (3 / 40) * (4 * S[5, 0] * l ** 2 - 135 * S[6, 4] + 18 * l * (S[5, 4] + S[6, 0])) / l ** 2
            K_m[23, 18] = (3 / 80) * (-19 * S[5, 0] * l ** 2 - 270 * S[6, 4] + 126 * l * (-S[5, 4] - S[6, 0])) / l ** 2
            K_m[23, 19] = (1 / 40) * (
                        -20 * S[5, 0] * l ** 2 + 585 * S[6, 4] + 4 * l * (37 * S[5, 4] - 18 * S[6, 0])) / l ** 2
            K_m[23, 20] = (1 / 40) * (-13 * S[5, 5] * l ** 2 - 1620 * S[6, 6] + 225 * l * (-S[5, 6] + S[6, 5])) / l ** 3
            K_m[23, 21] = (9 / 40) * (
                        6 * S[5, 5] * l ** 2 + 720 * S[6, 6] + 5 * l * (23 * S[5, 6] - 9 * S[6, 5])) / l ** 3
            K_m[23, 22] = (9 / 40) * (
                        -21 * S[5, 5] * l ** 2 - 900 * S[6, 6] + 5 * l * (-31 * S[5, 6] - 9 * S[6, 5])) / l ** 3
            K_m[23, 23] = (1 / 40) * (148 * S[5, 5] * l ** 2 + 3240 * S[6, 6] + 585 * l * (S[5, 6] + S[6, 5])) / l ** 3

            self._element_stiffness_matrix = K_m.tocsc()

        return self._element_stiffness_matrix

    def B_matrix(self, z):
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        B = sp.dok_array((7, 24), dtype=dtype)

        B[0, 0] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[0, 1] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[0, 2] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[0, 3] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[0, 16] = -1 + (11 / 2) * z / l - 9 * z ** 2 / l ** 2 + (9 / 2) * z ** 3 / l ** 3
        B[0, 17] = (9 / 2) * z * (-2 * l ** 2 + 5 * l * z - 3 * z ** 2) / l ** 3
        B[0, 18] = (9 / 2) * z * (l ** 2 - 4 * l * z + 3 * z ** 2) / l ** 3
        B[0, 19] = (1 / 2) * z * (-2 * l ** 2 + 9 * l * z - 9 * z ** 2) / l ** 3
        B[1, 4] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[1, 5] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[1, 6] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[1, 7] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[1, 12] = 1 - 11 / 2 * z / l + 9 * z ** 2 / l ** 2 - 9 / 2 * z ** 3 / l ** 3
        B[1, 13] = (9 / 2) * z * (2 * l ** 2 - 5 * l * z + 3 * z ** 2) / l ** 3
        B[1, 14] = (9 / 2) * z * (-l ** 2 + 4 * l * z - 3 * z ** 2) / l ** 3
        B[1, 15] = (1 / 2) * z * (2 * l ** 2 - 9 * l * z + 9 * z ** 2) / l ** 3
        B[2, 8] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[2, 9] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[2, 10] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[2, 11] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[3, 12] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[3, 13] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[3, 14] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[3, 15] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[4, 16] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[4, 17] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[4, 18] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[4, 19] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[5, 20] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[5, 21] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[5, 22] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[5, 23] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[6, 20] = 9 * (2 * l - 3 * z) / l ** 3
        B[6, 21] = 9 * (-5 * l + 9 * z) / l ** 3
        B[6, 22] = 9 * (4 * l - 9 * z) / l ** 3
        B[6, 23] = 9 * (-l + 3 * z) / l ** 3

        return B


class BeamElement4NodeWithoutWarping(BeamElement4Node):
    """
    A element of the 1D finite elements beam model. The elements have four nodes and 24 DOF.
    The warping part of the stiffness cross-section matrices is ignored.
    """
    def __init__(self, node1, node2, stiffness, inertia, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        node1: BeamNode
            First node of the element.
        node2: BeamNode
            Second node of the element.
        stiffness: TimoschenkoWithRestrainedWarpingStiffness
            The stiffness of the element (7x7).
        inertia: IInertia
            The inertia of the element.
        """
        super().__init__(node1, node2, stiffness, inertia, **kwargs)

    @staticmethod
    def ignore_warping() -> bool:
        return True

    @property
    def element_stiffness_matrix(self):
        """numpy.ndarray: The FE element stiffness matrix."""
        if not hasattr(self, '_element_stiffness_matrix'):
            dtype = self._dtype
            l = self.length
            S = self.cross_section_stiffness_matrix
            K_m = sp.dok_array((24, 24), dtype=dtype)

            K_m[0, 0] = (37 / 10) * S[0, 0] / l
            K_m[0, 1] = -189 / 40 * S[0, 0] / l
            K_m[0, 2] = (27 / 20) * S[0, 0] / l
            K_m[0, 3] = -13 / 40 * S[0, 0] / l
            K_m[0, 4] = (37 / 10) * S[0, 1] / l
            K_m[0, 5] = -189 / 40 * S[0, 1] / l
            K_m[0, 6] = (27 / 20) * S[0, 1] / l
            K_m[0, 7] = -13 / 40 * S[0, 1] / l
            K_m[0, 8] = (37 / 10) * S[0, 2] / l
            K_m[0, 9] = -189 / 40 * S[0, 2] / l
            K_m[0, 10] = (27 / 20) * S[0, 2] / l
            K_m[0, 11] = -13 / 40 * S[0, 2] / l
            K_m[0, 12] = -1 / 2 * S[0, 1] + (37 / 10) * S[0, 3] / l
            K_m[0, 13] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[0, 14] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[0, 15] = (1 / 80) * (-7 * S[0, 1] * l - 26 * S[0, 3]) / l
            K_m[0, 16] = (1 / 2) * S[0, 0] + (37 / 10) * S[0, 4] / l
            K_m[0, 17] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[0, 18] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[0, 19] = (1 / 80) * (7 * S[0, 0] * l - 26 * S[0, 4]) / l
            K_m[0, 20] = (37 / 10) * S[0, 5] / l
            K_m[0, 21] = -189 / 40 * S[0, 5] / l
            K_m[0, 22] = (27 / 20) * S[0, 5] / l
            K_m[0, 23] = -13 / 40 * S[0, 5] / l
            K_m[1, 0] = -189 / 40 * S[0, 0] / l
            K_m[1, 1] = (54 / 5) * S[0, 0] / l
            K_m[1, 2] = -297 / 40 * S[0, 0] / l
            K_m[1, 3] = (27 / 20) * S[0, 0] / l
            K_m[1, 4] = -189 / 40 * S[0, 1] / l
            K_m[1, 5] = (54 / 5) * S[0, 1] / l
            K_m[1, 6] = -297 / 40 * S[0, 1] / l
            K_m[1, 7] = (27 / 20) * S[0, 1] / l
            K_m[1, 8] = -189 / 40 * S[0, 2] / l
            K_m[1, 9] = (54 / 5) * S[0, 2] / l
            K_m[1, 10] = -297 / 40 * S[0, 2] / l
            K_m[1, 11] = (27 / 20) * S[0, 2] / l
            K_m[1, 12] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[1, 13] = (54 / 5) * S[0, 3] / l
            K_m[1, 14] = (27 / 80) * (-3 * S[0, 1] * l - 22 * S[0, 3]) / l
            K_m[1, 15] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[1, 16] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[1, 17] = (54 / 5) * S[0, 4] / l
            K_m[1, 18] = (27 / 80) * (3 * S[0, 0] * l - 22 * S[0, 4]) / l
            K_m[1, 19] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[1, 20] = -189 / 40 * S[0, 5] / l
            K_m[1, 21] = (54 / 5) * S[0, 5] / l
            K_m[1, 22] = -297 / 40 * S[0, 5] / l
            K_m[1, 23] = (27 / 20) * S[0, 5] / l
            K_m[2, 0] = (27 / 20) * S[0, 0] / l
            K_m[2, 1] = -297 / 40 * S[0, 0] / l
            K_m[2, 2] = (54 / 5) * S[0, 0] / l
            K_m[2, 3] = -189 / 40 * S[0, 0] / l
            K_m[2, 4] = (27 / 20) * S[0, 1] / l
            K_m[2, 5] = -297 / 40 * S[0, 1] / l
            K_m[2, 6] = (54 / 5) * S[0, 1] / l
            K_m[2, 7] = -189 / 40 * S[0, 1] / l
            K_m[2, 8] = (27 / 20) * S[0, 2] / l
            K_m[2, 9] = -297 / 40 * S[0, 2] / l
            K_m[2, 10] = (54 / 5) * S[0, 2] / l
            K_m[2, 11] = -189 / 40 * S[0, 2] / l
            K_m[2, 12] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[2, 13] = (27 / 80) * (3 * S[0, 1] * l - 22 * S[0, 3]) / l
            K_m[2, 14] = (54 / 5) * S[0, 3] / l
            K_m[2, 15] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[2, 16] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[2, 17] = (27 / 80) * (-3 * S[0, 0] * l - 22 * S[0, 4]) / l
            K_m[2, 18] = (54 / 5) * S[0, 4] / l
            K_m[2, 19] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[2, 20] = (27 / 20) * S[0, 5] / l
            K_m[2, 21] = -297 / 40 * S[0, 5] / l
            K_m[2, 22] = (54 / 5) * S[0, 5] / l
            K_m[2, 23] = -189 / 40 * S[0, 5] / l
            K_m[3, 0] = -13 / 40 * S[0, 0] / l
            K_m[3, 1] = (27 / 20) * S[0, 0] / l
            K_m[3, 2] = -189 / 40 * S[0, 0] / l
            K_m[3, 3] = (37 / 10) * S[0, 0] / l
            K_m[3, 4] = -13 / 40 * S[0, 1] / l
            K_m[3, 5] = (27 / 20) * S[0, 1] / l
            K_m[3, 6] = -189 / 40 * S[0, 1] / l
            K_m[3, 7] = (37 / 10) * S[0, 1] / l
            K_m[3, 8] = -13 / 40 * S[0, 2] / l
            K_m[3, 9] = (27 / 20) * S[0, 2] / l
            K_m[3, 10] = -189 / 40 * S[0, 2] / l
            K_m[3, 11] = (37 / 10) * S[0, 2] / l
            K_m[3, 12] = (1 / 80) * (7 * S[0, 1] * l - 26 * S[0, 3]) / l
            K_m[3, 13] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[0, 3]) / l
            K_m[3, 14] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[0, 3]) / l
            K_m[3, 15] = (1 / 2) * S[0, 1] + (37 / 10) * S[0, 3] / l
            K_m[3, 16] = (1 / 80) * (-7 * S[0, 0] * l - 26 * S[0, 4]) / l
            K_m[3, 17] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[0, 4]) / l
            K_m[3, 18] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[0, 4]) / l
            K_m[3, 19] = -1 / 2 * S[0, 0] + (37 / 10) * S[0, 4] / l
            K_m[3, 20] = -13 / 40 * S[0, 5] / l
            K_m[3, 21] = (27 / 20) * S[0, 5] / l
            K_m[3, 22] = -189 / 40 * S[0, 5] / l
            K_m[3, 23] = (37 / 10) * S[0, 5] / l
            K_m[4, 0] = (37 / 10) * S[1, 0] / l
            K_m[4, 1] = -189 / 40 * S[1, 0] / l
            K_m[4, 2] = (27 / 20) * S[1, 0] / l
            K_m[4, 3] = -13 / 40 * S[1, 0] / l
            K_m[4, 4] = (37 / 10) * S[1, 1] / l
            K_m[4, 5] = -189 / 40 * S[1, 1] / l
            K_m[4, 6] = (27 / 20) * S[1, 1] / l
            K_m[4, 7] = -13 / 40 * S[1, 1] / l
            K_m[4, 8] = (37 / 10) * S[1, 2] / l
            K_m[4, 9] = -189 / 40 * S[1, 2] / l
            K_m[4, 10] = (27 / 20) * S[1, 2] / l
            K_m[4, 11] = -13 / 40 * S[1, 2] / l
            K_m[4, 12] = -1 / 2 * S[1, 1] + (37 / 10) * S[1, 3] / l
            K_m[4, 13] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[4, 14] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[4, 15] = (1 / 80) * (-7 * S[1, 1] * l - 26 * S[1, 3]) / l
            K_m[4, 16] = (1 / 2) * S[1, 0] + (37 / 10) * S[1, 4] / l
            K_m[4, 17] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[4, 18] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[4, 19] = (1 / 80) * (7 * S[1, 0] * l - 26 * S[1, 4]) / l
            K_m[4, 20] = (37 / 10) * S[1, 5] / l
            K_m[4, 21] = -189 / 40 * S[1, 5] / l
            K_m[4, 22] = (27 / 20) * S[1, 5] / l
            K_m[4, 23] = -13 / 40 * S[1, 5] / l
            K_m[5, 0] = -189 / 40 * S[1, 0] / l
            K_m[5, 1] = (54 / 5) * S[1, 0] / l
            K_m[5, 2] = -297 / 40 * S[1, 0] / l
            K_m[5, 3] = (27 / 20) * S[1, 0] / l
            K_m[5, 4] = -189 / 40 * S[1, 1] / l
            K_m[5, 5] = (54 / 5) * S[1, 1] / l
            K_m[5, 6] = -297 / 40 * S[1, 1] / l
            K_m[5, 7] = (27 / 20) * S[1, 1] / l
            K_m[5, 8] = -189 / 40 * S[1, 2] / l
            K_m[5, 9] = (54 / 5) * S[1, 2] / l
            K_m[5, 10] = -297 / 40 * S[1, 2] / l
            K_m[5, 11] = (27 / 20) * S[1, 2] / l
            K_m[5, 12] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[5, 13] = (54 / 5) * S[1, 3] / l
            K_m[5, 14] = (27 / 80) * (-3 * S[1, 1] * l - 22 * S[1, 3]) / l
            K_m[5, 15] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[5, 16] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[5, 17] = (54 / 5) * S[1, 4] / l
            K_m[5, 18] = (27 / 80) * (3 * S[1, 0] * l - 22 * S[1, 4]) / l
            K_m[5, 19] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[5, 20] = -189 / 40 * S[1, 5] / l
            K_m[5, 21] = (54 / 5) * S[1, 5] / l
            K_m[5, 22] = -297 / 40 * S[1, 5] / l
            K_m[5, 23] = (27 / 20) * S[1, 5] / l
            K_m[6, 0] = (27 / 20) * S[1, 0] / l
            K_m[6, 1] = -297 / 40 * S[1, 0] / l
            K_m[6, 2] = (54 / 5) * S[1, 0] / l
            K_m[6, 3] = -189 / 40 * S[1, 0] / l
            K_m[6, 4] = (27 / 20) * S[1, 1] / l
            K_m[6, 5] = -297 / 40 * S[1, 1] / l
            K_m[6, 6] = (54 / 5) * S[1, 1] / l
            K_m[6, 7] = -189 / 40 * S[1, 1] / l
            K_m[6, 8] = (27 / 20) * S[1, 2] / l
            K_m[6, 9] = -297 / 40 * S[1, 2] / l
            K_m[6, 10] = (54 / 5) * S[1, 2] / l
            K_m[6, 11] = -189 / 40 * S[1, 2] / l
            K_m[6, 12] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[6, 13] = (27 / 80) * (3 * S[1, 1] * l - 22 * S[1, 3]) / l
            K_m[6, 14] = (54 / 5) * S[1, 3] / l
            K_m[6, 15] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[6, 16] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[6, 17] = (27 / 80) * (-3 * S[1, 0] * l - 22 * S[1, 4]) / l
            K_m[6, 18] = (54 / 5) * S[1, 4] / l
            K_m[6, 19] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[6, 20] = (27 / 20) * S[1, 5] / l
            K_m[6, 21] = -297 / 40 * S[1, 5] / l
            K_m[6, 22] = (54 / 5) * S[1, 5] / l
            K_m[6, 23] = -189 / 40 * S[1, 5] / l
            K_m[7, 0] = -13 / 40 * S[1, 0] / l
            K_m[7, 1] = (27 / 20) * S[1, 0] / l
            K_m[7, 2] = -189 / 40 * S[1, 0] / l
            K_m[7, 3] = (37 / 10) * S[1, 0] / l
            K_m[7, 4] = -13 / 40 * S[1, 1] / l
            K_m[7, 5] = (27 / 20) * S[1, 1] / l
            K_m[7, 6] = -189 / 40 * S[1, 1] / l
            K_m[7, 7] = (37 / 10) * S[1, 1] / l
            K_m[7, 8] = -13 / 40 * S[1, 2] / l
            K_m[7, 9] = (27 / 20) * S[1, 2] / l
            K_m[7, 10] = -189 / 40 * S[1, 2] / l
            K_m[7, 11] = (37 / 10) * S[1, 2] / l
            K_m[7, 12] = (1 / 80) * (7 * S[1, 1] * l - 26 * S[1, 3]) / l
            K_m[7, 13] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[1, 3]) / l
            K_m[7, 14] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[1, 3]) / l
            K_m[7, 15] = (1 / 2) * S[1, 1] + (37 / 10) * S[1, 3] / l
            K_m[7, 16] = (1 / 80) * (-7 * S[1, 0] * l - 26 * S[1, 4]) / l
            K_m[7, 17] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[1, 4]) / l
            K_m[7, 18] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[1, 4]) / l
            K_m[7, 19] = -1 / 2 * S[1, 0] + (37 / 10) * S[1, 4] / l
            K_m[7, 20] = -13 / 40 * S[1, 5] / l
            K_m[7, 21] = (27 / 20) * S[1, 5] / l
            K_m[7, 22] = -189 / 40 * S[1, 5] / l
            K_m[7, 23] = (37 / 10) * S[1, 5] / l
            K_m[8, 0] = (37 / 10) * S[2, 0] / l
            K_m[8, 1] = -189 / 40 * S[2, 0] / l
            K_m[8, 2] = (27 / 20) * S[2, 0] / l
            K_m[8, 3] = -13 / 40 * S[2, 0] / l
            K_m[8, 4] = (37 / 10) * S[2, 1] / l
            K_m[8, 5] = -189 / 40 * S[2, 1] / l
            K_m[8, 6] = (27 / 20) * S[2, 1] / l
            K_m[8, 7] = -13 / 40 * S[2, 1] / l
            K_m[8, 8] = (37 / 10) * S[2, 2] / l
            K_m[8, 9] = -189 / 40 * S[2, 2] / l
            K_m[8, 10] = (27 / 20) * S[2, 2] / l
            K_m[8, 11] = -13 / 40 * S[2, 2] / l
            K_m[8, 12] = -1 / 2 * S[2, 1] + (37 / 10) * S[2, 3] / l
            K_m[8, 13] = (3 / 80) * (-19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[8, 14] = (3 / 20) * (2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[8, 15] = (1 / 80) * (-7 * S[2, 1] * l - 26 * S[2, 3]) / l
            K_m[8, 16] = (1 / 2) * S[2, 0] + (37 / 10) * S[2, 4] / l
            K_m[8, 17] = (3 / 80) * (19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[8, 18] = (3 / 20) * (-2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[8, 19] = (1 / 80) * (7 * S[2, 0] * l - 26 * S[2, 4]) / l
            K_m[8, 20] = (37 / 10) * S[2, 5] / l
            K_m[8, 21] = -189 / 40 * S[2, 5] / l
            K_m[8, 22] = (27 / 20) * S[2, 5] / l
            K_m[8, 23] = -13 / 40 * S[2, 5] / l
            K_m[9, 0] = -189 / 40 * S[2, 0] / l
            K_m[9, 1] = (54 / 5) * S[2, 0] / l
            K_m[9, 2] = -297 / 40 * S[2, 0] / l
            K_m[9, 3] = (27 / 20) * S[2, 0] / l
            K_m[9, 4] = -189 / 40 * S[2, 1] / l
            K_m[9, 5] = (54 / 5) * S[2, 1] / l
            K_m[9, 6] = -297 / 40 * S[2, 1] / l
            K_m[9, 7] = (27 / 20) * S[2, 1] / l
            K_m[9, 8] = -189 / 40 * S[2, 2] / l
            K_m[9, 9] = (54 / 5) * S[2, 2] / l
            K_m[9, 10] = -297 / 40 * S[2, 2] / l
            K_m[9, 11] = (27 / 20) * S[2, 2] / l
            K_m[9, 12] = (3 / 80) * (19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[9, 13] = (54 / 5) * S[2, 3] / l
            K_m[9, 14] = (27 / 80) * (-3 * S[2, 1] * l - 22 * S[2, 3]) / l
            K_m[9, 15] = (3 / 20) * (2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[9, 16] = (3 / 80) * (-19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[9, 17] = (54 / 5) * S[2, 4] / l
            K_m[9, 18] = (27 / 80) * (3 * S[2, 0] * l - 22 * S[2, 4]) / l
            K_m[9, 19] = (3 / 20) * (-2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[9, 20] = -189 / 40 * S[2, 5] / l
            K_m[9, 21] = (54 / 5) * S[2, 5] / l
            K_m[9, 22] = -297 / 40 * S[2, 5] / l
            K_m[9, 23] = (27 / 20) * S[2, 5] / l
            K_m[10, 0] = (27 / 20) * S[2, 0] / l
            K_m[10, 1] = -297 / 40 * S[2, 0] / l
            K_m[10, 2] = (54 / 5) * S[2, 0] / l
            K_m[10, 3] = -189 / 40 * S[2, 0] / l
            K_m[10, 4] = (27 / 20) * S[2, 1] / l
            K_m[10, 5] = -297 / 40 * S[2, 1] / l
            K_m[10, 6] = (54 / 5) * S[2, 1] / l
            K_m[10, 7] = -189 / 40 * S[2, 1] / l
            K_m[10, 8] = (27 / 20) * S[2, 2] / l
            K_m[10, 9] = -297 / 40 * S[2, 2] / l
            K_m[10, 10] = (54 / 5) * S[2, 2] / l
            K_m[10, 11] = -189 / 40 * S[2, 2] / l
            K_m[10, 12] = (3 / 20) * (-2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[10, 13] = (27 / 80) * (3 * S[2, 1] * l - 22 * S[2, 3]) / l
            K_m[10, 14] = (54 / 5) * S[2, 3] / l
            K_m[10, 15] = (3 / 80) * (-19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[10, 16] = (3 / 20) * (2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[10, 17] = (27 / 80) * (-3 * S[2, 0] * l - 22 * S[2, 4]) / l
            K_m[10, 18] = (54 / 5) * S[2, 4] / l
            K_m[10, 19] = (3 / 80) * (19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[10, 20] = (27 / 20) * S[2, 5] / l
            K_m[10, 21] = -297 / 40 * S[2, 5] / l
            K_m[10, 22] = (54 / 5) * S[2, 5] / l
            K_m[10, 23] = -189 / 40 * S[2, 5] / l
            K_m[11, 0] = -13 / 40 * S[2, 0] / l
            K_m[11, 1] = (27 / 20) * S[2, 0] / l
            K_m[11, 2] = -189 / 40 * S[2, 0] / l
            K_m[11, 3] = (37 / 10) * S[2, 0] / l
            K_m[11, 4] = -13 / 40 * S[2, 1] / l
            K_m[11, 5] = (27 / 20) * S[2, 1] / l
            K_m[11, 6] = -189 / 40 * S[2, 1] / l
            K_m[11, 7] = (37 / 10) * S[2, 1] / l
            K_m[11, 8] = -13 / 40 * S[2, 2] / l
            K_m[11, 9] = (27 / 20) * S[2, 2] / l
            K_m[11, 10] = -189 / 40 * S[2, 2] / l
            K_m[11, 11] = (37 / 10) * S[2, 2] / l
            K_m[11, 12] = (1 / 80) * (7 * S[2, 1] * l - 26 * S[2, 3]) / l
            K_m[11, 13] = (3 / 20) * (-2 * S[2, 1] * l + 9 * S[2, 3]) / l
            K_m[11, 14] = (3 / 80) * (19 * S[2, 1] * l - 126 * S[2, 3]) / l
            K_m[11, 15] = (1 / 2) * S[2, 1] + (37 / 10) * S[2, 3] / l
            K_m[11, 16] = (1 / 80) * (-7 * S[2, 0] * l - 26 * S[2, 4]) / l
            K_m[11, 17] = (3 / 20) * (2 * S[2, 0] * l + 9 * S[2, 4]) / l
            K_m[11, 18] = (3 / 80) * (-19 * S[2, 0] * l - 126 * S[2, 4]) / l
            K_m[11, 19] = -1 / 2 * S[2, 0] + (37 / 10) * S[2, 4] / l
            K_m[11, 20] = -13 / 40 * S[2, 5] / l
            K_m[11, 21] = (27 / 20) * S[2, 5] / l
            K_m[11, 22] = -189 / 40 * S[2, 5] / l
            K_m[11, 23] = (37 / 10) * S[2, 5] / l
            K_m[12, 0] = -1 / 2 * S[1, 0] + (37 / 10) * S[3, 0] / l
            K_m[12, 1] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[12, 2] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[12, 3] = (1 / 80) * (7 * S[1, 0] * l - 26 * S[3, 0]) / l
            K_m[12, 4] = -1 / 2 * S[1, 1] + (37 / 10) * S[3, 1] / l
            K_m[12, 5] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[12, 6] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[12, 7] = (1 / 80) * (7 * S[1, 1] * l - 26 * S[3, 1]) / l
            K_m[12, 8] = -1 / 2 * S[1, 2] + (37 / 10) * S[3, 2] / l
            K_m[12, 9] = (3 / 80) * (19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[12, 10] = (3 / 20) * (-2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[12, 11] = (1 / 80) * (7 * S[1, 2] * l - 26 * S[3, 2]) / l
            K_m[12, 12] = (1 / 210) * (777 * S[3, 3] + l * (16 * S[1, 1] * l - 105 * S[1, 3] - 105 * S[3, 1])) / l
            K_m[12, 13] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l + 133 * S[1, 3] - 133 * S[3, 1])) / l
            K_m[12, 14] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l - 14 * S[1, 3] + 14 * S[3, 1])) / l
            K_m[12, 15] = (1 / 1680) * (-546 * S[3, 3] + l * (19 * S[1, 1] * l + 147 * S[1, 3] - 147 * S[3, 1])) / l
            K_m[12, 16] = (1 / 210) * (777 * S[3, 4] + l * (-16 * S[1, 0] * l - 105 * S[1, 4] + 105 * S[3, 0])) / l
            K_m[12, 17] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l + 133 * S[1, 4] + 133 * S[3, 0])) / l
            K_m[12, 18] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l - 14 * S[1, 4] - 14 * S[3, 0])) / l
            K_m[12, 19] = (1 / 1680) * (-546 * S[3, 4] + l * (-19 * S[1, 0] * l + 147 * S[1, 4] + 147 * S[3, 0])) / l
            K_m[12, 20] = -1 / 2 * S[1, 5] + (37 / 10) * S[3, 5] / l
            K_m[12, 21] = (3 / 80) * (19 * S[1, 5] * l - 126 * S[3, 5]) / l
            K_m[12, 22] = (3 / 20) * (-2 * S[1, 5] * l + 9 * S[3, 5]) / l
            K_m[12, 23] = (1 / 80) * (7 * S[1, 5] * l - 26 * S[3, 5]) / l
            K_m[13, 0] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[13, 1] = (54 / 5) * S[3, 0] / l
            K_m[13, 2] = (27 / 80) * (3 * S[1, 0] * l - 22 * S[3, 0]) / l
            K_m[13, 3] = (3 / 20) * (-2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[13, 4] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[13, 5] = (54 / 5) * S[3, 1] / l
            K_m[13, 6] = (27 / 80) * (3 * S[1, 1] * l - 22 * S[3, 1]) / l
            K_m[13, 7] = (3 / 20) * (-2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[13, 8] = (3 / 80) * (-19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[13, 9] = (54 / 5) * S[3, 2] / l
            K_m[13, 10] = (27 / 80) * (3 * S[1, 2] * l - 22 * S[3, 2]) / l
            K_m[13, 11] = (3 / 20) * (-2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[13, 12] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l - 133 * S[1, 3] + 133 * S[3, 1])) / l
            K_m[13, 13] = (27 / 70) * (S[1, 1] * l ** 2 + 28 * S[3, 3]) / l
            K_m[13, 14] = (27 / 560) * (-154 * S[3, 3] + l * (-S[1, 1] * l + 21 * S[1, 3] - 21 * S[3, 1])) / l
            K_m[13, 15] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l - 14 * S[1, 3] + 14 * S[3, 1])) / l
            K_m[13, 16] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l - 133 * S[1, 4] - 133 * S[3, 0])) / l
            K_m[13, 17] = (27 / 70) * (-S[1, 0] * l ** 2 + 28 * S[3, 4]) / l
            K_m[13, 18] = (27 / 560) * (-154 * S[3, 4] + l * (S[1, 0] * l + 21 * S[1, 4] + 21 * S[3, 0])) / l
            K_m[13, 19] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l - 14 * S[1, 4] - 14 * S[3, 0])) / l
            K_m[13, 20] = (3 / 80) * (-19 * S[1, 5] * l - 126 * S[3, 5]) / l
            K_m[13, 21] = (54 / 5) * S[3, 5] / l
            K_m[13, 22] = (27 / 80) * (3 * S[1, 5] * l - 22 * S[3, 5]) / l
            K_m[13, 23] = (3 / 20) * (-2 * S[1, 5] * l + 9 * S[3, 5]) / l
            K_m[14, 0] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[14, 1] = (27 / 80) * (-3 * S[1, 0] * l - 22 * S[3, 0]) / l
            K_m[14, 2] = (54 / 5) * S[3, 0] / l
            K_m[14, 3] = (3 / 80) * (19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[14, 4] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[14, 5] = (27 / 80) * (-3 * S[1, 1] * l - 22 * S[3, 1]) / l
            K_m[14, 6] = (54 / 5) * S[3, 1] / l
            K_m[14, 7] = (3 / 80) * (19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[14, 8] = (3 / 20) * (2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[14, 9] = (27 / 80) * (-3 * S[1, 2] * l - 22 * S[3, 2]) / l
            K_m[14, 10] = (54 / 5) * S[3, 2] / l
            K_m[14, 11] = (3 / 80) * (19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[14, 12] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l + 14 * S[1, 3] - 14 * S[3, 1])) / l
            K_m[14, 13] = (27 / 560) * (-154 * S[3, 3] + l * (-S[1, 1] * l - 21 * S[1, 3] + 21 * S[3, 1])) / l
            K_m[14, 14] = (27 / 70) * (S[1, 1] * l ** 2 + 28 * S[3, 3]) / l
            K_m[14, 15] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l + 133 * S[1, 3] - 133 * S[3, 1])) / l
            K_m[14, 16] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l + 14 * S[1, 4] + 14 * S[3, 0])) / l
            K_m[14, 17] = (27 / 560) * (-154 * S[3, 4] + l * (S[1, 0] * l - 21 * S[1, 4] - 21 * S[3, 0])) / l
            K_m[14, 18] = (27 / 70) * (-S[1, 0] * l ** 2 + 28 * S[3, 4]) / l
            K_m[14, 19] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l + 133 * S[1, 4] + 133 * S[3, 0])) / l
            K_m[14, 20] = (3 / 20) * (2 * S[1, 5] * l + 9 * S[3, 5]) / l
            K_m[14, 21] = (27 / 80) * (-3 * S[1, 5] * l - 22 * S[3, 5]) / l
            K_m[14, 22] = (54 / 5) * S[3, 5] / l
            K_m[14, 23] = (3 / 80) * (19 * S[1, 5] * l - 126 * S[3, 5]) / l
            K_m[15, 0] = (1 / 80) * (-7 * S[1, 0] * l - 26 * S[3, 0]) / l
            K_m[15, 1] = (3 / 20) * (2 * S[1, 0] * l + 9 * S[3, 0]) / l
            K_m[15, 2] = (3 / 80) * (-19 * S[1, 0] * l - 126 * S[3, 0]) / l
            K_m[15, 3] = (1 / 2) * S[1, 0] + (37 / 10) * S[3, 0] / l
            K_m[15, 4] = (1 / 80) * (-7 * S[1, 1] * l - 26 * S[3, 1]) / l
            K_m[15, 5] = (3 / 20) * (2 * S[1, 1] * l + 9 * S[3, 1]) / l
            K_m[15, 6] = (3 / 80) * (-19 * S[1, 1] * l - 126 * S[3, 1]) / l
            K_m[15, 7] = (1 / 2) * S[1, 1] + (37 / 10) * S[3, 1] / l
            K_m[15, 8] = (1 / 80) * (-7 * S[1, 2] * l - 26 * S[3, 2]) / l
            K_m[15, 9] = (3 / 20) * (2 * S[1, 2] * l + 9 * S[3, 2]) / l
            K_m[15, 10] = (3 / 80) * (-19 * S[1, 2] * l - 126 * S[3, 2]) / l
            K_m[15, 11] = (1 / 2) * S[1, 2] + (37 / 10) * S[3, 2] / l
            K_m[15, 12] = (1 / 1680) * (-546 * S[3, 3] + l * (19 * S[1, 1] * l - 147 * S[1, 3] + 147 * S[3, 1])) / l
            K_m[15, 13] = (3 / 140) * (63 * S[3, 3] + l * (-S[1, 1] * l + 14 * S[1, 3] - 14 * S[3, 1])) / l
            K_m[15, 14] = (3 / 560) * (-882 * S[3, 3] + l * (11 * S[1, 1] * l - 133 * S[1, 3] + 133 * S[3, 1])) / l
            K_m[15, 15] = (1 / 210) * (777 * S[3, 3] + l * (16 * S[1, 1] * l + 105 * S[1, 3] + 105 * S[3, 1])) / l
            K_m[15, 16] = (1 / 1680) * (-546 * S[3, 4] + l * (-19 * S[1, 0] * l - 147 * S[1, 4] - 147 * S[3, 0])) / l
            K_m[15, 17] = (3 / 140) * (63 * S[3, 4] + l * (S[1, 0] * l + 14 * S[1, 4] + 14 * S[3, 0])) / l
            K_m[15, 18] = (3 / 560) * (-882 * S[3, 4] + l * (-11 * S[1, 0] * l - 133 * S[1, 4] - 133 * S[3, 0])) / l
            K_m[15, 19] = (1 / 210) * (777 * S[3, 4] + l * (-16 * S[1, 0] * l + 105 * S[1, 4] - 105 * S[3, 0])) / l
            K_m[15, 20] = (1 / 80) * (-7 * S[1, 5] * l - 26 * S[3, 5]) / l
            K_m[15, 21] = (3 / 20) * (2 * S[1, 5] * l + 9 * S[3, 5]) / l
            K_m[15, 22] = (3 / 80) * (-19 * S[1, 5] * l - 126 * S[3, 5]) / l
            K_m[15, 23] = (1 / 2) * S[1, 5] + (37 / 10) * S[3, 5] / l
            K_m[16, 0] = (1 / 2) * S[0, 0] + (37 / 10) * S[4, 0] / l
            K_m[16, 1] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[16, 2] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[16, 3] = (1 / 80) * (-7 * S[0, 0] * l - 26 * S[4, 0]) / l
            K_m[16, 4] = (1 / 2) * S[0, 1] + (37 / 10) * S[4, 1] / l
            K_m[16, 5] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[16, 6] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[16, 7] = (1 / 80) * (-7 * S[0, 1] * l - 26 * S[4, 1]) / l
            K_m[16, 8] = (1 / 2) * S[0, 2] + (37 / 10) * S[4, 2] / l
            K_m[16, 9] = (3 / 80) * (-19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[16, 10] = (3 / 20) * (2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[16, 11] = (1 / 80) * (-7 * S[0, 2] * l - 26 * S[4, 2]) / l
            K_m[16, 12] = (1 / 210) * (777 * S[4, 3] + l * (-16 * S[0, 1] * l + 105 * S[0, 3] - 105 * S[4, 1])) / l
            K_m[16, 13] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l - 133 * S[0, 3] - 133 * S[4, 1])) / l
            K_m[16, 14] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l + 14 * S[0, 3] + 14 * S[4, 1])) / l
            K_m[16, 15] = (1 / 1680) * (-546 * S[4, 3] + l * (-19 * S[0, 1] * l - 147 * S[0, 3] - 147 * S[4, 1])) / l
            K_m[16, 16] = (1 / 210) * (777 * S[4, 4] + l * (16 * S[0, 0] * l + 105 * S[0, 4] + 105 * S[4, 0])) / l
            K_m[16, 17] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l - 133 * S[0, 4] + 133 * S[4, 0])) / l
            K_m[16, 18] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l + 14 * S[0, 4] - 14 * S[4, 0])) / l
            K_m[16, 19] = (1 / 1680) * (-546 * S[4, 4] + l * (19 * S[0, 0] * l - 147 * S[0, 4] + 147 * S[4, 0])) / l
            K_m[16, 20] = (1 / 2) * S[0, 5] + (37 / 10) * S[4, 5] / l
            K_m[16, 21] = (3 / 80) * (-19 * S[0, 5] * l - 126 * S[4, 5]) / l
            K_m[16, 22] = (3 / 20) * (2 * S[0, 5] * l + 9 * S[4, 5]) / l
            K_m[16, 23] = (1 / 80) * (-7 * S[0, 5] * l - 26 * S[4, 5]) / l
            K_m[17, 0] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[17, 1] = (54 / 5) * S[4, 0] / l
            K_m[17, 2] = (27 / 80) * (-3 * S[0, 0] * l - 22 * S[4, 0]) / l
            K_m[17, 3] = (3 / 20) * (2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[17, 4] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[17, 5] = (54 / 5) * S[4, 1] / l
            K_m[17, 6] = (27 / 80) * (-3 * S[0, 1] * l - 22 * S[4, 1]) / l
            K_m[17, 7] = (3 / 20) * (2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[17, 8] = (3 / 80) * (19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[17, 9] = (54 / 5) * S[4, 2] / l
            K_m[17, 10] = (27 / 80) * (-3 * S[0, 2] * l - 22 * S[4, 2]) / l
            K_m[17, 11] = (3 / 20) * (2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[17, 12] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l + 133 * S[0, 3] + 133 * S[4, 1])) / l
            K_m[17, 13] = (27 / 70) * (-S[0, 1] * l ** 2 + 28 * S[4, 3]) / l
            K_m[17, 14] = (27 / 560) * (-154 * S[4, 3] + l * (S[0, 1] * l - 21 * S[0, 3] - 21 * S[4, 1])) / l
            K_m[17, 15] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l + 14 * S[0, 3] + 14 * S[4, 1])) / l
            K_m[17, 16] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l + 133 * S[0, 4] - 133 * S[4, 0])) / l
            K_m[17, 17] = (27 / 70) * (S[0, 0] * l ** 2 + 28 * S[4, 4]) / l
            K_m[17, 18] = (27 / 560) * (-154 * S[4, 4] + l * (-S[0, 0] * l - 21 * S[0, 4] + 21 * S[4, 0])) / l
            K_m[17, 19] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l + 14 * S[0, 4] - 14 * S[4, 0])) / l
            K_m[17, 20] = (3 / 80) * (19 * S[0, 5] * l - 126 * S[4, 5]) / l
            K_m[17, 21] = (54 / 5) * S[4, 5] / l
            K_m[17, 22] = (27 / 80) * (-3 * S[0, 5] * l - 22 * S[4, 5]) / l
            K_m[17, 23] = (3 / 20) * (2 * S[0, 5] * l + 9 * S[4, 5]) / l
            K_m[18, 0] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[18, 1] = (27 / 80) * (3 * S[0, 0] * l - 22 * S[4, 0]) / l
            K_m[18, 2] = (54 / 5) * S[4, 0] / l
            K_m[18, 3] = (3 / 80) * (-19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[18, 4] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[18, 5] = (27 / 80) * (3 * S[0, 1] * l - 22 * S[4, 1]) / l
            K_m[18, 6] = (54 / 5) * S[4, 1] / l
            K_m[18, 7] = (3 / 80) * (-19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[18, 8] = (3 / 20) * (-2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[18, 9] = (27 / 80) * (3 * S[0, 2] * l - 22 * S[4, 2]) / l
            K_m[18, 10] = (54 / 5) * S[4, 2] / l
            K_m[18, 11] = (3 / 80) * (-19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[18, 12] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l - 14 * S[0, 3] - 14 * S[4, 1])) / l
            K_m[18, 13] = (27 / 560) * (-154 * S[4, 3] + l * (S[0, 1] * l + 21 * S[0, 3] + 21 * S[4, 1])) / l
            K_m[18, 14] = (27 / 70) * (-S[0, 1] * l ** 2 + 28 * S[4, 3]) / l
            K_m[18, 15] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l - 133 * S[0, 3] - 133 * S[4, 1])) / l
            K_m[18, 16] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l - 14 * S[0, 4] + 14 * S[4, 0])) / l
            K_m[18, 17] = (27 / 560) * (-154 * S[4, 4] + l * (-S[0, 0] * l + 21 * S[0, 4] - 21 * S[4, 0])) / l
            K_m[18, 18] = (27 / 70) * (S[0, 0] * l ** 2 + 28 * S[4, 4]) / l
            K_m[18, 19] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l - 133 * S[0, 4] + 133 * S[4, 0])) / l
            K_m[18, 20] = (3 / 20) * (-2 * S[0, 5] * l + 9 * S[4, 5]) / l
            K_m[18, 21] = (27 / 80) * (3 * S[0, 5] * l - 22 * S[4, 5]) / l
            K_m[18, 22] = (54 / 5) * S[4, 5] / l
            K_m[18, 23] = (3 / 80) * (-19 * S[0, 5] * l - 126 * S[4, 5]) / l
            K_m[19, 0] = (1 / 80) * (7 * S[0, 0] * l - 26 * S[4, 0]) / l
            K_m[19, 1] = (3 / 20) * (-2 * S[0, 0] * l + 9 * S[4, 0]) / l
            K_m[19, 2] = (3 / 80) * (19 * S[0, 0] * l - 126 * S[4, 0]) / l
            K_m[19, 3] = -1 / 2 * S[0, 0] + (37 / 10) * S[4, 0] / l
            K_m[19, 4] = (1 / 80) * (7 * S[0, 1] * l - 26 * S[4, 1]) / l
            K_m[19, 5] = (3 / 20) * (-2 * S[0, 1] * l + 9 * S[4, 1]) / l
            K_m[19, 6] = (3 / 80) * (19 * S[0, 1] * l - 126 * S[4, 1]) / l
            K_m[19, 7] = -1 / 2 * S[0, 1] + (37 / 10) * S[4, 1] / l
            K_m[19, 8] = (1 / 80) * (7 * S[0, 2] * l - 26 * S[4, 2]) / l
            K_m[19, 9] = (3 / 20) * (-2 * S[0, 2] * l + 9 * S[4, 2]) / l
            K_m[19, 10] = (3 / 80) * (19 * S[0, 2] * l - 126 * S[4, 2]) / l
            K_m[19, 11] = -1 / 2 * S[0, 2] + (37 / 10) * S[4, 2] / l
            K_m[19, 12] = (1 / 1680) * (-546 * S[4, 3] + l * (-19 * S[0, 1] * l + 147 * S[0, 3] + 147 * S[4, 1])) / l
            K_m[19, 13] = (3 / 140) * (63 * S[4, 3] + l * (S[0, 1] * l - 14 * S[0, 3] - 14 * S[4, 1])) / l
            K_m[19, 14] = (3 / 560) * (-882 * S[4, 3] + l * (-11 * S[0, 1] * l + 133 * S[0, 3] + 133 * S[4, 1])) / l
            K_m[19, 15] = (1 / 210) * (777 * S[4, 3] + l * (-16 * S[0, 1] * l - 105 * S[0, 3] + 105 * S[4, 1])) / l
            K_m[19, 16] = (1 / 1680) * (-546 * S[4, 4] + l * (19 * S[0, 0] * l + 147 * S[0, 4] - 147 * S[4, 0])) / l
            K_m[19, 17] = (3 / 140) * (63 * S[4, 4] + l * (-S[0, 0] * l - 14 * S[0, 4] + 14 * S[4, 0])) / l
            K_m[19, 18] = (3 / 560) * (-882 * S[4, 4] + l * (11 * S[0, 0] * l + 133 * S[0, 4] - 133 * S[4, 0])) / l
            K_m[19, 19] = (1 / 210) * (777 * S[4, 4] + l * (16 * S[0, 0] * l - 105 * S[0, 4] - 105 * S[4, 0])) / l
            K_m[19, 20] = (1 / 80) * (7 * S[0, 5] * l - 26 * S[4, 5]) / l
            K_m[19, 21] = (3 / 20) * (-2 * S[0, 5] * l + 9 * S[4, 5]) / l
            K_m[19, 22] = (3 / 80) * (19 * S[0, 5] * l - 126 * S[4, 5]) / l
            K_m[19, 23] = -1 / 2 * S[0, 5] + (37 / 10) * S[4, 5] / l
            K_m[20, 0] = (37 / 10) * S[5, 0] / l
            K_m[20, 1] = -189 / 40 * S[5, 0] / l
            K_m[20, 2] = (27 / 20) * S[5, 0] / l
            K_m[20, 3] = -13 / 40 * S[5, 0] / l
            K_m[20, 4] = (37 / 10) * S[5, 1] / l
            K_m[20, 5] = -189 / 40 * S[5, 1] / l
            K_m[20, 6] = (27 / 20) * S[5, 1] / l
            K_m[20, 7] = -13 / 40 * S[5, 1] / l
            K_m[20, 8] = (37 / 10) * S[5, 2] / l
            K_m[20, 9] = -189 / 40 * S[5, 2] / l
            K_m[20, 10] = (27 / 20) * S[5, 2] / l
            K_m[20, 11] = -13 / 40 * S[5, 2] / l
            K_m[20, 12] = -1 / 2 * S[5, 1] + (37 / 10) * S[5, 3] / l
            K_m[20, 13] = (3 / 80) * (-19 * S[5, 1] * l - 126 * S[5, 3]) / l
            K_m[20, 14] = (3 / 20) * (2 * S[5, 1] * l + 9 * S[5, 3]) / l
            K_m[20, 15] = (1 / 80) * (-7 * S[5, 1] * l - 26 * S[5, 3]) / l
            K_m[20, 16] = (1 / 2) * S[5, 0] + (37 / 10) * S[5, 4] / l
            K_m[20, 17] = (3 / 80) * (19 * S[5, 0] * l - 126 * S[5, 4]) / l
            K_m[20, 18] = (3 / 20) * (-2 * S[5, 0] * l + 9 * S[5, 4]) / l
            K_m[20, 19] = (1 / 80) * (7 * S[5, 0] * l - 26 * S[5, 4]) / l
            K_m[20, 20] = (37 / 10) * S[5, 5] / l
            K_m[20, 21] = -189 / 40 * S[5, 5] / l
            K_m[20, 22] = (27 / 20) * S[5, 5] / l
            K_m[20, 23] = -13 / 40 * S[5, 5] / l
            K_m[21, 0] = -189 / 40 * S[5, 0] / l
            K_m[21, 1] = (54 / 5) * S[5, 0] / l
            K_m[21, 2] = -297 / 40 * S[5, 0] / l
            K_m[21, 3] = (27 / 20) * S[5, 0] / l
            K_m[21, 4] = -189 / 40 * S[5, 1] / l
            K_m[21, 5] = (54 / 5) * S[5, 1] / l
            K_m[21, 6] = -297 / 40 * S[5, 1] / l
            K_m[21, 7] = (27 / 20) * S[5, 1] / l
            K_m[21, 8] = -189 / 40 * S[5, 2] / l
            K_m[21, 9] = (54 / 5) * S[5, 2] / l
            K_m[21, 10] = -297 / 40 * S[5, 2] / l
            K_m[21, 11] = (27 / 20) * S[5, 2] / l
            K_m[21, 12] = (3 / 80) * (19 * S[5, 1] * l - 126 * S[5, 3]) / l
            K_m[21, 13] = (54 / 5) * S[5, 3] / l
            K_m[21, 14] = (27 / 80) * (-3 * S[5, 1] * l - 22 * S[5, 3]) / l
            K_m[21, 15] = (3 / 20) * (2 * S[5, 1] * l + 9 * S[5, 3]) / l
            K_m[21, 16] = (3 / 80) * (-19 * S[5, 0] * l - 126 * S[5, 4]) / l
            K_m[21, 17] = (54 / 5) * S[5, 4] / l
            K_m[21, 18] = (27 / 80) * (3 * S[5, 0] * l - 22 * S[5, 4]) / l
            K_m[21, 19] = (3 / 20) * (-2 * S[5, 0] * l + 9 * S[5, 4]) / l
            K_m[21, 20] = -189 / 40 * S[5, 5] / l
            K_m[21, 21] = (54 / 5) * S[5, 5] / l
            K_m[21, 22] = -297 / 40 * S[5, 5] / l
            K_m[21, 23] = (27 / 20) * S[5, 5] / l
            K_m[22, 0] = (27 / 20) * S[5, 0] / l
            K_m[22, 1] = -297 / 40 * S[5, 0] / l
            K_m[22, 2] = (54 / 5) * S[5, 0] / l
            K_m[22, 3] = -189 / 40 * S[5, 0] / l
            K_m[22, 4] = (27 / 20) * S[5, 1] / l
            K_m[22, 5] = -297 / 40 * S[5, 1] / l
            K_m[22, 6] = (54 / 5) * S[5, 1] / l
            K_m[22, 7] = -189 / 40 * S[5, 1] / l
            K_m[22, 8] = (27 / 20) * S[5, 2] / l
            K_m[22, 9] = -297 / 40 * S[5, 2] / l
            K_m[22, 10] = (54 / 5) * S[5, 2] / l
            K_m[22, 11] = -189 / 40 * S[5, 2] / l
            K_m[22, 12] = (3 / 20) * (-2 * S[5, 1] * l + 9 * S[5, 3]) / l
            K_m[22, 13] = (27 / 80) * (3 * S[5, 1] * l - 22 * S[5, 3]) / l
            K_m[22, 14] = (54 / 5) * S[5, 3] / l
            K_m[22, 15] = (3 / 80) * (-19 * S[5, 1] * l - 126 * S[5, 3]) / l
            K_m[22, 16] = (3 / 20) * (2 * S[5, 0] * l + 9 * S[5, 4]) / l
            K_m[22, 17] = (27 / 80) * (-3 * S[5, 0] * l - 22 * S[5, 4]) / l
            K_m[22, 18] = (54 / 5) * S[5, 4] / l
            K_m[22, 19] = (3 / 80) * (19 * S[5, 0] * l - 126 * S[5, 4]) / l
            K_m[22, 20] = (27 / 20) * S[5, 5] / l
            K_m[22, 21] = -297 / 40 * S[5, 5] / l
            K_m[22, 22] = (54 / 5) * S[5, 5] / l
            K_m[22, 23] = -189 / 40 * S[5, 5] / l
            K_m[23, 0] = -13 / 40 * S[5, 0] / l
            K_m[23, 1] = (27 / 20) * S[5, 0] / l
            K_m[23, 2] = -189 / 40 * S[5, 0] / l
            K_m[23, 3] = (37 / 10) * S[5, 0] / l
            K_m[23, 4] = -13 / 40 * S[5, 1] / l
            K_m[23, 5] = (27 / 20) * S[5, 1] / l
            K_m[23, 6] = -189 / 40 * S[5, 1] / l
            K_m[23, 7] = (37 / 10) * S[5, 1] / l
            K_m[23, 8] = -13 / 40 * S[5, 2] / l
            K_m[23, 9] = (27 / 20) * S[5, 2] / l
            K_m[23, 10] = -189 / 40 * S[5, 2] / l
            K_m[23, 11] = (37 / 10) * S[5, 2] / l
            K_m[23, 12] = (1 / 80) * (7 * S[5, 1] * l - 26 * S[5, 3]) / l
            K_m[23, 13] = (3 / 20) * (-2 * S[5, 1] * l + 9 * S[5, 3]) / l
            K_m[23, 14] = (3 / 80) * (19 * S[5, 1] * l - 126 * S[5, 3]) / l
            K_m[23, 15] = (1 / 2) * S[5, 1] + (37 / 10) * S[5, 3] / l
            K_m[23, 16] = (1 / 80) * (-7 * S[5, 0] * l - 26 * S[5, 4]) / l
            K_m[23, 17] = (3 / 20) * (2 * S[5, 0] * l + 9 * S[5, 4]) / l
            K_m[23, 18] = (3 / 80) * (-19 * S[5, 0] * l - 126 * S[5, 4]) / l
            K_m[23, 19] = -1 / 2 * S[5, 0] + (37 / 10) * S[5, 4] / l
            K_m[23, 20] = -13 / 40 * S[5, 5] / l
            K_m[23, 21] = (27 / 20) * S[5, 5] / l
            K_m[23, 22] = -189 / 40 * S[5, 5] / l
            K_m[23, 23] = (37 / 10) * S[5, 5] / l

            self._element_stiffness_matrix = K_m.tocsc()

        return self._element_stiffness_matrix

    def B_matrix(self, z):
        """
        Returns the B matrix of the element at a given z coordinate. The B matrix is used to calculate
        the cross section displacements at one point from the local element displacement vector.

        Parameters
        ----------
        z: float
            The global position. Must be in the range of the element.

        Returns
        -------
        numpy.ndarray
            The B matrix.
        """
        dtype = self._dtype
        l = self.length

        assert 0 <= z <= l

        B = sp.dok_array((6, 24), dtype=dtype)

        B[0, 0] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[0, 1] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[0, 2] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[0, 3] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[0, 16] = -1 + (11 / 2) * z / l - 9 * z ** 2 / l ** 2 + (9 / 2) * z ** 3 / l ** 3
        B[0, 17] = (9 / 2) * z * (-2 * l ** 2 + 5 * l * z - 3 * z ** 2) / l ** 3
        B[0, 18] = (9 / 2) * z * (l ** 2 - 4 * l * z + 3 * z ** 2) / l ** 3
        B[0, 19] = (1 / 2) * z * (-2 * l ** 2 + 9 * l * z - 9 * z ** 2) / l ** 3
        B[1, 4] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[1, 5] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[1, 6] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[1, 7] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[1, 12] = 1 - 11 / 2 * z / l + 9 * z ** 2 / l ** 2 - 9 / 2 * z ** 3 / l ** 3
        B[1, 13] = (9 / 2) * z * (2 * l ** 2 - 5 * l * z + 3 * z ** 2) / l ** 3
        B[1, 14] = (9 / 2) * z * (-l ** 2 + 4 * l * z - 3 * z ** 2) / l ** 3
        B[1, 15] = (1 / 2) * z * (2 * l ** 2 - 9 * l * z + 9 * z ** 2) / l ** 3
        B[2, 8] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[2, 9] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[2, 10] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[2, 11] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[3, 12] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[3, 13] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[3, 14] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[3, 15] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[4, 16] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[4, 17] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[4, 18] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[4, 19] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3
        B[5, 20] = (1 / 2) * (-11 * l ** 2 + 36 * l * z - 27 * z ** 2) / l ** 3
        B[5, 21] = (9 / 2) * (2 * l ** 2 - 10 * l * z + 9 * z ** 2) / l ** 3
        B[5, 22] = (9 / 2) * (-l ** 2 + 8 * l * z - 9 * z ** 2) / l ** 3
        B[5, 23] = (l ** 2 - 9 * l * z + (27 / 2) * z ** 2) / l ** 3

        return B


class Beam:
    """
    Represents a 1D finite elements beam. The element stiffness is a
    7x7 TimoschenkoWithRestrainedWarpingStiffness matrix.

    Attributes
    ----------
    _elements: list(BeamElement)
        List of elements of the beam.
    _nodes: list(BeamNode)
        List of nodes of the beam.
    _beam_dof: int
        Number of total DOF of the beam.
    _A_elements: dict(BeamElement, scipy.sparse.csc_array)
        Matrices to get the element displacements for each element from the global displacements.
    """
    def __init__(
            self,
            z2_nodes,
            pos_nodes,
            element_stiffness_matrices,
            element_inertia_matrices,
            element_type: type[AbstractBeamElement],
            dtype=np.float64,
    ):
        """
        Constructor.

        Parameters
        ----------
        z2_nodes: list(float)
            List of the node positions on the beam axis.
        pos_nodes: list(Vector)
            List of the coordinates of the beam nodes.
        element_stiffness_matrices: list(np.ndarray)
            List of stiffness matrices of the elements.
        element_inertia_matrices: list(np.ndarray)
            List of inertia matrices of the elements.
        element_type
            Element type to use.
        """
        self._element_type = element_type
        self._dtype = dtype
        assert len(pos_nodes) == (len(element_stiffness_matrices) + 1)
        assert len(pos_nodes) == len(z2_nodes)
        num_elements = len(pos_nodes) - 1
        self._beam_dof = self.element_dof + (num_elements - 1) * self.dof_increment_per_element

        self._nodes = [BeamNode(z2_nodes[i], pos_nodes[i]) for i in range(num_elements + 1)]
        self._elements = [
            element_type(self.nodes[i], self.nodes[i + 1], element_stiffness_matrices[i], element_inertia_matrices[i], dtype=dtype)
            for i in range(num_elements)
        ]

        A = element_type.A_matrix()
        self._A_elements = {}
        for i in range(num_elements):
            A_element = sp.dok_array((self.element_dof, self.beam_dof), dtype=dtype)
            A_element[
                0:self.element_dof,
                i * self.dof_increment_per_element:i * self.dof_increment_per_element + self.element_dof
            ] = A
            self._A_elements[self.elements[i]] = A_element.tocsc()

        # for old shape function, check if all directions are [0, 0, 1]
        if element_type == BeamElementJung:
            for i in range(num_elements):
                if (self.elements[i].direction - Vector([0, 0, 1])).length > 1e-8:
                    raise RuntimeError("Not all elements have the right direction. Cannot use old shape functions.")

    @property
    def element_dof(self) -> int:
        """Number of DOF per element."""
        return self._element_type.element_dof()

    @property
    def dof_increment_per_element(self) -> int:
        """The increment of global DOF per new element."""
        return self._element_type.dof_increment_per_element()

    @property
    def elements(self):
        """list(BeamElement): List of elements of the beam."""
        return self._elements

    @property
    def nodes(self):
        """list(BeamNode): List of nodes of the beam."""
        return self._nodes

    @property
    def num_elements(self):
        """int: Number of elements of the beam."""
        return len(self._elements)

    @property
    def beam_dof(self):
        """int: Number of total DOF of the beam."""
        return self._beam_dof

    @property
    def A_elements(self):
        """
        dict(BeamElement, scipy.sparse.csc_array):
            Matrices to get the element displacements for each element from the global displacements.
        """
        return self._A_elements

    def _assemble_beam_stiffness_matrix(self):
        """
        Assemble the beam stiffness matrix from the element stiffness matrices.

        Returns
        -------
        scipy.sparse.csc_array
            Beam stiffness matrix.
        """
        dtype = self._dtype
        beam_dof = self.beam_dof
        K_beam = sp.csc_array((beam_dof, beam_dof), dtype=dtype)
        for element in self.elements:
            A_element = self.A_elements[element]
            K_element = element.element_stiffness_matrix
            if self._element_type.deformation_transformation():
                T_element = element.T_e_g
                K_beam += A_element.T @ T_element.T @ K_element @ T_element @ A_element
            else:
                K_beam += A_element.T @ K_element @ A_element
        return K_beam

    def _assemble_beam_mass_matrix(self):
        """
        Assemble the beam mass matrix from the element mass matrices.

        Returns
        -------
        scipy.sparse.csc_array
            Beam mass matrix.
        """
        dtype = self._dtype
        # TODO: for performance do the mass matrix calculation in the same loop as the stiffness matrix calculation
        beam_dof = self.beam_dof
        M_beam = sp.csc_array((beam_dof, beam_dof), dtype=dtype)
        for element in self.elements:
            A_element = self.A_elements[element]
            M_element = element.element_mass_matrix
            if self._element_type.deformation_transformation():
                T_element = element.T_e_g
                M_beam += A_element.T @ T_element.T @ M_element @ T_element @ A_element
            else:
                M_beam += A_element.T @ M_element @ A_element
        return M_beam

    def _assemble_line_load_vector_from_line_load_function(self, line_load_function):
        """
        Calculates the load vector for the beam from a given line load function.

        Parameters
        ----------
        line_load_function: function(dof, z)
            Line load of the node DOF 'dof' at the beam position 'z'.

        Returns
        -------
        scipy.sparse.csc_array
            Beam line load vector.
        """
        dtype = self._dtype
        R_L_beam = np.zeros(self.beam_dof, dtype=dtype)
        for element in self.elements:
            A_element = self.A_elements[element]
            R_L_element = element.node_loads_from_line_load_function(line_load_function)
            R_L_beam += A_element.T.dot(R_L_element)
        return sp.csc_array([R_L_beam], dtype=dtype).T

    def _get_permutation_matrix(self, u_beam_fixed):
        """
        Calculates the permutation matrix from a list of given displacements.

        Parameters
        ----------
        u_beam_fixed: list((int, float)
            The list of the given displacements: list(Index of the global DOF, displacement).

        Returns
        -------
        scipy.sparse.csc_array
            Permutation matrix.
        """
        dtype = self._dtype
        i_u_fixed = [i for i, u in u_beam_fixed]
        new_idx = i_u_fixed + [i for i in range(self.beam_dof) if i not in i_u_fixed]
        V = sp.dok_array((self.beam_dof, self.beam_dof), dtype=dtype)
        for i in range(self.beam_dof):
            V[i, new_idx[i]] = 1
        return V.tocsc()

    def _get_beam_submatrices(self, mat_beam, permutation_matrix, num_fixed_displacements):
        """
        Returns the sub-matrices of the beam stiffness matrix for a list of given displacements.

        Parameters
        ----------
        mat_beam: scipy.sparse.csc_array
            Beam matrix.
        permutation_matrix: scipy.sparse.csc_array
            The permutation matrix.
        num_fixed_displacements: int
            The number of the given displacements.

        Returns
        -------
        scipy.sparse.csc_array
            Left upper sub-matrices of the beam matrix.
        scipy.sparse.csc_array
            Right lower sub-matrices of the beam matrix.
        scipy.sparse.csc_array
            Right upper sub-matrices of the beam matrix.
        scipy.sparse.csc_array
            Left lower sub-matrices of the beam matrix.
        """
        beam_dof = self.beam_dof

        V = permutation_matrix
        mat_permutted = V @ mat_beam @ V.T

        mat_aa = mat_permutted[0:num_fixed_displacements, 0:num_fixed_displacements]
        mat_bb = mat_permutted[num_fixed_displacements:beam_dof, num_fixed_displacements:beam_dof]
        mat_ab = mat_permutted[0:num_fixed_displacements, num_fixed_displacements:beam_dof]
        mat_ba = mat_permutted[num_fixed_displacements:beam_dof, 0:num_fixed_displacements]

        # TODO: K_AB == K_BA.T

        return mat_aa, mat_bb, mat_ab, mat_ba

    def _global_data_from_node_data(self, node_data):
        """
        Returns the global data from the node data.

        Parameters
        ----------
        node_data: list((int, int, float)
            The list of the data of the node DOF's:
            list(index of the node (0 .. n_nodes-1), index of the node DOF (0 .. 6), data).

        Returns
        -------
        list((int, float)
            The list of the global data: list(index of the global DOF, data).
        """
        return [(node_idx * self.dof_increment_per_element + dof_idx, data) for node_idx, dof_idx, data in node_data]

    def get_load_vector(self, node_loads=None, line_load_function=None):
        """
        Returns the global load vector from given node loads and line loads.

        Parameters
        ----------
        node_loads: list((int, int, float)) (default: None)
            The list of the load of the node DOF's:
            list(index of the node (0 .. n_nodes-1), index of the node DOF (0 .. 6), load).
            None for no node loads.
        line_load_function: function(dof, z) (default: None)
            Line load of the node DOF 'dof' at the beam position 'z'.

        Returns
        -------
        scipy.sparse.csc_array
            Vector of the global node loads.
        """
        dtype = self._dtype

        # Point loads
        R_C = sp.dok_array((self.beam_dof, 1), dtype=dtype)
        if node_loads is not None:
            for node_idx, dof_idx, load in node_loads:
                R_C[node_idx * self.dof_increment_per_element + dof_idx, 0] = load
        R_C = R_C.tocsc()

        # Line loads
        if line_load_function is not None:
            R_L = self._assemble_line_load_vector_from_line_load_function(line_load_function)

        return (R_L + R_C) if (line_load_function is not None) else R_C

    def static_analysis(self, fixed_displacements, load_vectors):
        """
        Returns the unknown node displacements and the unknown node reactions for one boundary condition
        (given by fixed_displacements) and several load vectors.

        Parameters
        ----------
        fixed_displacements: list((int, int, float)
            The list of the given displacements:
            list(index of the node (0 .. n_nodes-1), index of the node DOF (0 .. 6), displacement).
        load_vectors: list(numpy.array)
            List of node load vectors.

        Returns
        -------
        list(np.ndarray)
            The global nodal displacement vectors for the load cases.
        list(dict((int, int): float)):
            Dict of the unknown node reactions:
            dict((index of the node (0 .. n_nodes-1), index of the node DOF (0 .. 6)): node reaction)
            for each load vector.
        """
        dtype = self._dtype

        u_beam_fixed = self._global_data_from_node_data(fixed_displacements)
        num_fixed_displacements = len(u_beam_fixed)
        V = self._get_permutation_matrix(u_beam_fixed)
        V_inv = V.T  # https://en.wikipedia.org/wiki/Permutation_matrix

        # TODO: u_beam_fixed muss set sein, keine doppelten Randbedingungen!
        u_a = np.array([[u for i, u in u_beam_fixed]], dtype=dtype).T
        K_beam = self._assemble_beam_stiffness_matrix()
        K_aa, K_bb, K_ab, K_ba = self._get_beam_submatrices(K_beam, V, num_fixed_displacements)

        if not len(load_vectors) == 1:
            # TODO: do not invert, solve directly
            K_bb_inv = sp_la.inv(K_bb)

        beam_displacements_list = []
        node_reactions_list = []
        # For each load vector
        for load_vector in load_vectors:
            R_p = V @ load_vector
            R_a = R_p[0:num_fixed_displacements]
            R_b = R_p[num_fixed_displacements:self.beam_dof]

            # Unknown node displacements
            b = R_b - K_ba.dot(u_a)
            if len(load_vectors) == 1:
                u_b = np.array([lgs_solve_sparse(K_bb, b, dtype=dtype)], dtype=dtype).T
            else:
                u_b = K_bb_inv @ b

            # Unknown node reactions
            R_r = K_aa.dot(u_a) + K_ab.dot(u_b) - R_a
            # R_r = V_inv * np.append(R_r_p, np.zeros((len(u_b), 1)), dtype=dtype)
            R_r_dict = {u_beam_fixed[i][0]: R_r[i, 0] for i in range(len(u_beam_fixed))}

            u_beam = V_inv.dot(np.vstack((u_a, u_b)))

            beam_displacements_list.append(u_beam)
            node_reactions_list.append({(global_node_idx // self.dof_increment_per_element,
                                         global_node_idx % self.dof_increment_per_element): node_reaction
                                        for global_node_idx, node_reaction in R_r_dict.items()})

        return beam_displacements_list, node_reactions_list

    def modal_analysis(self, fixed_displacements, num_modes=10):
        """
        Calculate the lowest eigenvalues and the eigenmodes from the stiffness and mass matrix of the beam:
        K x = lambda M x
        Fixed_displacements for the boundary conditions, empty list calculates free vibration modes.

        Parameters
        ----------
        fixed_displacements: list((int, int, float)
            The list of the given displacements:
            list(index of the node (0 .. n_nodes-1), index of the node DOF (0 .. 6), displacement).
        num_modes: int (default: 10)
            Number of eigenmodes to calculate. None for the max number of eigenmodes.

        Returns
        -------
        dict(float, numpy.array)
            Dict of the eigenmodes:
                Key: eigenvalue
                Value: Vector of the global node displacements of the corresponding eigenmode
        """
        # Set load case vector
        u_beam_fixed = self._global_data_from_node_data(fixed_displacements)
        num_fixed_displacements = len(u_beam_fixed)
        V = self._get_permutation_matrix(u_beam_fixed)
        V_inv = V.T  # https://en.wikipedia.org/wiki/Permutation_matrix

        # TODO: u_beam_fixed muss set sein, keine doppelten Randbedingungen!
        u_a = [u for i, u in u_beam_fixed]
        K_beam = self._assemble_beam_stiffness_matrix()
        K_aa, K_bb, K_ab, K_ba = self._get_beam_submatrices(K_beam, V, num_fixed_displacements)
        M_beam = self._assemble_beam_mass_matrix()
        M_aa, M_bb, M_ab, M_ba = self._get_beam_submatrices(M_beam, V, num_fixed_displacements)

        # sigma=0, which='LM': using shift-invert mode due to https://docs.scipy.org/doc/scipy/tutorial/arpack.html
        eigenvalues, eigenvectors = sp_la.eigsh(
            K_bb,
            (K_bb.shape[0] - 2) if num_modes is None else num_modes,
            M_bb,
            sigma=0,
            which='LM',
        )
        frequencies = np.real(np.sqrt(eigenvalues)) / (2 * np.pi)

        displacements = []
        for eigenvector in eigenvectors.T:
            u_b = np.real(eigenvector)
            u_beam = V_inv @ np.append(u_a, u_b)
            displacements.append(u_beam)

        assert len(frequencies) == len(displacements)

        return {frequencies[i]: displacements[i] for i in range(len(frequencies))}

    def element_and_element_displacement_vector_global_from_z2_coordinate(self, displacement_vector, z2):
        """
        Returns the six displacements of the beam at a given position from the beam displacement vector.

        Parameters
        ----------
        displacement_vector: np.ndarray
            The beam displacement vector.
        z2: float
            The global position where to calculate the displacements.

        Returns
        -------
        np.ndarray
            The element displacement vector in the global sorting.
        list(float)
            List of the six displacements.
        """
        elements = list(filter(lambda e: e.node1.z2 <= z2 <= e.node2.z2, self.elements))
        if len(elements) == 0:
            raise RuntimeError('No element found for the given z2-coordinate')
        #         if len(elements) > 1:
        #             raise RuntimeWarning('For the given z-coordinate more than one element is found')
        element = elements[0]
        element_first_node_idx = self.elements.index(element) * self.dof_increment_per_element
        element_displacement_vector_global = displacement_vector[
                                             element_first_node_idx:element_first_node_idx + self.element_dof]
        return element, element_displacement_vector_global

    def post_processing(self, displacement_vector, z2):
        """
        Returns the beam six displacements at a given position.

        Parameters
        ----------
        displacement_vector: numpy.array
            The global nodal displacement vector.
        z2: float
            The global position where to calculate the displacements. Must be in the range of the element.

        Returns
        -------
        list(float)
            List of the six beam displacements.
        TimoschenkoWithRestrainedWarpingDisplacements
            The cross section displacements.
        ClassicCrossSectionLoadsWithBimoment
            The cross section internal loads.
        """
        element, element_displacement_vector_global = self.element_and_element_displacement_vector_global_from_z2_coordinate(
            displacement_vector, z2)
        return element.post_processing(element_displacement_vector_global, z2)

    @staticmethod
    def create_beam(cross_section_data, z2_cross_sections, z2_beam_nodes, z2_2_point_wing, element_type: type[AbstractBeamElement], **kwargs):
        """
        Creates a PreDoCS beam model. The cross section calculation is performed at
        the given positions (z_cross_sections), the beam element properties are interpolated between these points
        at 'z_beam_nodes' using spline interpolation.

        Parameters
        ----------
        cross_section_data: list((ICrossSectionStiffness, ICrossSectionInertia))
            List of the cross section data.
        z_cross_sections: list(float)
            List of z-coordinates of the cross sections.
        z_beam_nodes: list(float)
            List of z-coordinates where the beam nodes should be placed.

        Returns
        -------
        Beam
            The PreDoCS beam.
        """
        pos_beam_nodes = [z2_2_point_wing(z2_i) for z2_i in z2_beam_nodes]

        # Create the beam
        z2_beam_elements = []
        for i in range(len(z2_beam_nodes) - 1):
            z2_beam_elements.append((z2_beam_nodes[i] + z2_beam_nodes[i + 1]) / 2)

        interpolated_stiffness_matrices, interpolated_inertia_matrices = \
            get_interpolated_stiffness_and_inertia_matrices(cross_section_data, z2_cross_sections, z2_beam_elements)  # TODO Modify for z2 coord

        beam = Beam(
            z2_beam_nodes,
            pos_beam_nodes,
            interpolated_stiffness_matrices,
            interpolated_inertia_matrices,
            element_type,
            **kwargs,
        )
        return beam

    @staticmethod
    def plot_stiffness_and_inertia(cs_data, z_cross_sections, beam_length, points_to_plot: int = 100,
                                   file_format_string: str = None, **kwargs):
        """
        Plots the stiffness and inertia distribution over the beam axis.

        Parameters
        ----------
        cs_data: list((ICrossSectionStiffness, ICrossSectionInertia))
            List of the cross section data.
        z_cross_sections: list(float)
            List of z-coordinates of the cross sections.
        beam_length: float
            Length of the beam
        points_to_plot: int
            Number of supporting point for the plot.
        file_format_string
            If set, the filename where to save the plots.
        """
        x = [beam_length / points_to_plot * i for i in range(points_to_plot + 1)]
        interpolated_stiffness_matrices, interpolated_inertia_matrices = \
            get_interpolated_stiffness_and_inertia_matrices(cs_data, z_cross_sections, x)

        for i in range(6):
            y = [interpolated_stiffness_matrices[ii][i, i] for ii in range(len(x))]
            plt.figure()
            plt.title('Mean Stiffness {}'.format(i + 1))
            plt.xlabel('Beam axis [m]')
            plt.ylabel('Stiffness')
            plt.plot(x, y)
            if file_format_string:
                plt.savefig(file_format_string.format(i))


def get_element_type_from_str(name: str) -> type[AbstractBeamElement]:
    match name:
        case 'jung':
            return BeamElementJung
        case '3node-warping':
            return BeamElement3NodeWithWarping
        case '3node-no-warping':
            return BeamElement3NodeWithoutWarping
        case '4node-warping':
            return BeamElement4NodeWithWarping
        case '4node-no-warping':
            return BeamElement4NodeWithoutWarping
        case _:
            raise ValueError(f'No element type found for "{name}".')
