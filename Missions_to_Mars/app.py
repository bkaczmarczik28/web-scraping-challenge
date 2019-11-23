from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of our Flask app.
app = Flask(__name__)

#create connection and create mongo database called mars_app using PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars=mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    #create collection 
    mars = mongo.db.mars

    #scrape data from the scrape_mars.py
    mars_data = scrape_mars.scrape_mars()

    #add scraped data to collection
    mars.update({}, mars_data, upsert=True)

    print("Scrapped Mars Data successfully")

    #redirect to main page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
