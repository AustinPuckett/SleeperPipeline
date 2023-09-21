# SleeperPipline
A data pipeline that pulls fantasy football data from the Sleeper API and stores it in a SQLite database.

## Overview
This package runs a three step process to pull data from a User's fantasy league from Sleeper (https://docs.sleeper.com/). The extract module makes the api calls and returns JSON data. The transform module transforms JSON data into table entries. The load module loads the table data into an sqlite database.

## Also Included:
For now, I am including a few sample visualizations as a part of this library. Test.

### Schedule Luck Visualization
"Schedule Luck" is defined as the number of wins a fantasy team actually won minus the average number of wins it would have won had the team played every possible schedule ("Schedule Wins"). To calculate Schedule Wins for a team in a single week, we count how many opponents the team would have won against in that week divided by the number of other teams in the league. To calculate schedule wins for the season, we add all of the schedule wins from all weeks for that team.

#### Example:

(fantasy_team - fantasy_points - Win/Loss - Schedule Wins)


Week 1 Matchups:

+ *(eagle_lover45 - 125 - W - 1.00) vs (cheese_lover67 - 116 - L - 0.66)*
+ *(lion_lover56 - 87 - W - 0.33) vs (bear_lover34 - 47 - L - 0.00)*


Week 2 Matchups:

+ *(eagle_lover45 - 98 - W - 1.00) vs (bear_lover34 - 97 - L - 0.66)*
+ *(lion_lover56 - 89 - W - 0.33) - (cheese_lover67 - 72 - L - 0.00)*


Week 3 Matchups:

+ *(eagle_lover45 - 99 - L - 0.00) vs (lion_lover56 - 102 - W - 0.33)*
+ *(bear_lover34 - 103 - L - 0.66) vs (cheese_lover67 - 105 - W - 1.00)*



End of Season Standings:

(fantasy_team - Win/Loss Record - Schedule Wins - Differential)

+ eagle_lover45 - 2/1 - 2 -  0.00 
+ bear_lover34 - 0/3 - 1.33 -  -1.33
+ lion_lover56 - 3/0 - 1.00 -  2.00
+ cheese_lover67 - 1/2 - 1.66 -  -0.66


So we say that lion_lover56 had the luckiest season and bear_lover34 had the unluckiest season

