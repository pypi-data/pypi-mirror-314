import logging
from loguru import logger as _logger
import traceback
import orjson
from rich import print as rprint
import sys
import rich.logging
import rich.traceback
from rich.traceback import Traceback
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import pprint as richp, Node, Pretty
from rich.pretty import pretty_repr

console = Console()


def get_pretty_output(obj):
    console = Console()
    # Create a StringIO buffer to capture the output
    with console.capture() as capture:
        # Create a Pretty object and render it to the capture buffer
        console.print(Pretty(obj, expand_all=True, overflow="ignore"))

    # Return the captured output as a string
    return capture.get()


def patching(record):
    msg = record.get("message")

    # Convert single quotes to double quotes for JSON compatibility
    msg = msg.replace("'", '"')

    try:
        # Attempt to parse the message as JSON
        json_res = orjson.loads(msg)
    except ValueError:
        # If parsing fails, return without modifying the record further
        json_res = {}

    # Ensure the 'extra' field is initialized
    if "extra" not in record:
        record["extra"] = {}

    # If the message was successfully parsed as JSON, add its contents to the 'extra' field

    if isinstance(json_res, dict):
        for key, value in json_res.items():
            record["extra"][key] = value

    # Add the log level to the 'extra' field
    record["extra"]["_level"] = record["level"].name


# List of modules to suppress in Rich traceback for cleaner output
SUPPRESSED_MODULES = [
    # "fire",
    # "monai.bundle",
    # "lighter.utils.cli",
    # "lighter.utils.runner",
    # "pytorch_lightning.trainer",
    # "lightning_utilities",
]


class Logger:
    def __init__(self):
        # This will install rich to traceback, which is quite handy
        rich.traceback.install(
            show_locals=False,
            suppress=[__import__(name) for name in SUPPRESSED_MODULES],
        )

        config = {
            "handlers": [
                {
                    "sink": RichHandler(
                        show_level=False,
                        show_time=True,
                        rich_tracebacks=True,
                        markup=True,
                        omit_repeated_times=False,
                    ),
                    # "sink": sys.stdout,
                    # This will force us to only use the rich handler on normal levels
                    "filter": lambda record: record["level"].name == "INFO",
                    "format": "{message}",
                },
                # {
                #     "sink": sys.stdout,
                #     "colorize": True,
                #     "backtrace": True,
                #     "diagnose": True,
                #     "enqueue": False,
                #     "format": "<cyan>❯ {module}:{function} ({line})</cyan> | <green>{time:YYYY-MM-DD at HH:mm:ss.sss}</green>",
                #     "filter": lambda record: record["level"].name == "INFO",
                # },
                {
                    "sink": "/opt/logs/logs.log",
                    "level": "DEBUG",
                    "serialize": True,
                    "enqueue": True,
                    "colorize": True,
                    "format": "<light-cyan>❯ {module}:{function} ({line})</light-cyan> | <light-black>{time:YYYY-MM-DD at HH:mm:ss.sss}</light-black>\n{message}",
                },
            ],
        }

        _logger.configure(**config)  # type: ignore
        self.logger = _logger.patch(patching)

    def error(self):
        console.print(Traceback())
        recent_traceback = traceback.format_exc(limit=10)
        self.logger.error(recent_traceback)

    def warning(self, obj):
        self.logger.opt(depth=2).warning(pretty_repr(obj))

    def info(self, obj):
        self.logger.opt(depth=2).info(pretty_repr(obj))

    def print(self, obj):
        self.logger.opt(depth=2).info(pretty_repr(obj))
        # rprint(obj)


pprint = print

logger = Logger()


# print = logger.logger.info
def print(obj):
    logger.print(obj)
    # logger.logger.info(obj)
