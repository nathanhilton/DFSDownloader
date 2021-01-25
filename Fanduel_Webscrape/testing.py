from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv 
import os
from tqdm import tqdm

# the is a comment to see if a can push from new computer!!!!
def main():
    January = []
    year = [January]
    months = ["/January"]
    for i in range(1,1):
        January.append(i)
    lengths = {1:1}

    if os.path.isdir("./Stat_Sheets") == False:
        os.mkdir("./Stat_Sheets")
    
    for z in tqdm(range(1,len(year) + 1)):
        folder = months[z - 1]
        if os.path.isdir("./Stat_Sheets" + folder) == False:
            os.mkdir("./Stat_Sheets" + folder)
        for w in range(1, lengths[z] + 1):
            my_url = "http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=" + str(z) + "&day=" + str(w) + "&year=2019" #bs4 setup stuff
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            soup = BeautifulSoup(page_html, "html.parser")

            players = soup.find_all("tr") # first player is always 10
            if (len(players) >= 10) : # checks if there were games that day
                fields = ["Name", "Position", "FDPoints", "Salary", "Team", "Opp.", "Home/Away", "Score", "Min", "stats", "Pts", 'Rbs', 'Ast', 'Stl', 'Blk', 'To', '3PM']
                rows = []
                playerTrackeer = 0
                for i in range(10,len(players)): # for the gaurds
                    try:
                        helper = players[i].find_all("td")
                        stats = splitStats(str(helper[8].text))
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
                                      stats[6] ])                                           # Three Pointers Made
                    except:
                        playerTrackeer = i + 2
                        break
                for i in range(playerTrackeer,len(players)): # for the forwards
                    try:
                        helper = players[i].find_all("td")  
                        stats = splitStats(str(helper[8].text))
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
                                      stats[6] ])                                           # Three Pointers Made
                    except:
                        playerTrackeer = i + 2
                        break
                for i in range(playerTrackeer,len(players)): # for the centers
                    try:
                        helper = players[i].find_all("td")  
                        stats = splitStats(str(helper[8].text))
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
                                      stats[6] ])                                           # Three Pointers Made
                    except:
                        playerTrackeer = i + 2
                        break

                filename = "Stat_Sheets/" + folder + "/" + str(z) + "-" + str(w) + "-2019.csv"
                with open(filename, "w", newline="") as csvfile: # writing to csv file  
                    csvwriter = csv.writer(csvfile)  
                    csvwriter.writerow(fields)  
                    csvwriter.writerows(rows) 
                
                
def homeVsAway(opp):
    if opp[0] == '@':
        return 'away'
    elif opp[0] == 'v':
        return 'home'
    else:
        return 'messed up'

def splitStats(stats):
    allStats = stats.split(' ')
    finalStats = [] # should be 11 long 

    indexer = 2
    indexer += getInfo(allStats, finalStats, indexer, 'pt')
    indexer += getInfo(allStats, finalStats, indexer, 'rb')
    indexer += getInfo(allStats, finalStats, indexer, 'as')
    indexer += getInfo(allStats, finalStats, indexer, 'st')
    indexer += getInfo(allStats, finalStats, indexer, 'bl')
    indexer += getInfo(allStats, finalStats, indexer, 'to')
    indexer += getInfo(allStats, finalStats, indexer, 'trey')
    
    return finalStats

def getInfo(allStats, finalStats, num, stat):
        index = allStats[num].find(stat)
        if index != -1:
            finalStats.append((allStats[num])[:index])
            return 1
        else:
            finalStats.append(0)
            return 0

if __name__ == "__main__":
    main()