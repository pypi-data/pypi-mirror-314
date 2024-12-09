import logging
import sys

logger = logging.getLogger("emp-agents")


def make_verbose(do_all: bool = False):
    if do_all:
        root = logging.getLogger()
    else:
        root = logger
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
