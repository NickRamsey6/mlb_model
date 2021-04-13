from sportsreference.mlb.teams import Teams
from sportsreference.mlb.boxscore import Boxscore
from sportsreference.mlb.schedule import Schedule
import pandas as pd

league_dfs_list = []
for team in Teams('2019'):
    schedule = team.schedule.dataframe_extended
    schedule['team'] = team.abbreviation

    # Clean up date format
    schedule['date'] = pd.to_datetime(schedule.date)
    schedule['date'] = schedule['date'].dt.strftime('%m/%d/%Y')

    # Add Home and Away Team Fields
    home_team = []
    away_team = []

    for ind in schedule.index:
        if schedule['winner'][ind] == 'Home':
            home_team.append(schedule['winning_abbr'][ind])
        else:
            home_team.append(schedule['losing_abbr'][ind])

        if schedule['winner'][ind] == 'Away':
            away_team.append(schedule['winning_abbr'][ind])
        else:
            away_team.append(schedule['losing_abbr'][ind])

    schedule.insert(81, 'home_team', home_team, True)
    schedule.insert(82, 'away_team', away_team, True)

    # Add cumulative runs scored and allowed columns
    team_runs_scored = []
    for ind in schedule.index:
        if schedule['away_team'][ind] == schedule['team'][ind]:
            team_runs_scored.append(schedule['away_runs'][ind])
        else:
            team_runs_scored.append(schedule['home_runs'][ind])

    schedule.insert(83, 'team_runs_scored', team_runs_scored, True)
    schedule['cumulative_runs_scored'] = schedule['team_runs_scored'].cumsum()

    team_runs_allowed = []
    for ind in schedule.index:
        if schedule['away_team'][ind] == schedule['team'][ind]:
            team_runs_allowed.append(schedule['home_runs'][ind])
        else:
            team_runs_allowed.append(schedule['away_runs'][ind])

    schedule.insert(84, 'team_runs_allowed', team_runs_allowed, True)
    schedule['cumulative_runs_allowed'] = schedule['team_runs_allowed'].cumsum()

    # Calculate scoring ratio and predicted win %
    schedule['scoring_ratio'] = schedule['cumulative_runs_scored'] / \
        schedule['cumulative_runs_allowed']

    schedule['pred_win_%'] = (schedule['scoring_ratio']
                              ** 2) / ((schedule['scoring_ratio'] ** 2) + 1)

    # Widdle down to needed columns
    schedule = schedule[['date', 'winning_abbr', 'away_runs', 'home_runs', 'away_team', 'home_team', 'team', 'team_runs_scored',
                         'team_runs_allowed', 'cumulative_runs_scored', 'cumulative_runs_allowed', 'scoring_ratio', 'pred_win_%']]

    # Add completed team df to list of dfs
    league_dfs_list.append(schedule)
    print('done')

final_df = pd.concat(league_dfs_list)
final_df.to_csv('league.csv', index=True)
