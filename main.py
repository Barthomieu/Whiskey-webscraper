from flask import Flask, request,render_template

from app.db_connection import conn



cursor =conn.cursor()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/mainpage')
def v_timestamp():
    cursor.execute("SELECT * FROM Whiskey_data")
    data = cursor.fetchall()
    return render_template('mainpage.html', data=data)

if __name__ ==  '__main__':
    app.run()