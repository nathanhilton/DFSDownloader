#how to get the stuff to pull up on command to make run
#conda activate base
#python

#importing the libraries to do it
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv  

def main():
    jan = feb = mar = apr = may = jun = jul = aug = sep = octo = nov = dec = []
    year = [jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec]
    for i in range(1,32):
        jan.append(i)
        mar.append(i)
        may.append(i)
        jul.append(i)
        aug.append(i)
        octo.append(i)
        dec.append(i)
    for i in range(1,31):
        apr.append(i)
        jun.append(i)
        sep.append(i)
        nov.append(i)
    for i in range(1,29):
        feb.append(i)
    lengths = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    for z in range(1,len(year) + 1):
        for w in range(1, lengths[z] + 1):
            my_url = "http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=" + str(z) + "&day=" + str(w) + "&year=2019" #bs4 setup stuff
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            soup = BeautifulSoup(page_html, "html.parser")

            players = soup.find_all("tr") # first player is always 10
            if (len(players) >= 10) : # checks if there were games that day
                fields = ["Name", "Position", "FDPoints", "Salary", "Team", "Opp.", "Score", "Min", "stats"]
                rows = []
                playerTrackeer = 0
                for i in range(10,len(players)): # for the gaurds
                    try:
                        helper = players[i].find_all("td")  
                        rows.append([players[i].find("a").text, helper[0].text, helper[2].text, helper[3].text, helper[4].text, helper[5].text, helper[6].text, helper[7].text, helper[8].text])
                    except:
                        playerTrackeer = i + 2
                        break
                for i in range(playerTrackeer,len(players)): # for the forwards
                    try:
                        helper = players[i].find_all("td")  
                        rows.append([players[i].find("a").text, helper[0].text, helper[2].text, helper[3].text, helper[4].text, helper[5].text, helper[6].text, helper[7].text, helper[8].text])
                    except:
                        playerTrackeer = i + 2
                        break
                for i in range(playerTrackeer,len(players)): # for the centers
                    try:
                        helper = players[i].find_all("td")  
                        rows.append([players[i].find("a").text, helper[0].text, helper[2].text, helper[3].text, helper[4].text, helper[5].text, helper[6].text, helper[7].text, helper[8].text])
                    except:
                        playerTrackeer = i + 2
                        break

                
                filename = "statSheets/NBAFanduel(" + str(z) + "." + str(w) + ").csv"    
                with open(filename, "w", newline="") as csvfile: # writing to csv file  
                    csvwriter = csv.writer(csvfile)  
                    csvwriter.writerow(fields)  
                    csvwriter.writerows(rows) 
                
                #https://www.youtube.com/watch?v=XQgXKtPSzUI

if __name__ == "__main__":
    main()