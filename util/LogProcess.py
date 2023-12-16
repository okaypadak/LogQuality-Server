import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# Log dosyas?n? ve konsolu destekleyen bir logger olu?turun
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Dosyaya loglama için TimedRotatingFileHandler kullan?n
file_handler = TimedRotatingFileHandler('track.log', when="midnight", interval=1, backupCount=5, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Konsola loglama için StreamHandler kullan?n
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

