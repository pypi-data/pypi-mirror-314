"""
This module contains the material interfaces.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from abc import ABC, abstractmethod
from typing import Union, Optional

import numpy as np


class IMaterial(ABC):
    """
    Description of a general material.
    """
    @property
    @abstractmethod
    def name(self) -> Union[str, None]:
        """Name of the material."""
        pass

    @property
    @abstractmethod
    def uid(self) -> Union[str, None]:
        """uID of the material."""
        pass

    @property
    @abstractmethod
    def density(self) -> Union[float, None]:
        """Density of the material."""
        pass

    @abstractmethod
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
        pass

    @property
    @abstractmethod
    def compliance_matrix(self) -> np.ndarray:
        """
        Yields the material compliance matrix (:math:`\\mathbf{S}=\\mathbf{C}^{-1}`, see [Jones1999]_, pp. 60).

        Returns
        -------
        np.ndarray (6,6)
            The compliance matrix.
        """
        pass

    @property
    @abstractmethod
    def stiffness_matrix(self) -> np.ndarray:
        """
        Yields the material stiffness matrix (:math:`\\mathbf{C}=\\mathbf{S}^{-1}`, see [Jones1999]_, pp. 58).

        Returns
        -------
        np.ndarray (6,6)
            The stiffness matrix.
        """
        pass

    @property
    @abstractmethod
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
        pass

    @property
    @abstractmethod
    def transverse_stiffness_matrix(self) -> np.ndarray:
        """
        TODO: tbd.

        Returns
        -------
        np.ndarray (2,2)
            The transverse stiffness matrix.
        """
        pass

    @property
    @abstractmethod
    def failure_data(self) -> object:
        """
        An object containing all the data describing the failure behavior of the material.
        """
        pass

    # @property
    # @abstractmethod
    # def max_stress(self) -> dict[str, float]:
    #     """
    #     The dict of the maximum allowable stresses of the material.
    #     Available keys:
    #         For tension:
    #             sigma_1t, sigma_2t sigma_3t
    #         For compression:
    #             sigma_1c, sigma_2c, sigma_3c
    #         For shear:
    #             sigma_12, sigma_13, sigma_23
    #     """
    #     pass
    #
    # @property
    # @abstractmethod
    # def max_strain(self) -> dict[str, float]:
    #     """
    #     The dict of the maximum allowable strains of the material.
    #     Available keys:
    #         For tension:
    #             epsilon_1t, epsilon_2t epsilon_3t
    #         For compression:
    #             epsilon_1c, epsilon_2c, epsilon_3c
    #         For shear:
    #             epsilon_12, epsilon_13, epsilon_23
    #     """
    #     pass


class IShell(ABC):
    @property
    @abstractmethod
    def name(self) -> Union[str, None]:
        """Name of the shell."""
        pass

    @property
    @abstractmethod
    def uid(self) -> Union[str, None]:
        """uID of the shell."""
        pass

    @property
    @abstractmethod
    def thickness(self) -> float:
        """Thickness of the shell."""
        pass

    @property
    @abstractmethod
    def density(self) -> Union[float, None]:
        """Density of the shell."""
        pass

    @property
    @abstractmethod
    def stiffness(self) -> 'IElementStiffness':
        """Stiffness of the shell."""
        pass

    @abstractmethod
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
        pass


class Shell(IShell, ABC):
    def __init__(
            self,
            name: Optional[str] = 'default name',
            uid: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        name
            Representing the working name of the material.
        uid
            uID of the material.
        """
        self._name = name
        self._uid = uid
        self._stiffness = None

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
    def stiffness(self) -> 'IElementStiffness':
        """Stiffness of the shell."""
        return self._stiffness

    @stiffness.setter
    def stiffness(self, value):
        self._stiffness = value
