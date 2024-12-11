"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.filters import *
except ImportError:
    log.info('Modul cpacs_interface.utils.filters not found. Use PreDoCS filters utils class.')

    from typing import List, Sequence


    def filter_names(names, substrings, inclusive=True, match_all=True):
        """
        Filter a list of names (i.e. strings) by given substring(s).

        Matches can be either inclusive or exclusive using the keyword argument inclusive.

        Additionally, the keyword argument match_all can be used to in-/exclude names matching any or all given substrings.

        Parameters
        ----------
        names : list of strings
            Names can be any Python strings.
        substrings : string or list of strings
            Portion(s) of the given names that are to be in-/excluded.
        inclusive: bool
            Switch to include/exclude matching substrings
        match_all: bool
            Switch to determine whether a match fulfils any or all given substrings.

        Returns
        -------
        list
            Reduced list, containing only the names matching all given criteria or empty list if no match found.

        Note
        ----
        No wildcards allowed!

        Examples
        --------
        >>> filter_names(['Hello', 'World'], 'l')
        ['Hello', 'World']
        >>> filter_names(['Hello', 'World'], 'll')
        ['Hello']
        >>> filter_names(['Hello', 'World'], ['el', 'rl'])
        []
        >>> filter_names(['Hello', 'World'], ['el', 'rl'], match_all=False)
        ['Hello', 'World']
        >>> filter_names(['Hello', 'World'], 'll', inclusive=False)
        ['World']

        """

        # checking and parsing of given arguments
        if not (isinstance(names, list) and all([isinstance(name, str) for name in names])):
            raise TypeError('Invalid type of first argument (names). Must be a list of strings.')
        if isinstance(substrings, str):
            filters = [substrings] if substrings else []
        elif isinstance(substrings, list) and all([isinstance(substr, str) for substr in substrings]):
            filters = substrings
        else:
            raise TypeError('Invalid type of second argument (substrings). Must be either string or list of strings.')
        if not isinstance(inclusive, bool):
            raise TypeError('Invalid type of third argument (inclusive). Must be boolean.')
        if not isinstance(match_all, bool):
            raise TypeError('Invalid type of fourth argument (match_all). Must be boolean.')

        # filtering as requested
        if inclusive and match_all:
            names_of_interest = []
            for name in names:
                if all([substr in name for substr in filters]):
                    names_of_interest.append(name)
        elif inclusive and not match_all:
            names_of_interest = []
            for name in names:
                if any([substr in name for substr in filters]):
                    names_of_interest.append(name)
        elif not inclusive and match_all:
            names_of_interest = names[:]
            for i, name in reversed(list(enumerate(names))):
                if filters and all([substr in name for substr in filters]):
                    names_of_interest.pop(i)
        else:  # both False
            names_of_interest = names[:]
            for i, name in reversed(list(enumerate(names))):
                if filters and any([substr in name for substr in filters]):
                    names_of_interest.pop(i)

        return names_of_interest


    def find_all(sequence: Sequence, attribute: str, value) -> Sequence:
        """
        Finds all objects in a list by a given attribute value.

        Parameters
        ----------
        sequence
            The sequence.
        attribute
            The name of the attribute.
        value
            The value to search for.

        Returns
        -------
        The list of objects found.
        """
        return [obj for obj in sequence if getattr(obj, attribute) == value]


    def find(sequence: Sequence, attribute: str, value, assert_single_result: bool = False):
        """
        Finds an object in a list by a given attribute value.

        Parameters
        ----------
        sequence
            The sequence.
        attribute
            The name of the attribute.
        value
            The value to search for.
        assert_single_result
            If True, an exception is raised if not exactly one matching object is found.

        Returns
        -------
        The object or None if not found.
        """
        if assert_single_result:
            results = [obj for obj in sequence if getattr(obj, attribute) == value]
            assert len(results) == 1
            return results[0]
        else:
            for obj in sequence:
                if getattr(obj, attribute) == value:
                    return obj
            return None


    def is_between(value: any, tup: list[any], tol: float = 1e-6) -> bool:
        """
        Checks if a value is between a tuple of values.

        Parameters
        ----------
        value
        tup

        Returns
        -------
        bool
        """
        assert len(tup) > 1, 'tuple to compare has only one or less values'
        if tup[0] - tol < value < tup[1] + tol:
            return True
        else:
            return False


    def flatten(d):
        res = []  # Result list
        if isinstance(d, dict):
            for key, val in d.items():
                res.extend(flatten(val))
        elif isinstance(d, list):
            res = d
        else:
            raise TypeError(f'Undefined type for flatten: {type(d)}')

        return res


    def unique(sequence: Sequence) -> List:
        """
        Similar to build in set method, but it preserves order of the sequence.

        Parameters
        ----------
        sequence: Sequence
            any sequence

        Returns
        -------
        List
            list of unique elements of sequence input
        """
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]


    def modified_kwargs(argsdict, **kwargs):
        res = argsdict.copy()
        for kw, arg in kwargs.items():
            res[kw] = arg
        return res


    def flatten_sublists(list_):
        return [item for sublist in list_ for item in sublist]

