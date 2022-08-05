import time
import logging
from data.file.csv_helper import FileReaderWorker
import os

def load_all_data(logger):
    delay = 1
    result_queue = []
    start_time = time.time()
    logger = logging.getLogger(__name__)
    logger.info('Start time: ' + str(start_time))

    BASE_DIR = os.getcwd()

    CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "customers.csv")
    logger.info(CUSTOMER_FILE_PATH)
    ADDRESS_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "addresses.csv")
    logger.info(ADDRESS_FILE_PATH)
    AGENT_ADDRESS_FILE_PATH =os.path.join(BASE_DIR, "csvdata", "agentaddresses.csv")
    logger.info(AGENT_ADDRESS_FILE_PATH)
    worker1 = FileReaderWorker(CUSTOMER_FILE_PATH, result_queue)
    worker2 = FileReaderWorker(ADDRESS_FILE_PATH, result_queue)
    worker3 = FileReaderWorker(AGENT_ADDRESS_FILE_PATH, result_queue)

    worker1.start()
    worker2.start()
    worker3.start()

    # Wait for the job to be done
    while len(result_queue) < 3:
        time.sleep(delay)

    job_done = True
    worker1.join()
    worker2.join()
    worker3.join()

    end_time = time.time()
    logger.info('End time: ' + str(end_time))
    logger.info("total time: " + str(end_time - start_time))
    if job_done is True:
        return result_queue


def load_customer_data(logger):

    BASE_DIR = os.getcwd()

    CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "customers.csv")
    logger.info(CUSTOMER_FILE_PATH)
    delay = 1
    result_queue = []
    start_time = time.time()
    logger.info('Start time: ' + str(start_time))
    worker1 = FileReaderWorker(CUSTOMER_FILE_PATH, result_queue)
    worker1.start()

    # Wait for the job to be done
    while len(result_queue) < 1:
        time.sleep(delay)
    job_done = True
    worker1.join()

    end_time = time.time()
    logger.info('End time: ' + str(end_time))
    logger.info("total time: " + str(end_time - start_time))
    if job_done:
        return result_queue
