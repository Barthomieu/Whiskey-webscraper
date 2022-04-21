import os

from flask import Flask, request,render_template

from app.db_connection import conn
from flask_assets import Environment, Bundle


cursor =conn.cursor()
app = Flask(__name__)

assets = Environment(app)

assets.load_path = [os.path.join(os.path.dirname(__file__), 'static'),]

# Preprocess scss and bundle CSS

css = Bundle(
  # Paths to CSS dependencies you don't want to run through scss go here
  Bundle(
    'css/styles.scss',
    filters = 'pyscss',
    depends = ('**/*.scss', '**/**/*.scss'),
  ),
  output = 'dist/app.css'
)

assets.register('app-css', css)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM Whiskey_data")
    data = cursor.fetchall()
    return render_template('index.html', data=data)
@app.route('/mainpage')
def v_timestamp():
    cursor.execute("SELECT * FROM Whiskey_data")
    data = cursor.fetchall()
    return render_template('mainpage.html', data=data)

if __name__ ==  '__main__':
    app.run()