import csv
from genericpath import exists 
import os
from sys import platform


class downloaderBase():
    def __init__(self, startDate, endDate, sport, platform):
        self.startDate = startDate
        self.endDate = endDate
        self.sport = sport
        self.platform = platform

    def download(self):
        pass

    def write_to_csv(self, filename, fields, rows):
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(fields)  
            csvwriter.writerows(rows)

    def create_folders_for_files(self, month, year):
        filepath = './Stat_Sheets/{sport}_{platform}/{year}/{month}/'.format(year=year, month=month, sport=self.sport, platform=self.platform)
        os.makedirs(filepath, exist_ok=True)
        return filepath