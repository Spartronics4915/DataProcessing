import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 18})


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
def get_scouting_data(input_filename):
    """
    This function reads the scouting data, cleans some of the data and renames the columns.

    """

    # Read data and set empty cells to 0.
    data = pd.read_csv(input_filename).fillna(0)

    # Convert Climbing column to a numeric value.
    data['ClimbScore'] = data['Climbing'].map({'Level 3': 12, 'Level 2': 6, 'Level 1': 3, 'Not on HAB': 0})

    # Convert percentage column to numeric value
    data['FractionDefense'] = data['% of time playing defense'].apply(lambda x: float(x.rstrip('%')))

    data = data.rename(columns={
        'Your name (FirstName LastName)': 'ScoutName',
        'Match #': 'Match',
        'Team #': 'Team',
        'Starting Position': 'StartPosition',
        'Starts on Level 2?': 'StartLevel2',
        'Moved during sandstorm?': 'MovedSandstorm',
        'Crossed HAB line?': 'HabLine',
        'Starts with': 'StartingPiece',
        '# of hatch panels placed during sandstorm': 'HatchSandstorm',
        '# of cargo placed during sandstorm': 'CargoSandstorm',
        '# of hatch panels on the cargo bay': 'HatchCargoBay',
        '# of hatch panels on the bottom of the rocket': 'HatchBottomRocket',
        '# of hatch panels on the middle of the rocket': 'HatchMidRocket',
        '# of hatch panels on the top of the rocket': 'HatchTopRocket',
        '# of hatch panels missed': 'HatchMissed',
        '# of cargo in the cargo bay': 'CargoCargoBay',
        '# of cargo in the bottom of the rocket': 'CargoBottomRocket',
        '# of cargo in the middle of the rocket': 'CargoMidRocket',
        '# of cargo in the top of the rocket': 'CargoTopRocket',
        '# of cargo missed': 'CargoMissed',
        'Played defense successfully': 'DefenseSuccess',
        'Weak to defense (tippy, easily pushed, etc)': 'WeakDefense',
        '% of time playing defense': 'PercentDefense',
        '# of fouls': 'Fouls',
        '# of tech fouls': 'TechFouls',
        'Robot disabled': 'RobotDisabled',
        'Robot failure': 'RobotFail',
        'Tipped over': 'TippedOver',
        'Reckless driving': 'Reckless',
        'Yellow card': 'YellowCard',
        'Red card': 'RedCard',
        })

    return data


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
def get_summary_data(input_filename):
    """
    This summary function is the same as used in the Google spreadsheet.

    """

    scouting_data = get_scouting_data(input_filename)

    # Convert required boolean columns to integers
    scouting_data['HabLine'] = scouting_data['HabLine'].astype(int)
    scouting_data['StartLevel2'] = scouting_data['StartLevel2'].astype(int)

    data = scouting_data[[
        'Match',
        'Team',
        'StartLevel2',
        'HabLine',
        'HatchSandstorm',
        'CargoSandstorm',
        'HatchCargoBay',
        'HatchBottomRocket',
        'HatchMidRocket',
        'HatchTopRocket',
        'CargoCargoBay',
        'CargoBottomRocket',
        'CargoMidRocket',
        'CargoTopRocket',
        'ClimbScore'
    ]]
    data = data.groupby(['Match', 'Team']).mean().groupby('Team').mean()

    data['HabScore'] = 3 * data['HabLine'] * (data['StartLevel2'] + 1)
    data['HatchScore'] = 2 * (data['HatchSandstorm'] + data['HatchCargoBay'] + data['HatchBottomRocket'] + data['HatchMidRocket'] + data['HatchTopRocket'])
    data['CargoScore'] = 3 * (data['CargoSandstorm'] + data['CargoCargoBay'] + data['CargoBottomRocket'] + data['CargoMidRocket'] + data['CargoTopRocket'])
    data['Score'] = data['HabScore'] + data['HatchScore'] + data['CargoScore'] + data['ClimbScore']

    # Sort the teams by total score in descending order.
    sorted_data = data.sort_values('Score', ascending=False)

    return sorted_data


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
def get_summary_data_poc(input_filename):
    """
    This summary function is just a proof of concept.

    """

    scouting_data = get_scouting_data(input_filename)

    # Convert required boolean columns to integers
    scouting_data['HabLine'] = scouting_data['HabLine'].astype(int)
    scouting_data['StartLevel2'] = scouting_data['StartLevel2'].astype(int)
    scouting_data['DefenseSuccess'] = scouting_data['DefenseSuccess'].astype(int)
    scouting_data['RobotDisabled'] = scouting_data['RobotDisabled'].astype(int)
    scouting_data['RobotFail'] = scouting_data['RobotFail'].astype(int)
    scouting_data['TippedOver'] = scouting_data['TippedOver'].astype(int)
    scouting_data['Reckless'] = scouting_data['Reckless'].astype(int)

    data = scouting_data[[
        'Match',
        'Team',
        'StartLevel2',
        'HabLine',
        'HatchSandstorm',
        'CargoSandstorm',
        'HatchCargoBay',
        'HatchBottomRocket',
        'HatchMidRocket',
        'HatchTopRocket',
        'CargoCargoBay',
        'CargoBottomRocket',
        'CargoMidRocket',
        'CargoTopRocket',
        'DefenseSuccess',
        'Fouls',
        'TechFouls',
        'RobotDisabled',
        'RobotFail',
        'TippedOver',
        'Reckless',
        'ClimbScore',
        'FractionDefense'
    ]]
    data = data.groupby(['Match', 'Team']).mean().groupby('Team').mean()

    data['HabScore'] = 3 * data['HabLine'] * (data['StartLevel2'] + 1)
    data['HatchScore'] = 2 * (data['HatchSandstorm'] + data['HatchCargoBay'] + data['HatchBottomRocket'] + 1.1 * data['HatchMidRocket'] + 1.1 * data['HatchTopRocket'])
    data['CargoScore'] = 3 * (data['CargoSandstorm'] + data['CargoCargoBay'] + data['CargoBottomRocket'] + 1.1 * data['CargoMidRocket'] + 1.1 * data['CargoTopRocket'])
    data['DefenseScore'] = 10 * data['DefenseSuccess'] * data['FractionDefense'] / 100
    data['FoulScore'] = 3 * data['Fouls'] + 10 * data['TechFouls']
    data['FailScore'] = 5 * (data['RobotDisabled'] + data['RobotFail'] + data['TippedOver'] + data['Reckless'])

    # Find the worst Foul/Fail score, and use it to determine a positive OppPenaltyScore.
    max_foul_fail = (data['FoulScore'] + data['FailScore']).max()
    data['OppPenaltyScore'] = max_foul_fail - (data['FoulScore'] + data['FailScore'])

    data['Score'] = data['HabScore'] + data['HatchScore'] + data['CargoScore'] + data['ClimbScore'] + data['DefenseScore'] + data['OppPenaltyScore']

    # Sort the teams by total score in descending order.
    sorted_data = data.sort_values('Score', ascending=False)

    return sorted_data


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
def plot_scores(summary_data, title='Scouting Data', horizontal=True, output_filename=''):
    """
    Plot the scores (simple cummulative scores)

    """

    colors = 'blue', 'red', 'yellow', 'lime'

    if horizontal:
        data = summary_data.sort_values('Score')
        data = data.loc[:, ['HabScore', 'HatchScore', 'CargoScore', 'ClimbScore']]
        data.plot.barh(stacked=True, figsize=(12, 18), width=0.75, title=title, color=colors)
    else:
        data = summary_data.loc[:, ['HabScore', 'HatchScore', 'CargoScore', 'ClimbScore']]
        data.plot.bar(stacked=True, figsize=(16, 10), width=0.75, title=title, color=colors)

    if output_filename:
        plt.savefig(output_filename)
        plt.close()


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
def plot_scores_poc(summary_data, title='Scouting Data (POC)', horizontal=True, output_filename=''):
    """
    Plot the scores (proof of concept)

    """

    colors = 'blue', 'red', 'yellow', 'lime', 'magenta', 'tab:brown'

    if horizontal:
        data = summary_data.sort_values('Score')
        data = data.loc[:, ['HabScore', 'HatchScore', 'CargoScore', 'ClimbScore', 'DefenseScore', 'OppPenaltyScore']]
        data.plot.barh(stacked=True, figsize=(12, 18), width=0.75, title=title, color=colors)
    else:
        data = summary_data.loc[:, ['HabScore', 'HatchScore', 'CargoScore', 'ClimbScore', 'DefenseScore', 'OppPenaltyScore']]
        data.plot.bar(stacked=True, figsize=(16, 10), width=0.75, title=title, color=colors)

    if output_filename:
        plt.savefig(output_filename)
        plt.close()


