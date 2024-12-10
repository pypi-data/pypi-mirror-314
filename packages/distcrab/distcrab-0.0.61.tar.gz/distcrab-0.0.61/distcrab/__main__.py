#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import run
from .main import Distcrab
from .future import future

run(future(Distcrab))
