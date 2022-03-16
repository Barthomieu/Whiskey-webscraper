import requests
from  requests import get
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import pandas as pd

#url = "https://www.whiskybase.com/market/browse?take=500&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

n_pages = 0


with open("test.csv", "w",encoding="utf-8") as file:
    writer = csv.writer(file)

    for page in range(0,10):

        n_pages += 1
        url = "https://www.whiskybase.com/market/browse?take=100&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page="+str(n_pages)
        r = get(url, headers=headers).text
        page_html = BeautifulSoup(r, "html.parser")

        firstrow_containers = page_html.find_all('tr', class_="mp-whisky-item mp-whisky-item-firstrow")
        secondrow_containers = page_html.find_all('tr', class_="mp-whisky-item mp-whisky-item-secondrow")

        if firstrow_containers  != []:

            namelist = list()
            pricelist = list()
            ratinglist = list()
            linkslist = list()
            countrylist = list()
            # getting data from table first row
            for container in firstrow_containers:
                #Names
                try:
                    name = container.find("a", {"class": "mp-whisky-item-name"}).text.replace('\t', "").replace('\n', "")

                except:
                    name = None
                namelist.append(name)
                #Links
                try:
                    link = container.find("a").get('href')
                except:
                    link = None
                linkslist.append(link)


            # getting data from table econd row
            for container in secondrow_containers:
                #price
                try:
                    price = container.find("div", {"class": "mp-whisky-item-price"}).text.replace('\t', "").replace('\n', "")
                except:
                    price = None
                pricelist.append(price)
                #ratings and adding date
                try:
                    rating = container.find("dl", {"class": "dl-horizontal"}).text.replace('\t', "").replace('\n', "")
                except:
                    rating = None
                ratinglist.append(rating)

                #Countrydetails
                try:
                    country = container.find("span", {"class": "ships-from"}).text.replace('\t', "").replace('\n', "")
                except:
                    country = None
                countrylist.append(country)


        else:
            break

        #adding into csv file
        rows = zip(namelist, pricelist, ratinglist, countrylist,  linkslist)
        for row in rows:
            writer.writerow(row)
        print(f"pobrano ze strony: {n_pages}")







