import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://shop.whiskybase.com/us/whisky/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
t={}
data=[]
c=0
for x in range(1,6):
    k = requests.get('https://shop.whiskybase.com/us/whisky/'.format(x)).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("div",{"class":"col-sm-4 col-xs-6 col-xxs-12 rowmargin"})


    for product in productlist:
        link = product.find("a").get('href')
        productlinks.append(link)


for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun=BeautifulSoup(f,'html.parser')

    try:
        price=hun.find("span",{"class":"price highlight-txt"}).text.replace('\n',"")
    except:
        price = None

    try:
        about=hun.find("div",{"class":"product-description"}).text.replace('\n',"")
    except:
        about=None

    try:
        rating = hun.find("dd",{"data-bottle-key":"rating"}).text.replace('\n',"")
    except:
        rating=None

    try:
        name=hun.find("h1").text.replace('\n',"")
    except:
        name=None

    whisky = {"name":name,"price":price,"rating":rating,"about":about}

    data.append(whisky)
    c=c+1
    print("completed",c)

df = pd.DataFrame(data)
df.to_csv('test.csv')
print(df)