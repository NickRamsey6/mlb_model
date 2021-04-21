from sportsreference.mlb.teams import Teams
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.schedule import Schedule
import pandas as pd


# Create dataframe of all unique games for a season
games = []
dates = []
team1 = []
team2 = []
for team in Teams('2019'):
    schedule = team.schedule

    for game in schedule:
        games.append(game.boxscore_index)
        dates.append(game.date)
        team1.append(team.abbreviation)
        team2.append(game.opponent_abbr)

sched_df = pd.DataFrame(list(zip(dates, games, team1, team2)), columns=[
                        'Date', 'Game', 'Team1', 'Team2'])
sched_df = sched_df.drop_duplicates(subset='Game')
print(sched_df)
