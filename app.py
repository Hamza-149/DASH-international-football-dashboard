import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data_processing import processing_data
from visualizations import goals_count_line_plot, trophy_count_hbarchart
from stats import get_highest_goalscoring_edition, get_country_with_highest_trophy_count, get_defending_champion


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
        # hbar chart to display the past champions of the selected tournament
        dbc.Col([
            dcc.Markdown(
                '##### Champions',
                style={"text-align": "center"},
            ),
            dcc.Graph(id='trophy-count-hbarchart', figure=trophy_count_hbarchart('FIFA World Cup', rs.copy()))
        ], width=9),

        # Countries who have won the most trophies
        dbc.Col([

            # defending champions
            dbc.Row([
                dcc.Markdown(
                    '##### Defending Champion',
                    style={"text-align": "center"},
                ),

                dbc.Row([
                    dbc.Col([
                        dcc.Markdown(
                            id='defending-champion-md-1',
                            style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                        ),
                    ], width=6),
                    dbc.Col([
                        dcc.Markdown(
                            id='defending-champion-md-2',
                            style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
                        ),
                    ], width=6),
                ], style={"padding-top": "20px", "padding-bottom": "20px"}),
            ]),

            # top 3 countries with most silverware
            dbc.Row([
                dcc.Markdown(
                    '##### Most Decorated Countries',
                    style={"text-align": "center"},
                ),

                dbc.Row([
                    dbc.Col([
                        dcc.Markdown(
                            id='most-decorated-countries-md-1',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "gold",
                            },
                        ),
                    ], width=6),
                    dbc.Col([
                        dcc.Markdown(
                            id='most-trophies-won-md-1',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "gold",
                            },
                        ),
                    ], width=6),
                ], style={"padding-top": "20px", "padding-bottom": "20px"}),

                dbc.Row([
                    dbc.Col([
                        dcc.Markdown(
                            id='most-decorated-countries-md-2',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "silver",
                            },
                        ),
                    ], width=6),
                    dbc.Col([
                        dcc.Markdown(
                            id='most-trophies-won-md-2',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "silver",
                            },
                        ),
                    ], width=6),
                ], style={"padding-top": "20px", "padding-bottom": "20px"}),

                dbc.Row([
                    dbc.Col([
                        dcc.Markdown(
                            id='most-decorated-countries-md-3',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "#CD7F32",
                            },
                        ),
                    ], width=6),
                    dbc.Col([
                        dcc.Markdown(
                            id='most-trophies-won-md-3',
                            style={
                                "text-align": "center",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "color": "#CD7F32",
                            },
                        ),
                    ], width=6),
                ], style={"padding-top": "20px", "padding-bottom": "20px"}),
            ]),

            # dcc.Markdown(
            #     '##### Most Decorated Countries',
            #     style={"text-align": "center"},
            # ),

            # # data 
            # dbc.Row([
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-decorated-countries-md-1',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-trophies-won-md-1',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            # ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            # dbc.Row([
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-decorated-countries-md-2',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-trophies-won-md-2',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            # ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            # dbc.Row([
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-decorated-countries-md-3',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            #     dbc.Col([
            #         dcc.Markdown(
            #             id='most-trophies-won-md-3',
            #             style={"text-align": "center", "padding-top": "10px", "padding-bottom": "10px"},
            #         ),
            #     ], width=6),
            # ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            
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
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "gold",
                        },
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-1',
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "gold",
                        },
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='highest-goalscoring-editions-md-2',
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "silver",
                        },
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-2',
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "silver",
                        },
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),

            dbc.Row([
                dbc.Col([
                    dcc.Markdown(
                        id='highest-goalscoring-editions-md-3',
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "#CD7F32",
                        },
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Markdown(
                        id='highest-num-goals-scored-md-3',
                        style={
                            "text-align": "center",
                            "padding-top": "10px",
                            "padding-bottom": "10px",
                            "color": "#CD7F32",
                        },
                    ),
                ], width=6),
            ], style={"padding-top": "20px", "padding-bottom": "20px"}),


            
        ], width=3)
    ], style={"padding-top": "20px", "padding-bottom": "20px"}),

        

])



@app.callback(
    [Output('goals-count-line-plot', 'figure'), 
     Output('trophy-count-hbarchart', 'figure'),
     Output('defending-champion-md-1', 'children'),
     Output('defending-champion-md-2', 'children'),
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

def update_data(selected_time_period, selected_tournament):
    # Filter the data based on selected years
    filtered_rs = rs[(rs['Year'] >= selected_time_period[0]) & (rs['Year'] <= selected_time_period[1])]

    # Create updated figures
    updated_goals_count_line_plot = goals_count_line_plot(selected_tournament, filtered_rs.copy())
    updated_trophy_count_hbarchart = trophy_count_hbarchart(selected_tournament, filtered_rs.copy())


    # obtaing data of the defending champion
    defending_champion_df = get_defending_champion(selected_tournament, filtered_rs.copy())
    defending_champion_md_2 = None

    if selected_time_period[1] in defending_champion_df.index.tolist():
        defending_champion_md_2 = str(selected_time_period[1])

    else:
        smallest_difference = float('inf')
        for date in defending_champion_df.index.tolist():
            difference = selected_time_period[1] - date
            if difference > 0 and difference < smallest_difference:
                smallest_difference = difference
                defending_champion_md_2 = str(date)

    defending_champion_md_1 = str(defending_champion_df[defending_champion_df.index == int(defending_champion_md_2)]['Winning Team'].values[0])


    # obtaining list of countries with highet trophy count
    country_with_highest_trophy_count_df = get_country_with_highest_trophy_count(selected_tournament, filtered_rs.copy())

    most_decorated_countries = country_with_highest_trophy_count_df['Winner'].tolist()
    most_trophies_won = country_with_highest_trophy_count_df['Trophies won overall'].tolist()

    most_decorated_countries_md_1 = '1. _' + str(most_decorated_countries[0]) + '_'
    most_decorated_countries_md_2 = '2. _' + str(most_decorated_countries[1]) + '_'
    most_decorated_countries_md_3 = '3. _' + str(most_decorated_countries[2]) + '_'
    most_trophies_won_md_1 = str(int(most_trophies_won[0]))
    most_trophies_won_md_2 = str(int(most_trophies_won[1]))
    most_trophies_won_md_3 = str(int(most_trophies_won[2]))

    # obtaining list high scoring tournament editions
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
        defending_champion_md_1,
        defending_champion_md_2,
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