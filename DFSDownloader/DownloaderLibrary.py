import csv 
import os


class downloaderBase():
    def __init__(self, startDate, endDate, sport='NBA', platform='fanduel'):
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
        try:
            os.mkdir('./Stat_Sheets/{year}/'.format(year=year))
            os.mkdir('./Stat_Sheets/{year}/{month}/'.format(year=year, month=month))
        except OSError: 
            try:
                os.mkdir('./Stat_Sheets/{year}/{month}/'.format(year=year, month=month))
            except:
                pass
