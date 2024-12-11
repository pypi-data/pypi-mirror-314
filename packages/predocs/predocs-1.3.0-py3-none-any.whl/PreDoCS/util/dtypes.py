#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.dtypes import *

except ImportError:
    log.info('Modul cpacs_interface.utils.dtypes not found. Use PreDoCS dtypes.')

    import cython
    import numpy as np

    import scipy.sparse.linalg as sp_la


    def dtype_is_complex(dtype) -> bool:
        if dtype == np.float64:
            return False
        elif dtype == np.int32 or dtype == np.int64:
            return False
        elif dtype == np.complex128:
            return True
        else:
            raise ValueError(f'Unknown dtype {dtype}')


    def dtype_from_value(value):
        if isinstance(value, np.ndarray):
            assert value.size == 1, f'Value {value} must not be a array.'
            return dtype_from_value(value.item())
        elif isinstance(value, np.float64) or isinstance(value, float):
            return np.float64
        elif isinstance(value, np.int32) or isinstance(value, np.int64) or isinstance(value, int):
            return np.int32
        elif isinstance(value, np.complex128) or isinstance(value, complex):
            return np.complex128
        else:
            raise ValueError(f'Unknown dtype {type(value)}')


    def dtype_from_values(values):
        dtypes = [dtype_from_value(v) for v in values]
        if np.complex128 in dtypes:
            return np.complex128
        elif np.float64 in dtypes:
            return np.float64
        elif np.int64 in dtypes:
            return np.int64
        else:
            return np.int32


    def cython_dtype_from_dtype(dtype):
        if dtype == np.float64:
            return cython.double
        elif dtype == np.int64:
            return cython.long
        elif dtype == np.int32:
            return cython.int
        elif dtype == np.complex128:
            return cython.doublecomplex
        else:
            raise ValueError(f'Unknown dtype {dtype}')


    def lgs_solve(A: np.ndarray, b: np.ndarray, dtype) -> np.ndarray:
        """
        Definition to solve np.linalg.solve with complex numbers.
            Ax = b
        see https://stackoverflow.com/questions/70216398/solving-linear-equation-of-complex-matrices

        :return: x
        """
        if dtype_is_complex(dtype):
            # print('There is a complex value in A.', A,b)
            x = np.linalg.solve(A, np.real(b)) + 1j * np.linalg.solve(A, np.imag(b))
            # y = np.linalg.solve(A, b)
            #
            # i = 1
            # if abs(x[i] - y[i]) > 10 ** (-30):
            #     #print(abs(x[i] - y[i]))
            #     assert x[i] == y[i]

        else:
            x = np.linalg.solve(A, b)
        return x


    def lgs_solve_sparse(A: np.ndarray, b: np.ndarray, dtype) -> np.ndarray:
        """
        Definition to solve np.linalg.solve with complex numbers.
            Ax = b
        see https://stackoverflow.com/questions/70216398/solving-linear-equation-of-complex-matrices

        :return: x
        """
        # if dtype_is_complex(dtype):
        #     # print('There is a complex value in A.', A,b)
        #     x = sp_la.spsolve(A, np.real(b)) + 1j * sp_la.spsolve(A, np.imag(b))
        #     # y = np.linalg.solve(A, b)
        #     #
        #     # i = 1
        #     # if abs(x[i] - y[i]) > 10 ** (-30):
        #     #     #print(abs(x[i] - y[i]))
        #     #     assert x[i] == y[i]
        #
        # else:
        x = sp_la.spsolve(A, b)
        return x

