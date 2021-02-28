from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv 
import os
import re
from tqdm import tqdm
import argparse
from argparse import ArgumentParser
from datetime import timedelta, date, datetime

# the is a comment to see if a can push from new computer!!!!
def main():
    # January = []
    # year = [January]
    # months = ["/January"]
    # for i in range(1,1):
    #     January.append(2)
    # lengths = {1:1}

    startDate = date(2019, 1, 1)
    endDate = date(2019, 1, 1)

    if os.path.isdir("./Stat_Sheets") == False:
        os.mkdir("./Stat_Sheets")
    print('\nDownloading Stats......')


    # for z in range(1,len(year) + 1):
    #     folder = months[z - 1]
    #     if os.path.isdir("./Stat_Sheets" + folder) == False:
    #         os.mkdir("./Stat_Sheets" + folder)
    #     for w in tqdm(range(1, lengths[z] + 1), desc=( (months[z - 1])[1:4] + ": " ) ):

    for currentDate in tqdm(daterange(startDate, endDate)):
        year = str(currentDate.year)
        month = str(currentDate.month)
        day = str(currentDate.day)
        monthString = str(datetime.strptime("1", "%m").strftime("%B"))
        try:
            os.mkdir('./Stat_Sheets/{year}/'.format(year=year))
            os.mkdir('./Stat_Sheets/{year}/{month}/'.format(year=year, month=monthString))
        except OSError as error: 
            print('')
        my_url = "http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon={month}&day={day}&year={year}".format(month=month, day=day, year=year) #bs4 setup stuff
        uClient = uReq(my_url)            
        page_html = uClient.read()
        uClient.close()
        soup = BeautifulSoup(page_html, "html.parser")
        players = soup.find_all("tr") # first player is always 10
        if (len(players) >= 10) : # checks if there were games that day
            fields = ["Name", "Position", "FDPoints", "Salary", "Team", "Opp.", "Home/Away", "Score", "Min", "Pts", 'Rbs', 'Ast', 'Stl', 'Blk', 'To', '3PM', 'FGM', 'FGA', 'FTM', 'FTA']
            rows = []
            playerTracker = 0
            for i in range(10,len(players)): # for the gaurds
                playerTracker = getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break
            for i in range(playerTracker,len(players)): # for the forwards
                playerTracker = getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break
            for i in range(playerTracker,len(players)): # for the centers
                playerTracker = getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break

            filename = 'Stat_Sheets/{year}/{monthString}/{month}-{day}-{year}.csv'.format(year=year, monthString=monthString, day=day, month=month)
            with open(filename, "w", newline="") as csvfile: # writing to csv file  
                csvwriter = csv.writer(csvfile)  
                csvwriter.writerow(fields)  
                csvwriter.writerows(rows) 
                    
    print('Download Completed!\n')


#################################################################### HELPER FUNCTIONS ####################################################################
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def getTheStats(players, i, rows, playerTracker):
    try:
        helper = players[i].find_all("td")
        stats = splitStatsIntoCatagories(str(helper[8].text))
        rows.append([ players[i].find("a").text,                            # Name
                      getPosition(helper[0].text),                          # Position
                      helper[2].text,                                       # FDPoints
                      re.sub('[$,]', '', helper[3].text),                   # Salary
                      helper[4].text,                                       # Team
                      str(helper[5].text)[2:len(str(helper[5].text))],      # Opponent    
                      homeVsAway(helper[5].text),                           # Home or Away
                      helper[6].text,                                       # Score of Game
                      helper[7].text,                                       # Minutes Played
                      stats[0],                                             # Points
                      stats[1],                                             # Rebounds
                      stats[2],                                             # Assists
                      stats[3],                                             # Steals
                      stats[4],                                             # Blocks
                      stats[5],                                             # Turnovers
                      stats[6],                                             # Three Pointers Made
                      stats[7],                                             # Field Goals Made
                      stats[8],                                             # Field Goals Attempted
                      stats[9],                                             # Free Throws Made
                      stats[10] ])                                          # Free Throws Attempted
        return -1
    except:
        return i + 2

def homeVsAway(opp):
    if opp[0] == '@':
        return 'away'
    elif opp[0] == 'v':
        return 'home'
    else:
        return 'messed up'

def splitStatsIntoCatagories(stats):
    allStats = stats.split(' ')
    finalStats = [] # should be 11 long 
    
    indexer = 2
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'pt')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'rb')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'as')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'st')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'bl')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'to')
    indexer += getInfoMainStats(allStats, finalStats, indexer, 'trey')
    indexer += getPercentages(allStats, finalStats, indexer, 'fg')
    indexer += getPercentages(allStats, finalStats, indexer, 'ft')
    
    return finalStats

def getInfoMainStats(allStats, finalStats, num, stat):
        if (len(allStats) > num):
            index = allStats[num].find(stat)
        else:
            index = -1
        if index != -1:
            finalStats.append((allStats[num])[:index])
            return 1
        else:
            finalStats.append(0)
            return 0

def getPercentages(allStats, finalStats, num, stat):
    if (len(allStats) > num):
        index = allStats[num].find(stat)
    else:
        index = -1
    if index != -1:
        dashIndex = allStats[num].find('-')
        finalStats.append((allStats[num])[:dashIndex])
        finalStats.append((allStats[num])[dashIndex+1:len(allStats[num])-2])
        return 1
    else:
        finalStats.append(0)
        finalStats.append(0)
        return 0

def getPosition(position):
    switcher = {
        'PG': 1,
        'SG': 2,
        'SF': 3,
        'PF': 4,
        'C': 5,
    }
    return switcher.get(position, -1)
##########################################################################################################################################################

if __name__ == "__main__":
    main()