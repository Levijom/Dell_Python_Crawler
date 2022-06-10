#####################################################
# PriceUpdater.py
# Copyright (C) Joao A. Haddad, 2020-2021
# Update 1.03 - Update to work with new Feb/2021 DSA
#####################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class PriceUpdater:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 90)
        self.driver.get("http://sales.dell.com")

    def __del__(self):
        self.driver.close()

    def worker(self, in_q, out_q, workerNum):
        MAX_TIME = 300
        while True:
            quoteNum = 0
            try:
                quoteNum, price, retries = in_q.get()
                print(f"worker #{workerNum}, Retries: {retries} -> {quoteNum} {price}")
                if quoteNum == "done":
                    return
                time_started = time.time()
                # url = (
                #     "https://sales.dell.com/#/quote/details/QuoteNumber/"
                #     + quoteNum.strip("\n")
                # )

                # Main Page should be open by now, using search button
                searchtext = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, ("intuitive-search-input"))
                    )
                )
                searchtext.clear()
                searchtext.send_keys(quoteNum.strip("\n"))
                searchtext.send_keys(Keys.ENTER)
                time.sleep(0.5)
                button1 = self.wait.until(
                    EC.element_to_be_clickable((By.ID, ("moreActionsDropdown")))
                )

                button1.click()
                button2 = self.wait.until(
                    EC.element_to_be_clickable((By.ID, ("btnCopyAsVersion")))
                )
                button2.click()
                # Creating a new version. Takes some time for the DOM to refresh

                unitprice = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "quoteCreate_LI_unitSellingPrice_0_0")
                    )
                )
                time.sleep(4)
                unitprice = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "quoteCreate_LI_unitSellingPrice_0_0")
                    )
                )
                unitprice.clear()
                unitprice.send_keys(price)
                unitprice.send_keys(Keys.ENTER)
                time.sleep(1)
                unitprice.send_keys(Keys.TAB)
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0,0)")
                # applychangebutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]")

                while True:  # To get the Apply Changes
                    if time.time() - time_started > MAX_TIME:
                        break
                    try:
                        # applychangebutton = driver.find_elements_by_css_selector("#quoteCreate_lineHeader > div > div.col-md-9.mg-top-20 > div:nth-child(2) > pricing-mode-toggler > div > button.btn.btn-primary.mg-left-10")
                        applychangebutton = self.driver.find_element_by_xpath(
                            '//*[@id="quoteCreate_lineHeader"]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]'
                        )
                        # applychangebutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]")
                        # applychangebutton = wait.until (EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]"))))
                        applychangebutton.click()
                        break
                    except:
                        time.sleep(1)
                time.sleep(2)
                while True:  # To get the Save Button
                    if time.time() - time_started > MAX_TIME:
                        break

                    try:
                        button3 = self.wait.until(
                            EC.element_to_be_clickable((By.ID, "button-success-split"))
                        )
                        button3.click()
                        break
                    except:
                        time.sleep(1)
                # print ("Chegou 1.5")
                time.sleep(2)
                # print("Chegou 2")
                while True:  # To get the Skip Button
                    if time.time() - time_started > MAX_TIME:
                        break
                    try:
                        skipbutton = self.wait.until(
                            EC.element_to_be_clickable(
                                (
                                    By.ID,
                                    ("quoteSaveUpdateRevenue_skipNoItemsToUpdate"),
                                )
                            )
                        )
                        skipbutton.click()
                        break
                    except:
                        time.sleep(1)
                time.sleep(20)

                if time.time() - time_started > MAX_TIME:
                    raise Exception("Timeout")

                # new_quotenumber = self.wait.until(
                #     EC.presence_of_element_located(
                #         (
                #             By.XPATH,
                #             "/html/body/app-root/div[1]/div[2]/div/div/ng-component/div/div/div[2]/div[1]/div[2]/quote-summary-title/div/div/div[1]/div/div[2]/div[1]/div[2]/span[2]",
                #         )
                #     )
                # )
                new_quotenumber = self.wait.until(
                    EC.presence_of_element_located((By.ID, "quoteNumber"))
                )
                new_quotenumber = self.driver.find_element_by_xpath(
                    "/html/body/app-root/div[1]/div[2]/div/div/ng-component/div/div/div[2]/div[1]/div[2]/quote-summary-title/div/div/div[1]/div/div[2]/div[2]/span"
                )
                # print(new_quotenumber.text)
                time.sleep(1)
                new_quotenumberversion = self.driver.find_element_by_id(
                    "quoteVersionsDropdownId"
                )
                quoteNumberWithVersion = (
                    new_quotenumber.text
                    + "."
                    + str(new_quotenumberversion.text.split()[1])
                )

                new_totalSellingPrice = self.driver.find_element_by_id(
                    "pricingSummary_sellingPrice"
                )
                print(
                    f"worker #{workerNum}: Finished - {quoteNumberWithVersion} {new_totalSellingPrice.text}"
                )
                out_q.put((quoteNumberWithVersion, new_totalSellingPrice.text, 0))

            except:
                temp = quoteNum.strip("\n")
                print(f"Worker #{workerNum}: Error getting quote #{temp}")
                out_q.put((quoteNum.strip("\n"), price, retries + 1))
