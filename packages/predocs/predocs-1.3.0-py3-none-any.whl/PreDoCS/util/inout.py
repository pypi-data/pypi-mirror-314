"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
"""
#  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.inout import *
except ImportError:
    log.info('Modul cpacs_interface.utils.inout not found. Use PreDoCS inout utils class.')

    import json
    import os

    import numpy as np
    from cloudpickle import cloudpickle
    from ruamel import yaml

    from .filters import filter_names


    def files_in_folder(directory):
        """
        Get a list of file names in a given directory.

        Parameters
        ----------
        directory : str
            Valid full path to an accessible directory.

        Returns
        -------
        list
            The names of all files in the given directory.

        Note: Works only for Python 3.5 and above (as os.scandir is used)
        """

        direntries = os.scandir(directory)
        return [direntry.name for direntry in direntries if direntry.is_file()]


    def files_in_folder_filtered(directory, inclusive="*", exclusive="", excl_prevails=True):
        """
        Get a filtered list of file names in a given directory.

        Parameters
        ----------
        directory : string
            Valid path to an accessible directory.
        inclusive : string or list of strings and/or lists
            Valid portions of the given names. If "*" (default), all files will be included.
            If a list is given, any file matching any contained string will be included.
            Sublists can be also be given. Only files, matching all strings contained in the sublist, will be included.
        exclusive : string or list of strings and/or lists
            Invalid portions of the given names. If "" (default), no files will be excluded.
            Same logic as inclusive
        excl_prevails : bool
            For files matching inclusive and exclusive: Switch to determine whether exclusion overrules inclusion (default)

        Returns
        -------
        list
            Filtered list of file names containing all valid substrings.

        Notes
        -----
        Do not use wildcards except for the default. Define multiple criteria instead.

        Examples
        --------
        **For all examples, the ``given_directory`` is assumed to contain the files ['Hello.exe', 'World.bat', 'Python.py]**

        >>> files_in_folder_filtered(given_directory)
        ['Hello.exe', 'World.bat', 'Python.py]
        >>> files_in_folder_filtered(given_directory, inclusive="l")
        ['Hello.exe', 'World.bat']
        >>> files_in_folder_filtered(given_directory, inclusive="l", exclusive=".bat")
        ['Hello.exe']
        >>> files_in_folder_filtered(given_directory, inclusive=["l", "o"])
        ['Hello.exe', 'World.bat', 'Python.py']
        >>> files_in_folder_filtered(given_directory, inclusive=[["l", "o"]])
        ['Hello.exe', 'World.bat']
        >>> files_in_folder_filtered(given_directory, inclusive=[["l", "o"],"py"])
        ['Hello.exe', 'World.bat', 'Python.py']

        """

        # checking and parsing of given arguments
        if isinstance(inclusive, str):
            if inclusive == "*":
                incl = [""]
            else:
                incl = [inclusive]
        elif isinstance(inclusive, list) and all([(isinstance(item, str) or (
                isinstance(item, list) and all([isinstance(subitem, str) for subitem in item]))) for item in
                                                  inclusive]):
            incl = inclusive[:]
        else:
            raise TypeError(
                'Invalid type of second argument (inclusive). Must be a string or a list of strings and/or lists of strings.')
        if isinstance(exclusive, str):
            if exclusive == "":
                excl = []
            else:
                excl = [exclusive]
        elif isinstance(exclusive, list) and all([(isinstance(item, str) or (
                isinstance(item, list) and all([isinstance(subitem, str) for subitem in item]))) for item in
                                                  exclusive]):
            excl = exclusive[:]
        else:
            raise TypeError(
                'Invalid type of third argument (exclusive). Must be a string or a list of strings and/or lists of strings.')
        if not isinstance(excl_prevails, bool):
            raise TypeError('Invalid type of fourth argument (excl_prevails). Must be boolean.')

        # filtering as requested
        file_list = files_in_folder(directory)
        files2incl = []
        files2excl = []
        # get lists of files to be included/excluded
        for item in incl:
            files2incl += filter_names(file_list, item, inclusive=True, match_all=True)
        for item in excl:
            files2excl += filter_names(file_list, item, inclusive=True, match_all=True)

        if excl_prevails:
            files_filtered = [fil for fil in file_list if (fil in files2incl and not fil in files2excl)]
        else:
            files_filtered = [fil for fil in file_list if (fil in files2incl or not fil in files2excl)]

        return files_filtered


    def export_csv(x, y, name, path):
        """

        Parameters
        ----------
        x: ndarray
            flat ndarray containing the x values
        y: ndarray
            flat ndarray containing the y values
        name: str
            example.csv
        path: str
            os.getcwd()

        """

        xy = np.concatenate([[x], [y]], axis=0)

        pathname = os.path.join(path, name)
        np.savetxt(pathname, xy.T, fmt='%10.5f', delimiter=' ')


    def read_yaml(filename: str, encoding: str = 'utf-8') -> object:
        with open(filename, 'r', encoding=encoding) as yaml_file:
            yaml_ = yaml.YAML()
            return yaml_.load(yaml_file)


    def write_yaml(filename: str, yaml_data: object, encoding: str = 'utf-8'):
        with open(filename, 'w', encoding=encoding) as yaml_file:
            yaml_ = yaml.YAML()

            # Style
            yaml_.indent(mapping=2, sequence=4, offset=2)
            yaml_.default_flow_style = False
            yaml_.width = 1e6

            # Representer for numpy types
            yaml_.Representer.add_representer(np.ndarray, lambda dumper, array: dumper.represent_list(array.tolist()))
            yaml_.Representer.add_representer(np.float64, lambda dumper, value: dumper.represent_float(value))
            yaml_.Representer.add_representer(np.int64, lambda dumper, value: dumper.represent_int(value))

            # Write data
            yaml_.dump(yaml_data, yaml_file)


    class NumpyEncoder(json.JSONEncoder):
        """
        https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
        """

        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
                return {'real': obj.real, 'imag': obj.imag}
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.void):
                return None
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return super(NumpyEncoder, self).default(obj)


    def write_json(file: str, data: object, indent: int = 2, encoding: str = 'utf-8'):
        """
        Saves data as JSON to file.

        Parameters
        ----------
        file
            The file where to save.
        data
            The data.
        indent:
            The intent for the JSON file.
        """
        with open(file, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, cls=NumpyEncoder)


    def read_json(file: str, encoding: str = 'utf-8') -> object:
        """
        Load data as JSON from a file.

        Parameters
        ----------
        file
            The file.

        Returns
        -------
        object
            The data.
        """
        with open(file, 'r', encoding=encoding) as f:
            return json.load(f)


    def write_cloudpickle(file: str, data: object):
        """
        Saves data as cloudpickle to file.

        Parameters
        ----------
        file
            The file where to save.
        data
            The data.
        """
        with open(file, 'wb') as f:
            cloudpickle.dump(data, f, protocol=-1)


    def read_cloudpickle(file: str) -> object:
        """
        Load data as cloudpickle from a file.

        Parameters
        ----------
        file
            The file.

        Returns
        -------
        object
            The data.
        """
        with open(file, 'rb') as f:
            return cloudpickle.load(f)
