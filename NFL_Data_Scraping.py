'''
Tables Index:

    NFL_Games.csv : Last 5 year games excluding this year
    NFL_Games_Current.csv : This years games
    Offense_Table_1.csv : Team Offense
    Offense_Table_2.csv : Passing Offense
    Offense_Table_3.csv : Rushing Offense
    Offense_Table_4.csv : Kick & Punt Returns
    Offense_Table_5.csv : Kicking
    Offense_Table_6.csv : Punting
    Offense_Table_7.csv : Scoring Offense
    Offense_Table_8.csv : Conversions
    Offense_Table_9.csv : Drive Averages
    Defense_Table_1.csv : Team Defense
    Defense_Table_2.csv : Team Advanced Defense
    Defense_Table_3.csv : Passing Defense
    Defense_Table_4.csv : Rushing Defense
    Defense_Table_5.csv : Kick & Punt Returns Against
    Defense_Table_6.csv : Kicking Against
    Defense_Table_7.csv : Punting Against
    Defense_Table_8.csv : Scoring Defense
    Defense_Table_9.csv : Conversions Against
    Defense_Table_10.csv : Drive Averages Against
'''

import pandas as pd
import os
from time import sleep
from random import randint
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

today = datetime.date.today()
year = today.year
files = []

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def replace_team_names(input_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        data = list(reader)

        columns_to_replace = [1, 4, 6]

        def replace_value(value):
            stripped_value = value.strip()
            if stripped_value == "Washington Redskins" or stripped_value == "Washington Football Team":
                return "Washington Commanders"
            elif stripped_value == "Oakland Raiders":
                return "Las Vegas Raiders"
            else:
                return value

        for row in data:
            for i in columns_to_replace:
                if 0 <= i < len(row):  # Check if the index is within the bounds of the row
                    row[i] = replace_value(row[i])

    with open(input_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)

    print("Replacement complete.")
    return input_file

def nfl_games():
    output_folder = 'NFL_Games'
    create_folder(output_folder)
    output_path = os.path.join(output_folder, 'NFL_Games.csv')
    if os.path.exists(output_path):
        os.remove(output_path)

    for y in range(year - 1, year - 6, -1):
        url = f"https://www.pro-football-reference.com/years/{y}/games.htm"
        dfs = pd.read_html(url)
        df = dfs[0]
        df['Year'] = y
        df = df[~df['Week'].str.startswith("Week", na=False)]
        df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)
        sleep(randint(10, 25))

    print("Complete NFL last 5 Year Game Results")
    return replace_team_names(output_path)

def nfl_games_current():
    output_folder = 'NFL_Games'
    create_folder(output_folder)
    output_path = os.path.join(output_folder, 'NFL_Games_Current.csv')
    if os.path.exists(output_path):
        os.remove(output_path)

    url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
    dfs = pd.read_html(url)
    df = dfs[0]
    df['Year'] = year
    df = df[~df['Week'].str.startswith("Week", na=False)]
    df.to_csv(output_path, mode='w', header=True, index=False)
    sleep(randint(10, 25))

    print("Complete NFL Current Year Game Results")
    return replace_team_names(output_path)

def nfl_offense():
    output_folder = 'Offense_Tables'
    create_folder(output_folder)
    csv_filenames = []
    
    for i in range(5, 14):
        csv_filename = os.path.join(output_folder, f"Offense_Table_{i - 4}.csv")
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for y in range(year - 1, year - 6, -1):
            url = f"https://www.pro-football-reference.com/years/{y}/"

            print(f"Before driver.get({url})")
            driver.get(url)
            print(f"After driver.get({url})")

            sleep(10)

            page_source = driver.page_source
            dfs = pd.read_html(page_source, header=1)

            for i in range(len(dfs)):

                dfs[i] = dfs[i][~(dfs[i].iloc[:, 0].isna() | (dfs[i].iloc[:, 0] == "Rk"))]
                if i == 6:
                    correct_header = ["Rk", "Tm", "G", "Cmp", "Att", "Cmp%",
                                      "Yds", "TD", "TD%", "Int", "Int%", "Lng",
                                      "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "Sk",
                                      "Yds", "Sk%", "NY/A", "ANY/A", "4QC",
                                      "GWD", "EXP"]

                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                      ignore_index=True)

                elif i == 7:
                    correct_header = ["Rk", "Tm", "G", "Att", "Yds", "TD",
                                      "Lng", "Y/A", "Y/G", "Fmb", "EXP"]

                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                      ignore_index=True)

                elif i == 8:
                    correct_header = ["Rk", "Tm", "G", "Ret", "Yds", "TD",
                                      "Lng", "Y/R", "Rt", "Yds", "TD", "Lng",
                                      "Y/Rt", "APYd"]

                    header_row = dfs[i].columns.tolist()
                    dfs[i].columns = correct_header

                elif i == 11:
                    correct_header = ["Rk", "Tm", "G", "RshTD", "RecTD",
                                      "PR TD", "KR TD", "FblTD", "IntTD", "OthTD",
                                      "AllTD", "2PM", "2PA", "D2P", "XPM",
                                      "XPA", "FGM", "FGA", "Sfty", "Pts", "Pts/G"]

                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                      ignore_index=True)

            print(f"Running for {url}")
            dataframes = []
            for i in range(5, 14):
                df = dfs[i]
                df['Year'] = y
                dataframes.append(df)
                sleep(randint(10, 25))
                csv_filename = os.path.join(output_folder, f"Offense_Table_{i - 4}.csv")
                csv_filenames.append(csv_filename)
                df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    print("Complete NFL Last 5 Year Offensive Stats")
    return [replace_team_names(file) for file in csv_filenames]

