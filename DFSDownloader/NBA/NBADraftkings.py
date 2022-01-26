from DownloaderLibrary import downloaderBase
from NBA.NBADownloader import NBADownloader


class NBADraftkings(NBADownloader):
    def __init__(self, startDate, endDate):
        NBADownloader.__init__(self, 'dk')
        downloaderBase.__init__(self, startDate, endDate, 'NBA', 'draftkings')