import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def goals_count_line_plot(tournament_name, rs):
     # Create a single plot
    fig = go.Figure()

    if tournament_name == "All":
        # creating dataframes for major tournaments
        world_cup = rs.loc[rs['Tournament'] == 'FIFA World Cup']
        copa_america = rs.loc[rs['Tournament'] == 'Copa América']
        afcon = rs.loc[rs['Tournament'] == 'African Cup of Nations']
        euros = rs.loc[rs['Tournament'] == 'UEFA Euro']
        asian_cup = rs.loc[rs['Tournament'] == 'AFC Asian Cup']

        # grouping dataframes with respect to the year and goals scored
        world_cup_goals = world_cup.groupby('Year')[['Home Score', 'Away Score']].sum()
        copa_america_goals = copa_america.groupby('Year')[['Home Score', 'Away Score']].sum()
        afcon_goals = afcon.groupby('Year')[['Home Score', 'Away Score']].sum()
        euros_goals = euros.groupby('Year')[['Home Score', 'Away Score']].sum()
        asian_cup_goals = asian_cup.groupby('Year')[['Home Score', 'Away Score']].sum()

        world_cup_goals['Goals Scored'] = world_cup_goals['Home Score'] + world_cup_goals['Away Score']
        copa_america_goals['Goals Scored'] = copa_america_goals['Home Score'] + copa_america_goals['Away Score']
        afcon_goals['Goals Scored'] = afcon_goals['Home Score'] + afcon_goals['Away Score']
        euros_goals['Goals Scored'] = euros_goals['Home Score'] + euros_goals['Away Score']
        asian_cup_goals['Goals Scored'] = asian_cup_goals['Home Score'] + asian_cup_goals['Away Score']

        # Add line plots to the single plot
        fig.add_trace(go.Scatter(x=world_cup_goals.index, y=world_cup_goals['Goals Scored'], mode='lines+markers', name='FIFA World Cup'))
        fig.add_trace(go.Scatter(x=copa_america_goals.index, y=copa_america_goals['Goals Scored'], mode='lines+markers', name='Copa América'))
        fig.add_trace(go.Scatter(x=afcon_goals.index, y=afcon_goals['Goals Scored'], mode='lines+markers', name='African Cup of Nations'))
        fig.add_trace(go.Scatter(x=euros_goals.index, y=euros_goals['Goals Scored'], mode='lines+markers', name='UEFA Euro'))
        fig.add_trace(go.Scatter(x=asian_cup_goals.index, y=asian_cup_goals['Goals Scored'], mode='lines+markers', name='AFC Asian Cup'))

    else :
        # creating dataframe for the tournament of choice
        tournament = rs.loc[rs['Tournament'] == tournament_name]

        # grouping dataframes with respect to the year and goals scored
        tournament_goals = tournament.groupby('Year')[['Home Score', 'Away Score']].sum()

        tournament_goals['Goals Scored'] = tournament_goals['Home Score'] + tournament_goals['Away Score']

        # Add line plots to the single plot
        fig.add_trace(go.Scatter(x=tournament_goals.index, y=tournament_goals['Goals Scored'], mode='lines+markers', name=tournament_name))
 

    # Update layout settings
    fig.update_layout(xaxis_title='Year', 
                      yaxis_title='Goals Scored',
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False),
                      plot_bgcolor="white",
                      margin={"r": 20, "t": 20, "b": 20}
                      )
    
    fig.update_xaxes(showgrid=False, linecolor="black")
    fig.update_xaxes(showgrid=False)

    return fig


