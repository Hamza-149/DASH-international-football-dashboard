import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data_processing import processing_data
from visualizations import goals_count_line_plot, trophy_count_hbarchart
from stats import get_highest_goalscoring_edition, get_country_with_highest_trophy_count


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

    # champions data
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '##### Champions',
                style={"text-align": "center"},
            ),
            dcc.Graph(id='trophy-count-hbarchart', figure=trophy_count_hbarchart('FIFA World Cup', rs.copy()))
        ], width=9),

        dbc.Col([
            dcc.Markdown(
                '##### Most Decorated Countries',
                style={"text-align": "center"},
            ),

            # Countries who have won the most
            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='most-decorated-countries-md-1',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='most-trophies-won-md-1',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='most-decorated-countries-md-2',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='most-trophies-won-md-2',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='most-decorated-countries-md-3',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='most-trophies-won-md-3',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            
        ], width=3)
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),



    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '##### Goals Scored Across Different Editions',
                style={"text-align": "center"},
            ),
            dcc.Graph(id='goals-count-line-plot', figure=goals_count_line_plot('FIFA World Cup', rs.copy()))
        ], width=9),

        # Top 3 editions wth most goals scored
        dbc.Col([
            dcc.Markdown(
                '##### Highest Goalscoring Editions',
                style={"text-align": "center"},
            ),

            # Year/Edition of highest scoring tournaments
            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='highest-goalscoring-editions-md-1',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-1',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='highest-goalscoring-editions-md-2',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-2',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='highest-goalscoring-editions-md-3',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-3',
                        style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            
        ], width=3)
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),


    # html.Div([
    #     dcc.Markdown(f"**Most trophies won by**  \n{country_with_highest_trophy_count(tournament_name, rs)}  \nTrophies: {highest_trophy_count(tournament_name, rs)}")
    # ], className='six columns'),
        
    
    

])



@app.callback(
    [Output('goals-count-line-plot', 'figure'), 
     Output('trophy-count-hbarchart', 'figure'),
     Output('most-decorated-countries-md-1', 'children'),
     Output('most-decorated-countries-md-2', 'children'),
     Output('most-decorated-countries-md-3', 'children'),
     Output('most-trophies-won-md-1', 'children'),
     Output('most-trophies-won-md-2', 'children'),
     Output('most-trophies-won-md-3', 'children'), 
     Output('highest-goalscoring-editions-md-1', 'children'),
     Output('highest-goalscoring-editions-md-2', 'children'),
     Output('highest-goalscoring-editions-md-3', 'children'),
     Output('highest-num-goals-scored-md-1', 'children'),
     Output('highest-num-goals-scored-md-2', 'children'),
     Output('highest-num-goals-scored-md-3', 'children'),
    ],

    [Input('time-slider', 'value'), 
     Input('tournament-dropdown', 'value')
    ]
)

def update_plots(selected_time_period, selected_tournament):
    # Filter the data based on selected years
    filtered_rs = rs[(rs['Year'] >= selected_time_period[0]) & (rs['Year'] <= selected_time_period[1])]

    # Create updated figures
    updated_goals_count_line_plot = goals_count_line_plot(selected_tournament, filtered_rs.copy())
    updated_trophy_count_hbarchart = trophy_count_hbarchart(selected_tournament, filtered_rs.copy())

    #
    country_with_highest_trophy_count_df = get_country_with_highest_trophy_count(selected_tournament, filtered_rs.copy())

    most_decorated_countries = country_with_highest_trophy_count_df['Winner'].tolist()
    most_trophies_won = country_with_highest_trophy_count_df['Trophies won overall'].tolist()

    most_decorated_countries_md_1 = '1. ' + str(most_decorated_countries[0])
    most_decorated_countries_md_2 = '2. ' + str(most_decorated_countries[1])
    most_decorated_countries_md_3 = '3. ' + str(most_decorated_countries[2])
    most_trophies_won_md_1 = str(int(most_trophies_won[0]))
    most_trophies_won_md_2 = str(int(most_trophies_won[1]))
    most_trophies_won_md_3 = str(int(most_trophies_won[2]))

    #
    highest_scoring_editions_df = get_highest_goalscoring_edition(selected_tournament, filtered_rs.copy())

    highest_scoring_editions = highest_scoring_editions_df.index.tolist()
    highest_num_goals_scored = highest_scoring_editions_df['Goals Scored'].tolist()


    highest_goalscoring_editions_md_1 = '1. ' + str(highest_scoring_editions[0])
    highest_goalscoring_editions_md_2 = '2. ' + str(highest_scoring_editions[1])
    highest_goalscoring_editions_md_3 = '3. ' + str(highest_scoring_editions[2])

    highest_num_goals_scored_md_1 = str(int(highest_num_goals_scored[0]))
    highest_num_goals_scored_md_2 = str(int(highest_num_goals_scored[1]))
    highest_num_goals_scored_md_3 = str(int(highest_num_goals_scored[2]))



    return (
        updated_goals_count_line_plot,
        updated_trophy_count_hbarchart,
        most_decorated_countries_md_1,
        most_decorated_countries_md_2,
        most_decorated_countries_md_3,
        most_trophies_won_md_1,
        most_trophies_won_md_2,
        most_trophies_won_md_3,
        highest_goalscoring_editions_md_1,
        highest_goalscoring_editions_md_2,
        highest_goalscoring_editions_md_3,
        highest_num_goals_scored_md_1,
        highest_num_goals_scored_md_2,
        highest_num_goals_scored_md_3
    )


if __name__ == '__main__':
    app.run_server(debug=True)