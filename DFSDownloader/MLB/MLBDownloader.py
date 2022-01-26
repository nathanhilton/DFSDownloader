from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import re
from datetime import datetime
from DownloaderLibrary import downloaderBase


class MLBDownloader(downloaderBase):
    def __init__(self, platform_shortened):
        self.platform_shortened = platform_shortened

    def download(self, currentDate):
        pass

    def getTheStats(self, players, i, rows, playerTracker):
        pass

    def homeVsAway(self, opp):
        pass

    def splitStatsIntoCatagories(self, stats):
        pass

    def getInfoMainStats(self, allStats, finalStats, num, stat):
        pass