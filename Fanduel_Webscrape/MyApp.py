from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv 
import os
from tqdm import tqdm

def main():
    January = February = March = April = May = June = July = August = September = October = November = December = []
    year = [January, February, March, April, May, June, July, August, September, October, November, December]
    months = ["/January", "/February", "/March", "/April", "/May", "/June", "/July", "/August", "/September", "/October", "/November", "/December"]
    for i in range(1,32):
        January.append(i)
        March.append(i)
        May.append(i)
        July.append(i)
        August.append(i)
        October.append(i)
        December.append(i)
    for i in range(1,31):
        April.append(i)
        June.append(i)
        September.append(i)
        November.append(i)
    for i in range(1,30):
        February.append(i)
    lengths = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    if os.path.isdir("./Stat_Sheets") == False:
        os.mkdir("./Stat_Sheets")
    print('\nDownloading Stats......')
    for z in range(1,len(year) + 1):
        folder = months[z - 1]
        if os.path.isdir("./Stat_Sheets" + folder) == False:
            os.mkdir("./Stat_Sheets" + folder)
        for w in tqdm(range(1, lengths[z] + 1), desc=( (months[z - 1])[1:4] + ": " ) ):
            my_url = "http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=" + str(z) + "&day=" + str(w) + "&year=2019" #bs4 setup stuff
            uClient = uReq(my_url)            
            page_html = uClient.read()
            uClient.close()
            soup = BeautifulSoup(page_html, "html.parser")
            players = soup.find_all("tr") # first player is always 10
            if (len(players) >= 10) : # checks if there were games that day
                fields = ["Name", "Position", "FDPoints", "Salary", "Team", "Opp.", "Home/Away", "Score", "Min", "stats", "Pts", 'Rbs', 'Ast', 'Stl', 'Blk', 'To', '3PM', 'FGM', 'FGA', 'FTM', 'FTA']
                rows = []
                playerTracker = 0
                ########## Gets the stats for the Guards ##########
                for i in range(10,len(players)): 
                    if getTheStats(players, i, rows, playerTracker) == -1:
                        break
                ######### Gets the stats for the Forwards #########
                for i in range(playerTracker,len(players)): # for the forwards
                    if getTheStats(players, i, rows, playerTracker) == -1:
                        break
                ######### Gets the stats for the Centers ##########
                for i in range(playerTracker,len(players)): # for the centers
                    if getTheStats(players, i, rows, playerTracker) == -1:
                        break
                ############# Exporting stats to CSV ##############
                filename = "Stat_Sheets/" + folder + "/" + str(z) + "-" + str(w) + "-2019.csv"
                with open(filename, "w", newline="") as csvfile: # writing to csv file  
                    csvwriter = csv.writer(csvfile)  
                    csvwriter.writerow(fields)  
                    csvwriter.writerows(rows) 
                    
    print('Download Completed!\n')


#################################################################### HELPER FUNCTIONS ####################################################################
def getTheStats(players, i, rows, playerTracker):
    try:
        helper = players[i].find_all("td")
        stats = splitStatsIntoCatagories(str(helper[8].text))
        rows.append([ players[i].find("a").text,                            # Name
                      helper[0].text,                                       # Position
                      helper[2].text,                                       # FDPoints
                      helper[3].text,                                       # Salary
                      helper[4].text,                                       # Team
                      str(helper[5].text)[2:len(str(helper[5].text))],      # Opponent    
                      homeVsAway(helper[5].text),                           # Home or Away
                      helper[6].text,                                       # Score of Game
                      helper[7].text,                                       # Minutes Played    
                      helper[8].text,                                       # Statistics
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
    except:
        playerTracker = i + 2
        return -1

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
##########################################################################################################################################################

if __name__ == "__main__":
    main()