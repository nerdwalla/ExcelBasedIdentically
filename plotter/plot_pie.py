import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd


class PiePlotter:

    def __init__(self, title):
        self.title = title
        # Creating an object
        # self.logger = logging.getLogger(__name__)

    def plot_pie_for_systems(self, duplicate_customers_by_system):
        if duplicate_customers_by_system.empty:
            print('PiePlotter:: Plotting Systems Type on Pie chart, Cant as '
                  'duplicate_customers_by_system is Empty')
        else:
            print('PiePlotter:: Plotting Systems on Pie chart ')
            print(duplicate_customers_by_system)

            duplicate_customers_by_system_counts = dict(duplicate_customers_by_system['updated_by'].value_counts())

            value_series = pd.Series(duplicate_customers_by_system_counts.values())

            key_series = pd.Series(duplicate_customers_by_system_counts.keys())

            colors = ['blue', 'red', 'lightblue', 'orange']
            fig = go.Figure(data=go.Pie(values=value_series,
                                        labels=key_series,
                                        title=self.title,
                                        marker_colors=colors))
            fig.update_traces(
                title_font=dict(size=25, family='Verdana',
                                color='darkred'),
                hoverinfo='label+percent',
                textinfo='percent',
                textfont_size=20,
            )

            tag = pyo.plot(fig, include_plotlyjs=False, output_type='div')
            print('PiePlotter:: DIV for Pie chart plotting ' + tag)
            return tag

    def plot_pie_for_customer_type(self, duplicate_customers, title):
        if duplicate_customers.empty:
            print('PiePlotter:: Plotting Customer Type on Pie chart, Cant as duplicate_customers '
                  'is Empty')
        else:
            print('PiePlotter:: Plotting Customer Type on Pie chart ')

            duplicate_customers_cust_type_counts = dict(duplicate_customers['cust_type'].value_counts())
            cust_type_counts = dict()
            cust_type_counts["Person"] = duplicate_customers_cust_type_counts["P"]
            cust_type_counts["Organization"] = duplicate_customers_cust_type_counts["O"]

            value_series = pd.Series(cust_type_counts.values())

            key_series = pd.Series(cust_type_counts.keys())

            colors = ['blue', 'red', 'lightblue', 'orange']
            fig = go.Figure(data=go.Pie(values=value_series,
                                        labels=key_series,
                                        title=title,
                                        marker_colors=colors))
            fig.update_traces(
                title_font=dict(size=25, family='Verdana',
                                color='darkred'),
                hoverinfo='label+percent',
                textinfo='percent',
                textfont_size=20,
            )

            tag = pyo.plot(fig, include_plotlyjs=False, output_type='div')
            print('PiePlotter:: DIV for Pie Chart plotting ' + tag)
            return tag