def trophy_count_hbarchart(tournament_name, rs):
    # Create a single plot with horizontal bar subplots
    fig_trophies = go.Figure()

    if tournament_name == "All":
        #creating dataframes for major tournaments
        world_cup = rs.loc[rs['Tournament'] == 'FIFA World Cup']
        copa_america = rs.loc[rs['Tournament'] == 'Copa América']
        afcon = rs.loc[rs['Tournament'] == 'African Cup of Nations']
        euros = rs.loc[rs['Tournament'] == 'UEFA Euro']
        asian_cup = rs.loc[rs['Tournament'] == 'AFC Asian Cup']

        # creating dataframes for finals of the respective tournaments
        world_cup_groupby = world_cup.groupby('Year')
        world_cup_final = world_cup_groupby.last()

        copa_america_groupby = copa_america.groupby('Year')
        copa_america_final = copa_america_groupby.last()

        afcon_groupby = afcon.groupby('Year')
        afcon_final = afcon_groupby.last()

        euros_groupby = euros.groupby('Year')
        euros_final = euros_groupby.last()

        asian_cup_groupby = asian_cup.groupby('Year')
        asian_cup_final = asian_cup_groupby.last()

        # resolving certain faults in the Finals data
        indexNames = copa_america_final[copa_america_final['Winning Team'] == 'Draw'].index
        copa_america_final.drop(indexNames, inplace = True)

        # creating dataframes to identify the winners and how many times they have won the tournament
        world_cup_champions = pd.DataFrame(world_cup_final['Winning Team'].value_counts().sort_index())
        copa_america_champions = pd.DataFrame(copa_america_final['Winning Team'].value_counts().sort_index())
        afcon_champions = pd.DataFrame(afcon_final['Winning Team'].value_counts().sort_index())
        euros_champions = pd.DataFrame(euros_final['Winning Team'].value_counts().sort_index())
        asian_cup_champions = pd.DataFrame(asian_cup_final['Winning Team'].value_counts().sort_index())

        # Resetting index
        world_cup_champions.reset_index(drop=False, inplace=True)
        copa_america_champions.reset_index(drop=False, inplace=True)
        afcon_champions.reset_index(drop=False, inplace=True)
        euros_champions.reset_index(drop=False, inplace=True)
        asian_cup_champions.reset_index(drop=False, inplace=True)

        # Renaming columns
        world_cup_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
        copa_america_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
        afcon_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
        euros_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)
        asian_cup_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)

        # Sort dataframes by trophies won in descending order
        world_cup_champions_sorted = world_cup_champions.sort_values(by='Trophies won overall', ascending=True)
        copa_america_champions_sorted = copa_america_champions.sort_values(by='Trophies won overall', ascending=True)
        afcon_champions_sorted = afcon_champions.sort_values(by='Trophies won overall', ascending=True)
        euros_champions_sorted = euros_champions.sort_values(by='Trophies won overall', ascending=True)
        asian_cup_champions_sorted = asian_cup_champions.sort_values(by='Trophies won overall', ascending=True)

        # Add horizontal bar plots to the single plot
        fig_trophies.add_trace(go.Bar(y=world_cup_champions_sorted['Winner'], x=world_cup_champions_sorted['Trophies won overall'], orientation='h', name='FIFA World Cup'))
        fig_trophies.add_trace(go.Bar(y=copa_america_champions_sorted['Winner'], x=copa_america_champions_sorted['Trophies won overall'], orientation='h', name='Copa América'))
        fig_trophies.add_trace(go.Bar(y=afcon_champions_sorted['Winner'], x=afcon_champions_sorted['Trophies won overall'], orientation='h', name='African Cup of Nations'))
        fig_trophies.add_trace(go.Bar(y=euros_champions_sorted['Winner'], x=euros_champions_sorted['Trophies won overall'], orientation='h', name='UEFA Euro'))
        fig_trophies.add_trace(go.Bar(y=asian_cup_champions_sorted['Winner'], x=asian_cup_champions_sorted['Trophies won overall'], orientation='h', name='AFC Asian Cup'))

    else:
        # creating dataframe for the tournament of choice
        tournament = rs.loc[rs['Tournament'] == tournament_name]

        # creating dataframes for finals of the respective tournaments
        tournament_groupby = tournament.groupby('Year')
        tournament_final = tournament_groupby.last()

        # resolving certain faults in the Finals data of the 'Copa América'
        if tournament_name == 'Copa América':
            # resolving certain faults in the Finals data
            indexNames = tournament_final[tournament_final['Winning Team'] == 'Draw'].index
            tournament_final.drop(indexNames, inplace = True)

        # creating dataframes to identify the winners and how many times they have won the tournament
        tournament_champions = pd.DataFrame(tournament_final['Winning Team'].value_counts().sort_index())

        # Resetting index
        tournament_champions.reset_index(drop=False, inplace=True)

        # Renaming columns
        tournament_champions.rename(columns={'Winning Team': 'Winner', 'count': 'Trophies won overall'}, inplace=True)

        # Sort dataframes by trophies won in descending order
        tournament_champions_sorted = tournament_champions.sort_values(by='Trophies won overall', ascending=True)

        # Add horizontal bar plots to the single plot
        fig_trophies.add_trace(go.Bar(y=tournament_champions_sorted['Winner'], x=tournament_champions_sorted['Trophies won overall'], orientation='h', name=tournament_name))


    # Update layout settings
    fig_trophies.update_layout(xaxis_title='No. of Trophies Won',
                               barmode='stack',
                               plot_bgcolor="white",
                               margin={"r": 20, "t": 20, "b": 20}
                               )
    
    fig_trophies.update_xaxes(tick0=0, dtick=1, showgrid=False, linecolor="black")
    fig_trophies.update_yaxes(showgrid=False)

    return fig_trophies