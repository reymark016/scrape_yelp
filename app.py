from flask import Flask
from yelp_scraper import Scrape

app = Flask(__name__)


@app.route('/')
def hello_world():
    return Scrape.scrape_yelp("")
