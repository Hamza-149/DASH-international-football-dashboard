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


# Initialize the Dash app
app = dash.Dash(__name__)


# Define the layout of the dashboard
app.layout = html.Div([

    # Add a slider for selecting time period
    dcc.RangeSlider(
        id='time-slider',
        marks={i: str(i) for i in range(1916, 2024, 10)},  # Marks for decades
        min=1916,
        max=2023,
        step=1,
        value=[1916, 2023]
    ),

    # Display the graph with the pre-created figure
    dcc.Graph(id='goals-count-line-plot', figure=goals_count_line_plot(rs)),

     # Display the bar chart with the pre-created figure
    dcc.Graph(id='trophy-count-hbarchart', figure=trophy_count_hbarchart(rs))

])


@app.callback(
    [Output('goals-count-line-plot', 'figure'), Output('trophy-count-hbarchart', 'figure')],  # Update the figure of this Graph component
    [Input('time-slider', 'value')] # Example: If you have an input component
)

def update_line_plot(selected_years):
    # Filter the data based on selected years
    filtered_rs = rs[(rs['Year'] >= selected_years[0]) & (rs['Year'] <= selected_years[1])]

    # Create updated figures
    updated_line_plot = goals_count_line_plot(filtered_rs)
    updated_bar_chart = trophy_count_hbarchart(filtered_rs)

    return updated_line_plot, updated_bar_chart


if __name__ == '__main__':
    app.run_server(debug=True)