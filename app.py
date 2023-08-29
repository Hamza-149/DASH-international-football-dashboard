import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


# # Create the navbar
# navbar = html.Div(
#     className="navbar navbar-expand-lg navbar-dark bg-dark",
#     children=[
#         html.Nav(
#             className="navbar-nav",
#             children=[
#                 html.Link(
#                     className="nav-item nav-link active",
#                     href="#",
#                     **{'children': 'Home'},
#                 ),
#                 html.Link(
#                     className="nav-item nav-link",
#                     href="#",
#                     **{'children': 'About'},
#                 ),
#                 html.Link(
#                     className="nav-item nav-link",
#                     href="#",
#                     **{'children': 'Contact'},
#                 ),
#             ],
#         )
#     ],
# )


# Define the layout of the dashboard
app.layout = dbc.Container([

    # Header section
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '## International Football Dashboard',
                style={"text-align": "center"},
                )
        ])
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),

    # Tournamnet dropdown list & silder for time period
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '##### Select Tournament',
                style={"text-align": "center"},
                ),

            # Dropdown containing tournament names for users to select
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
        ], width=3),

        dbc.Col([
            dcc.Markdown(
                '##### Select Time Period',
                style={"text-align": "center"},
                ),

            # Add a slider for selecting time period
            dcc.RangeSlider(
                id='time-slider',
                marks={i: str(i) for i in range(1916, 2024, 10)},  # Marks for decades
                min=1916,
                max=2023,
                step=1,
                value=[1916, 2023]
            )
        ], width=9)
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),

    #
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '##### Most Decorated Countries',
                style={"text-align": "center"},
            ),
            dcc.Graph(id='trophy-count-hbarchart', figure=trophy_count_hbarchart('FIFA World Cup', rs))
        ], width=6),

        dbc.Col([
            dcc.Markdown(
                '##### Goals Scored Across Different Editions',
                style={"text-align": "center"},
            ),
            dcc.Graph(id='goals-count-line-plot', figure=goals_count_line_plot('FIFA World Cup', rs))
        ], width=6)
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),


    # html.Div([
    #     dcc.Markdown(f"**Most trophies won by**  \n{country_with_highest_trophy_count(tournament_name, rs)}  \nTrophies: {highest_trophy_count(tournament_name, rs)}")
    # ], className='six columns'),
        
    
    

])



@app.callback(
    [Output('goals-count-line-plot', 'figure'), Output('trophy-count-hbarchart', 'figure')],  # Update the figure of this Graph component
    [Input('time-slider', 'value'), Input('tournament-dropdown', 'value')] # Example: If you have an input component
)

def update_plots(selected_time_period, selected_tournament):
    # Filter the data based on selected years
    filtered_rs = rs[(rs['Year'] >= selected_time_period[0]) & (rs['Year'] <= selected_time_period[1])]

    # Create updated figures
    updated_goals_count_line_plot = goals_count_line_plot(selected_tournament, filtered_rs)
    updated_trophy_count_hbarchart = trophy_count_hbarchart(selected_tournament, filtered_rs)

    return updated_goals_count_line_plot, updated_trophy_count_hbarchart


if __name__ == '__main__':
    app.run_server(debug=True)