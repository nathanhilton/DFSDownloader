from DownloaderLibrary import downloaderBase
from MLB.MLBDownloader import MLBDownloader


class MLBDraftkings(MLBDownloader):
    def __init__(self, startDate, endDate):
        MLBDownloader.__init__(self, 'dk')
        downloaderBase.__init__(self, startDate, endDate, 'MLB', 'draftkings')