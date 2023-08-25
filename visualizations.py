import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def goals_count_line_plot(rs):

    #creating dataframes for major tournaments
    world_cup = rs.loc[rs['Tournament'] == 'FIFA World Cup']
    copa_america = rs.loc[rs['Tournament'] == 'Copa América']
    afcon = rs.loc[rs['Tournament'] == 'African Cup of Nations']
    euros = rs.loc[rs['Tournament'] == 'UEFA Euro']

    # grouping dataframes with respect to the year and goals scored
    world_cup_goals = world_cup.groupby('Year')[['Home Score', 'Away Score']].sum()
    copa_america_goals = copa_america.groupby('Year')[['Home Score', 'Away Score']].sum()
    afcon_goals = afcon.groupby('Year')[['Home Score', 'Away Score']].sum()
    euros_goals = euros.groupby('Year')[['Home Score', 'Away Score']].sum()

    world_cup_goals['Goals Scored'] = world_cup_goals['Home Score'] + world_cup_goals['Away Score']
    copa_america_goals['Goals Scored'] = copa_america_goals['Home Score'] + copa_america_goals['Away Score']
    afcon_goals['Goals Scored'] = afcon_goals['Home Score'] + afcon_goals['Away Score']
    euros_goals['Goals Scored'] = euros_goals['Home Score'] + euros_goals['Away Score']


    # Create a single plot
    fig = go.Figure()

    # Add line plots to the single plot
    fig.add_trace(go.Scatter(x=world_cup_goals.index, y=world_cup_goals['Goals Scored'], mode='lines+markers', name='FIFA World Cup'))
    fig.add_trace(go.Scatter(x=copa_america_goals.index, y=copa_america_goals['Goals Scored'], mode='lines+markers', name='Copa América'))
    fig.add_trace(go.Scatter(x=afcon_goals.index, y=afcon_goals['Goals Scored'], mode='lines+markers', name='African Cup of Nations'))
    fig.add_trace(go.Scatter(x=euros_goals.index, y=euros_goals['Goals Scored'], mode='lines+markers', name='UEFA Euro'))

    # Update layout settings
    fig.update_layout(title='Goals Scored in Different Tournaments', xaxis_title='Time', yaxis_title='Goals Scored')

    return fig


def trophy_count_hbarchart(rs):

    #creating dataframes for major tournaments
    world_cup = rs.loc[rs['Tournament'] == 'FIFA World Cup']
    copa_america = rs.loc[rs['Tournament'] == 'Copa América']
    afcon = rs.loc[rs['Tournament'] == 'African Cup of Nations']
    euros = rs.loc[rs['Tournament'] == 'UEFA Euro']

    # creating dataframes for finals of the respective tournaments
    world_cup_groupby = world_cup.groupby('Year')
    world_cup_final = world_cup_groupby.last()

    copa_america_groupby = copa_america.groupby('Year')
    copa_america_final = copa_america_groupby.last()

    afcon_groupby = afcon.groupby('Year')
    afcon_final = afcon_groupby.last()

    euros_groupby = euros.groupby('Year')
    euros_final = euros_groupby.last()

    # resolving certain faults in the Finals data
    indexNames = copa_america_final[copa_america_final['Winning Team'] == 'Draw'].index
    copa_america_final.drop(indexNames, inplace = True)

    # creating dataframes to identify the winners and how many times they have won the tournament
    world_cup_champions = pd.DataFrame(world_cup_final['Winning Team'].value_counts().sort_index())
    copa_america_champions = pd.DataFrame(copa_america_final['Winning Team'].value_counts().sort_index())
    afcon_champions = pd.DataFrame(afcon_final['Winning Team'].value_counts().sort_index())
    euros_champions = pd.DataFrame(euros_final['Winning Team'].value_counts().sort_index())

    # Resetting index
    world_cup_champions.reset_index(drop=False, inplace=True)
    copa_america_champions.reset_index(drop=False, inplace=True)
    afcon_champions.reset_index(drop=False, inplace=True)
    euros_champions.reset_index(drop=False, inplace=True)

    # Renaming columns
    world_cup_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
    copa_america_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
    afcon_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
    euros_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)

    # Sort dataframes by trophies won in descending order
    world_cup_champions_sorted = world_cup_champions.sort_values(by='Trophies won overall', ascending=False)
    copa_america_champions_sorted = copa_america_champions.sort_values(by='Trophies won overall', ascending=False)
    afcon_champions_sorted = afcon_champions.sort_values(by='Trophies won overall', ascending=False)
    euros_champions_sorted = euros_champions.sort_values(by='Trophies won overall', ascending=False)

    # Create a single plot with horizontal bar subplots
    fig_trophies = go.Figure()

    # Add horizontal bar plots to the single plot
    fig_trophies.add_trace(go.Bar(y=world_cup_champions_sorted['Winner'], x=world_cup_champions_sorted['Trophies won overall'], orientation='h', name='FIFA World Cup'))
    fig_trophies.add_trace(go.Bar(y=copa_america_champions_sorted['Winner'], x=copa_america_champions_sorted['Trophies won overall'], orientation='h', name='Copa América'))
    fig_trophies.add_trace(go.Bar(y=afcon_champions_sorted['Winner'], x=afcon_champions_sorted['Trophies won overall'], orientation='h', name='African Cup of Nations'))
    fig_trophies.add_trace(go.Bar(y=euros_champions_sorted['Winner'], x=euros_champions_sorted['Trophies won overall'], orientation='h', name='UEFA Euro'))

    # Update layout settings
    fig_trophies.update_layout(title='Most decorated countries', barmode='stack')

    # Set a taller height for the plot
    fig_trophies.update_layout(height=800)

    return fig_trophies