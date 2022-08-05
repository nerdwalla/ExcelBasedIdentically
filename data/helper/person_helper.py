class PersonDataHelper:
    def __init__(self, person_df):
        self.person_df = person_df
        self.cust_id_list = list()

    def find_duplicates(self):
        # find duplicates by FirstName + LastName + TaxId
        duplicate_person = self.person_df[self.person_df.duplicated(['first_name', 'last_name', 'tax_id'])]
        if not duplicate_person.empty:
            self.cust_id_list.extend(duplicate_person['cust_id'].tolist())

        # find duplicates by FirstName + LastName + Phone
        duplicate_person = self.person_df[self.person_df.duplicated(['first_name', 'last_name', 'phone'])]
        if not duplicate_person.empty:
            self.cust_id_list.extend(duplicate_person['cust_id'].tolist())

        # find duplicates by FirstName + LastName + Email
        duplicate_person = self.person_df[self.person_df.duplicated(['first_name', 'last_name', 'email'])]
        if not duplicate_person.empty:
            self.cust_id_list.extend(duplicate_person['cust_id'].tolist())

        return list(set(self.cust_id_list))
