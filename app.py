import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from data_processing import processing_data
from visualizations import goals_count_line_plot, trophy_count_hbarchart


# reading the CSV files
results_df = pd.read_csv('datasets/results.csv')
shootouts_df = pd.read_csv('datasets/shootouts.csv')
goalscorers_df = pd.read_csv('datasets/goalscorers.csv')

# cleaning and preparing our data
rs = processing_data(results_df, shootouts_df)

# #creating dataframes for major tournaments
# world_cup = rs.loc[rs['Tournament'] == 'FIFA World Cup']
# copa_america = rs.loc[rs['Tournament'] == 'Copa América']
# afcon = rs.loc[rs['Tournament'] == 'African Cup of Nations']
# euros = rs.loc[rs['Tournament'] == 'UEFA Euro']
# asian_cup = rs.loc[rs['Tournament'] == 'AFC Asian Cup']


# Initialize the Dash app
app = dash.Dash(__name__)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 


# Define the layout of the dashboard
app.layout = html.Div([

    # Add a slider for selecting time period
    html.Div([
        dcc.RangeSlider(
            id='time-slider',
            marks={i: str(i) for i in range(1916, 2024, 10)},  # Marks for decades
            min=1916,
            max=2023,
            step=1,
            value=[1916, 2023]
        )
    ]),

    # Dropdown containing tournament names for users to select
    html.Div([
        dcc.Dropdown(
            id='tournament-dropdown',
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'FIFA World Cup', 'value': 'FIFA World Cup'},
                {'label': 'Copa América', 'value': 'Copa América'},
                {'label': 'African Cup of Nations', 'value': 'African Cup of Nations'},
                {'label': 'UEFA Euro', 'value': 'UEFA Euro'},
                {'label': 'AFC Asian Cup', 'value': 'AFC Asian Cup'}
            ],
            value='FIFA World Cup'  # Default value
        )
    ]),

    html.Div([
            dcc.Graph(id='goals-count-line-plot', figure=goals_count_line_plot('FIFA World Cup', rs))
        ], className='six columns'),
        
     html.Div([
        dcc.Graph(id='trophy-count-hbarchart', figure=trophy_count_hbarchart('FIFA World Cup', rs))
    ], className='col-md-6'),
    
    # html.Div([
    #     dcc.Markdown(f"**Most trophies won by**  \n{country_with_highest_trophy_count(tournament_name, rs)}  \nTrophies: {highest_trophy_count(tournament_name, rs)}")
    # ], className='six columns'),

])

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

@app.callback(
    [Output('goals-count-line-plot', 'figure'), Output('trophy-count-hbarchart', 'figure')],  # Update the figure of this Graph component
    [Input('time-slider', 'value'), Input('tournament-dropdown', 'value')] # Example: If you have an input component
)

def update_line_plot(selected_time_period, selected_tournament):
    # Filter the data based on selected years
    filtered_rs = rs[(rs['Year'] >= selected_time_period[0]) & (rs['Year'] <= selected_time_period[1])]

    # Create updated figures
    updated_line_plot = goals_count_line_plot(selected_tournament, filtered_rs)
    updated_bar_chart = trophy_count_hbarchart(selected_tournament, filtered_rs)

    return updated_line_plot, updated_bar_chart


if __name__ == '__main__':
    app.run_server(debug=True)