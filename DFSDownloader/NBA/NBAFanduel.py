from DownloaderLibrary import downloaderBase
from NBA.NBADownloader import NBADownloader


class NBAFanduel(NBADownloader):
    def __init__(self, startDate, endDate):
        NBADownloader.__init__(self, 'fd')
        downloaderBase.__init__(self, startDate, endDate, 'NBA', 'fanduel')