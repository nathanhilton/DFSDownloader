from DownloaderLibrary import downloaderBase
from NFL.NFLDownloader import NFLDownloader


class NFLDraftkings(NFLDownloader):
    def __init__(self, startDate, endDate):
        NFLDownloader.__init__(self, 'dk')
        downloaderBase.__init__(self, startDate, endDate, 'NFL', 'draftkings')