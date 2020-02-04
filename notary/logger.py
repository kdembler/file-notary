import logging
from logging.handlers import QueueListener, QueueHandler
import multiprocessing as mp


def logger_init():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(name)s - %(message)s"))

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
