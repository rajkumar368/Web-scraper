import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
import time
from selenium.webdriver.firefox.options import Options
import logging
import os

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger=logging.getLogger()

loop_counter = 0
url = os.environ.get('SCRAPER2_URL', '')
loop_exit = True if not url else False

while loop_exit == False:
    try:
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
        browser.get(url) 
        time.sleep(25) 
        res = browser.page_source
        soups = BeautifulSoup(res,"html.parser")
        data_list = []
        loop_counter+=1

        cards = soups.find_all("div", attrs={"class":"ant-row sc-cVAliH kBgXJj"})
        for card in cards:
            name = card.find(class_='sc-kHxSLA epBIqP').select_one("div p:nth-of-type(1)").text
            if name in [None, "\u200c", " "]:
                logger.error("Data not loaded properly, wait for next try. \n")
                break
            else:
                raw_data = card.find_all("div", attrs={"class":"ant-col ant-col-5"})
                APY = raw_data[0].find(class_='sc-gXRoDt iAvKeU').text
                TVL = raw_data[1].text
                Leverage = card.find(class_='ant-col ant-col-4').select_one('input').get('value')

                APY=None if APY=='\u200c' else APY
                TVL=None if TVL=='\u200c' else TVL
                data_list.append({'name': name, 'APY': APY, 'TVL': TVL, 'Leverage': Leverage})
                loop_exit=True

        if not data_list:
            logger.error("Data not found! \n")

        print(data_list)
        if loop_counter == 2:
            loop_exit = True
            logger.error("Too many tries, issues with server. \n")

    except Exception as e:
        logger.error("Exception occurred, issue with script. \n", exc_info=True)

    browser.close()
