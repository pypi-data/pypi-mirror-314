# cython: profile=True
"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.vector import *

except ImportError:
    log.info('Modul cpacs_interface.utils.vector not found. Use PreDoCS vector.')

    import cython
    #  content of lightworks project created by FA-FLB
    #  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

    import numpy as np

    from PreDoCS.util.dtypes import dtype_from_values


    class Vector(np.ndarray):
        """
        Represents a n-dimensional vector. The class inherits from numpy.ndarray.
        """

        def __new__(cls, input_array=(0., 0.)):
            """
            Constructor.

            Parameters
            ----------
            input_array : numpy.array, numpy.matrix, list, tuple
                Components of the vector.
            """
            obj = np.asarray(input_array).view(cls).astype(dtype_from_values(input_array))
            return obj

        @property
        def x(self) -> 'dtype':
            """float: The first component of the vector."""
            return self[0]

        @property
        def y(self) -> 'dtype':
            """float: The second component of the vector."""
            return self[1]

        @property
        def z(self) -> 'dtype':
            """
            Returns
            -------
            float
                The third component of the vector.

            Raises
            ------
            IndexError
                If the third component is not defined.
            """
            return self[2]

        def __eq__(self, other) -> bool:
            return np.array_equal(self, other)

        def __ne__(self, other) -> bool:
            return not np.array_equal(self, other)

        def __iter__(self):
            for x in np.nditer(self):
                yield x.item()

        def __lt__(self, other) -> bool:
            """
            Overrides the '<'-operator. Compares the vectors lexicographically.

            Returns
            -------
            bool
                True, if self is smaller than other.

            Raises
            ------
            NotImplemented
                If other is not an instance of Vector.
            """
            if isinstance(other, Vector):
                return list(self) < list(other)
            else:
                raise NotImplementedError()

        def __gt__(self, other) -> bool:
            """
            see __lt__() method
            """
            if isinstance(other, Vector):
                return list(self) > list(other)
            else:
                raise NotImplementedError()

        def dist(self, other) -> 'dtype':
            """
            Returns the distance between this and an other vector.

            Parameters
            ----------
            other : Vector
                The other vector, the dimensions must agree.

            Returns
            -------
            float
                Distance.
            """
            return (self - other).length

        @property
        def length(self) -> 'dtype':
            """float: Length of the vector."""
            if len(self) == 1:
                return self[0]
            elif len(self) == 2:
                return np.sqrt(self[0] ** 2 + self[1] ** 2)
            elif len(self) == 3:
                return np.sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)
            else:
                return np.linalg.norm(self)

        @property
        def normalised(self) -> 'Vector':
            """Vector: The normalized vector."""
            return self / self.length

        @property
        def normal_vector_2d(self) -> 'Vector':
            """
            Returns the vector standing normal on the given vector in the x-y-plane.
            """
            assert len(self) == 2
            return Vector([self[1], -self[0]])

        def angle_between(self, other) -> 'dtype':
            """
            Returns the angle between this and an other vector.

            Parameters
            ----------
            other : Vector
                The other vector. Two- or three-dimensional. Dimensions must agree.

            Returns
            -------
            float
                angle between this and an other vector in RAD.
            """
            return np.arccos(np.clip(np.dot(self.normalised, other.normalised), -1.0, 1.0))

        @property
        def angle_in_plane(self) -> 'dtype':
            """
            float:
                Returns the angle of this vector in the x-y-plane. This vector has to be two-dimensional.
                The angel is signed (mathematical direction of rotation) and is between -PI and PI.
            """
            assert len(self) == 2  # Two-dimensional vector
            if self.y == 0:
                if self.x > 0:
                    return 0
                else:
                    return np.pi
            else:
                return np.sign(self.y) * Vector([1., 0.]).angle_between(self)

