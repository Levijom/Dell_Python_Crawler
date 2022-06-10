###########################################################
# QuoteCrawler v2.0 - Crawler.py                          #
# Copyright (C) Joao A. Haddad - Sep-Dec/2020             #
# Usage: python QuoteCrawler SOURCE.TXT DESTINATION.XLSX  #
###########################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Crawler:

    #    driver = webdriver.chrome.webdriver.WebDriver

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)

        try:
            print("Loading DSA to Clear Banner")
            self.driver.get("https://sales.dell.com")
        except:
            time.sleep(1)
        time.sleep(40)  # Jose added this in to get aroudn the Banner Issue, during this sleep, go to the first Quote URL https://sales.dell.com/#/quote/details/QuoteNumber/3000111672265.1

    def __del__(self):
        self.driver.close()

    def RunCrawler(self, quoteNumber: str) -> dict:

        # This is use for url related quote numbers
        urlQuoteNumber = quoteNumber.split()[0].strip("US-").replace(".", "/")

        # Modified this to fit the url convention
        url = "https://sales.dell.com/#/quote/details/QuoteNumber/" + urlQuoteNumber.strip(
            "\n"
        )
        response = {}
        response["FullQuoteNumber"] = quoteNumber
        wait = WebDriverWait(self.driver, 90)

        try:
            print("Trying quote #" + quoteNumber.strip("\n"))
            self.driver.get(url)
            self.driver.refresh()
            time.sleep(1)
            while True:
                try:
                    q1 = wait.until(
                        EC.presence_of_element_located((By.ID, ("quoteNumber")))
                    )
                    if len(q1.text) != 0:
                        break
                    else:
                        time.sleep(1)
                except:
                    time.sleep(1)
            print("Quote# " + q1.text)
            response["quotenumber"] = q1.text

            q2 = wait.until(
                EC.presence_of_element_located((By.ID, ("quoteDetail_versionToggle")))
            )
            response["quotenumberversion"] = str(q2.text.split()[1])

            q3 = wait.until(
                EC.presence_of_element_located((By.ID, ("quoteDetail_items_header_s")))
            )
            response["solutionnumber"] = str(q3.text.split()[2])

            q4 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_summary_listPrice"))
                )
            )
            response["TotalListPrice"] = float(q4.text.strip("$").replace(",", ""))

            q5 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_summary_sellingPrice"))
                )
            )
            response["TotalSellingPrice"] = float(q5.text.strip("$").replace(",", ""))

            q6 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_summary_shippingPriceAmount"))
                )
            )
            response["TotalShippingPrice"] = float(q6.text.strip("$").replace(",", ""))

            q7 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_summary_discountPercent"))
                )
            )

            response["TotalDiscount"] = float(q7.text.split()[2].strip("%")) / 100.0

            q8 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_GI_with_pricing_modifier"))
                )
            )
            response["OverallModifier"] = float(q8.text)
            # new ones

            q9 = wait.until(
                EC.presence_of_element_located(
                    (By.ID, ("quoteDetail_GI_shippingAddress_0"))
                )
            )
            response["shippingAdress"] = q9.text

            q10 = wait.until(
                EC.presence_of_element_located((By.ID, ("quoteDetail_title")))
            )
            response["quoteName"] = q10.text

            # Need to add the configuration of the quote
            ListSubItems = []
            numSubItems = 0
            while True:  # Checking how many items are in a quote
                SubItem = "toggleMoreLess_0_" + str(numSubItems)
                print(SubItem)
                try:
                    print("Trying " + SubItem)
                    timetowait = 60 if numSubItems == 0 else 1
                    SeeMore = WebDriverWait(self.driver, timetowait).until(
                        EC.presence_of_element_located((By.ID, (SubItem)))
                    )
                    # print("CHEGOU1")
                    SeeMore = WebDriverWait(self.driver, timetowait).until(
                        EC.element_to_be_clickable((By.ID, (SubItem)))
                    )
                    SeeMore.click()
                    # Found that subGroup
                    print("Found " + SubItem)
                    print("-------------")
                    print("SubItem " + str(numSubItems))

                    currentSubItem = {}

                    q20 = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.ID,
                                ("quoteDetail_LI_PI_unitPrice_0_" + str(numSubItems)),
                            )
                        )
                    )
                    currentSubItem["ListPrice"] = float(
                        q20.text.strip("$").replace(",", "")
                    )

                    q21 = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.ID,
                                (
                                    "quoteDetail_LI_PI_unitSellingPrice_OC_0_"
                                    + str(numSubItems)
                                ),
                            )
                        )
                    )
                    currentSubItem["SellingPrice"] = float(
                        q21.text.strip("$").replace(",", "")
                    )

                    q22 = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.ID,
                                (
                                    "quoteDetail_LI_pricingModifier_0_"
                                    + str(numSubItems)
                                ),
                            )
                        )
                    )
                    currentSubItem["Modifier"] = float(q22.text)

                    q23 = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.ID,
                                (
                                    "quoteDetail_LI_PI_dolPercentage_0_"
                                    + str(numSubItems)
                                ),
                            )
                        )
                    )
                    currentSubItem["DOL"] = float(q23.text.strip("%")) / 100.0

                    q24 = wait.until(
                        EC.presence_of_element_located(
                            (By.ID, ("lineitem_config_block_0_" + str(numSubItems)))
                        )
                    )
                    currentSubItem["configuration"] = q24.text
                    # new ones

                    q25 = wait.until(
                        EC.presence_of_element_located(
                            (By.ID, ("quoteDetail_LI_quantity_0_" + str(numSubItems)))
                        )
                    )
                    currentSubItem["quantity"] = int(q25.text.replace(",", ""))

                    numSubItems += 1
                    ListSubItems.append(currentSubItem)  # go to the next item

                except:
                    response["SubItems"] = ListSubItems
                    break
            if len(response["SubItems"]) > 0:
                response["Completed"] = True
            else:
                response["Completed"] = False

            return response
        except:

            response = {}
            response["FullQuoteNumber"] = quoteNumber
            response["Completed"] = False
            return response
