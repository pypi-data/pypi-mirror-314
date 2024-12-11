"""
Abstract interfaces and interface classes for cross section displacements, loads and stiffness.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from abc import ABC, abstractmethod

import numpy as np

from PreDoCS.MaterialAnalysis.Interfaces import IShell
from PreDoCS.util.util import idx, get_principal_axis_angle
from PreDoCS.util.vector import Vector


class ICrossSectionProcessor(ABC):
    """
    Represents a cross section analysis.
    """

    @abstractmethod
    def force_update(self) -> None:
        """
        Forced update of the cached values.
        """
        pass

    @abstractmethod
    def _update_if_required(self) -> None:
        """
        Update the cached values.
        """
        pass

    @property
    @abstractmethod
    def discreet_geometry(self):
        """IDiscreetCrossSectionGeometry: The geometry for the cross section analysis."""
        pass
    
    @discreet_geometry.setter
    @abstractmethod
    def discreet_geometry(self, discreet_geometry):
        pass
    
    @property
    @abstractmethod
    def stiffness(self):
        """IStiffness: Returns the cross section stiffness."""
        pass
    
    @property
    @abstractmethod
    def inertia(self):
        """IInertia: Returns the cross section inertia."""
        pass
    
    @property
    @abstractmethod
    def elastic_center(self):
        """Vector: Elastic center of the cross section."""
        pass
    
    @property
    @abstractmethod
    def principal_axis_angle(self):
        """
        float:
            Angle between elastic coordinate system and principal axis coordinate system in RAD.
        """
        pass
    
    @property
    @abstractmethod
    def shear_center(self):
        """Vector: Shear center of the cross section."""
        pass
    
    @abstractmethod
    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.
        
        Parameters
        ----------
        internal_loads: IInternalLoads
            Cross section internal loads.
        
        Returns
        -------
        IDisplacements
            Displacements of the cross section.
        """
        pass
    
    @abstractmethod
    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.
        
        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.
        
        Returns
        -------
        dict(IElement, IElementLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        pass

    @abstractmethod
    def calc_element_load_states(self, displacements):
        """
        Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(IElement, IElementLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def calc_element_min_max_load_states(self, displacements):
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
        pass
    
    @abstractmethod
    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) for one load case.
        
        Parameters
        ----------
        internal_loads: IInternalLoads
            Cross section internal loads.
        
        Returns
        -------
        IDisplacements
            Displacements of the cross section.
        dict(IElement, IElementLoadState)
            The load states of the discreet elements of the cross section.
        """
        pass


class ICrossSectionLoads(ABC):
    """
    The internal loads of a cross section for a load case.
    """
    pass


class ICrossSectionDisplacements(ABC):
    """
    The displacements of a cross section for a load case.
    """
    pass


class INode(ABC):
    """
    A node of a discreet cross section. The node has no exact position and is used to describe the connection
    of the elements.
    """
    
    @abstractmethod
    def __hash__(self):
        """
        Returns
        -------
        int
            Returns a unique hash for the node.
        """
        pass
    
    @property
    @abstractmethod
    def id(self):
        """
        int:
            Returns the id of the node. Multiple nodes can have the same id.
        """
        pass
    
    @abstractmethod
    def __eq__(self, other):
        """
        Overrides the '=='-operator. Compares the id's of the nodes.
        
        Returns
        -------
        bool
            True, the id's of self and other are equal.
        """
        pass

    @property
    @abstractmethod
    def position(self):
        """
        Vector:
            Returns the position of the node in the discreet cross section.
        """
        pass


class IElement(ABC):
    """
    A discreet element of a cross section. The element is is made up of one material.
    Two nodes determine the orientation of an element. The nodes are in line with the elastic axis of the element.

    Coordinate system:
        * Length-direction (s): connection vector from the position of the first node
            to the position of the second node.
        * Depth-direction (z): The same as the cross section depth-direction (z).
        * Thickness-direction (n): perpendicular to length- and depth-direction.
    
    """
    @property
    @abstractmethod
    def id(self):
        """int: Returns the id of the element."""
        pass
    
    @property
    @abstractmethod
    def node1(self):
        """INode: Returns the first node of the element."""
        pass
    
    @property
    @abstractmethod
    def node2(self):
        """INode: Returns the second node of the element."""
        pass
    
    # @property
    # @abstractmethod
    # def node1_midsurface_position(self):
    #     """
    #     Vector:
    #         Returns position of the first node of the element on the element midsurface.
    #     """
    #     pass
    #
    # @property
    # @abstractmethod
    # def node2_midsurface_position(self):
    #     """
    #     Vector:
    #         Returns position of the second node of the element on the element midsurface.
    #     """
    #     pass
    #
    # @property
    # @abstractmethod
    # def midsurface_position(self):
    #     """Vector: Mean position of the element, on the midsurface."""
    #     pass
    
    @property
    @abstractmethod
    def position(self):
        """Vector: Mean position of the element (elastic center)."""
        pass
    
    @property
    @abstractmethod
    def angle_in_cross_section(self):
        """
        float:
            Returns the angle of the element in RAD in the cross section plane.
        """
        pass
    
    @property
    @abstractmethod
    def length_vector(self):
        """
        Vector:
            Returns the vector in length-direction of the element.
            The length of the vector equals the length of the element.
        """
        pass
    
    @property
    @abstractmethod
    def length(self):
        """float: Length of the element."""
        pass
    
    @property
    @abstractmethod
    def thickness_vector(self):
        """
        Vector:
            Returns the vector in thickness-direction of the element.
            The length of the vector equals the thickness of the element.
        """
        pass
    
    @property
    @abstractmethod
    def thickness(self):
        """float: Thickness of the element."""
        pass
    
    @property
    @abstractmethod
    def area(self):
        """float: Area of the element."""
        pass
    
    @property
    @abstractmethod
    def component(self):
        """Component: Component, the element belongs to."""
        pass
        
    @property
    @abstractmethod
    def shell(self) -> IShell:
        """Shell of the element."""
        pass


class IElementStiffness(ABC):
    """
    Stiffness for an IElement.
    """

    @property
    @abstractmethod
    def thickness(self):
        """float: Thickness of the material."""
        pass

    @abstractmethod
    def __eq__(self, other):
        """
        Parameters
        ----------
        other: IHomogenousMaterialData
            Other material data.

        Returns
        -------
        bool
            True, if the both materials are identical.
        """
        pass


class IElementLoadState(ABC):
    """
    Stain and stress state of an IElement.
    """

    @property
    @abstractmethod
    def strain_state(self):
        """dict(str, float): Stain state of an element."""
        pass

    @property
    @abstractmethod
    def stress_state(self):
        """dict(str, float): Stress state of an element."""
        pass


class ICrossSectionInertia(ABC):
    """
    Inertia properties of a cross section.
    """
    pass


class ICrossSectionStiffness(ABC):
    """
    Stiffness properties of a cross section.
    """
    pass


class CrossSectionInertia(ICrossSectionInertia):
    """
    Inertia properties of a cross section.

    Attributes
    ----------
    _inertia_matrix: numpy.ndarray
        6x6 inertia matrix.
    """
    def __init__(self, inertia_matrix):
        """
        Constructor.
        
        Parameters
        ----------
        inertia_matrix: numpy.ndarray
            6x6 inertia matrix.
        """
        assert isinstance(inertia_matrix, np.ndarray)
        assert inertia_matrix.shape == (6, 6)
        self._inertia_matrix = inertia_matrix
    
    @property
    def inertia_matrix(self) -> np.ndarray:
        """6x6 inertia matrix."""
        return self._inertia_matrix


# DISPLACEMENTS ########################################################################################################


class EulerBernoulliWithTorsionDisplacements(ICrossSectionDisplacements):
    """
    The Euler-Bernoulli displacements (extension and two curvatures) and twisting of a cross section for a load case.

    Extension:     w_0'
    Curvatures:    Theta_x', Theta_y'
    Twisting:      phi'

    Attributes
    ----------
    _extension: float
        Extension.
    _curvature: Vector
        The two curvatures.
    _twisting: float
        The twisting.
    """

    def __init__(self, extension, curvature, twisting):
        """
        Constructor.

        Parameters
        ----------
        extension: float
            Extension.
        curvatures: Vector
            The two curvatures.
        twisting: float
            The twisting.
        """
        assert isinstance(curvature, Vector)
        assert len(curvature) == 2
        self._extension = extension
        self._curvature = curvature
        self._twisting = twisting

    @property
    def extension(self):
        """float: Extension."""
        return self._extension

    @property
    def curvature(self):
        """Vector: The two curvatures."""
        return self._curvature

    @property
    def twisting(self):
        """float: The twisting."""
        return self._twisting


class TimoschenkoDisplacements(ICrossSectionDisplacements):
    """
    The Timoschenko displacements (extension, two shear strains and two curvatures),
    twisting of a cross section for a load case.

    Strain vector:           (gamma_xz, gamma_yz, w_0')
    Curvature vector:        (Theta_x', Theta_y', phi')

    Attributes
    ----------
    _strain: Vector
        Strain vector.
    _curvature: Vector
        Curvature vector.
    """

    def __init__(self, strain, curvature):
        """
        Constructor.

        Parameters
        ----------
        strain: Vector
            Strain vector.
        curvature: Vector
            Curvature vector.
        """
        assert isinstance(strain, Vector)
        assert len(strain) == 3
        assert isinstance(curvature, Vector)
        assert len(curvature) == 3
        self._strain = strain
        self._curvature = curvature

    @property
    def strain(self):
        """Vector: Strain vector."""
        return self._strain

    @property
    def curvature(self):
        """Vector: Curvature vector."""
        return self._curvature

    @staticmethod
    def from_list(displacement_list: list[float]):
        assert len(displacement_list) == 6
        return TimoschenkoDisplacements(
            Vector(displacement_list[0:3]),
            Vector(displacement_list[3:6])
        )

    def tolist(self):
        """
        Returns the cross section displacements as a list, order: strains and curvatures.

        Returns
        -------
        list(float)
            The cross section displacements as list.
        """
        return self._strain.tolist() + self._curvature.tolist()


class TimoschenkoWithRestrainedWarpingDisplacements(ICrossSectionDisplacements):
    """
    The Timoschenko displacements (extension, two shear strains and two curvatures),
    twisting and derivation of twisting of a cross section for a load case.

    Strain vector:           (gamma_xz, gamma_yz, w_0')
    Curvature vector:        (Theta_x', Theta_y', phi')
    Derivation of twisting:  phi''

    Attributes
    ----------
    _strain: Vector
        Strain vector.
    _curvature: Vector
        Curvature vector.
    _twisting_derivation: float
        Derivation of twisting.
    """

    def __init__(self, strain, curvature, twisting_derivation):
        """
        Constructor.

        Parameters
        ----------
        strain: Vector
            Strain vector.
        curvature: Vector
            Curvature vector.
        twisting_derivation: float
            Derivation of twisting.
        """
        assert isinstance(strain, Vector)
        assert len(strain) == 3
        assert isinstance(curvature, Vector)
        assert len(curvature) == 3
        self._strain = strain
        self._curvature = curvature
        self._twisting_derivation = twisting_derivation

    @property
    def strain(self):
        """Vector: Strain vector."""
        return self._strain

    @property
    def curvature(self):
        """Vector: Curvature vector."""
        return self._curvature

    @property
    def twisting_derivation(self):
        """float: Derivation of twisting."""
        return self._twisting_derivation

    @staticmethod
    def from_list(displacement_list: list[float]):
        assert len(displacement_list) == 7
        return TimoschenkoWithRestrainedWarpingDisplacements(
            Vector(displacement_list[0:3]),
            Vector(displacement_list[3:6]),
            displacement_list[6],
        )

    def tolist(self):
        """
        Returns the cross section displacements as a list, order: strains, curvatures and twisting derivation.

        Returns
        -------
        list(float)
            The cross section displacements as list.
        """
        return self._strain.tolist() + self._curvature.tolist() + [self._twisting_derivation]


# LOADS ################################################################################################################


class ClassicCrossSectionLoads(ICrossSectionLoads):
    """
    The classic internal loads (3 forces and 3 moments) of a cross section for a load case.

    Attributes
    ----------
    _forces: Vector
        Internal force vector (3 components).
    _moments: Vector
        Internal moment vector (3 components).
    """

    def __init__(self, forces, moments):
        """
        Constructor.

        Parameters
        ----------
        forces: Vector
            Internal force vector (3 components).
        moments: Vector
            Internal moment vector (3 components).
        """
        assert isinstance(forces, Vector)
        assert len(forces) == 3
        assert isinstance(moments, Vector)
        assert len(moments) == 3
        self._forces = forces
        self._moments = moments

    @property
    def forces(self):
        """Vector: Internal force vector (3 components)."""
        return self._forces

    @property
    def moments(self):
        """Vector: Internal moment vector (3 components)."""
        return self._moments

    @staticmethod
    def from_list(loads_list: list[float]):
        assert len(loads_list) == 6
        return ClassicCrossSectionLoads(
            Vector(loads_list[0:3]),
            Vector(loads_list[3:6]),
        )

    def tolist(self):
        """
        Returns the internal loads as a list, order: forces in x-, y- and z-direction,
        moments around the x-, y- and z-direction.

        Returns
        -------
        list(float)
            The internal loads as list.
        """
        return self._forces.tolist() + self._moments.tolist()


class ClassicCrossSectionLoadsWithBimoment(ClassicCrossSectionLoads):
    """
    The classic internal loads (3 forces, 3 moments) with bimoment of a cross section for a load case.

    Attributes
    ----------
    _bimoment: dype
        The bimoment through restrained warping.
    """

    def __init__(self, forces, moments, bimoment):
        """
        Constructor.

        Parameters
        ----------
        forces: Vector
            Internal force vector (3 components).
        moments: Vector
            Internal moment vector (3 components).
        bimoment: dype
            The bimoment through restrained warping.
        """
        super().__init__(forces, moments)
        self._bimoment = bimoment

    @property
    def bimoment(self):
        """float: The bimoment through restrained warping."""
        return self._bimoment

    @staticmethod
    def from_list(loads_list: list[float]):
        assert len(loads_list) == 7
        return ClassicCrossSectionLoadsWithBimoment(
            Vector(loads_list[0:3]),
            Vector(loads_list[3:6]),
            loads_list[6],
        )

    def tolist(self):
        """
        Returns the internal loads as a list, order: forces in x-, y- and z-direction,
        moments around the x-, y- and z-direction and bimoment.

        Returns
        -------
        list(float)
            The internal loads as list.
        """
        return self._forces.tolist() + self._moments.tolist() + [self._bimoment]


# STIFFNESS ############################################################################################################


class EulerBernoulliWithTorsionStiffness(ICrossSectionStiffness):
    """
    Stiffness properties of a cross section.
    Euler-Bernoulli bending (full 3x3-matrix) with a torsion stiffness.

    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        3x3 Euler-Bernoulli bending matrix.
    _GI_T: float
        Torsion stiffness.
    """

    def __init__(self, stiffness_matrix, GI_T):
        """
        Constructor.

        Parameters
        ----------
        stiffness_matrix: numpy.ndarray
            3x3 Euler-Bernoulli bending matrix.
        GI_T: float
            Torsion stiffness.
        """
        assert isinstance(stiffness_matrix, np.ndarray)
        assert stiffness_matrix.shape == (3, 3)
        self._stiffness_matrix = stiffness_matrix
        self._GI_T = GI_T

    @property
    def stiffness_matrix(self):
        """numpy.ndarray: 3x3 Euler-Bernoulli bending matrix."""
        return self._stiffness_matrix

    @property
    def GI_T(self):
        """float: Torsion stiffness.
        """
        return self._GI_T


class TimoschenkoStiffness(ICrossSectionStiffness):
    """
    Stiffness properties of a cross section (Timoschenko bending, full 6x6-matrix)

    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        6x6 stiffness matrix.
    """

    def __init__(self, stiffness_matrix):
        """
        Constructor.

        Parameters
        ----------
        stiffness_matrix: numpy.ndarray
            6x6 stiffness matrix.
        """
        assert isinstance(stiffness_matrix, np.ndarray)
        assert stiffness_matrix.shape == (6, 6)
        self._stiffness_matrix = stiffness_matrix

    @property
    def stiffness_matrix(self):
        """numpy.ndarray: 6x6 stiffness matrix."""
        return self._stiffness_matrix

    def get_euler_bernoulli_stiffness_matrix(self):
        """
        Returns
        -------
        numpy.ndarray
            3x3 Euler-Bernoulli stiffness matrix.
        """
        S = self._stiffness_matrix
        return np.array([[S[idx(33)], S[idx(34)], S[idx(35)]],
                         [S[idx(43)], S[idx(44)], S[idx(45)]],
                         [S[idx(53)], S[idx(54)], S[idx(55)]]])


class TimoschenkoWithRestrainedWarpingStiffness(ICrossSectionStiffness):
    """
    Stiffness properties of a cross section (Timoschenko bending with restained warping, full 7x7-matrix)

    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        7x7 stiffness matrix.
    """

    def __init__(self, stiffness_matrix):
        """
        Constructor.

        Parameters
        ----------
        stiffness_matrix: numpy.ndarray
            7x7 stiffness matrix.
        """
        assert isinstance(stiffness_matrix, np.ndarray)
        assert stiffness_matrix.shape == (7, 7)
        self._stiffness_matrix = stiffness_matrix

    @property
    def stiffness_matrix(self):
        """numpy.ndarray: 7x7 stiffness matrix."""
        return self._stiffness_matrix

    def get_euler_bernoulli_stiffness_matrix(self):
        """
        Returns
        -------
        numpy.ndarray
            3x3 Euler-Bernoulli stiffness matrix.
        """
        S = self._stiffness_matrix
        return np.array([[S[idx(33)], S[idx(34)], S[idx(35)]],
                         [S[idx(43)], S[idx(44)], S[idx(45)]],
                         [S[idx(53)], S[idx(54)], S[idx(55)]]])
