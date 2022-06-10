###########################################################
# QuoteCrawler v2.0                                       #
# Copyright (C) Joao A. Haddad - Sep-Dec/2020             #
# Usage: python QuoteCrawler SOURCE.TXT DESTINATION.XLSX  #
###########################################################

import argparse

from src.cache import Cache
from src.crawler import Crawler
from src.spreadsheet import Spreadsheet

version = "2.0"
parser = argparse.ArgumentParser()
parser.add_argument("sourceFile", type=str, help="Source File (txt format)")
parser.add_argument("destFile", type=str, help="Destination file (xlsx format)")
parser.add_argument(
    "--customerready", help="Remove internal information", action="store_true"
)
parser.add_argument("--version", help="Show version", action="version", version=version)

args = parser.parse_args()

try:
    sourceFile = open(args.sourceFile, "rt")
except:
    print("Error opening file " + args.sourceFile)
    quit()

quote_list = sourceFile.readlines()  # List of Quotes
response = []
sourceFile.close()


cache = Cache()
crawler = Crawler()
for quoteNumberFromList in quote_list:
    quoteNumberFromList = quoteNumberFromList.split()[0].strip("US-").replace("/", ".")
    if quoteNumberFromList == "IGNORE":
        response.append({"Completed": False, "FullQuoteNumber": "Ignored"})
        continue
    current = cache.isQuoteCached(quoteNumberFromList)
    if current == {}:
        # NotFound in Cache
        print("Not in Cache")
        current = crawler.RunCrawler(quoteNumberFromList)
        if current["Completed"] == True:
            cache.addToCache(current)
            cache.saveCacheToDisk()

    response.append(current)

spreadsheet = Spreadsheet(args.destFile, len(response))
spreadsheet.WritetoExcel(response, args.customerready)


# TO do an internal URL: worksheet.write_url('A1',  'internal:testao!A1')