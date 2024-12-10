# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
"""
Personal knowledge Library
--------------------------
This library provides a set of tools to manage Wacom private knowledge graph API.
All services are wrapped in a pythonic way to make it easy to use.
Additionally, the library provides a set of tools to utilise Wikidata.
"""
import logging
from typing import Union

__author__ = "Markus Weber"
__copyright__ = "Copyright 2021-2024 Wacom. All rights reserved."
__credits__ = ["Markus Weber"]
__license__ = "Wacom"
__maintainer__ = ["Markus Weber"]
__email__ = "markus.weber@wacom.com"
__status__ = "beta"
__version__ = "2.4.2"

# Create the Logger
logger: Union[logging.Logger, None] = None

if logger is None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch: logging.StreamHandler = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)


__all__ = ['__copyright__', '__credits__', '__license__', '__maintainer__', '__email__', '__status__', '__version__',
           'logger', 'base', 'nel', 'public', 'services', 'utils']

from knowledge import base
from knowledge import nel
from knowledge import public
from knowledge import services
from knowledge import utils
