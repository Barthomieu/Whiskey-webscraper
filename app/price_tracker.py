from db_connection import conn
from  requests import get
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
base_url = "https://www.whiskybase.com/market/whisky/"

id_list = []
with conn.cursor() as cursor:
    cursor.execute(f'''SELECT product_id FROM Whiskey_data''')
    for row in cursor:
        for field in row:
            id_list.append(field)




for id in id_list:
    r = get(base_url+str(id), headers=headers).text
    page_html = BeautifulSoup(r, "html.parser")
    #tutaj wycjagnąc wszystkie dane łącznie z data i zapisac do nowej tabeli w bazie razem z id produktu


    print(page_html)
