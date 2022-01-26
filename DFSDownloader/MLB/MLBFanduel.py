from DownloaderLibrary import downloaderBase
from MLB.MLBDownloader import MLBDownloader


class MLBFanduel(MLBDownloader):
    def __init__(self, startDate, endDate):
        MLBDownloader.__init__(self, 'fd')
        downloaderBase.__init__(self, startDate, endDate, 'MLB', 'fanduel')