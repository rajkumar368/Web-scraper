import requests
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger=logging.getLogger()


loop_counter = 0
url = os.environ.get('SCRAPER3_URL', None)
loop_exit = True if not url else False


while loop_exit == False:
    try:
        response = requests.get(url) 
        soups = BeautifulSoup(response.content,"html.parser")
        soup = soups.find_all("div", attrs={"class" : "pool-card"})
        data_list = []

        for data in soup:
            loop_exit = True
            name = data.get('data-pool-title', None)
            daily = f"{round(float(data.get('data-daily', 0)),2)}%"
            yearly = f"{round(float(data.get('data-apy', 0)),2)}%"
            TVL = f"{round(float(data.get('data-tvl', 0)),2)}$"
            data_list.append({'Name': name, 'Daily': daily, 'Yearly': yearly, 'TVL': TVL })
        
        if not data_list:
            loop_counter+=1
            logger.error("Data not found, might be issue with script  \n")
        print(data_list)

        if loop_counter == 10:
            loop_exit = True
            logger.error("Too many tries, issues with server? \n")

    except Exception as e:
        loop_counter+=1
        logger.error("Exception occurred, issue with script \n", exc_info=True)        
