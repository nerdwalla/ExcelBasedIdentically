import pandas as pd


class AgentDataHelper:

    def __init__(self, agents_address_df):
        self.agents_address_df = agents_address_df

    def get_agents_location(self, duplicate_customers_df):
        duplicate_customers_agent_id_list = duplicate_customers_df['updated_by'].tolist()
        agent_count = duplicate_customers_df['updated_by'].value_counts()

        agent_info_df = self.agents_address_df.loc[
            self.agents_address_df['agent_id'].isin(duplicate_customers_agent_id_list)]

        map_df = pd.DataFrame(columns=['latitude', 'longitude', 'count', 'city', 'text'])
        for index, row in agent_info_df.iterrows():
            count = agent_count[row['agent_id']]
            # location_dict = {'latitude': row['latitude'], 'longitude': row['longitude'], 'count': int(count),
            #                  'city': row['city'], 'text': row['agent_id'] + " - " + row['city'] + " - " + str(count)}
            # map_df = map_df.append(location_dict, ignore_index=True)
            # map_df = pd.concat(map_df, pd.DataFrame.from_dict(location_dict))
            # print(location_dict)
            # dict_df = pd.DataFrame(list(location_dict.items()), columns=['latitude', 'longitude', 'count', 'city', 'text'])
            # dict_df = pd.DataFrame([location_dict])
            # map_df = pd.concat(map_df, dict_df)
            map_df.loc[len(map_df.index)] = [row['latitude'],  row['longitude'], int(count), row['city'], row['agent_id'] + " - " + row['city'] + " - " + str(count)]
        return map_df



    def get_agents_id_list(self, duplicate_customers_df):
        duplicate_customers_agent_id_list = duplicate_customers_df['updated_by'].tolist()
        duplicate_customers_agent_id_list = list(set(duplicate_customers_agent_id_list))
        return duplicate_customers_agent_id_list
