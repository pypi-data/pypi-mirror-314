"""
This module contains the material interfaces.

.. codeauthor:: Hendrik Traub  <hendrik.traub@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

from abc import ABC, abstractmethod


class ILoadCase(ABC):
    """
    Description of a general load case.
    """
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def fx(self):
        pass

    @property
    @abstractmethod
    def fy(self):
        pass

    @property
    @abstractmethod
    def fz(self):
        pass

    @property
    @abstractmethod
    def mx(self):
        pass

    @property
    @abstractmethod
    def my(self):
        pass

    @property
    @abstractmethod
    def mz(self):
        pass


class ILoadReferencePoints(ABC):
    """
    Definition of load reference Points
    """
    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @property
    @abstractmethod
    def z(self):
        pass

