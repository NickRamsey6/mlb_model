from sportsreference.mlb.teams import Teams
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.schedule import Schedule
import pandas as pd
import datetime

opening_day = datetime.datetime(2019, 3, 28)
x = opening_day.strftime('%m/%d/%Y')

# Create dataframe of all unique games for a season
games = []
dates = []
team1 = []
team2 = []
for team in Teams('2019'):
    schedule = team.schedule

    for game in schedule:
        games.append(game.boxscore_index)
        dates.append(game.datetime)
        team1.append(team.abbreviation)
        team2.append(game.opponent_abbr)

sched_df = pd.DataFrame(list(zip(dates, games, team1, team2)), columns=[
                        'Date', 'Game', 'Team1', 'Team2'])
sched_df = sched_df.drop_duplicates(subset='Game')

sched_df['Date'] = pd.to_datetime(sched_df.Date)
sched_df['Date'] = sched_df['Date'].dt.strftime('%m/%d/%Y')
# Filter out opening games
sched_df = sched_df[sched_df['Date'] > x]


# # # WIP filter league_df by date

league_df = pd.read_csv('league.csv')

team1pred = []
team2pred = []
winners = []
for ind in sched_df.index:
    team1 = sched_df['Team1'][ind]
    team2 = sched_df['Team2'][ind]
    gameday = sched_df['Date'][ind]
    # Team 1 Work
    team1df = league_df[league_df.team == team1]
    team1df = team1df[team1df['date'] < gameday]
    team1df_dates = team1df['date'].to_list()
    team1_most_recent_game = [max(team1df_dates)]
    team1df = team1df[team1df['date'].isin(
        team1_most_recent_game).copy(deep=False)]

    team1pred.append(team1df.iloc[0]['pred_win_%'])
    # Team 2 Work
    team2df = league_df[league_df.team == team2]
    team2df = team2df[team2df['date'] < gameday]
    team2df_dates = team2df['date'].to_list()
    team2_most_recent_game = [max(team2df_dates)]
    team2df = team2df[team2df['date'].isin(
        team2_most_recent_game).copy(deep=False)]

    team2pred.append(team2df.iloc[0]['pred_win_%'])

    if team1df.iloc[0]['pred_win_%'] > team2df.iloc[0]['pred_win_%']:
        winners.append(team1df.iloc[0]['team'])
    else:
        winners.append(team2df.iloc[0]['team'])


sched_df.insert(4, 'team1 pred', team1pred, True)
sched_df.insert(5, 'team2 pred', team2pred, True)
sched_df.insert(6, 'Winner', winners, True)
print(sched_df)
