import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

# load the dataset
df = pd.read_csv('gdp_pcap.csv')

# fix dataset by creating year column
df.replace({r'k$': 'e3'}, regex=True, inplace=True)
df = df.melt(id_vars=['country'], var_name='year', value_name='gdpPercap').astype({'year': 'int64', 'gdpPercap': 'float'})

# stylesheet
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# define the layout of the app
app.layout = html.Div(children=[
    html.H1('Gapminder GDP Per Capita Analysis', style={'textAlign': 'center'}),
    html.P('''
        This dashboard allows users to explore GDP per capita for different countries over time (1800 - 2100). 
        The dropdown menu can be used to select one or multiple countries and the slider to choose a range of years. 
        The graph will update to show the selected countries and year range.
    ''', style={'textAlign': 'center'}),

    # dropdown for country selection
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value=['Afghanistan'],  # Default value
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    # slider for year range selection
    html.Div([
        dcc.RangeSlider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=[df['year'].min(), df['year'].max()],
            marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max() + 1, 15)},
            step=None
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    # graph to display GDP per capita
    dcc.Graph(id='gdp-graph')
])

# callback for the dropdown
@callback(
    Output('gdp-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_years):
    filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]
    graph = px.line(filtered_df, x='year', y='gdpPercap', color='country', title='GDP Per Capita Over Time')
    graph.update_layout(xaxis_title='Year', yaxis_title='GDP per Capita')
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
