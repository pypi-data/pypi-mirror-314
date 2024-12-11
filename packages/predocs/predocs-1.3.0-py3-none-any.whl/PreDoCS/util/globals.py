"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from cpacs_interface.utils.globals import *
except ImportError:
    log.info('Modul cpacs_interface.utils.globals not found. Use PreDoCS globals utils class.')

    import logging
    import os
    import sys
    from contextlib import ContextDecorator
    from importlib.metadata import version
    from pathlib import Path
    from typing import Union
    import numpy as np

    num = np

    _is_init = False


    def core_init(run_dir: Union[str, Path] = None):
        """
        Sets the path to PYTHONPATH environment variable and starts a logger. The log-files will
        be created in the current working directory.
        """
        global _is_init
        if _is_init:
            logging.warning('CPACS Interface already initialised.')
        else:
            root = logging.getLogger()
            root.handlers.clear()
            root.setLevel(logging.DEBUG)
            log_format = logging.Formatter("%(asctime)s: %(levelname)s: %(module)s: %(message)s")
            logging.captureWarnings(True)

            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(log_format)
            ch.setLevel(logging.INFO)
            root.addHandler(ch)

            if run_dir is not None:
                if not Path(run_dir).exists():
                    os.makedirs(run_dir)
                path = Path(run_dir) / 'run.log'
            else:
                path = 'run.log'

            write_version_file(run_dir)

            run = logging.FileHandler(path, mode='w')
            run.setFormatter(log_format)
            run.setLevel(logging.INFO)
            root.addHandler(run)

            if run_dir is not None:
                path = Path(run_dir) / 'debug.log'
            else:
                path = 'debug.log'
            debug = logging.FileHandler(path, mode='w')
            debug.setFormatter(log_format)
            debug.setLevel(logging.DEBUG)
            root.addHandler(debug)

            log = logging.getLogger(__name__)
            log.debug('logger started')

            _is_init = True


    def write_version_file(run_dir: Union[str, Path] = None) -> Path:
        """
        Writes a cpacs_interface version file in run_dir or in current working directory if run_dir is None.

        Parameters
        ----------
        run_dir : Union[str, Path]
            path to write the version file to

        """
        if run_dir is None:
            run_dir = Path().cwd()
        else:
            assert Path(run_dir).exists(), f'path {run_dir} does not exist or is not a path.'
        file_path = Path(run_dir) / 'predocs_version.txt'
        with open(file_path, 'w+') as f:
            f.write(f"predocs: {version('predocs')}")
        return file_path


    class DuplicateFilter(ContextDecorator):
        """
        Filters away duplicate log messages.
        Modified version of: https://stackoverflow.com/a/31953563/965332
        """

        def __init__(self, logger):
            self.msgs = set()
            self.logger = logger

        def filter(self, record):
            msg = str(record.msg)
            is_duplicate = msg in self.msgs
            if not is_duplicate:
                self.msgs.add(msg)
            return not is_duplicate

        def __enter__(self):
            self.logger.addFilter(self)

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self in self.logger.filters:
                self.logger.removeFilter(self)


    class Found(Exception):
        """
        Class for exiting nested loops.
        """
        pass
