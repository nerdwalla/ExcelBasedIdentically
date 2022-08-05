from threading import Thread, Lock
import pandas as pd
# import logging


class FileReaderWorker(Thread):
    __lock = Lock()

    def __init__(self, csvpath, result_queue):
        Thread.__init__(self)

        self.csvpath = csvpath
        self.result_queue = result_queue

        # # Setting the threshold of logger to DEBUG
        # self.logger.setLevel(logging.INFO)

    def run(self):
        print("Reading File from..." + str(self.csvpath))
        try:

            data = pd.read_csv(self.csvpath)

            print("Result with: " + str(self.csvpath))
            print(data)
            self.result_queue.append(data)
        except Exception as e:
            print("Result with: " + str(e))

        print("Done With Reading File from .." + str(self.csvpath))


