
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .logger import logger
from .parser import PARSER

async def future(Procedure):
    async for item in Procedure(**vars(PARSER.parse_args())):
        try:
            logger.warning(item.decode())
        except Exception:
            logger.warning(item)
