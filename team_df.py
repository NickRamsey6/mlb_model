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
team_runs = []
for ind in sea_df.index:
    if sea_df['away_team'][ind] == 'SEA':
        team_runs.append(sea_df['away_runs'][ind])
    else:
        team_runs.append(sea_df['home_runs'][ind])

sea_df.insert(83, 'team_runs', team_runs, True)

sea_df['cumulative_runs'] = sea_df['team_runs'].cumsum()

sea_df = sea_df[['date', 'winning_abbr', 'away_runs',
                 'home_runs', 'away_team', 'home_team', 'team', 'team_runs', 'cumulative_runs']]
print(sea_df)
