from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv 
import os
import re
from tqdm import tqdm
import argparse
from argparse import ArgumentParser
from datetime import timedelta, date, datetime
import numpy as np

from NBA_Fanduel import NBA_Fanduel

# the is a comment to see if a can push from new computer!!!!
def main():
    parser = ArgumentParser()
    parser.add_argument("startDate", metavar='start_date', type=str, help="starting date for downloads")
    parser.add_argument("endDate", metavar='end_date', type=str, help="tiled image width and height")
    # parser.add_argument("sport", metavar='sport', type=str, help="tiled image width and height")
    # parser.add_argument("website", metavar='website', type=str, help="tiled image width and height")
    
    args = parser.parse_args()
    startTemp = args.startDate.split('-')
    startDate = date(int(startTemp[0]), int(startTemp[1]), int(startTemp[2]))
    endTemp = args.endDate.split('-')
    endDate = date(int(endTemp[0]), int(endTemp[1]), int(endTemp[2]))
    deltaDate = timedelta(days=1)

    if ((endDate - startDate). days < 0):
        raise TypeError('end date need to be after start date!')
    if os.path.isdir("./Stat_Sheets") == False:
        os.mkdir("./Stat_Sheets")
    print('\nDownloading Stats......')
    
    downloader = NBA_Fanduel(startDate, endDate)
    
    for i in tqdm(range(0, (endDate - startDate).days + 1), desc='Progess Bar: '):
        currentDate = startDate + (deltaDate * i)
        downloader.download(currentDate)
                    
    print('Download Completed!\n')

if __name__ == "__main__":
    main()