#-----------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    auburn_data = get_summary_data('../Data/Scouting_2019/Auburn_MtView.csv')
    plot_scores(auburn_data, 'Auburn Mt View Scouting Data 2019', output_filename='auburn.png')
    plot_scores(auburn_data, 'Auburn Mt View Scouting Data 2019', horizontal=False, output_filename='auburn_vert.png')

    auburn_data_poc = get_summary_data_poc('../Data/Scouting_2019/Auburn_MtView.csv')
    plot_scores_poc(auburn_data_poc, 'Auburn Mt View Scouting Data 2019 (POC)', output_filename='auburn_poc.png')
    plot_scores_poc(auburn_data_poc, 'Auburn Mt View Scouting Data 2019 (POC)', horizontal=False, output_filename='auburn_vert_poc.png')

    gp_data = get_summary_data('../Data/Scouting_2019/Glacier_Peak.csv')
    plot_scores(gp_data, 'Glacier Peak Scouting Data 2019', output_filename='glacier_peak.png')
    plot_scores(gp_data, 'Glacier Peak Scouting Data 2019', horizontal=False, output_filename='glacier_peak_vert.png')

    gp_data_poc = get_summary_data_poc('../Data/Scouting_2019/Glacier_Peak.csv')
    plot_scores_poc(gp_data_poc, 'Glacier Peak Scouting Data 2019 (POC)', output_filename='glacier_peak_poc.png')
    plot_scores_poc(gp_data_poc, 'Glacier Peak Scouting Data 2019 (POC)', horizontal=False, output_filename='glacier_peak_vert_poc.png')

