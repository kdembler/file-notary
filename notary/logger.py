import logging
from logging.handlers import QueueListener, QueueHandler
import multiprocessing as mp


def logger_init():
    log_queue = mp.Queue()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(name)s - %(message)s"))

    listener = QueueListener(log_queue, handler)
    listener.start()

    configure_logger(log_queue)

    return log_queue, listener


def configure_logger(log_queue):
    handler = QueueHandler(log_queue)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

# def get_log_queue():
#     # logging.basicConfig(level=logging.INFO)
#     log_queue = mp.Queue()
#     root = logging.getLogger()
#     h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
#     f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
#     h.setFormatter(f)
#     root.addHandler(h)
#     listener = mp.Process(target=log_listener, args=(log_queue, ))
#     listener.start()
#     return log_queue
#
#
# def log_listener(queue):
#     while True:
#         record = queue.get()
#         logger = logging.getLogger(record.name)
#         logger.handle(record)
