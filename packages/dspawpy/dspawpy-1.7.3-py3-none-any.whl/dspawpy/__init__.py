import os
import sys

import polars as pl
from loguru import logger

pl.Config.set_tbl_hide_column_data_types(True)

# allow expand all rows and columns
if os.environ.get("ALWAYS_EXPAND") == "True":
    pl.Config.set_tbl_rows(-1)
    pl.Config.set_tbl_cols(-1)


if os.environ.get("dspawpy_cli_test") == "manual":
    append_json = True
    auto_test_cli = False
elif os.environ.get("dspawpy_cli_test") == "auto":
    append_json = False
    auto_test_cli = True
else:
    append_json = False
    auto_test_cli = False


__version__ = "1.7.3"
assert sys.version_info >= (3, 8)

logger.remove()
level = os.getenv("DLL")  # dspawpy log level
if level:  # default to simulate no log
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:MM-DD HH:mm:ss:SSS}</green> | <level>{message}</level>",
    )
else:
    logger.add(
        sys.stderr,
        colorize=True,
        format="<level>{message}</level>",
    )

logger.add(
    ".dspawpy.log",
    level="DEBUG",
    rotation="1 day",
    retention="1 week",
    compression="zip",
)
