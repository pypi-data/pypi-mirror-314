#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from argparse import ArgumentParser, Action

class FirmwareAction(Action):
    def __init__(self, option_strings, abbr, *args, **kwargs):
        self.abbr = abbr
        super(FirmwareAction, self).__init__(option_strings=option_strings, *args, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            setattr(namespace, self.dest, values)
        else:
            setattr(namespace, self.dest, self.abbr)

PARSER = ArgumentParser()
PARSER.add_argument('--host', type=str, default=environ.get('SSH_HOST', '192.168.1.200'))
PARSER.add_argument('--port', type=int, default=environ.get('SSH_PORT', 22))
PARSER.add_argument('--username', type=str, default=environ.get('SSH_USERNAME', 'root'))
PARSER.add_argument('--password', type=str, default=environ.get('SSH_PASSWORD', 'elite2014'))
PARSER.add_argument('--firmware', action=FirmwareAction, default=environ.get('FIRMWARE', None), abbr='http://192.168.21.1:5080/APP/develop/develop/update/industry/preview/test-cmake/firmware.bin')
PARSER.add_argument('--branch', type=str, default=environ.get('GIT_BRANCH', None))
PARSER.add_argument('--version', type=str, default=environ.get('GIT_VERSION', None))
PARSER.add_argument('--download', action='store_true', default=environ.get('DOWNLOAD', False))
