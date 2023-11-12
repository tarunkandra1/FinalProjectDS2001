import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

GAME_RESULTS = '/Users/tarun/Desktop/DS2001_Final/nfl_results.csv'

def graph_corr(df1, df2, Bool):
# This function gives you graph of two different pieces of data.
# If the Boolean is set to true, it will give you the correlation coefficient,
# If it is set to false, it will return the graph info which is a list containing information about
# the plot which is found with numpy.
    df1 = df1[0:32]
    df2 = df2[0:32]
    
    sns.regplot(x = df1, y = df2, order = 1, ci = None)
    plt.show()
    
    graph_info = np.polyfit(df1, df2, 1)
    if Bool == True:
        corr = np.corrcoef(df1, df2)
        corr_coeff = corr[0,1]
        return corr_coeff
    m = graph_info[0]
    b = graph_info[1]
    print("The line for linear regression is " + str(m) + "x" + " + " + str(b))
    return graph_info



def mean_yardsW(df):
    yds_in_win = df['YdsW'].mean()
    return yds_in_win

def mean_yardsL(df):
    yds_in_loss = df['YdsL'].mean()
    return yds_in_loss

if __name__ == "__main__":

    teams = {
    'Arizona Cardinals': [0, 0],
    'Atlanta Falcons': [0, 0],
    'Baltimore Ravens': [0, 0],
    'Buffalo Bills': [0, 0],
    'Carolina Panthers': [ 0, 0],
    'Chicago Bears': [0, 0],
    'Cincinnati Bengals': [0, 0],
    'Cleveland Browns': [0, 0],
    'Dallas Cowboys': [0, 0],
    'Denver Broncos': [0, 0],
    'Detroit Lions': [0, 0],
    'Green Bay Packers': [0, 0],
    'Houston Texans': [0, 0],
    'Indianapolis Colts': [0, 0],
    'Jacksonville Jaguars': [0, 0],
    'Kansas City Chiefs': [0, 0],
    'Las Vegas Raiders': [0, 0],
    'Los Angeles Chargers': [0, 0],
    'Los Angeles Rams': [0, 0],
    'Miami Dolphins': [0, 0],
    'Minnesota Vikings': [0, 0],
    'New England Patriots': [0, 0],
    'New Orleans Saints': [0, 0],
    'New York Giants': [0, 0],
    'New York Jets': [0, 0],
    'Philadelphia Eagles': [0, 0],
    'Pittsburgh Steelers': [0, 0],
    'San Francisco 49ers': [0, 0],
    'Seattle Seahawks': [0, 0],
    'Tampa Bay Buccaneers': [0, 0],
    'Tennessee Titans': [0, 0],
}

    df = pd.read_csv('/Users/tarun/Desktop/DS2001_Final/nfl_results.csv')
    df_defense1 = pd.read_csv('/Users/tarun/Desktop/DS2001_Final/defensive_stats1.csv')

    # This is to delete the duplicate, because our csv has a lot of unncessesary data
    df = df[0:1427]

    years = df_defense1.groupby(['Year'])
    yds = years.get_group(2022)["Yds"]
    PA = years.get_group(2022)["PA"]

    
    corr_coeff = graph_corr(yds,PA, True)
    graph_info = graph_corr(yds, PA, False)
 

    # This finds the index where df is not equal to Week and sets df equal to only the indexes where it is
    df = df[df.iloc[:, 0] != 'Week']
    
    df['YdsL'] = df['YdsL'].astype(float)
    df['YdsW'] = df['YdsW'].astype(float)

    group_win = df.groupby(['Winner/tie'])
    group_loss = df.groupby(['Loser/tie'])

    for i in teams:
        W = len(group_win.get_group(i))
        L = len(group_loss.get_group(i))
        #print(len(group_win.get_group(i)), "Games were won in the last 5 years by the" , i)
        #print(len(group_loss.get_group(i)), "Games were lost in the last 5 years by the" , i)
        teams[i] = [W,L]
