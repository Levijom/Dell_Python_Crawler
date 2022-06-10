###########################################################
# QuoteCrawler v2.0                                       #
# Copyright (C) Joao A. Haddad - Sep-Dec/2020             #
# Usage: python QuoteCrawler SOURCE.TXT DESTINATION.XLSX  #
###########################################################

import argparse

from src.cache import Cache
from src.crawler import Crawler
from src.spreadsheet import Spreadsheet

# Sets up some stuff so we can read the input txt files
version = "2.0"
parser = argparse.ArgumentParser()
parser.add_argument("sourceFile", type=str, help="Source File (txt format)")
parser.add_argument("destFile", type=str, help="Destination file (xlsx format)")
parser.add_argument(
    "--customerready", help="Remove internal information", action="store_true"
)
parser.add_argument("--version", help="Show version", action="version", version=version)

args = parser.parse_args()

# Error handling if we can't open the input txt files
try:
    sourceFile = open(args.sourceFile, "rt")
except:
    print("Error opening file " + args.sourceFile)
    quit()

# Makes "quote_list" become a list of the quotes from the input txt files
quote_list = sourceFile.readlines()  # List of Quotes
response = []
sourceFile.close()

# Get the cached stuff
cache = Cache()

# Initializes the crawler
crawler = Crawler()

# Iterate through each line of input text file, assign quote number as "quoteNumberFromList"
for quoteNumberFromList in quote_list:

    # Potential Error Point: replaces / with . but we need the opposite for URL use
    quoteNumberFromList = quoteNumberFromList.split()[0].strip("US-").replace("/", ".")

    # Don't use quote called "Ignore", skips the rest of this iteration
    if quoteNumberFromList == "IGNORE":
        response.append({"Completed": False, "FullQuoteNumber": "Ignored"})
        continue

    # Get quote from cache if it is there.
    current = cache.isQuoteCached(quoteNumberFromList)

    # This "if" checks if we got current from cache
    if current == {}:
        # Enters here iff not found in Cache
        print("Not in Cache")

        # "quoteNumberFromList" may need to be modified to fit url convention
        # current will hold all the data scraped off the web-page in current["quoteNumber"], current["solutionnumber"]
        # And so on, values are addressed by their ID.  also holds current["completed"] which a bool
        current = crawler.RunCrawler(quoteNumberFromList)
        if current["Completed"]:
            cache.addToCache(current)
            cache.saveCacheToDisk()

    # response will hold a vector of current vectors, to be iterated through later
    response.append(current)

spreadsheet = Spreadsheet(args.destFile, len(response))
spreadsheet.WritetoExcel(response, args.customerready)

# TO do an internal URL: worksheet.write_url('A1',  'internal:testao!A1')
