from  requests import get
from bs4 import BeautifulSoup
from app.db_manager.db_connection import conn
#url = "https://www.whiskybase.com/market/browse?take=500&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page=1"
from app.scrappers.update_whiskey_data import update_whiskey_data


def link_scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    n_pages = 0
    cursor = conn.cursor()

    for page in range(0,15):

        n_pages += 1

        url = "https://www.whiskybase.com/market/browse?take=500&search=&price%5B%5D=-1&fillinglevel_id%5B%5D=&sort=added&direction=desc&page="+str(n_pages)
        r = get(url, headers=headers).text
        page_html = BeautifulSoup(r, "html.parser")

        firstrow_containers = page_html.find_all('tr', class_="mp-whisky-item mp-whisky-item-firstrow")


        if firstrow_containers  != []:

            # getting data from table first row
            for container in firstrow_containers:
                #Names
                try:
                    name = container.find("a", {"class": "mp-whisky-item-name"}).text.replace('\t', "").replace('\n', "").replace("'", "")
                except:
                    name = None

                #Links
                try:
                    link = container.find("a").get('href')
                    id = link[41:]
                except:
                    link = None

                if link != None:
                   #print(f"dodaje do bazy:  {int(id)}, '{name}', '{link}')")
                    with conn.cursor() as cursor:
                        cursor.execute(f'''IF EXISTS ( SELECT * FROM Whiskey_data WHERE product_id = {int(id)} )
                                    BEGIN
                                    Print'istnieje'    
                                    END
                                    ELSE 
                                    BEGIN
                                    INSERT INTO Whiskey_data(product_id, product_name, store_link,update_data   )
                                     VALUES({int(id)}, '{name}', '{link}', 0)
                                    END''')

        else:
            break

        update_whiskey_data()
        #print(f"pobrano ze strony: {n_pages}")

