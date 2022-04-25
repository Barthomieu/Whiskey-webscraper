from db_connection import conn
from  requests import get
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
base_url = "https://www.whiskybase.com/market/whisky/"

update_list = []
with conn.cursor() as cursor:
    cursor.execute(f'''SELECT product_id FROM Whiskey_data where update_data is null OR update_data = 0''') # pobieram id rekordów bez kompletnych danych
    for row in cursor:
        for field in row:
            update_list.append(field)


print(update_list)


for bottle_id in update_list:
    r = get(base_url + str(bottle_id), headers=headers).text
    page_html = BeautifulSoup(r, "html.parser")

    #rating
    try:
        rating_all = page_html.find("dl", {"class": "dl-horizontal"}).text.replace('\t', "").replace('\n', "")
        rating = rating_all[7:13]
    except:
        rating = None
    print(rating)

    table = page_html.find("table", attrs={"class":"datalist mp-whisky"})
    if table != None:
        df = pd.read_html(str(table))[0]
        #kategoria
        try:
            category = df[df[0] == "Category"][1].values[0]
        except:
            category = None

        print(category)
        # butelkowane
        try:
            bottled = df[df[0] == "Bottled"][1].values[0]
        except:
            bottled = None
            # kraj dostawy
        print(bottled)
        try:
            ships_from = df[df[0] == "Ships fromd"][1].values[0]
        except:
            ships_from = None
        print(ships_from)

        with conn.cursor() as cursor:
            cursor.execute(f'''UPDATE  Whiskey_data 
                            SET category = '{category}',
                                bottled = '{bottled}',
                                rating = '{rating}',
                                ships_from = '{ships_from}',
                                update_data = 1                        
                            WHERE product_id = {bottle_id}''')

    else:
        print("brak danych")



