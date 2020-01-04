# In this example, three scouts observe match 1, in which Team 1000 scores 12 points while Team 2000
# scores zero points. Only one scout observes match 2, however, in which the scoring is reversed.

import pandas as pd

scouting_data = pd.DataFrame({
    'Scout': ['Han', 'Han', 'Chewbacca', 'Chewbacca', 'Luke', 'Luke', 'Chewbacca', 'Chewbacca'],
    'Match': [1, 1, 1, 1, 1, 1, 2, 2],
    'Team': [1000, 2000, 1000, 2000, 1000, 2000, 1000, 2000],
    'Score': [12, 0, 12, 0, 12, 0, 0, 12]
})

# If we simply take the average of all observations for each team, we get the wrong result.

scouting_data.groupby('Team').mean()

# To correct this, first group by both Match and Team.

scouting_data.groupby(['Match', 'Team']).mean()

# Finally, group again by Team to get the correct average.

scouting_data.groupby(['Match', 'Team']).mean().groupby('Team').mean()

