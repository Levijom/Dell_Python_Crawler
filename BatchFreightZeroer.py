from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


import argparse
import re
import time

#Getting Correct Command Line requirements
#Usage: python BatchFreightZeroer.py SOURCE.TXT DESTINATION.TXT

parser = argparse.ArgumentParser()
parser.add_argument("sourceFile", type=str, help="Source File (txt format)")
args = parser.parse_args()

try:
    sourceFile = open(args.sourceFile,"r")

except:
    print("Error opening file "+ args.sourceFile)
    quit()

quote_list = sourceFile.readlines()  #List of Quotes
sourceFile.close() 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 90)
actions = ActionChains(driver)

quote = 0

for quoteNumberFromList in quote_list:
    quote = quoteNumberFromList.split()[0].strip("US-").replace('/','.')
    print ("Changing Quote #" + quote +" - zeroing freight")

    url="https://sales.dell.com/#/quote/details/QuoteNumber/" + quote.strip('\n')

    try:
        print ("Trying quote #" +quote.strip('\n'))
       
        driver.get(url)
        driver.refresh()
        
        button1 = wait.until (EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/quote-details-navigation/div/button"))))
        button1.click()
        button2 = wait.until(EC.element_to_be_clickable((By.ID,("quoteDetail_copyQuoteVersion")))) 
        button2.click()
        #Creating a new version. Takes some time for the DOM to refresh
        
        while (True):
            try:
                #quoteCreate_groupAccordion_0 > div.collapse.in.show > quote-create-shipping-group-details > div.dsaAccordion
                group_0 = wait.until(EC.presence_of_element_located((By.ID, ("quoteCreate_group_0"))))
                driver.execute_script("arguments[0].scrollIntoView();", group_0)
                #actions.move_to_element(group_0).perform()
                shippinginfo = wait.until(EC.presence_of_element_located((By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[3]/div/div/div/div/div/div/div[3]/quote-create-shipping-group-details/div[2]/accordion/accordion-group/div/div[1]/div/div/div/span"))))
                shippinginfo.click()
                selection = Select (wait.until(EC.presence_of_element_located((By.ID, ("quoteCreate_GI_0_shippingMethod")))))
                selection.select_by_visible_text('Standard Delivery Free Cost')
                break
            except:
                time.sleep(1)
                #driver.execute_script("window.scrollTo(0,0)")

        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0,0)")
        #applychangebutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]")

        # while (True):  #To get the Apply Changes
        #     try:
        #         #applychangebutton = driver.find_elements_by_css_selector("#quoteCreate_lineHeader > div > div.col-md-9.mg-top-20 > div:nth-child(2) > pricing-mode-toggler > div > button.btn.btn-primary.mg-left-10")
        #         applychangebutton = driver.find_element_by_xpath('//*[@id="quoteCreate_lineHeader"]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]')
        #         #applychangebutton = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]")
        #         #applychangebutton = wait.until (EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/quote-create-root/quote-create/div/div/div[1]/quote-create-shipping-group/div/div[1]/div/div[2]/div[2]/pricing-mode-toggler/div/button[2]"))))
        #         applychangebutton.click()
        #         break
        #     except:
        #         time.sleep(1)
        # time.sleep(2)
        while (True):   #To get the Save Button
            try:
                button3 = wait.until(EC.element_to_be_clickable((By.ID, "button-success-split")))
                button3.click()
                break
            except:
                time.sleep(1)
        #print ("Chegou 1.5")
        time.sleep(2)
        #print("Chegou 2")
        while (True):   #To get the Skip Button
            try:
                skipbutton = wait.until (EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/div/div/div[3]/button"))))
                skipbutton.click()
                break
            except:
                time.sleep(1)
        time.sleep(20)
        new_quotenumber = wait.until(EC.visibility_of_element_located((By.ID, "quoteNumber")))
        time.sleep(1)
        new_quotenumberversion = driver.find_element_by_id("quoteDetail_versionToggle")
        quoteNumberWithVersion = new_quotenumber.text+"."+str(new_quotenumberversion.text.split()[1])
        
        new_totalSellingPrice = driver.find_element_by_id("quoteDetail_summary_sellingPrice")
        print("Finished - "+quoteNumberWithVersion+"  Price = " + new_totalSellingPrice.text)
    except:
        print("Error getting quote #" +quote.strip('\n'))
driver.close()