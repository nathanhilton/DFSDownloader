from tqdm import tqdm
from argparse import ArgumentParser
from datetime import timedelta, date
from NBA.NBADraftkings import NBADraftkings
from NBA.NBAFanduel import NBAFanduel
from NFL.NFLDraftkings import NFLDraftkings
from NFL.NFLFanduel import NFLFanduel
from MLB.MLBDraftkings import MLBDraftkings
from MLB.MLBFanduel import MLBFanduel


def main():
    parser = ArgumentParser()
    parser.add_argument("startDate", metavar='start_date', type=str, help="starting date for downloads")
    parser.add_argument("endDate", metavar='end_date', type=str, help="starting date for downloads")
    parser.add_argument("sport", metavar='sport', type=str, help="options are NFL and NBA")
    parser.add_argument("website", metavar='website', type=str, help="options are Draftkings and Fanduel")
    
    args = parser.parse_args()
    startDate = date.fromisoformat(args.startDate)
    endDate = date.fromisoformat(args.endDate)
    sport = args.sport.lower()
    website = args.website.lower()
    deltaDate = timedelta(days=1)

    # checking if parameters are valid
    if (endDate - startDate).days < 0:
        raise TypeError('end date need to be after start date!')
    
    if sport == 'nba' and website == 'fanduel':
        downloader = NBAFanduel(startDate, endDate)
    elif sport == 'nba' and website == 'draftkings':
        downloader = NBADraftkings(startDate, endDate)
    elif sport == 'nfl' and website == 'fanduel':
        downloader = NFLFanduel(startDate, endDate)
    elif sport == 'nfl' and website == 'draftkings':
        downloader = NFLDraftkings(startDate, endDate)
    elif sport == 'mlb' and website == 'fanduel':
        downloader = MLBFanduel(startDate, endDate)
    elif sport == 'mlb' and website == 'draftkings':
        downloader = MLBDraftkings(startDate, endDate)
    else:
        print('Enter a valid combination of sport and website')
        return
    
    for i in tqdm(range(0, (endDate - startDate).days + 1), desc='Progess Bar: '):
        currentDate = startDate + (deltaDate * i)
        downloader.download(currentDate)
                    
    print('Download Completed!\n')


if __name__ == "__main__":
    main()
