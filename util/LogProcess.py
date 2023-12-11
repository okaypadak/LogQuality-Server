import subprocess
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = TimedRotatingFileHandler('track.log', when="midnight", interval=1, backupCount=5)  # Günde bir kez yeni dosya oluşturun
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)