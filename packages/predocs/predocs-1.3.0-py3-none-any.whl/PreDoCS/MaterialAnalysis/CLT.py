"""
This module is an implementation of the classical laminate theory (CLT) with an extension for transverse shear stiffness.
Further information are available at [Jones1999]_ and [Schürmann2007]_.

The laminate is build of plys of orthotropic material stacked together.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import numpy as np
from numpy import sin, cos

from typing import Union, Optional

from PreDoCS.MaterialAnalysis.Interfaces import IMaterial, Shell
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.data import equal_content

log = get_module_logger(__name__)


class Ply:
    """
    This class represents an orthotropic ply. The ply is assumed as homogenous and its mechanical behaviour can be described
    by nine independent constants: three elastic moduli, three shear moduli and three Poisson's ratios.
    The ply-coordinate-system is the 1-2-3-coordinate system. The 3-direction is the thickness direction of the ply,
    the 1- and 2-directions are the orthotropic axis. Further information at [Jones1999]_, pp. 63.
    The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    The stiffness matrix is splitted in two parts: the first part for the CLT (disk load only) and the second part for transverse shear stiffness.
    """
    def __init__(
            self,
            material: IMaterial,
            thickness: float,
            orientation: float,
            name: Optional[str] = 'default name',
            ply_index_global: Optional[int] = None,
            labels: Optional[list] = None,
            dtype=np.float64,
    ):
        """
        Constructor.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        material
            The material of the ply.
        thickness
            The ply thickness.
        orientation
            The rotation angle of the ply around the normal direction in degree.
        labels
            Labels of the ply to identify special plys, i.e. the sandwich core.
        """
        self._name = name
        self._material = material
        self._thickness = thickness
        self._orientation = orientation
        self._ply_index_global = ply_index_global
        self._labels = labels
        self._dtype = dtype

        # self.sigma_1t = None
        # self.sigma_2t = None
        # self.sigma_3t = None
        # self.sigma_1c = None
        # self.sigma_2c = None
        # self.sigma_3c = None
        # self.sigma_12 = None
        # self.sigma_13 = None
        # self.sigma_23 = None
        #
        # self.epsilon_1t = None
        # self.epsilon_2t = None
        # self.epsilon_3t = None
        # self.epsilon_1c = None
        # self.epsilon_2c = None
        # self.epsilon_3c = None
        # self.epsilon_12 = None
    #
    # @staticmethod
    # def from_engineering_constants_orthotropic_for_becas(name, density, E1, E2, E3, nu12, nu13, nu23, G12, G31, G23):
    #     """
    #     Creates ply from given engineering constants of an orthotropic material.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    #     Additionally saves the engineering constants for the BECAS calculations to the object.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     E1: float
    #         Elastic modulus in 1-direction.
    #     E2: float
    #         Elastic modulus in 2-direction.
    #     E3: float
    #         Elastic modulus in 3-direction.
    #     nu12: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension in 2-direction for an axial extension in 1-direction.
    #     nu13: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension in 3-direction for an axial extension in 1-direction.
    #     nu23: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension in 3-direction for an axial extension in 2-direction.
    #     G12: float
    #         Shear modulus in the 1-2-plane.
    #     G31: float
    #         Shear modulus in the 3-1-plane.
    #     G23: float
    #         Shear modulus in the 2-3-plane.
    #     """
    #     ply = Ply.from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G12, G31, G23)
    #     ply.E1 = E1
    #     ply.E2 = E2
    #     ply.E3 = E3
    #     ply.nu12 = nu12
    #     ply.nu13 = nu13
    #     ply.nu23 = nu23
    #     ply.G12 = G12
    #     ply.G31 = G31
    #     ply.G23 = G23
    #     return ply
    #
    # @staticmethod
    # def from_engineering_constants_transverse_isotropic_for_becas(name, density, E1, E2, nu12, nu22, G21):
    #     """
    #     Creates ply from given engineering constants of a transverse isotropic material.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    #     Additionally saves the engineering constants for the BECAS calculations to the object.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     E1: float
    #         Elastic modulus in 1-direction.
    #     E2: float
    #         Elastic modulus normal to the 1-direction.
    #     nu12: float
    #         Major Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to 1-direction for an axial extension in 1-direction.
    #     nu22: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to the 1-direction for an axial extension normal to the 1-direction.
    #     G21: float
    #         Shear modulus in a plane containing the 1-axis.
    #     density: float
    #         Mass density of the ply.
    #     """
    #     E3 = E2
    #     nu13 = nu12
    #     nu23 = nu22
    #     G22 = E2/(2*(1+nu22))
    #     G23 = G22
    #     G12 = G21
    #     G31 = G21
    #
    #     ply = Ply.from_engineering_constants_transverse_isotropic(name, density, E1, E2, nu12, nu22, G21)
    #     ply.E1 = E1
    #     ply.E2 = E2
    #     ply.E3 = E3
    #     ply.nu12 = nu12
    #     ply.nu13 = nu13
    #     ply.nu23 = nu23
    #     ply.G12 = G12
    #     ply.G31 = G31
    #     ply.G23 = G23
    #     return ply
    #
    # @staticmethod
    # def from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G12, G31, G23):
    #     """
    #     Creates ply from given engineering constants of an orthotropic material.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     E1: float
    #         Elastic modulus in 1-direction.
    #     E2: float
    #         Elastic modulus in 2-direction.
    #     nu12: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension in 2-direction for an axial extension in 1-direction.
    #     G12: float
    #         Shear modulus in the 1-2-plane.
    #     G31: float
    #         Shear modulus in the 3-1-plane.
    #     G23: float
    #         Shear modulus in the 2-3-plane.
    #     """
    #     Q11 = -E1**2/(E2*nu12**2 - E1)
    #     Q22 = -E1*E2/(E2*nu12**2 - E1)
    #     Q12 = -E1*E2*nu12/(E2*nu12**2 - E1)
    #     Q44 = G23
    #     Q55 = G31
    #     Q66 = G12
    #
    #     Q_c = np.array([[Q11, Q12,  0.],
    #                     [Q12, Q22,  0.],
    #                     [ 0.,  0., Q66]], dtype=self._dtype)
    #     Q_t = np.array([[Q44,  0.],
    #                     [ 0., Q55]], dtype=self._dtype)
    #
    #     return Ply(name, density, Q_c, Q_t)
    #
    # @staticmethod
    # def from_stiffness_matrix_orthotropic(name, density, C11, C22, C33, C44, C55, C66, C12, C13, C23):
    #     """
    #     Creates ply from given stiffness matrix C of an orthotropic material, see [Jones1999]_, pp. 59.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     Cxy: float
    #         Component xy of the stiffness matrix.
    #     """
    #     Q11 = C11 - C13**2/C33
    #     Q22 = C22 - C23**2/C33
    #     Q12 = C12 - C13*C23/C33
    #     Q_c = np.array([[Q11, Q12,  0.],
    #                     [Q12, Q22,  0.],
    #                     [ 0.,  0., C66]], dtype=self._dtype)
    #     Q_t = np.array([[C44,  0.],
    #                     [ 0., C55]], dtype=self._dtype)
    #     return Ply(name, density, Q_c, Q_t)
    #
    # @staticmethod
    # def from_engineering_constants_transverse_isotropic(name, density, E1, E2, nu12, nu22, G21):
    #     """
    #     Creates ply from given engineering constants of a transverse isotropic material.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, p. 70.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     E1: float
    #         Elastic modulus in 1-direction.
    #     E2: float
    #         Elastic modulus normal to the 1-direction.
    #     nu12: float
    #         Major Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to 1-direction for an axial extension in 1-direction.
    #     nu22: float
    #         Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to the 1-direction for an axial extension normal to the 1-direction.
    #     G21: float
    #         Shear modulus in a plane containing the 1-axis.
    #     """
    #     G22 = E2/(2*(1+nu22))
    #     return Ply.from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G21, G21, G22)
    #
    # @staticmethod
    # def from_stiffness_matrix_transverse_isotropic(name, density, C11, C22, C44, C66, C12, C23):
    #     """
    #     Creates ply from given stiffness matrix C of a transverse isotropic material.
    #     The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the ply.
    #     density: float
    #         Mass density of the ply.
    #     Cxy: float
    #         Component xy of the stiffness matrix.
    #     """
    #     return Ply.from_stiffness_matrix_orthotropic(name, density, C11, C22, C22, C44, C44, C66, C12, C12, C23)

    # @staticmethod
    # def init_from_cpacs_old(mp: dict[str, Union[float, str]]) -> 'Ply':
    #     """
    #     This method initiates an instance of class Ply from the old CPACS material definition.
    #
    #     Parameters
    #     ----------
    #     mp
    #         dict of the material properties.
    #
    #     Returns
    #     -------
    #     Ply
    #         Instance of Ply material.
    #     """
    #     material = Ply.from_stiffness_matrix_orthotropic(
    #         C11=mp['k11'],
    #         C12=mp['k12'],
    #         C13=mp['k13'],
    #         C22=mp['k22'],
    #         C23=mp['k23'],
    #         C33=mp['k33'],
    #         C44=mp['k44'],
    #         C55=mp['k55'],
    #         C66=mp['k66'],
    #         name=mp['name'],
    #         density=mp['rho'],
    #     )
    #     if 'sig11t' in mp.keys():
    #         material.set_failure_stresses(
    #             sigma_1t=mp['sig11t'],
    #             sigma_2t=mp['sig22t'],
    #             sigma_3t=mp['sig33t'],
    #             sigma_1c=mp['sig11c'],
    #             sigma_2c=mp['sig22c'],
    #             sigma_3c=mp['sig33c'],
    #             sigma_23=mp['tau12'],
    #             sigma_13=mp['tau13'],
    #             sigma_12=mp['tau23'],
    #         )
    #     if 'maxStrain' in mp.keys():
    #         material.set_failure_strains(
    #             epsilon_1t=mp['maxStrain'],
    #             epsilon_2t=mp['maxStrain'],
    #             epsilon_3t=mp['maxStrain'],
    #             epsilon_1c=mp['maxStrain'],
    #             epsilon_2c=mp['maxStrain'],
    #             epsilon_3c=mp['maxStrain'],
    #             epsilon_12=mp['maxStrain'],
    #         )
    #
    #     return material
    #
    # @staticmethod
    # def init_from_cpacs_new_solid(mp: dict[str, Union[float, str]]) -> 'Ply':
    #     """
    #     This method initiates an instance of class Ply from the new CPACS material definition.
    #
    #     Parameters
    #     ----------
    #     mp
    #         dict of the material properties.
    #
    #     Returns
    #     -------
    #     Ply
    #         Instance of Ply material.
    #     """
    #     material = Ply.from_engineering_constants_orthotropic_for_becas(
    #         E1=mp['E1'],
    #         E2=mp['E2'],
    #         E3=mp['E2'],
    #         nu12=mp['nu12'],
    #         nu23=mp['nu23'],
    #         nu13=mp['nu31'] * mp['E1'] / mp['E3'],
    #         G12=mp['G12'],
    #         G23=mp['G23'],
    #         G31=mp['G31'],
    #         name=mp['name'],
    #         density=mp['rho'],
    #     )
    #     material.set_failure_stresses(
    #         sigma_1t=mp.get('sig1t'),
    #         sigma_2t=mp.get('sig2t'),
    #         sigma_3t=mp.get('sig3t'),
    #         sigma_1c=mp.get('sig1c'),
    #         sigma_2c=mp.get('sig2c'),
    #         sigma_3c=mp.get('sig3c'),
    #         sigma_23=mp.get('tau23'),
    #         sigma_13=mp.get('tau31'),
    #         sigma_12=mp.get('tau12'),
    #     )
    #     material.set_failure_strains(
    #         epsilon_1t=mp.get('eps1t'),
    #         epsilon_2t=mp.get('eps2t'),
    #         epsilon_3t=mp.get('eps3t'),
    #         epsilon_1c=mp.get('eps1c'),
    #         epsilon_2c=mp.get('eps2c'),
    #         epsilon_3c=mp.get('eps3c'),
    #         epsilon_12=mp.get('gamma12'),
    #     )
    #
    #     return material
    #
    # def set_failure_stresses(self, sigma_1t, sigma_2t, sigma_3t,
    #                          sigma_1c, sigma_2c, sigma_3c,
    #                          sigma_23, sigma_13, sigma_12):
    #     """
    #     This method sets the allowable material stresses in each direction.
    #
    #     Parameters
    #     ----------
    #
    #     ... : float
    #         The allowable stress in 1 - direction
    #
    #
    #     """
    #     self.sigma_1t = sigma_1t
    #     self.sigma_2t = sigma_2t
    #     self.sigma_3t = sigma_3t
    #
    #     self.sigma_1c = sigma_1c
    #     self.sigma_2c = sigma_2c
    #     self.sigma_3c = sigma_3c
    #
    #     self.sigma_12 = sigma_12
    #     self.sigma_13 = sigma_13
    #     self.sigma_23 = sigma_23
    #
    # def set_failure_strains(self,
    #                         epsilon_1t,
    #                         epsilon_2t,
    #                         epsilon_3t,
    #                         epsilon_1c,
    #                         epsilon_2c,
    #                         epsilon_3c,
    #                         epsilon_12):
    #     """
    #     This method sets the allowable material stresses in each direction.
    #
    #     Parameters
    #     ----------
    #     ... : float
    #         The allowable stress in 1 - direction
    #
    #     """
    #     self.epsilon_1t = epsilon_1t
    #     self.epsilon_2t = epsilon_2t
    #     self.epsilon_3t = epsilon_3t
    #     self.epsilon_1c = epsilon_1c
    #     self.epsilon_2c = epsilon_2c
    #     self.epsilon_3c = epsilon_3c
    #     self.epsilon_12 = epsilon_12

    def __repr__(self):
        return f'<CLT.Ply name:{self._name} (material, thickness, orientation): ({self._material.name}, {self._thickness}, {self._orientation})>'

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

    # @property
    # def stiffness_matrix(self):
    #     E1 = self.E1
    #     E2 = self.E2
    #     E3 = self.E3
    #     nu12 = self.nu12
    #     nu13 = self.nu13
    #     nu23 = self.nu23
    #     G12 = self.G12
    #     G31 = self.G31
    #     G23 = self.G23
    #
    #     compliance_matrix = np.array([
    #         [1/E1, -nu12/E1, -nu13/E1, 0, 0, 0],
    #         [-nu12/E1, 1/E2, -nu23/E2, 0, 0, 0],
    #         [-nu13/E1, -nu23/E2, 1/E3, 0, 0, 0],
    #         [0, 0, 0, 1/G23, 0, 0],
    #         [0, 0, 0, 0, 1/G31, 0],
    #         [0, 0, 0, 0, 0, 1/G12]
    #     ], dtype=self._dtype)
    #     return inv(compliance_matrix)

    @property
    def name(self) -> str:
        """Name of the ply."""
        return self._name

    @property
    def ply_index_global(self) -> int:
        return self._ply_index_global

    @ply_index_global.setter
    def ply_index_global(self, value):
        self._ply_index_global = value

    @property
    def thickness(self) -> float:
        """The ply thickness."""
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def orientation(self) -> float:
        """The rotation angle of the ply around the normal direction in degree."""
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    @property
    def material(self) -> IMaterial:
        """The material of the ply."""
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def labels(self) -> Optional[list[str]]:
        """Labels of the ply to identify special plys, i.e. the sandwich core."""
        return self._labels

    @labels.setter
    def labels(self, value):
        self._labels = value

    @property
    def Q_c(self) -> np.ndarray:
        """numpy.ndarray: Disk stiffness matrix of the ply."""
        return self._material.membrane_stiffness_matrix
     
    @property
    def Q_t(self) -> np.ndarray:
        """numpy.ndarray: Transverse shear stiffness matrix of the ply."""
        return self._material.transverse_stiffness_matrix

    @property
    def Q_rotated(self):
        """
        Returns the stiffness matrix of the ply in a rotated coordinate system rotated with the given angle in a
        mathematical positive direction about the third axis of the ply coordinate system, see [Jones1999]_, pp. 74.
        The stiffness matrix is splitted in two parts:
        the first part for the CLT (disk load only) and the second part for transverse shear stiffness.

        Returns
        -------
        numpy.ndarray
            Disk stiffness matrix of the ply in the rotated coordinate system.
        numpy.ndarray
            Transverse shear stiffness matrix of the ply in the rotated coordinate system.
        """
        Q_c = self.Q_c
        Q_t = self.Q_t
        Q_c_rotated = np.dot(np.dot(np.dot(np.dot(self.T_c_inverse, Q_c), self.R_c), self.T_c), self.R_c_inv)
        Q_t_rotated = np.dot(np.dot(np.dot(np.dot(self.T_t_inverse, Q_t), self.R_t), self.T_t), self.R_t_inv)
        return Q_c_rotated, Q_t_rotated

    @property
    def R_c(self):
        """
        Returns the R matrix for the rotation of the ply disk stiffness matrix. The R matrix converts the tensor strains to the
        engineering strains for the disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Disk R matrix.
        """
        return np.array([[1., 0., 0.],
                         [0., 1., 0.],
                         [0., 0., 2.]], dtype=self._dtype)

    @property
    def R_c_inv(self):
        """
        Returns the inverse R matrix for the rotation of the ply disk stiffness matrix. The inverse R matrix converts the engineering
        strains to the tensor strains for the disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Inverse disk R matrix.
        """
        return np.array([[1., 0.,  0.],
                         [0., 1.,  0.],
                         [0., 0., 0.5]], dtype=self._dtype)

    @property
    def R_t(self):
        """
        Returns the R matrix for the rotation of the ply transverse shear stiffness matrix. The R matrix converts the tensor strains to the
        engineering strains for the disk stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Transverse shear R matrix.
        """
        return np.array([[2., 0.],
                         [0., 2.]], dtype=self._dtype)

    @property
    def R_t_inv(self):
        """
        Returns the inverse R matrix for the rotation of the ply transverse shear stiffness matrix. The inverse R matrix converts
        the engineering strains to the tensor strains for the disk stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Inverse transverse shear R matrix.
        """
        return np.array([[0.5,  0.],
                         [ 0., 0.5]], dtype=self._dtype)

    @property
    def T_c(self):
        """
        Returns the rotation matrix for the rotation of the ply disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Rotation matrix.
        """
        Theta = np.deg2rad(1) * self._orientation
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[  c*c, s*s,   2*c*s ],
                         [  s*s, c*c,  -2*c*s ],
                         [ -c*s, c*s, c*c-s*s ]], dtype=self._dtype)

    @property
    def T_c_inverse(self):
        """
        Returns the inverse rotation matrix for the rotation of the ply disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Inverse rotation matrix.
        """
        Theta = np.deg2rad(1) * self._orientation
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[ c*c,  s*s,  -2*c*s ],
                         [ s*s,  c*c,   2*c*s ],
                         [ c*s, -c*s, c*c-s*s ]], dtype=self._dtype)

    @property
    def T_t(self):
        """
        Returns the rotation matrix for the rotation of the ply shear stiffness stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Rotation matrix.
        """
        Theta = np.deg2rad(1) * self._orientation
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[ c, -s ],
                         [ s,  c ]], dtype=self._dtype)

    @property
    def T_t_inverse(self):
        """
        Returns the inverse rotation matrix for the rotation of the ply shear stiffness stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Inverse rotation matrix.
        """
        Theta = np.deg2rad(1) * self._orientation
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[  c, s ],
                         [ -s, c ]], dtype=self._dtype)


