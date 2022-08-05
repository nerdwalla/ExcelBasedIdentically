import time
from data.file.csv_helper import FileReaderWorker
import os


def load_all_data():
    delay = 1
    result_queue = []
    start_time = time.time()

    print('Start time: ' + str(start_time))

    BASE_DIR = os.getcwd()

    CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "customers.csv")
    print(CUSTOMER_FILE_PATH)
    ADDRESS_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "addresses.csv")
    print(ADDRESS_FILE_PATH)
    AGENT_ADDRESS_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "agentaddresses.csv")
    print(AGENT_ADDRESS_FILE_PATH)
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
    print('End time: ' + str(end_time))
    print("total time: " + str(end_time - start_time))
    if job_done is True:
        return result_queue


def load_customer_data(logger):
    BASE_DIR = os.getcwd()

    CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "customers.csv")
    print(CUSTOMER_FILE_PATH)
    delay = 1
    result_queue = []
    start_time = time.time()
    print('Start time: ' + str(start_time))
    worker1 = FileReaderWorker(CUSTOMER_FILE_PATH, result_queue)
    worker1.start()

    # Wait for the job to be done
    while len(result_queue) < 1:
        time.sleep(delay)
    job_done = True
    worker1.join()

    end_time = time.time()
    print('End time: ' + str(end_time))
    print("total time: " + str(end_time - start_time))
    if job_done:
        return result_queue
