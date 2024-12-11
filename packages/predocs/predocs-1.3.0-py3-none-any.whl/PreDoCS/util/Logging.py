"""
Logging for PreDoCS.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import logging


def get_module_logger(mod_name):
    # logging.captureWarnings(True)
    #
    # logger = logging.getLogger(mod_name)
    # logger.setLevel(logging.INFO)
    #
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #
    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    #
    # fh = logging.FileHandler('predocs.log')
    # fh.setFormatter(formatter)
    # fh.setLevel(logging.DEBUG)
    # logger.addHandler(fh)
    #
    # return logger

    return logging.getLogger(mod_name)
