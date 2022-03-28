import pyodbc
cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:infserver.database.windows.net,1433;Database=whiskeytracker;Uid=Flachowcy22;Pwd={Bylezdac22.};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


cursor = cnxn.cursor()
cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
print("Finished creating table")