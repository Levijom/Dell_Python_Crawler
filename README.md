# DSA_Crawler

Author: Joao A. Haddad

DSA Crawler tools help simplify the process of updating and presenting quotes to customers. It was specifically created to help when there are dozens (or hundreds) of quotes to be processed.

## Quote Reader

Quote Reader creates an Excel spreadsheet with all the quotes in a clean way to present pricing and configuration to the customer

## Price Updater

Price Updater automatically updates quotes to a new version with the price added to the input file

## How to install

- Install Python3
- Install the Chrome Driver that matches your Chrome version
    `https://chromedriver.chromium.org/getting-started`
- Copy all the files to c:\DSA_Crawler folder
- run `python -m install -r requirements.txt`

## To run the Quote Reader

`python .\QuoteCrawler.py --customerready .\input\20210524.txt  .\output\20210524.xlsx`

## To run the Price Updater

variables: input file and number of threads. The input file is related to unit pricing.

`python .\multitaskPriceUpdater.py input\20210520.txt --threads 1`

Sample files for the Quote Reader and Price Updater are available on the input folder

## Features not created

Neither solution works with quotes that have multiple groups. Usually EI and Blades quotes have multiple groups.




Read Crawler

python .\QuoteCrawler.py --customerready .\input\220118FinalBidv3.txt  .\output\220118FinalBidv4.xlsx
python .\QuoteCrawler.py --customerready .\input\JOAOTEST.txt  .\output\JOAOTEST.xlsx

Write Crawler