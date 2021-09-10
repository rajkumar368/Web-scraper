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
logger.setLevel(logging.DEBUG)

loop_counter = 0
url = os.environ.get('SCRAPER1_URL', None)
loop_exit = True if not url else False

while loop_exit == False:
    try:
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
        browser.get(url) 
        time.sleep(13) 
        loop_counter+=1

        res = browser.page_source
        soups = BeautifulSoup(res,"html.parser")
        data_list = []

        name = soups.find_all("span", attrs={"class":"css-1bb389o eg253nq2"})
        if not name:
            logger.error("Data not loaded properly, please run script again \n")
        else:
            loop_exit = True
            price = soups.find_all("div", attrs={"class":"css-1oun8zc eg253nq9"})
            percent = soups.find_all("div", attrs={"class":"css-10o2cbe eg253nq9"})

            for data in  zip(name, price, percent):
                data_list.append({"name":data[0].text, "price": data[1].text, "percent": data[2].text })
        print(data_list)

        if loop_counter == 10:
            loop_exit = True
            logger.error("Too many tries, issues with server? \n")

    except Exception as e:
        logger.error("Exception occurred, issue with script \n", exc_info=True)

    browser.close()
