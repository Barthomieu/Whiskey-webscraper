import pyodbc
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:infserver.database.windows.net,1433;Database=whiskeytracker;Uid=Flachowcy22;Pwd=Bylezdac22.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


#cursor = conn.cursor()
#cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
#with conn.cursor() as cursor:
   # cursor.execute("SELECT * FROM Whiskey_data")




#cnxn.commit()