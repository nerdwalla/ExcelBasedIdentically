from threading import Thread, Lock
import pandas as pd
import logging


class FileReaderWorker(Thread):
    __lock = Lock()

    def __init__(self, csvpath, result_queue):
        Thread.__init__(self)

        self.csvpath = csvpath
        self.result_queue = result_queue
        self.logger = logging.getLogger(__name__)

        # # Setting the threshold of logger to DEBUG
        # self.logger.setLevel(logging.INFO)

    def run(self):
        self.logger.info("Reading File from..." + str(self.csvpath))
        try:

            data = pd.read_csv(self.csvpath)

            self.logger.info("Result with: " + str(self.csvpath))
            self.logger.info(data)
            self.result_queue.append(data)
        except Exception as e:
            self.logger.error("Result with: " + str(e))

        self.logger.info("Done With Reading File from .." + str(self.csvpath))


