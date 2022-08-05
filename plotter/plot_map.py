import plotly.graph_objects as go
import plotly.offline as pyo


class MapPlotter:

    def __init__(self, title, plotter_logger):
        self.title = title
        # Creating an object
        self.logger = plotter_logger

    def plot_agents_to_map(self, location_df):
        if location_df.empty:
            print('MapPlotter:: Plotting agents on map,  Cant map as location_df is empty ')
        else:
            print('MapPlotter:: Plotting agents on map ')
            print(location_df)
            colors = ["#FEDE00", "#A64AC9", "#04ECF0", "#FF652F", "#C55FFC"]
            location_df['count'] = location_df['count'].astype(str).astype(int)
            count_max = location_df['count'].max()
            if count_max < 50:
                location_df['count'] = location_df['count'] + 50

            fig = go.Figure()
            fig.add_trace(go.Scattergeo(
                locationmode='USA-states',
                lon=location_df['longitude'],
                lat=location_df['latitude'],
                text=location_df['text'],
                marker=dict(
                    size=location_df['count'],
                    color=colors,
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode='area'
                )
            )
            )
            fig.update_layout(
                title_text=self.title,
                showlegend=False,
                geo=dict(
                    scope='usa',
                    landcolor='rgb(217, 217, 217)'
                )
            )
            tag = pyo.plot(fig, include_plotlyjs=False, output_type='div')
            print('MapPlotter:: DIV for map plotting ' + tag)
            return tag
