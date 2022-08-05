import os
import pandas as pd


class CustomerDataHelper():

    def __init__(self):
        BASE_DIR = os.getcwd()

        self.CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "csvdata", "customers.csv")
        print(self.CUSTOMER_FILE_PATH)

    def delete_customer(self, customer_id_list):
        customer_id_list = [str(x) for x in customer_id_list]
        data = pd.read_csv(self.CUSTOMER_FILE_PATH)
        data.loc[data.cust_id.isin(customer_id_list), 'activeind'] = -1

    def reinitiate_customer(self, customer_id_list):
        customer_id_list = [str(x) for x in customer_id_list]
        data = pd.read_csv(self.CUSTOMER_FILE_PATH)
        data.loc[data.cust_id.isin(customer_id_list), 'activeind'] = 1
