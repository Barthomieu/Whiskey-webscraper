import datetime

from app.db_manager.db_connection import conn
from  requests import get
from bs4 import BeautifulSoup

def price_tracker():
    #print("scraper uruchomiony")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    base_url = "https://www.whiskybase.com/market/whisky/"

    id_list = []
    with conn.cursor() as cursor:
        cursor.execute(f'''SELECT product_id FROM Whiskey_data''')
        for row in cursor:
            for field in row:
                id_list.append(field)

    id_cena = []
    with conn.cursor() as cursor:
        cursor.execute(f'''SELECT ID,Price FROM Whiskey_price''')
        for row in cursor:
            for field in row:
                id_cena.append(field)
    #print(id_cena)


    #for id in id_cena:
        #if id_list.__contains__(id[0]):
            #id_list.remove(id[0])


    for id in id_list:
        r = get(base_url+str(id), headers=headers).text
        page_html = BeautifulSoup(r, "html.parser")
        #tutaj wycjagnąc wszystkie dane łącznie z data i zapisac do nowej tabeli w bazie razem z id produktu
        # Ceny
        try:
            price = page_html.find("div", {"id": "mp-whisky-price"},"span").text.replace('\t', "").replace('\n', "").replace("USD$", "").replace("€", "").replace(" ","").replace("£", "").replace("CHF","")
            if(len(price)>15):
                price = page_html.find("span", {"id": "mp-whisky-price-str"}).text.replace('\t', "").replace('\n',"").replace("USD$", "").replace("€", "").replace(" ", "").replace("£", "").replace("CHF","")
        except:
            price = None
        if(price == None):
            try:
                price = page_html.find("div", {"class": "mp-whisky-item-price"},"span").text.replace('\t', "").replace('\n', "").replace("USD$", "").replace("€", "").replace(" ","").replace("£", "").replace("CHF","")
            except:
                price = None

        # Data
        data = datetime.datetime.now().today()

        if(price != None):
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f'''IF EXISTS
                    (
                    SELECT *
                    FROM Whiskey_price
                    WHERE ID = {id} AND Price = {price}) 
                    Begin
                    Print'istnieje'    
                    END
                    ELSE 
                    BEGIN
                    INSERT INTO Whiskey_price VALUES({int(id)}, {price}, '{data}')
                    END''')
            except:
                pass

    #print("Zaktualizowany ceny")



        #print(page_html)

