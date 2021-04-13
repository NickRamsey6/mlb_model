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
road_team = []

for ind in sea_df.index:
    if sea_df['winner'][ind] == 'Home':
        home_team.append(sea_df['winning_abbr'][ind])
    else:
        home_team.append(sea_df['losing_abbr'][ind])

    if sea_df['winner'][ind] == 'Away':
        road_team.append(sea_df['winning_abbr'][ind])
    else:
        road_team.append(sea_df['losing_abbr'][ind])

sea_df.insert(81, 'home_team', home_team, True)
sea_df.insert(82, 'road_team', road_team, True)

print(sea_df)