def nfl_offense_current():
    output_folder = 'Offense_Tables_Current'
    create_folder(output_folder)
    csv_filenames = []
    
    for i in range(4, 14):
        csv_filename = os.path.join(output_folder, f"Offense_Table_Current_{i - 4}.csv")
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"https://www.pro-football-reference.com/years/{year}/"

        print(f"Before driver.get({url})")
        driver.get(url)
        print(f"After driver.get({url})")

        sleep(10)

        page_source = driver.page_source
        dfs = pd.read_html(page_source, header=1)

        for i in range(4, len(dfs)):

            dfs[i] = dfs[i][~(dfs[i].iloc[:, 0].isna() | (dfs[i].iloc[:, 0] == "Rk"))]
            if i == 5:
                correct_header = ["Rk", "Tm", "G", "Cmp", "Att", "Cmp%",
                                  "Yds", "TD", "TD%", "Int", "Int%", "Lng",
                                  "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "Sk",
                                  "Yds", "Sk%", "NY/A", "ANY/A",
                                  "4QC", "GWD", "EXP"]

                header_row = dfs[i].columns.tolist()
                dfs[i] = dfs[i].iloc[0:, :]
                dfs[i].columns = correct_header
                dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                  ignore_index=True)

            elif i == 6:
                correct_header = ["Rk", "Tm", "G", "Att", "Yds", "TD",
                                  "Lng", "Y/A", "Y/G", "Fmb", "EXP"]

                header_row = dfs[i].columns.tolist()
                dfs[i] = dfs[i].iloc[0:, :]
                dfs[i].columns = correct_header
                dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                  ignore_index=True)

            elif i == 10:
                correct_header = ["Rk", "Tm", "G", "RshTD", "RecTD",
                                  "PR TD", "KR TD", "FblTD", "IntTD", "OthTD",
                                  "AllTD", "2PM", "2PA", "D2P", "XPM", "XPA",
                                  "FGM", "FGA", "Sfty", "Pts", "Pts/G"]

                header_row = dfs[i].columns.tolist()
                dfs[i] = dfs[i].iloc[0:, :]
                dfs[i].columns = correct_header
                dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]],
                                  ignore_index=True)

        print(f"Running for {url}")
        dataframes = []
        for i in range(4, len(dfs)):
            df = dfs[i]
            df['Year'] = year
            dataframes.append(df)
            sleep(randint(10, 25))
            csv_filename = os.path.join(output_folder, f"Offense_Table_Current_{i - 3}.csv")
            csv_filenames.append(csv_filename)
            df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    print("Complete NFL Current Year Offensive Stats")
    return [replace_team_names(file) for file in csv_filenames]

def nfl_defense():
    output_folder = 'Defense_Tables'
    create_folder(output_folder)
    csv_filenames = []
    
    for i in range(0, 11):
        csv_filename = os.path.join(output_folder, f"Defense_Table_{i}.csv")
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for y in range(year - 1, year - 6, -1):
            url = f"https://www.pro-football-reference.com/years/{y}/opp.htm"
        
            print(f"Before driver.get({url})")
            driver.get(url)
            print(f"After driver.get({url})")

            sleep(10)

            page_source = driver.page_source
            dfs = pd.read_html(page_source, header=1)
            
            for i in range(0,len(dfs)):
            
                dfs[i] = dfs[i][~(dfs[i].iloc[:, 0].isna() | (dfs[i].iloc[:, 0] == "Rk"))]
                dfs[i] = dfs[i][~dfs[i].iloc[:, 0].str.startswith("Tm", na=False)]
      
                if i == 1:
                    correct_header = [ "Tm", "G", "Att", "Cmp", "Yds", "TD",
                                      "DADOT", "Air", "YAC", "Bltz", "Bltz%", 
                                      "Hrry", "Hrry%", "QBKD", "QBKD%",
                                      "Sk", "Prss", "Prss%", "MTkl"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)
                    
                elif i == 2:
                    correct_header = [ "Rk", "Tm", "G", "Cmp", "Att", "Cmp%", 
                                      "Yds", "TD", "TD%", "Int", "PD", "Int%", 
                                      "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "Sk",
                                      "Yds", "QBHits", "TFL", "Sk%", "NY/A", 
                                      "ANY/A", "EXP"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)

                    
                elif i == 3: 
                    correct_header = ["Rk", "Tm", "G", "Att", "Yds", "TD", 
                                      "Y/A", "Y/G", "EXP"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)
                    
                elif i == 7:
                    correct_header = ["Rk", "Tm", "G", "RshTD", "RecTD", 
                                      "PR TD", "KR TD", "FblTD", "IntTD", "OthTD",
                                      "AllTD", "2PM", "2PA", "D2P", "XPM", 
                                      "XPA", "FGM", "FGA", "Sfty", "Pts", "Pts/G"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)

            print(f"Running for {url}")
            dataframes = [] 
            for i in range(0, len(dfs)):
                df = dfs[i]
                df['Year'] = y 
                dataframes.append(df)
                sleep(randint(10, 25))
                csv_filename = os.path.join(output_folder, f"Defense_Table_{i+1}.csv")
                csv_filenames.append(csv_filename)
                df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)
            
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    print("Complete NFL Last 5 Year Defensive Stats")
    return [replace_team_names(file) for file in csv_filenames]

