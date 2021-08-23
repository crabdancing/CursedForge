# Copyleft (C) Alexandria Pettit 2021
# Simple bit of logging boilerplate


import logging
import sys

log_file_name: str = 'main.log'

root_logger = logging.root
# This ensures that all messages can get through at root level
# Message filtering happens in the handlers instead,
# allowing us to have different log levels for each handler.
# Each handler will need to be passed in a list to every class that logs.
# Yes, this is very annoying.
root_logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.DEBUG)
root_logger.addHandler(stream_handler)

file_handler = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
