# Daily Fantasy Sports Historical Data Downloader

## About The Project

The purpose of this repository is to easily allow people to download historical daily fantasy sports data. Currently there is no easy way to download this data, but this repository will allow users to easily download the data with one terminal command! <br />

The current list of daily fantasy sports platforms supported:
<li>NBA Fanduel</li>
<br />

## Getting Started

The first step is to clone the repository. This can be done with the command 
   ```sh
   git clone https://github.com/nathanhilton/DFSDownloader.git
   ```

After entering the created directory, the next step is to download all the necessary libaries with the command
   ```sh
   pip install -r requirements.txt
   ```
Now you are ready to start downloading data!<br />
<br />

## How To Use

### Format
To download the data you will need to run a terminal command with the following format
   ```sh
   python main.py start_date end_date sport platform
   ```

The two required parameters needed are the start date and end date in the format <br />

### Example
An example of downloading all the data from August 2020 would look like this
   ```sh
   python main.py 2020-08-01 2020-08-31 NBA Fanduel
   ```
<br />

## Future Plans
<li>Adding more sports and platforms</li>
