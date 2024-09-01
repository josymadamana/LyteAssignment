import os
import logging
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
TEST_LOG_FILENAME = os.path.join(LOG_PATH, f"pytest-{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(filename=TEST_LOG_FILENAME, level=logging.INFO,
                    format= '[%(asctime)s] [%(pathname)s:%(lineno)d] [%(levelname)s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('LyteProject')
