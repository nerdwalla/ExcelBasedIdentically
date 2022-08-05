from data.helper.org_helper import OrgDataHelper
from data.helper.person_helper import PersonDataHelper


class SearchDuplicateHelper:

    def __init__(self, customer_df, address_df):
        self.customer_df = customer_df
        self.address_df = address_df
        self.cust_id_list = list()

    def find_duplicates(self):
        persons = self.customer_df.loc[self.customer_df['cust_type'] == 'P']
        orgs = self.customer_df.loc[self.customer_df['cust_type'] == 'O']

        if not persons.empty:
            person_data_helper = PersonDataHelper(persons)
            self.cust_id_list.extend(person_data_helper.find_duplicates())

        if not orgs.empty:
            org_data_helper = OrgDataHelper(orgs)
            self.cust_id_list.extend(org_data_helper.find_duplicates(self.address_df))

        return self.cust_id_list
