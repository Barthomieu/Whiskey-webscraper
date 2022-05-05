import os

from flask import Flask, request,render_template

from scrappers.db_connection import conn
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
    cursor.execute(f"""SELECT	product_name
		,(select top 1 Price where Id = product_id order by Data desc)
		-- TODO dodać obliczanie zmienności ceny
		,store_link
		,D.category
		,bottled 
		,rating
		,ships_from

	FROM Whiskey_data D
	JOIN Whiskey_price P on D.product_id=P.ID""")
    data = cursor.fetchall()
    return render_template('index.html', data=data)
@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

if __name__ ==  '__main__':
    app.run()