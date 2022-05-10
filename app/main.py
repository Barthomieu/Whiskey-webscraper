import os

from flask import Flask, request,render_template

from app.scrappers.link_scrapper import link_scraper
from app.scrappers.price_tracker import price_tracker
from app.db_manager.db_connection import conn
from flask_assets import Environment, Bundle
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


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


scheduler = BackgroundScheduler()
scheduler.add_job(func=price_tracker, trigger="interval", hours=1)
scheduler.add_job(func=link_scraper, trigger="interval", days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
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
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ ==  '__main__':
    app.run(debug=True)