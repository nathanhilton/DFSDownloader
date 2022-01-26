class downloaderBase():
    def __init__(self, startDate, endDate, sport='NBA', platform='fanduel'):
        self.startDate = startDate
        self.endDate = endDate
        self.sport = sport
        self.platform = platform

    def download(self):
        pass
