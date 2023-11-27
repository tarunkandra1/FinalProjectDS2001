import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


warnings.filterwarnings("ignore")
GAME_RESULTS = '/Users/tarun/Desktop/DS2001_Final/nfl_results.csv'

def graph_corr(df1, df2, Bool):
    # The parameters are 2 dataframes and a Boolean
    # This function gives you graph of two different pieces of data.
    # If the Boolean is set to true, it will give you the correlation coefficient,
    # If it is set to false, it will return the graph info which is a list containing information about
    # the plot which is found with numpy.

    
    sns.regplot(x = df1, y = df2, order = 1, ci = None)
    plt.show()
    
    graph_info = np.polyfit(df1, df2, 1)
    if Bool == True:
        # If you want the correlation coefficient, you can put true for the graph_corr function
        corr = np.corrcoef(df1, df2)
        corr_coeff = corr[0,1]
        return corr_coeff
    # If you want other stats about the line, you put false for the boolean
    m = graph_info[0]
    b = graph_info[1]
    print("The line for linear regression is " + str(m) + "x" + " + " + str(b))
    return graph_info


def team_wins(df, teams):
    # Finds the amount of wins a team has in a certain dataset, returns a dataframe
    # The parameters are a dataframe and a dictionary

    group_win = df.groupby(['Winner/tie'])
    group_loss = df.groupby(['Loser/tie'])

    for i in teams:
        W = len(group_win.get_group(i))
        L = len(group_loss.get_group(i))
        #print(len(group_win.get_group(i)), "Games were won in the last 5 years by the" , i)
        #print(len(group_loss.get_group(i)), "Games were lost in the last 5 years by the" , i)
        teams[i] = [W,L,0]
    df_teamstats = pd.DataFrame(teams)
    df_teamstats.rename({0: 'Wins', 1: 'Losses', 2: 'Defensive Rating', 3: 'Offensive Rating', 4: 'Net Rating'}, inplace= True)
    return df_teamstats


def rate_team(df, avg, teams):
    new_teams = teams.copy()
    team_name = df['Tm']
    xYds = df['Yds'].iloc[0]
    yYds = avg['Yds'].iloc[0]
    adj_yds = (xYds / yYds)
    
    xPA = df['PA'].iloc[0]
    yPA = avg['PA'].iloc[0]
    adj_PA = xPA / yPA

    xTO = df['TO%'].iloc[0]
    yTO = avg['TO%'].iloc[0]
    adj_TO = (xTO / yTO)

    rating = (adj_TO + adj_PA + adj_yds) / 3.0
    new_teams.loc['Defensive Rating', team_name] = rating
    return new_teams

def mean_yardsW(df):
    # Finds the mean yards in a win parameter is a dataframe
    yds_in_win = df['YdsW'].mean()
    return yds_in_win

def mean_yardsL(df):
    # Finds the mean yards in a loss parameter is also a dataframe
    yds_in_loss = df['YdsL'].mean()
    return yds_in_loss

