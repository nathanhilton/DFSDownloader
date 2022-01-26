from DownloaderLibrary import downloaderBase
from NFL.NFLDownloader import NFLDownloader


class NFLFanduel(NFLDownloader):
    def __init__(self, startDate, endDate):
        NFLDownloader.__init__(self, 'fd')
        downloaderBase.__init__(self, startDate, endDate, 'NFL', 'fanduel')