class Laminate(Shell):
    """
    This class represents a laminate build of plys of orthotropic material stacked together. The coordinate system of the laminate is the
    x-y-z-coordinate-system, the z-axis equals the 3-axis of the plys and the thickness direction. The laminate can be charged with
    disk- and plate-loads (A-B-D-matrices), see [Jones1999]_, pp. 187. An extension for transverse shear loads is made (A_s-matrix).
    """
    def __init__(
            self,
            layup: Union[list[Ply], list[tuple[IMaterial, float, float]]],
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
            dtype=np.float64,
    ):
        """
        Constructor.
        
        Parameters
        ----------
        layup
            The layup of the laminate, list of plys or tuple for each ply: (material, thickness, orientation).
        name
            Representing the working name of the laminate.
        uid
            uID of the laminate.
        """
        super().__init__(
            name=name,
            uid=uid,
        )
        self._dtype = dtype

        if isinstance(layup[0], Ply):
            self._layup = layup
        else:
            self._layup = [
                Ply(material=layer[0], thickness=layer[1], orientation=layer[2], name=f'Ply #{i+1}')
                for i, layer in enumerate(layup)
            ]

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
        if not (type(other) == type(self)):
            return False
        if not (self.name == other.name):
            return False
        if not (self.uid == other.uid):
            return False
        if not len(self.layup) == len(other.layup):
            return False
        res = True
        for i in range(len(self.layup)):
            if not self.layup[i].equal_content(other.layup[i]):
                res = False
        return res

    def get_ABD_matrices(self, reference_surface=None):
        """
        Returns the stiffness matrices of the laminate, see [Jones1999]_, p. 198.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix, 3x3).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix, 3x3).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix, 3x3).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix, 2x2).
        """
        dtype = self._dtype

        size_ABD = 3
        size_A_s = 2
        A = np.zeros((size_ABD, size_ABD), dtype=dtype)
        B = np.zeros((size_ABD, size_ABD), dtype=dtype)
        D = np.zeros((size_ABD, size_ABD), dtype=dtype)
        A_s = np.zeros((size_A_s, size_A_s), dtype=dtype)
        if reference_surface is None:
            reference_surface = self.thickness / 2.
        z_last = -reference_surface
        for ply in self._layup:
            thickness = ply.thickness
            Q_c_laminate, Q_t_laminate = ply.Q_rotated
            A += Q_c_laminate * thickness
            B += Q_c_laminate * ((z_last+thickness)**2 - z_last**2) / 2.
            D += Q_c_laminate * ((z_last+thickness)**3 - z_last**3) / 3.
            A_s += Q_t_laminate * thickness
            z_last += thickness
        return A, B, D, A_s
        
    def get_ABD_matrix(self, reference_surface=None):
        """
        Returns the combined stiffness matrix of the laminate.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Laminate extension and bending stiffness matrix (ABD-matrix, 6x6).
        """
        A, B, D, A_s = self.get_ABD_matrices(reference_surface)
        ABD = np.vstack((np.hstack((A, B)), np.hstack((B.T, D))))
        return ABD
    
    @staticmethod
    def ADB_matrix_to_dict(A, D, B, A_s):
        """
        Converts the laminate stiffness matrices to dict's. For the A, B and D matrices the indices 11, 22, 66, 12, 16 and 26 are set,
        for the A_s matrix the indices 44, 55 and 45 are set.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix).
        """
        A_dict = {11:A[0,0], 22:A[1,1], 66:A[2,2], 12:A[0,1], 16:A[0,2], 26:A[1,2]}
        B_dict = {11:B[0,0], 22:B[1,1], 66:B[2,2], 12:B[0,1], 16:B[0,2], 26:B[1,2]}
        D_dict = {11:D[0,0], 22:D[1,1], 66:D[2,2], 12:D[0,1], 16:D[0,2], 26:D[1,2]}
        A_s_dict = {44:A_s[0,0], 55:A_s[1,1], 45:A_s[0,1]}
        return A_dict, B_dict, D_dict, A_s_dict
    
    def get_ABD_dict(self, reference_surface=None):
        """
        Returns the stiffness matrices of the laminate as dicts's, see [Jones1999]_, p. 198. The neutral plane is calculated
        according to [Schürmann2007]_, pp. 335.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix, 3x3).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix, 3x3).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix, 3x3).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix, 2x2).
        """
        A, B, D, A_s = self.get_ABD_matrices(reference_surface)
        return Laminate.ADB_matrix_to_dict(A, D, B, A_s)

    @staticmethod
    def get_engineering_constants_base(ABD, thickness, method, ABD_inv=None):
        """
        Returns the engineering constants of the laminate (E_1, E_2, G).

        Parameters
        ----------
        ABD: numpy.ndarray
            The ABD stiffness matrix of the laminate.
        thickness: float
            The thickness of the laminate.
        method: str (default: 'with_poisson_effect')
            Method, how to calculate the engineering constants. Possible choices:
                'with_poisson_effect': see [Schürmann2007]_, p. 226.
                'without_poisson_effect':
                'wiedemann': see [Wiedemann2007]_, p. 155.
                'song': No stress in 1-direction, no strain in the other direction, see [Song].
        ABD_inv: numpy.ndarray (default: None)
            If available, the interted ABD stiffness matrix of the laminate.

        Returns
        -------
        float
            Elastic modulus in 1-direction.
        float
            Elastic modulus in 2-direction.
        float
            Shear modulus in the 1-2-plane (membrane shear modulus).
        """
        t = thickness
        if ABD_inv is None:
            ABD_inv = np.linalg.inv(ABD)
        if method == 'with_poisson_effect':
            E_1 = 1. / (ABD_inv[0, 0] * t)
            E_2 = 1. / (ABD_inv[1, 1] * t)
            G = 1. / (ABD_inv[2, 2] * t)
            return E_1, E_2, G
        elif method == 'without_poisson_effect':
            E_1 = ABD[0, 0] / t
            E_2 = ABD[1, 1] / t
            G = ABD[2, 2] / t
            return E_1, E_2, G
        elif method == 'song':
            K_11 = (ABD[0, 0] * ABD[1, 1] - ABD[0, 1] ** 2) / ABD[1, 1]
            K_22 = (ABD[1, 1] * ABD[2, 2] - ABD[1, 2] ** 2) / ABD[1, 1]
            return K_11 / t, None, K_22 / t
        elif method == 'wiedemann':
            E_1 = 1. / (ABD_inv[0, 0] * t)
            E_2 = 1. / (ABD_inv[1, 1] * t)
            G = 1. / ((ABD_inv[2, 2] / 2 + ABD_inv[0, 1]) * t)
            return E_1, E_2, G
        else:
            raise RuntimeError('Method not known')

    def get_engineering_constants(self, method='with_poisson_effect', reference_surface=None):
        """
        Returns the engineering constants of the laminate (E_1, E_2, G).
        
        Parameters
        ----------
        method: str (default: 'with_poisson_effect')
            Method, how to calculate the engineering constants. Possible choices:
                'with_poisson_effect': see [Schürmann2007]_, p. 226.
                'without_poisson_effect': 
                'wiedemann': see [Wiedemann2007]_, p. 155.
                'song': No stress in 1-direction, no strain in the other direction, see [Song].
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.

        Returns
        -------
        float
            Elastic modulus in 1-direction.
        float
            Elastic modulus in 2-direction.
        float
            Shear modulus in the 1-2-plane (membrane shear modulus).
        """
        ABD = self.get_ABD_matrix(reference_surface)
        return Laminate.get_engineering_constants_base(ABD, self.thickness, method)

    @property
    def thickness(self) -> float:
        """Thickness of the laminate."""
        return sum([ply.thickness for ply in self._layup])
    
    @property
    def density(self) -> float:
        """Mass density of the laminate."""
        return sum([ply.material.density * ply.thickness for ply in self._layup]) / self.thickness
    
    @property
    def layup(self) -> list[Ply]:
        """The layup of the laminate, list of plys."""
        return self._layup
