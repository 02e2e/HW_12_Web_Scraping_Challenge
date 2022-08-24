from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_news

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
#scrape runs once the button is pressed
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_find = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_find)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    #use the same dictionary name from scrape_mars_news
    mars_data = scrape_mars_news.scrape_info()

    # Insert the record
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
