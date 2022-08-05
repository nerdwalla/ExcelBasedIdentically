from flask import Flask, render_template, request
from data.helper.search_duplicate_helper import SearchDuplicateHelper
from data.helper.agent_helper import AgentDataHelper
from plotter.plot_map import MapPlotter
from plotter.plot_pie import PiePlotter
from all_data_loader import load_all_data, load_customer_data
import concurrent.futures

app = Flask(__name__)
customer_df = None
address_df = None
agent_address_df = None
duplicate_customer_df = None


@app.route("/", methods=['GET', 'POST'])
def index():
    # global server_logger
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # print('Page Loaded')
        print('Page Loaded')
        # find_duplicate_customers()
    return render_template('index.html')


@app.route('/add_user/')
def add_user():
    # print('Add user clicked')
    print('Add User Clicked')
    return ""


@app.route('/plot-agents/')
def plot_agents():
    # global server_logger
    print('plot-agent got clicked!')
    # app.logger.info('plot-agent got clicked!')
    image_file_name = create_plot_image()
    return image_file_name


@app.route('/remove-duplicates/')
def remove_duplicates():
    # global server_logger
    print('remove_duplicates got clicked!')
    # app.logger.info('remove_duplicates got clicked!')
    global duplicate_customer_df
    try:
        # reload_customer_data()
        if not duplicate_customer_df.empty:
            table_data = build_customer_table(duplicate_customer_df)
            # delete_duplicate_customers(duplicate_customer_df["cust_id"].tolist())
            return table_data
        else:
            div_tag = "<div><p>No duplicates found</p></div>"
            return div_tag
    except Exception as e:
        print(e)
        # app.logger.error(e)


@app.route('/find-duplicates/')
def find_duplicates():
    # global server_logger
    print('find_duplicates got clicked!')
    # app.logger.info('find_duplicates got clicked!')
    global duplicate_customer_df

    table_data = build_customer_table(duplicate_customer_df)
    return table_data


@app.route('/find-systems/')
def find_systems():
    # global server_logger
    print('find-systems got clicked!')
    # app.logger.info('find_systems got clicked!')
    div_tag = plot_system_pie(duplicate_customer_df)
    return div_tag


@app.route('/duplicate-customer-type/')
def duplicate_customer_type():
    global server_logger
    print('duplicate_customer_type got clicked!')
    # app.logger.info('duplicate_customer_type got clicked!')
    div_tag = plot_customer_type_pie(duplicate_customer_df)
    return div_tag


def build_customer_table(duplicate_customers):
    if not duplicate_customers.empty:
        customer_table_str = '<caption>Duplicate records removed <span class="count">(Count: ' + str(len(
            duplicate_customers)) + ')<span></caption><thead> <tr><th>Customer ID</th><th>Company Name</th><th>First ' \
                                    'Name</th> <th>Last Name</th><th>Updated by</th></tr></thead><tbody> '
        for idx, row in duplicate_customers.iterrows():
            customer_table_str += '<tr>'
            customer_table_str += '<td>'
            customer_table_str += str(row['cust_id'])
            customer_table_str += '</td>'
            customer_table_str += '<td>'
            customer_table_str += str(row['company_name'])
            customer_table_str += '</td>'
            customer_table_str += '<td>'
            customer_table_str += row['first_name']
            customer_table_str += '</td>'
            customer_table_str += '<td>'
            customer_table_str += row['last_name']
            customer_table_str += '</td>'
            customer_table_str += '<td>'
            customer_table_str += row['updated_by']
            customer_table_str += '</td>'
            customer_table_str += '</tr>'
        customer_table_str += '</tbody>'
        return customer_table_str
    else:
        div_tag = "<div><p>No duplicates found</p></div>"
        return div_tag


def plot_system_pie(duplicate_customers):
    # global plotter_logger
    if not duplicate_customers.empty:
        agent_starter_string = "agent"
        duplicate_customers_by_system = duplicate_customers[
            ~duplicate_customers["updated_by"].str.startswith(agent_starter_string, na=False)]

        plotter = PiePlotter("Systems with Duplicate Customers")

        div_tag = plotter.plot_pie_for_systems(duplicate_customers_by_system)
        return div_tag
    else:
        div_tag = "<div><p>No duplicates found</p></div>"
        return div_tag


def plot_customer_type_pie(duplicate_customers):
    if not duplicate_customers.empty:
        plotter = PiePlotter("Duplicate Customers by customer type")
        div_tag = plotter.plot_pie_for_customer_type(duplicate_customers, "Duplicate Customers by customer type")
        return div_tag
    else:
        div_tag = "<div><p>No duplicates found</p></div>"
        return div_tag


def load_data():
    global customer_df, address_df, agent_address_df
    # get Data from customers table
    print("Loading data...")
    # app.logger.info("Loading data...")
    result_queue = load_all_data()

    for result in result_queue:
        if "first_name" in result.columns:
            temp_customer_df = result
            temp_customer_df.fillna('', inplace=True)
            customer_df = temp_customer_df[temp_customer_df['activeind'] == 1]
        elif "agent_id" in result.columns:
            agent_address_df = result
            agent_address_df.fillna('', inplace=True)
        elif "city" in result.columns:
            address_df = result
            address_df.fillna('', inplace=True)


def find_duplicate_customer_ids():
    global customer_df, address_df
    search_helper = SearchDuplicateHelper(customer_df, address_df)
    return search_helper.find_duplicates()


# def delete_duplicate_customers(duplicate_cust_id_list):
#     global customer_df, server_logger
#     print("Number of duplicates: ", len(duplicate_cust_id_list))
#
#     if duplicate_cust_id_list is not None and len(duplicate_cust_id_list) != 0:
#         # delete the duplicates
#         dao = CustomerDAO()
#         dao.delete_customer(duplicate_cust_id_list)


def find_duplicate_customers():
    global customer_df, address_df
    global duplicate_customer_df
    search_helper = SearchDuplicateHelper(customer_df, address_df)
    duplicate_customer_id_list = search_helper.find_duplicates()
    duplicate_customer_df = customer_df.loc[customer_df['cust_id'].isin(duplicate_customer_id_list)]


def find_agents_ids_of_duplicate_customers():
    global duplicate_customer_df
    agent_helper = AgentDataHelper()
    agent_id_list = agent_helper.get_agents_id_list(duplicate_customer_df)
    return agent_id_list


def create_plot_image():
    global duplicate_customer_df
    if not duplicate_customer_df.empty:
        agent_helper = AgentDataHelper(agent_address_df)
        location_df = agent_helper.get_agents_location(duplicate_customer_df)
        plotter = MapPlotter("Agents with Duplicate Customers")
        div_tag = plotter.plot_agents_to_map(location_df)
        # print(div_tag)
        app.logger.info(div_tag)
        return div_tag
    else:
        div_tag = "<div><p>No duplicates found</p></div>"
        app.logger.info(div_tag)
        return div_tag


def reload_customer_data():
    global customer_df
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(load_customer_data)
        return_value = future.result()
        print(return_value)
        # app.logger.info(return_value)
    # result_queue = load_customer_data(data_loader_logger)
    for result in return_value:
        if "first_name" in result.columns:
            customer_df = result
            customer_df.fillna('', inplace=True)


if __name__ == '__main__':
    # Load Data
    load_data()
    find_duplicate_customers()
    # Run Application
    app.run()
