"""
This module contains the implementations for the material interfaces.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from typing import Union, Optional

import numpy as np

from PreDoCS.CrossSectionAnalysis.Interfaces import IElementStiffness
from PreDoCS.MaterialAnalysis.CLT import Laminate, Ply
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement, CompositeElementStiffness, IsotropicElement, \
    IsotropicElementStiffness
from PreDoCS.MaterialAnalysis.Interfaces import IMaterial, IShell, Shell
from PreDoCS.MaterialAnalysis.Materials import Isotropic
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.data import equal_content

log = get_module_logger(__name__)


class IsotropicShell(Shell):
    """
    Description of an isotropic shell.
    """
    def __init__(
            self,
            material: Isotropic,
            thickness: float,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
    ):
        """
        Class initialisation.

        Parameters
        ----------
        material
            Material of the shell.
        thickness
            Thickness of the shell.
        name
            Representing the working name of the shell.
        uid
            uID of the shell.
        """
        super().__init__(
            name=name,
            uid=uid,
        )
        self._material = material
        self._thickness = thickness

    # @staticmethod
    # def from_E_and_G(name, thickness, density, E, G):
    #     """
    #     Create isotropic material from modulus of elasticity and shear modulus.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the material.
    #     thickness: float
    #         Thickness of the material.
    #     density: float
    #         Density of the material.
    #     E: float
    #         Modulus of elasticity of the material.
    #     G: float
    #         Shear modulus of the material.
    #     """
    #     nu = E / (2 * G) - 1
    #     return IsotropicMaterial(name, thickness, density, E, nu)
    #
    # @staticmethod
    # def from_E_and_nu(name, thickness, density, E, nu):
    #     """
    #     Create isotropic material from modulus of elasticity and poisson's ratio.
    #
    #     Parameters
    #     ----------
    #     name: str
    #         Name of the material.
    #     thickness: float
    #         Thickness of the material.
    #     density: float
    #         Density of the material.
    #     E: float
    #         Modulus of elasticity of the material.
    #     nu: float
    #         Poisson's ratio of the material.
    #     """
    #     return IsotropicMaterial(name, thickness, density, E, nu)
    #
    # @staticmethod
    # def init_from_cpacs_old(mp: dict[str, Union[float, str]]) -> 'IsotropicMaterial':
    #     """
    #     This method initiates an instance of class IsotropicMaterial from the old CPACS material definition.
    #
    #     Parameters
    #     ----------
    #     mp
    #         dict of the material properties.
    #
    #     Returns
    #     -------
    #     IsotropicMaterial
    #         Instance of IsotropicMaterial material
    #     """
    #     material = IsotropicMaterial.from_E_and_G(
    #         E=mp['k11'],
    #         G=mp['k12'],
    #         name=mp['name'],
    #         density=mp['rho'],
    #         thickness=None,
    #     )
    #     if 'sig11' in mp.keys():
    #         material.set_failure_stresses(
    #             sigma_11=mp['sig11'],
    #             sigma_12=mp['tau12'],
    #         )
    #     if 'maxStrain' in mp.keys():
    #         material.set_failure_strains(
    #             epsilon=mp['maxStrain'],
    #         )
    #
    #     return material
    #
    # @staticmethod
    # def init_from_cpacs_new(mp: dict[str, Union[float, str]]) -> 'IsotropicMaterial':
    #     """
    #     This method initiates an instance of class IsotropicMaterial from the new CPACS material definition.
    #
    #     Parameters
    #     ----------
    #     mp
    #         dict of the material properties.
    #
    #     Returns
    #     -------
    #     IsotropicMaterial
    #         Instance of IsotropicMaterial material
    #     """
    #     material = IsotropicMaterial.from_E_and_nu(
    #         E=mp['E'],
    #         nu=mp['nu'],
    #         name=mp['name'],
    #         density=mp['rho'],
    #         thickness=None,
    #     )
    #     material.set_failure_stresses(
    #         sigma_11=mp.get('sigt'),
    #         sigma_12=mp.get('tau12'),
    #     )
    #     material.set_failure_strains(
    #         epsilon=mp.get('epsc'),
    #         epsilon_t=mp.get('epst'),
    #         gamma=mp.get('gamma12'),
    #     )
    #
    #     return material

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
    def material(self) -> Isotropic:
        """The material of the shell."""
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def thickness(self) -> float:
        """Thickness of the shell."""
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def density(self) -> Union[float, None]:
        """Density of the shell."""
        return self._material.density


