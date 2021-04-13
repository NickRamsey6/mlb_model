from sportsreference.mlb.teams import Teams
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.schedule import Schedule
import pandas as pd


##### Single Team Work ######
# Clean up date format
sea_df = Schedule('SEA').dataframe_extended
sea_df['date'] = pd.to_datetime(sea_df.date)
sea_df['date'] = sea_df['date'].dt.strftime('%m/%d/%Y')


# Add Home and Away Team fields
home_team = []
away_team = []

for ind in sea_df.index:
    if sea_df['winner'][ind] == 'Home':
        home_team.append(sea_df['winning_abbr'][ind])
    else:
        home_team.append(sea_df['losing_abbr'][ind])

    if sea_df['winner'][ind] == 'Away':
        away_team.append(sea_df['winning_abbr'][ind])
    else:
        away_team.append(sea_df['losing_abbr'][ind])

sea_df.insert(81, 'home_team', home_team, True)
sea_df.insert(82, 'away_team', away_team, True)

sea_df['team'] = 'SEA'

# Add Cumulative Runs Scored Column
team_runs_scored = []
for ind in sea_df.index:
    if sea_df['away_team'][ind] == 'SEA':
        team_runs_scored.append(sea_df['away_runs'][ind])
    else:
        team_runs_scored.append(sea_df['home_runs'][ind])

sea_df.insert(83, 'team_runs_scored', team_runs_scored, True)

sea_df['cumulative_runs_scored'] = sea_df['team_runs_scored'].cumsum()

sea_df = sea_df[['date', 'winning_abbr', 'away_runs',
                 'home_runs', 'away_team', 'home_team', 'team', 'team_runs_scored', 'cumulative_runs_scored']]
print(sea_df)
