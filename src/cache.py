###########################################################
# QuoteCrawler v2.0 - Cache.py                            #
# Copyright (C) Joao A. Haddad - Sep-Dec/2020             #
# Usage: python QuoteCrawler SOURCE.TXT DESTINATION.XLSX  #
###########################################################

import json


class Cache:
    # cached = []

    def __init__(self):

        # Opening cache file

        try:
            cacheFile = open("cache.json")
            self.cached = json.load(cacheFile)
            cacheFile.close()
            backupFile = open("cache.json.backup", "w")
            backupFile.write(json.dumps(self.cached))
            backupFile.close()
        except:
            self.cached = []

    def isQuoteCached(self, quote: str) -> dict:
        for item in self.cached:
            if item["FullQuoteNumber"] == quote:
                if item["Completed"] == True:
                    return item
        return {}

    def addToCache(self, quote: dict):
        self.cached.append(quote)
        return

    def saveCacheToDisk(self) -> bool:
        try:
            cacheFile = open("cache.json", "w")
            cacheFile.write(json.dumps(self.cached))
            cacheFile.close()
        except:
            return False
        return True
