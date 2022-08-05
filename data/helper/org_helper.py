class OrgDataHelper:

    def __init__(self, org_df):
        self.org_df = org_df
        self.cust_id_list = list()

    def find_duplicates(self, address_df):
        # find duplicates by Name + TaxId
        duplicate_orgs = self.org_df[self.org_df.duplicated(['company_name', 'tax_id'])]
        if not duplicate_orgs.empty:
            self.cust_id_list.extend(duplicate_orgs['cust_id'].tolist())

        # find duplicates by Name + Address
        duplicate_orgs = self.org_df[self.org_df.duplicated(['company_name'], keep=False)]
        cust_list = duplicate_orgs['cust_id'].tolist()
        if not duplicate_orgs.empty:
            address_cust_df = address_df.loc[address_df['cust_id'].isin(cust_list)]
            duplicate_address = address_cust_df[
                address_cust_df.duplicated(['address', 'city', 'county', 'state', 'zip'], keep=False)]
            duplicate_orgs = duplicate_address[duplicate_address.duplicated(['cust_id'])]
            if not duplicate_orgs.empty:
                self.cust_id_list.extend(duplicate_orgs['cust_id'].tolist())

        return list(set(self.cust_id_list))