class CompositeShell(Laminate):
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
            layup=layup,
            name=name,
            uid=uid,
            dtype=dtype,
        )


def get_stiffness_for_shell(shell: IShell, element_type, dtype=np.float64, **element_kwargs):
    """
    Returns the homogenous material data of the material for the element type.

    Parameters
    ----------
    shell
        The shell.
    element_type: class <- IElement
        The element type.
    engineering_constants_method: str
        See CLT.Laminate.get_engineering_constants.

    Returns
    -------
    IElementStiffness
        The stiffness of the element.
    """
    # New stiffness
    if isinstance(shell, IsotropicShell) and issubclass(element_type, IsotropicElement):
        stiffness = IsotropicElementStiffness.from_isotropic_shell(shell, dtype=dtype)
    elif isinstance(shell, IsotropicShell) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_isotropic_shell(shell, dtype=dtype)
    elif isinstance(shell, CompositeShell) and issubclass(element_type, IsotropicElement):
        assert 'engineering_constants_method' in element_kwargs
        stiffness = IsotropicElementStiffness.from_composite_shell(
            shell, dtype=dtype, engineering_constants_method=element_kwargs['engineering_constants_method'],
        )
    elif isinstance(shell, CompositeShell) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_composite_shell(shell, dtype=dtype)
    else:
        raise RuntimeError(
            'Shell type "{}" or element type "{}" not defined'.format(str(type(shell)), str(element_type)))
    return stiffness


def get_stiffness_for_shell_VCP(skin, element_type, dtype=np.float64, **element_kwargs):
    """
    Returns the homogenous material data of the material for the element type.

    Parameters
    ----------
    skin
        The lightworks skin.
    element_type: class <- IElement
        The element type.
    engineering_constants_method: str
        See CLT.Laminate.get_engineering_constants.

    Returns
    -------
    IElementStiffness
        The stiffness of the element.
    """
    try:
        from lightworks.mechana.skins.metal import Sheet as Sheet_lw
        from lightworks.mechana.skins.composite import Laminate as Laminate_lw
        from lightworks.mechana.skins.composite import LaminationParameter as LaminationParameter_lw
    except ImportError:
        message = 'Modul lightworks.mechana not found. Material world VCP can not be used.'
        log.error(message)
        raise ImportError(message)

    if isinstance(skin, Sheet_lw) and issubclass(element_type, IsotropicElement):
        stiffness = IsotropicElementStiffness.from_skin(skin, dtype=dtype)
    elif isinstance(skin, Sheet_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(skin, dtype=dtype)
    elif isinstance(skin, Laminate_lw) and issubclass(element_type, IsotropicElement):
        assert 'method' in element_kwargs
        stiffness = IsotropicElementStiffness.from_skin(skin, dtype=dtype, **element_kwargs)
    elif isinstance(skin, Laminate_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(skin, dtype=dtype)
    elif isinstance(skin, LaminationParameter_lw) and issubclass(element_type, IsotropicElement):
        assert 'method' in element_kwargs
        stiffness = IsotropicElementStiffness.from_skin(skin, dtype=dtype, **element_kwargs)
    elif isinstance(skin, LaminationParameter_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(skin, dtype=dtype)
    else:
        raise RuntimeError(
            'Skin type "{}" or element type "{}" not defined'.format(str(type(skin)), str(element_type)))

    return stiffness
