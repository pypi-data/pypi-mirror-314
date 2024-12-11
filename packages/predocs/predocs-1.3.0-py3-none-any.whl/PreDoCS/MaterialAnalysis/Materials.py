"""
This module provides classes for mechanical materials.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from PreDoCS.MaterialAnalysis.CLT import Laminate as Laminate_predocs
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElementStiffness, \
    CompositeElementStiffness, IsotropicElement, CompositeElement
from PreDoCS.MaterialAnalysis.Interfaces import IMaterial
from PreDoCS.util.Logging import get_module_logger

import logging
from dataclasses import dataclass, field
from typing import Union, Optional

import numpy as np

from PreDoCS.MaterialAnalysis.Interfaces import IMaterial
from PreDoCS.util.data import check_symmetric_exact, equal_content

log = logging.getLogger(__name__)


@dataclass
class MaterialFailureData:
    """
    Data class containing all material data used for the failure analysis.

    Attributes
    ----------
    max_stress
        The dict of the maximum allowable stresses of the material.
        Available keys:
            For tension:
                sigma_1t, sigma_2t sigma_3t
            For compression:
                sigma_1c, sigma_2c, sigma_3c
            For shear:
                sigma_12, sigma_13, sigma_23
    max_strain
        The dict of the maximum allowable strains of the material.
        Available keys:
            For tension:
                epsilon_1t, epsilon_2t epsilon_3t
            For compression:
                epsilon_1c, epsilon_2c, epsilon_3c
            For shear:
                epsilon_12, epsilon_13, epsilon_23
    """
    max_stress: dict[str, float] = field(default_factory=lambda: dict())
    max_strain: dict[str, float] = field(default_factory=lambda: dict())

    def set_failure_stresses(self, **kwargs: float):
        """
        This methods sets the maximum allowable stresses of the material.

        Parameters
        ----------
        kwargs
            See max_stress property.
        """
        self.max_stress = {k: v for k, v in kwargs.items() if v is not None}

    def set_failure_strains(self, **kwargs: float):
        """
        This methods sets the maximum allowable strains of the material.

        Parameters
        ----------
        kwargs
            See max_strain property.
        """
        self.max_strain = {k: v for k, v in kwargs.items() if v is not None}

    # def set_failure_stresses(self, sigma_11, sigma_12):
    #     """
    #     This methods sets the allowable equivalent stress.
    #
    #     Parameters
    #     ----------
    #
    #     sigma : float
    #         The allowable stress
    #
    #
    #     """
    #     self.sigma_1c = sigma_11 if sigma_11 else None
    #     self.sigma_2c = sigma_11 if sigma_11 else None
    #     self.sigma_3c = sigma_11 if sigma_11 else None
    #     self.sigma_1t = sigma_11 if sigma_11 else None
    #     self.sigma_2t = sigma_11 if sigma_11 else None
    #     self.sigma_3t = sigma_11 if sigma_11 else None
    #     self.sigma_12 = sigma_12 if sigma_12 else None
    #     self.sigma_13 = sigma_12 if sigma_12 else None
    #     self.sigma_23 = sigma_12 if sigma_12 else None
    #
    # def set_failure_strains(self, epsilon, epsilon_t=None, gamma=None):
    #     """
    #     This methods sets the allowable equivalent strain for compression and
    #     if given a different value for tension.
    #
    #     Parameters
    #     ----------
    #
    #     epsilon_t : float
    #         allowable strain for tension (Optional)
    #     epsilon : float
    #         The allowable strain
    #     gamma: float
    #         allowable shear strain
    #     """
    #     if epsilon_t is None:
    #         epsilon_t = epsilon
    #     if gamma is None:
    #         if epsilon is None:
    #             gamma = None
    #         else:
    #             gamma = epsilon / 2
    #     self.epsilon_1c = epsilon
    #     self.epsilon_2c = epsilon
    #     self.epsilon_3c = epsilon
    #     self.epsilon_1t = epsilon_t
    #     self.epsilon_2t = epsilon_t
    #     self.epsilon_3t = epsilon_t
    #     self.epsilon_12 = gamma
    #     self.epsilon_23 = gamma


