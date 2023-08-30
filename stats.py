import pandas as pd

def get_country_with_highest_trophy_count(tournament_name, rs):
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
    tournament_champions_sorted = tournament_champions.sort_values(by='Trophies won overall', ascending=False)

    return tournament_champions_sorted

    


def get_highest_goalscoring_edition(tournament_name, rs):
    # creating dataframe for the tournament of choice
    tournament = rs.loc[rs['Tournament'] == tournament_name]

    # grouping dataframes with respect to the year and goals scored
    tournament_goals = tournament.groupby('Year')[['Home Score', 'Away Score']].sum()

    tournament_goals['Goals Scored'] = tournament_goals['Home Score'] + tournament_goals['Away Score']

    # sorting dataframe in descending order of goals scored
    tournament_goals_sorted = tournament_goals.sort_values(by='Goals Scored', ascending=False)

    return tournament_goals_sorted