# logging_setup.py
import logging

def setup_logging():
    logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

setup_logging()
