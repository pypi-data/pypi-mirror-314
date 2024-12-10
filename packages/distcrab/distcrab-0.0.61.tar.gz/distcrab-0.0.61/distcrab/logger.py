#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, WARN
from sys import stdout

logger = getLogger()
logger.setLevel(WARN)
handler = StreamHandler(stdout)
handler.setLevel(WARN)
handler.terminator = ''
logger.addHandler(handler)
