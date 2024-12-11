"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.data import *
except ImportError:
    log.info('Modul cpacs_interface.utils.data not found. Use PreDoCS data utils class.')

    import copy
    import logging
    import traceback
    from typing import Callable

    import numpy as np
    from deepdiff import DeepDiff
    from scipy import interpolate

    log = logging.getLogger(__name__)


    def nested_dict_update(base: dict, update: dict) -> dict:
        """
        Updates the base dict with updates and preserve present values in base.

        Parameters
        ----------
        base: dict
            dict to be updates
        update: dict
            dict with updates

        Returns
        -------
        dict
            updated base

        """
        for key, value in update.items():
            if key in base.keys():
                if type(value) is dict:
                    nested_dict_update(base[key], value)
                else:
                    base[key] = value
            else:
                base[key] = value
        return base


    def equal_attributes(one, other):
        """
        Check if to objects have identical attributes.

        Parameters
        ----------
        one
            One object.
        other
            The other object.

        Returns
        -------
        True if they are identical, False if not.
        """
        # TODO: DeepDiff durch was performanteres ersetzen
        return len(DeepDiff(one.__dict__, other.__dict__)) == 0


    def get_equal_attributes_key(the_dict, obj):
        for k, v in the_dict.items():
            if equal_attributes(obj, v):
                return k
        return None


    def equal_content(obj1, obj2):
        if not (type(obj1) == type(obj2)):
            return False
        vars1 = vars(obj1)
        vars2 = vars(obj2)
        if not (vars1.keys() == vars2.keys()):
            return False
        for key in vars1.keys():
            if isinstance(vars1[key], np.ndarray):
                if not np.all(vars1[key] == vars2[key]):
                    return False
            else:
                if not (vars1[key] == vars2[key]):
                    return False
        return True


    def get_equal_content_key(the_dict, obj):
        for k, v in the_dict.items():
            if obj.equal_content(v):
                return k
        return None


    def ceil(a: np.ndarray, precision=0):
        """Got from https://stackoverflow.com/questions/58065055/floor-and-ceil-with-number-of-decimals"""
        return np.true_divide(np.ceil(a * 10 ** precision), 10 ** precision)


    def floor(a: np.ndarray, precision=0):
        """Got from https://stackoverflow.com/questions/58065055/floor-and-ceil-with-number-of-decimals"""
        return np.true_divide(np.floor(a * 10 ** precision), 10 ** precision)


    def replace_values_in_string(text, args_dict):
        """from https://stackoverflow.com/questions/14156473/can-you-write-a-str-replace-using-dictionary-values-in-python"""
        for key in args_dict.keys():
            text = text.replace(key, str(args_dict[key]))
        return text


    def replace_values_in_string_single(text, args_dict):
        """from https://stackoverflow.com/questions/14156473/can-you-write-a-str-replace-using-dictionary-values-in-python"""
        for key in args_dict.keys():
            if key in text:
                text = text.replace(key, str(args_dict[key]))
                break
        return text


    def check_symmetric(a, rtol=1e-05, atol=1e-08):
        """Check, if two matrices are symmetric."""
        return np.allclose(a, a.T, rtol=rtol, atol=atol)


    def check_symmetric_exact(a):
        """Check, if two matrices are symmetric."""
        return np.all(a == a.T)


    def make_hash(o):
        """
        Makes a hash from a dictionary, list, tuple or set to any level, that contains
        only other hashable types (including any lists, tuples, sets, and
        dictionaries).

        https://stackoverflow.com/questions/5884066/hashing-a-dictionary
        """
        if isinstance(o, (set, tuple, list, np.ndarray)):
            return tuple([make_hash(e) for e in o])
        elif not isinstance(o, dict):
            return hash(o)

        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = make_hash(v)

        return hash(tuple(frozenset(sorted(new_o.items()))))


    def interp1d(x, y, **kwargs) -> Callable:
        """
        Interpolates data. Based on the scipy.interpolate.interp1d function, but checks if the x-values are
        unique. If not, they are adjusted to be unique.
        Otherwise, the function behavior is undefined.

        For parameters see

        Parameters
        ----------
        x : (npoints, ) array_like
            A 1-D array of real values.
        y : (..., npoints, ...) array_like
            A N-D array of real values. The length of `y` along the interpolation
            axis must be equal to the length of `x`. Use the ``axis`` parameter
            to select correct axis. Unlike other interpolators, the default
            interpolation axis is the last axis of `y`.
        kwargs
            `scipy.interpolate.interp1d` parameters, see
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html

        Returns
        -------
        Interpolation function.
        """
        # Check for not unique x-values and make x unique
        if not np.all(np.unique(x, return_counts=True)[1] == 1):
            log.debug(f'interp1d: x-values are not unique:\n{"".join(traceback.format_stack())}')
        while not np.all(np.unique(x, return_counts=True)[1] == 1):
            # Decrease first not unique grid value
            uniq, uniq_idx, counts = np.unique(x, return_index=True, return_counts=True)
            not_unique_idx = np.where(counts > 1)[0]
            assert len(not_unique_idx) > 0
            x[uniq_idx[not_unique_idx[0]]] -= 1e-10

        return interpolate.interp1d(x, y, **kwargs)


    def monotonically_increasing(l: list[float]) -> bool:
        """
        https://stackoverflow.com/questions/30734258/efficiently-check-if-numpy-ndarray-values-are-strictly-increasing
        """
        return all(x < y for x, y in zip(l, l[1:]))


    def save_divide(a, b):
        """Performs a / b, but returns 0, if b is 0."""
        return np.divide(a, b, out=np.zeros_like(a), where=b != 0)
