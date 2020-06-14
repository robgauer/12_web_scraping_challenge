from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
#mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    #mars_data = mongo.db.mars_data.find_one()
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_db=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_db = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    #mongo.db.mars_data.update({}, mars_data, upsert=True)
    mongo.db.mars_data.update({}, mars_db, upsert=True)
    return 'Mars Data Update Complete!'

if __name__ == "__main__":
    app.run(debug=True)