class Anisotropic(IMaterial):
    """
    This class implements Hookes Law for anisotropic materials, see [Jones1999]_, pp. 60.

    It follows the Voight notation for second-order tensors.

    Interesting urls:

    #. https://en.wikipedia.org/wiki/Voigt_notation
    #. https://en.wikipedia.org/wiki/Cauchy_stress_tensor
    #. https://en.wikipedia.org/wiki/Hooke%27s_law#Anisotropic_materials
    #. http://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke.cfm#GeneralizedHooke

    """
    def __init__(
            self,
            compliance_matrix: np.ndarray,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        The class is instantiated with 21 stiffness defining parameters, the name and the density.

        Parameters
        ----------
        compliance_matrix
            The components of the compliance matrix (6x6) :math:`\\mathbf{S}=\\mathbf{C}^{-1}`.
            See [Jones1999]_, pp. 60.
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.
        """
        self._dtype = dtype
        self._name = name
        self._uid = uid
        self._density = density

        self._compliance_matrix = None
        self._stiffness_matrix = None
        self._membrane_stiffness_matrix = None
        self._transverse_stiffness_matrix = None

        self._calc_stiffness(compliance_matrix)

        self._failure_data = None

    @property
    def name(self) -> Union[str, None]:
        return self._name

    @name.setter
    def name(self, value: Union[str, None]):
        self._name = str(value) if value is not None else None

    @property
    def uid(self) -> Union[str, None]:
        return self._uid

    @uid.setter
    def uid(self, value: Union[str, None]):
        self._uid = str(value) if value is not None else None

    @property
    def density(self) -> Union[float, None]:
        return self._density

    @property
    def failure_data(self) -> object:
        return self._failure_data

    @failure_data.setter
    def failure_data(self, value: object):
        self._failure_data = value

    def equal_content(self, other) -> bool:
        """
        Compares the content of this object with another.

        Parameters
        ----------
        other
            Other object.

        Returns
        -------
        True, if both objects have the same content.
        """
        return equal_content(self, other)

    @property
    def compliance_matrix(self) -> np.ndarray:
        """
        Yields the material compliance matrix (:math:`\\mathbf{S}=\\mathbf{C}^{-1}`, see [Jones1999]_, pp. 60).

        Returns
        -------
        np.ndarray (6,6)
            The compliance matrix.
        """
        return self._compliance_matrix

    @property
    def stiffness_matrix(self) -> np.ndarray:
        """
        Yields the material stiffness matrix (:math:`\\mathbf{C}=\\mathbf{S}^{-1}`, see [Jones1999]_, pp. 58).

        Returns
        -------
        np.ndarray (6,6)
            The stiffness matrix.
        """
        return self._stiffness_matrix

    @property
    def membrane_stiffness_matrix(self) -> np.ndarray:
        """
        Yields the disk stiffness matrix from the material :math:`\\mathbf{Q}`.
        It is formed under the assumption of plane stress :math:`\\sigma_{3}=0, \\tau_{23}=0, \\tua_{31}=0`
        (see [Jones1999]_, pp. 70).

        Returns
        -------
        np.ndarray (3,3)
            The membrane stiffness matrix.
        """
        return self._membrane_stiffness_matrix

    @property
    def transverse_stiffness_matrix(self) -> np.ndarray:
        """
        TODO: tbd.

        Returns
        -------
        np.ndarray (2,2)
            The transverse stiffness matrix."""
        return self._transverse_stiffness_matrix

    def _calc_stiffness(self, compliance_matrix: np.ndarray):
        """
        Calculates all stiffness matrices from a given compliance matrix.

        Parameters
        ----------
        compliance_matrix
            The components of the compliance matrix (6x6) :math:`\\mathbf{S}=\\mathbf{C}^{-1}`.
            See [Jones1999]_, pp. 60.
        """
        if not check_symmetric_exact(compliance_matrix):
            log.warning(f'Material {self}: the stiffness and compliance matrix have to be symmetric!')

        if not np.all(np.linalg.eigvals(compliance_matrix) > 0):
            log.warning(f'Material {self}: the stiffness and compliance matrix have to be positive definite!')

        self._compliance_matrix = compliance_matrix

        # Stiffness matrix
        self._stiffness_matrix = np.linalg.inv(compliance_matrix)

        # Membrane stiffness
        indices_membrane = np.array([0, 1, 5], dtype=np.intp)
        self._membrane_stiffness_matrix = np.linalg.inv(compliance_matrix[indices_membrane[:, np.newaxis], indices_membrane])

        # Transverse stiffness
        indices_transverse = np.array([3, 4], dtype=np.intp)
        self._transverse_stiffness_matrix = self._stiffness_matrix[indices_transverse[:, np.newaxis], indices_transverse]


class Orthotropic(Anisotropic):
    """
    First, please see the Anisotropic material.

    This class represents an orthotropic material.
    The material is assumed as homogenous and its mechanical behaviour can be described by nine independent constants:
    three elastic moduli, three shear moduli and three Poisson's ratios.

    See [Jones1999]_, pp. 60.

    Further interesting reads:

    #. http://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke_orthotropic.cfm

    """
    def __init__(
            self,
            E_11,
            E_22,
            E_33,
            nu_12,
            nu_23,
            nu_13,
            G_12,
            G_23,
            G_13,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        The class is instantiated with the 9 orthotropic engineering constants.

        Parameters
        ----------
        E_11 : float
            The necessary youngs modulus component needed to construct an orthotropic
            material.
            1 - direction
            must be positive
        E_22 : float
            The necessary youngs modulus component needed to construct an orthotropic
            material.
            2 - direction
            must be positive
        E_33 : float
            The necessary youngs modulus component needed to construct an orthotropic
            material.
            3 - direction
            must be positive
        nu_12 : float
            Poisson's ratio in 1-2 direction
        nu_23 : float
            Poisson's ratio in 2-3 direction
        nu_13 : float
            Poisson's ratio in 1-3 direction
        G_12 : float
            Shear modulus
            1-2 direction
            must be positive
        G_23 : float
            Shear modulus
            2-3 direction
            must be positive
        G_13 : float
            Shear modulus
            1-3 direction
            must be positive
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.
        """
        # Compliance matrix, see [Jones1999]_, pp. 64
        S11 = 1 / E_11
        S12 = -nu_12 / E_11
        S13 = -nu_13 / E_11
        S22 = 1 / E_22
        S23 = -nu_23 / E_22
        S33 = 1 / E_33
        S44 = 1 / (G_23)
        S55 = 1 / (G_13)
        S66 = 1 / (G_12)
        compliance_matrix = self.assemble_compliance_stiffness_matrix(
            S11, S12, S13, S22, S23, S33, S44, S55, S66, dtype=dtype,
        )

        super().__init__(
            compliance_matrix=compliance_matrix,
            name=name,
            uid=uid,
            density=density,
            dtype=dtype,
        )
        # self.raw_data = {
        #     'E_11': E_11,
        #     'E_22': E_22,
        #     'E_33': E_33,
        #     'nu_12': nu_12,
        #     'nu_23': nu_23,
        #     'nu_13': nu_13,
        #     'G_12': G_12,
        #     'G_23': G_23,
        #     'G_13': G_13
        # }

    # @staticmethod
    # def stiffness2compliance(C11, C12, C13, C22, C23, C33, C44, C55, C66):
    #     """
    #     Inverts Orthotropic stiffness analytically, Jones1999 Equation 2.34
    #
    #     Parameters
    #     ----------
    #     Cij: float
    #         Non zero entries of the stiffness matrix, also known as Kij
    #
    #     Returns
    #     -------
    #     Sij: float
    #         Entries of the compliance matrix
    #     """
    #     C = C11 * C22 * C33 - C11 * C23 ** 2 - C22 * C13 ** 2 - C33 * C12 ** 2 + 2 * C12 * C23 * C13
    #
    #     S11 = (C22 * C33 - C23 ** 2) / C
    #     S12 = (C12 * C23 - C12 * C33) / C
    #     S13 = (C12 * C23 - C13 * C22) / C
    #     S22 = (C33 * C11 - C13 ** 2) / C
    #     S23 = (C12 * C13 - C23 * C11) / C
    #     S33 = (C11 * C22 - C12 ** 2) / C
    #     S44 = (1 / C44)
    #     S55 = (1 / C55)
    #     S66 = (1 / C66)
    #
    #     return S11, S12, S13, S22, S23, S33, S44, S55, S66
    #
    # def compliance2stiffness(self, S11, S12, S13, S22, S23, S33, S44, S55, S66):
    #     """
    #     Inverts Orthotropic compliance analytically, Jones1999 Equation 2.34
    #
    #     "In Equation (2.34), the symbols C and S can be interchanged everywhere
    #     to provide the converse relationship" Jones 1999
    #
    #     Parameters
    #     ----------
    #     Sij: float
    #         Entries of the compliance matrix
    #
    #     Returns
    #     -------
    #     Cij: float
    #         Non zero entries of the stiffness matrix, also known as Kij
    #     """
    #     C11, C12, C13, C22, C23, C33, C44, C55, C66 = self.stiffness2compliance(S11, S12, S13, S22, S23, S33, S44, S55,
    #                                                                             S66)
    #
    #     return C11, C12, C13, C22, C23, C33, C44, C55, C66

    @classmethod
    def assemble_compliance_stiffness_matrix(cls, S11, S12, S13, S22, S23, S33, S44, S55, S66, dtype=np.float64) -> np.ndarray:
        """
        Returns a compliance or stiffness matrix of an orthotropic material from the given non zero elements.

        See [Jones1999]_, p. 64, eq. 2.25.

        Parameters
        ----------
        Sij: float
            Non zero entries of the compliance or stiffness matrix.

        Returns
        -------
        np.ndarray (6,6)
            The compliance or stiffness matrix.
        """
        return np.array([
            [S11, S12, S13, 0, 0, 0],
            [S12, S22, S23, 0, 0, 0],
            [S13, S23, S33, 0, 0, 0],
            [0, 0, 0, S44, 0, 0],
            [0, 0, 0, 0, S55, 0],
            [0, 0, 0, 0, 0, S66],
        ], dtype=dtype)

    @classmethod
    def disassemble_compliance_stiffness_matrix(cls, matrix: np.ndarray):
        """
        Returns non zero elements of a compliance or stiffness matrix of an orthotropic material.

        See [Jones1999]_, p. 64, eq. 2.25.

        Parameters
        ----------
        np.ndarray (6,6)
            The compliance or stiffness matrix.

        Returns
        -------
        Sij: float
            Non zero entries of the compliance or stiffness matrix.
        """
        S11 = matrix[0, 0]
        S12 = matrix[0, 1]
        S13 = matrix[0, 2]
        S22 = matrix[1, 1]
        S23 = matrix[1, 2]
        S33 = matrix[2, 2]
        S44 = matrix[3, 3]
        S55 = matrix[4, 4]
        S66 = matrix[5, 5]
        return S11, S12, S13, S22, S23, S33, S44, S55, S66

    @classmethod
    def compliance2engineering(cls, S11, S12, S13, S22, S23, S33, S44, S55, S66):
        """
        Calculates the engineering constants (Young's modulus etc.) from a compliance matrix of an orthotropic material.

        See [Jones1999]_, p. 64, eq. 2.25.

        Parameters
        ----------
        Sij: float
            Non zero entries of the compliance matrix

        Returns
        -------
        E: float
            Young's modulus
        G: float
            Shear modulus
        nu: float
            Poissons Ratio
        """
        E11 = 1 / S11
        E22 = 1 / S22
        E33 = 1 / S33
        G12 = 1 / S66
        G23 = 1 / S44
        G13 = 1 / S55

        nu12 = -E11 * S12
        nu23 = -E22 * S23
        nu13 = -E11 * S13

        return E11, E22, E33, nu23, nu13, nu12, G23, G13, G12

    @classmethod
    def init_from_stiffness(
            cls,
            C11, C12, C13, C22, C23, C33, C44, C55, C66,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        This method initiates an instance of class Orthotropic from a given stiffness matrix.

        This method was initially written for instantiating a Material from a CPACS import.

        Parameters
        ----------
        Cij: float
            Entries of the stiffness matrix.
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.

        Returns
        -------
        Orthotropic
            Instance of Orthotropic material
        """
        # Stiffness matrix
        stiffness_matrix = cls.assemble_compliance_stiffness_matrix(
            C11, C12, C13, C22, C23, C33, C44, C55, C66, dtype=dtype,
        )

        # Compliance matrix
        compliance_matrix = np.linalg.inv(stiffness_matrix)
        S11, S12, S13, S22, S23, S33, S44, S55, S66 = cls.disassemble_compliance_stiffness_matrix(compliance_matrix)

        # Engineering constants
        E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = \
            cls.compliance2engineering(S11, S12, S13, S22, S23, S33, S44, S55, S66)

        orthotropic_material = Orthotropic(
            E_11=E11, E_22=E22, E_33=E33,
            nu_12=nu12, nu_23=nu23, nu_13=nu13,
            G_12=G12, G_23=G23, G_13=G13,
            name=name, uid=uid, density=density, dtype=dtype,
        )

        return orthotropic_material

    @property
    def engineering_constants(self):
        """
        Returns the engineering constants.

        Returns
        -------
        E: float
            Young's modulus
        G: float
            Shear modulus
        nu: float
            Poissons Ratio
        """
        # Compliance matrix
        S11, S12, S13, S22, S23, S33, S44, S55, S66 = self.disassemble_compliance_stiffness_matrix(self._compliance_matrix)

        # Engineering constants
        E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = \
            self.compliance2engineering(S11, S12, S13, S22, S23, S33, S44, S55, S66)

        return E11, E22, E33, nu23, nu13, nu12, G23, G13, G12


class Transverse_Isotropic(Orthotropic):
    """
    First, please see the Anisotropic material.

    See [Jones1999]_, pp. 60.

    Further interesting reads:

    #. Schürmann (S. 182)
    #. http://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke_iso_transverse.cfm
    #. https://de.wikipedia.org/wiki/Transversale_Isotropie

    """
    def __init__(
            self,
            E_11, E_22, nu_12, nu_23, G_21,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        The class is instantiated with 5 engineering constants needed to
        construct a transverse isotropic material.

        Parameters
        ----------
        E_11 : float (must be positive)
            The youngs modulus in 11 - direction
        E_22 : float (must be positive)
            The youngs modulus in 22 - direction
        nu_12 : float
            In-plane Poisson's ratio
        nu_23 : float
            Poisson's ratio (has no impact for 2d-analysis)
        G_21 : float (must be positive)
            In-plane Shear modulus
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.
        """
        # See [Schuermann2007]_, pp. 183, eq. 7.6
        super().__init__(
            E_11=E_11,
            E_22=E_22,
            E_33=E_22,
            nu_23=nu_23,
            nu_13=nu_12,
            nu_12=nu_12,
            G_23=E_22 / (2 * (1 + nu_23)),
            G_13=G_21,
            G_12=G_21,
            name=name,
            uid=uid,
            density=density,
            dtype=dtype,
        )

    @classmethod
    def init_from_stiffness(
            cls,
            C11, C12, C22, C23, C66,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        This method initiates an instance of class Transverse_Isotropic from a given stiffness matrix.

        Parameters
        ----------
        Cij: float
            Entries of the stiffness matrix.
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.

        Returns
        -------
        Transverse_Isotropic
            Instance of Transverse_Isotropic material.
        """
        # Stiffness matrix
        C44 = (C22 - C23) / 2
        stiffness_matrix = cls.assemble_compliance_stiffness_matrix(
            C11, C12, C12, C22, C23, C22, C44, C66, C66, dtype=dtype,
        )

        # Compliance matrix
        compliance_matrix = np.linalg.inv(stiffness_matrix)
        S11, S12, S13, S22, S23, S33, S44, S55, S66 = cls.disassemble_compliance_stiffness_matrix(compliance_matrix)

        # Engineering constants
        E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = \
            cls.compliance2engineering(S11, S12, S13, S22, S23, S33, S44, S55, S66)

        transverse_isotropic_material = Transverse_Isotropic(
            E_11=E11, E_22=E22,
            nu_12=nu12, nu_23=nu23,
            G_21=G12,
            name=name, uid=uid, density=density, dtype=dtype,
        )

        return transverse_isotropic_material


class Isotropic(Orthotropic):
    """
    First, please see the Anisotropic material.

    See [Jones1999]_, pp. 60.

    Interesting reads:

    #. http://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke_isotropic.cfm
    """
    def __init__(
            self,
            E, nu,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        The class is instantiated with 2 engineering constants needed to
        construct an isotropic material.

        Parameters
        ----------
        E : float (must be positive)
            The youngs modulus needed to construct an orthotropic material.
        nu : float
            Poisson's ratio. nu has to be in ]-1, 0.5[, [Jones1999]_, eq. 2.43.
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.

        """
        if not (-1 < nu < 0.5):
            log.warning(f'nu has to be in ]-1, 0.5[, Jones 1999, eq. 2.43 but is {nu} for material {self}.')

        G = E / (2 * (1 + nu))
        super().__init__(
            E_11=E,
            E_22=E,
            E_33=E,
            nu_12=nu,
            nu_23=nu,
            nu_13=nu,
            G_12=G,
            G_23=G,
            G_13=G,
            name=name,
            uid=uid,
            density=density,
            dtype=dtype,
        )

    @classmethod
    def init_from_stiffness(
            cls,
            C11, C12,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            density: float = None,
            dtype=np.float64,
    ):
        """
        This method initiates an instance of class Isotropic from a given stiffness matrix.

        [Jones1999]_, p. 60, eq. 2.17

        Parameters
        ----------
        Cij: float
            Entries of the stiffness matrix.
        name
            Representing the working name of the material.
        uid
            uID of the material.
        density
            The density of the material.

        Returns
        -------
        Isotropic
            Instance of Isotropic material
        """
        # Stiffness matrix
        C13 = C12
        C22 = C11
        C23 = C12
        C33 = C11
        C44 = (C11 - C12) / 2
        C55 = (C11 - C12) / 2
        C66 = (C11 - C12) / 2
        stiffness_matrix = cls.assemble_compliance_stiffness_matrix(
            C11, C12, C13, C22, C23, C33, C44, C55, C66, dtype=dtype,
        )

        # Compliance matrix
        compliance_matrix = np.linalg.inv(stiffness_matrix)
        S11, S12, S13, S22, S23, S33, S44, S55, S66 = cls.disassemble_compliance_stiffness_matrix(compliance_matrix)

        # Engineering constants
        E11, E22, E33, nu23, nu13, nu12, G23, G13, G12 = \
            cls.compliance2engineering(S11, S12, S13, S22, S23, S33, S44, S55, S66)

        isotropic_material = Isotropic(
            E=E11, nu=nu12,
            name=name, uid=uid, density=density, dtype=dtype,
        )

        return isotropic_material