def nfl_defense_current():
    
    output_folder = 'Defense_Tables_Current'
    create_folder(output_folder)
    csv_filenames = []
    
    for i in range(0, 11):
        csv_filename = os.path.join(output_folder, f"Defense_Table_Current_{i}.csv")
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    csv_filenames = []

    try:
            url = f"https://www.pro-football-reference.com/years/{year}/opp.htm"
        
            print(f"Before driver.get({url})")
            driver.get(url)
            print(f"After driver.get({url})")

            sleep(10)

            page_source = driver.page_source
            dfs = pd.read_html(page_source, header=1)
            
            for i in range(0,len(dfs)):
            
                dfs[i] = dfs[i][~(dfs[i].iloc[:, 0].isna() | (dfs[i].iloc[:, 0] == "Rk"))]
                dfs[i] = dfs[i][~dfs[i].iloc[:, 0].str.startswith("Tm", na=False)]
      
                if i == 1:
                    correct_header = [    "Tm", "G", "Att", "Cmp", "Yds", "TD",
                                      "DADOT", "Air", "YAC", "Bltz", "Bltz%", 
                                      "Hrry", "Hrry%", "QBKD", "QBKD%",
                                      "Sk", "Prss", "Prss%", "MTkl"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)
                    
                elif i == 2:
                    correct_header = [ "Rk", "Tm", "G", "Cmp", "Att", "Cmp%",
                                      "Yds", "TD", "TD%", "Int", "PD", "Int%", 
                                      "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "Sk",
                                      "Yds", "QBHits", "TFL", "Sk%", "NY/A", "ANY/A",
                                      "EXP"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)

                    
                elif i == 3: 
                    correct_header = ["Rk", "Tm", "G", "Att", "Yds", "TD", "Y/A",
                                      "Y/G", "EXP"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)
                    
                elif i == 7:
                    correct_header = ["Rk", "Tm", "G", "RshTD", "RecTD", "PR TD",
                                      "KR TD", "FblTD", "IntTD", "OthTD", "AllTD", 
                                      "2PM", "2PA", "D2P", "XPM", "XPA", "FGM", 
                                      "FGA", "Sfty", "Pts", "Pts/G"]
                    
                    header_row = dfs[i].columns.tolist()
                    dfs[i] = dfs[i].iloc[0:, :]
                    dfs[i].columns = correct_header
                    dfs[i] = pd.concat([pd.DataFrame([header_row], columns=dfs[i].columns), dfs[i]], ignore_index=True)

            print(f"Running for {url}")
            dataframes = [] 
            for i in range(0, len(dfs)):
                df = dfs[i]
                df['Year'] = year
                dataframes.append(df)
                sleep(randint(10, 25))
                csv_filename = os.path.join(output_folder, f"Defense_Table_Current_{i+1}.csv")
                csv_filenames.append(csv_filename)
                df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)
            
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    print("Complete NFL Current Year Defensive Stats")
    return [replace_team_names(file) for file in csv_filenames]

if __name__ == "__main__":
    
    x = input("If Last 5 Year stats desired enter True: ")
    
    file_current = [nfl_games_current()]
    files_current = [nfl_defense_current(), nfl_offense_current()]
    for file in file_current:
            replace_team_names(file)
    for file_list in files_current:
        for file in file_list:
            replace_team_names(file)
    
    if x == "True":
        files_old = [nfl_offense(), nfl_defense()]
        file_old = [nfl_games()]
        for file in file_old:
            replace_team_names(file)
        for file_list in files_old:
            for file in file_list:
                replace_team_names(file)
