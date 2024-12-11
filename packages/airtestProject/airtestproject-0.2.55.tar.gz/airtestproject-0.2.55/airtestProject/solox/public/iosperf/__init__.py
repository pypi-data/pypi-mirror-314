#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Created on Mon Jan 04 2021 17:59:30 by codeskyblue
"""

# from airtestProject.solox.public.iosperf._device import BaseDevice as Device
# from airtestProject.solox.public.iosperf._usbmux import Usbmux, ConnectionType
from airtestProject.solox.public.iosperf._perf import Performance, DataType
from airtestProject.solox.public.iosperf.exceptions import *
from airtestProject.solox.public.iosperf._proto import PROGRAM_NAME
from loguru import logger


logger.disable(PROGRAM_NAME)