if __name__ == "__main__":
    nfl_teams = [
    'Arizona Cardinals',
    'Atlanta Falcons',
    'Baltimore Ravens',
    'Buffalo Bills',
    'Carolina Panthers',
    'Chicago Bears',
    'Cincinnati Bengals',
    'Cleveland Browns',
    'Dallas Cowboys',
    'Denver Broncos',
    'Detroit Lions',
    'Green Bay Packers',
    'Houston Texans',
    'Indianapolis Colts',
    'Jacksonville Jaguars',
    'Kansas City Chiefs',
    'Las Vegas Raiders',
    'Los Angeles Chargers',
    'Los Angeles Rams',
    'Miami Dolphins',
    'Minnesota Vikings',
    'New England Patriots',
    'New Orleans Saints',
    'New York Giants',
    'New York Jets',
    'Philadelphia Eagles',
    'Pittsburgh Steelers',
    'San Francisco 49ers',
    'Seattle Seahawks',
    'Tampa Bay Buccaneers',
    'Tennessee Titans',
    'Washington Commanders'
]
    teams_data = {
    'Arizona Cardinals': [0, 0, 0, 0, 0],
    'Atlanta Falcons': [0, 0, 0, 0, 0],
    'Baltimore Ravens': [0, 0, 0, 0, 0],
    'Buffalo Bills': [0, 0, 0, 0, 0],
    'Carolina Panthers': [ 0, 0, 0, 0, 0],
    'Chicago Bears': [0, 0, 0, 0, 0],
    'Cincinnati Bengals': [0, 0, 0, 0, 0],
    'Cleveland Browns': [0, 0, 0, 0, 0],
    'Dallas Cowboys': [0, 0, 0, 0, 0],
    'Denver Broncos': [0, 0, 0, 0, 0],
    'Detroit Lions': [0, 0, 0, 0, 0],
    'Green Bay Packers': [0, 0, 0, 0, 0],
    'Houston Texans': [0, 0, 0, 0, 0],
    'Indianapolis Colts': [0, 0, 0, 0, 0],
    'Jacksonville Jaguars': [0, 0, 0, 0, 0],
    'Kansas City Chiefs': [0, 0, 0, 0, 0],
    'Las Vegas Raiders': [0, 0, 0, 0, 0],
    'Los Angeles Chargers': [0, 0, 0, 0, 0],
    'Los Angeles Rams': [0, 0, 0, 0, 0],
    'Miami Dolphins': [0, 0, 0, 0, 0],
    'Minnesota Vikings': [0, 0, 0, 0, 0],
    'New England Patriots': [0, 0, 0, 0, 0],
    'New Orleans Saints': [0, 0, 0, 0, 0],
    'New York Giants': [0, 0, 0, 0, 0],
    'New York Jets': [0, 0, 0, 0, 0],
    'Philadelphia Eagles': [0, 0, 0, 0 ,0],
    'Pittsburgh Steelers': [0, 0, 0, 0, 0],
    'San Francisco 49ers': [0, 0, 0, 0, 0],
    'Seattle Seahawks': [0, 0, 0, 0, 0],
    'Tampa Bay Buccaneers': [0, 0, 0, 0, 0],
    'Tennessee Titans': [0, 0, 0, 0, 0],
    'Washington Commanders': [0, 0, 0, 0, 0]
}

    df = pd.read_csv('/Users/tarun/Desktop/DS2001_Final/nfl_results.csv')
    df_defense1 = pd.read_csv('/Users/tarun/Desktop/DS2001_Final/defensive_stats1.csv')

    # This is to delete the duplicate, because our csv has a lot of unncessesary data
    df = df[0:1427]
    # This finds the index where df is not equal to Week and sets df equal to only the indexes where it is
    df = df[df.iloc[:, 0] != 'Week']

    teams_data = team_wins(df, teams_data)


    df['YdsL'] = df['YdsL'].astype(float)
    df['YdsW'] = df['YdsW'].astype(float)
    
    years = df_defense1.groupby(['Year'])
    yds = years.get_group(2022)["Yds"]
    PA = years.get_group(2022)["PA"]

    teams_def = df_defense1.groupby(['Tm'])
    year = 2022
    average = years.get_group(year)[32:33]
    new_teams = teams_data
    for team, data in teams_def:
        data = data[data['Year'] == year]        
        defstats = data[data['Year'] == year]
        new_teams = rate_team(defstats ,average, new_teams)
    new_teams = new_teams.drop(["League Total", 'Avg Tm/G', 'Avg Team'], axis = 1)
    print(new_teams)
    



# This is the code which we used to find the graph of total yards correlated to total PA
"""
    Total_yds = pd.DataFrame()
    Total_PA = pd.DataFrame()
    for i in range(2018,2022):
        x = years.get_group(i)["Yds"][0:32]
        y = years.get_group(i)["PA"][0:32]
        Total_yds = pd.concat([Total_yds, x], axis = 0)
        Total_PA = pd.concat([Total_PA, y], axis = 0)
    Total_yds.squeeze()
    Total_PA.squeeze()
    var1 = Total_yds[0].values
    var2 = Total_PA[0].values
    graph_corr(var1 ,var2, True)
"""   
    #corr_coeff = graph_corr(yds,PA, True)
    #graph_info = graph_corr(yds, PA, False)
 
