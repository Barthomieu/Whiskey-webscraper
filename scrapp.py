import requests
from  requests import get
from bs4 import BeautifulSoup
import pandas as pd

#url = "https://www.whiskybase.com/market/browse?take=500&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}




n_pages = 0

for page in range(0,5):
    Whiskey_list = list()
    n_pages += 1
    url = "https://www.whiskybase.com/market/browse?take=50&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page="+str(n_pages)
    r = get(url, headers=headers).text
    page_html = BeautifulSoup(r, "html.parser")
    Whiskey_containers = page_html.find_all('tr', class_="mp-whisky-item mp-whisky-item-firstrow")
    print(Whiskey_containers)
