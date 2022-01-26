from sys import platform
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
from DownloaderLibrary import downloaderBase


class NBADownloader(downloaderBase):
    def __init__(self, platform_shortened):
        self.platform_shortened = platform_shortened

    def download(self, currentDate):
        year = str(currentDate.year)
        month = str(currentDate.month)
        day = str(currentDate.day)
        monthString = str(datetime.strptime(month, "%m").strftime("%B"))

        my_url = "http://rotoguru1.com/cgi-bin/hyday.pl?game={platform}&mon={month}&day={day}&year={year}".format(month=month, day=day, year=year, platform=self.platform_shortened) #bs4 setup stuff
        uClient = uReq(my_url)            
        page_html = uClient.read()
        uClient.close()
        soup = BeautifulSoup(page_html, "html.parser")
        players = soup.find_all("tr") # first player is always 10

        if (len(players) >= 10) : # checks if there were games that day
            fields = ["Name", "Position", "Points", "Salary", "Team", "Opp.", "Home/Away", "Score", "Min", "Pts", 'Rbs', 'Ast', 'Stl', 'Blk', 'To', '3PM', 'FGM', 'FGA', 'FTM', 'FTA']
            rows = []   
            playerTracker = 0
            for i in range(10,len(players)): # for the gaurds
                playerTracker = self.getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break
            for i in range(playerTracker,len(players)): # for the forwards
                playerTracker = self.getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break
            for i in range(playerTracker,len(players)): # for the centers
                playerTracker = self.getTheStats(players, i, rows, playerTracker)
                if playerTracker != -1:
                    break
            
            if len(rows) != 0:
                filepath = self.create_folders_for_files(monthString, year)
                filename = filepath + '{month}-{day}-{year}.csv'.format(year=year, day=day, month=month)
                self.write_to_csv(filename, fields, rows)


    def getTheStats(self, players, i, rows, playerTracker):
            try:
                helper = players[i].find_all("td")
                stats = self.splitStatsIntoCatagories(str(helper[8].text))
                rows.append([ players[i].find("a").text,                          # Name
                            helper[0].text,                     # Position
                            helper[2].text,                                       # FDPoints
                            re.sub('[$,]', '', helper[3].text),                   # Salary
                            helper[4].text,                                       # Team
                            str(helper[5].text)[2:len(str(helper[5].text))],      # Opponent    
                            self.homeVsAway(helper[5].text),                      # Home or Away
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

    def homeVsAway(self, opp):
        if opp[0] == '@':
            return 'away'
        elif opp[0] == 'v':
            return 'home'
        else:
            return 'messed up'

    def splitStatsIntoCatagories(self, stats):
        allStats = stats.split(' ')
        finalStats = [] # should be 11 long 
        
        indexer = 2
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'pt')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'rb')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'as')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'st')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'bl')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'to')
        indexer += self.getInfoMainStats(allStats, finalStats, indexer, 'trey')
        indexer += self.getPercentages(allStats, finalStats, indexer, 'fg')
        indexer += self.getPercentages(allStats, finalStats, indexer, 'ft')
        
        return finalStats

    def getInfoMainStats(self, allStats, finalStats, num, stat):
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

    def getPercentages(self, allStats, finalStats, num, stat):
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

    # don't believe i need this function
    # def getPosition(self, position):
    #     switcher = {
    #         'PG': 1,
    #         'SG': 2,
    #         'SF': 3,
    #         'PF': 4,
    #         'C': 5,
    #     }
    #     return switcher.get(position, -1)