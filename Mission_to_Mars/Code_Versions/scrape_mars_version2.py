# Mission to Mars
#
## File Information and Author
#### File Name:  scrape_mars.py
#### Derived from Pandas file:  mission_to_mars.ipynb
#### Date Due:  Saturday June 13, 2020
#### Author:  Rob Gauer


### Setup and Dependencies
#--------------------
import pandas as pd
import os
import requests as req
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

### Initialization and Setup
#--------------------
def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    #return Browser("chrome", **executable_path, headless=False)
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

### Define code for Scrape
#--------------------
# Scrape and Initialize Browser
def scrape():
    browser = init_browser()

    
    ### NASA Mars News 
    #--------------------
    # Visit url for NASA Mars News -- Latest News
    nasa_news_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_news_url)
    time.sleep(5)
    nasa_news_html = browser.html

    # Parse HTML with Beautiful Soup  
    nasa_news_soup = bs(nasa_news_html, "html.parser")

    # Get article title and paragraph text
    article = nasa_news_soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text


    ### JPL Mars Space Featured Image
    #--------------------
    # Visit url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(3)
    
    # Go to 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')
    
    # Go to 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    jpl_image_html = browser.html
    jpl_image_soup = bs(jpl_image_html, "html.parser")

    # Get featured image
    featured_image_url = jpl_image_soup.find('figure', class_='lede').a['href']
    featured_jpl_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    
    ### Mars Weather
    #--------------------
    # Visit Twitter url for latest Mars Weather
    mars_weather_tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_tweet_url)
    mars_weather_html = browser.html

    # Parse HTML with Beautiful Soup
    mars_weather_soup = bs(mars_weather_html, 'html.parser')

    # Extract latest tweet
    tweet_container = mars_weather_soup.find_all('div', class_="js-tweet-text-container")

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            #print(mars_weather)
            #print(tweet)
            break
        else: 
            pass
    
    
    ### Mars Facts
    #--------------------
    # Visit Mars Facts webpage for interesting facts about Mars
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(3)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    table = pd.read_html(facts_url)
    mars_facts = table[0]

    # Rename columns
    mars_facts.columns = ['Description','Value']

    # Reset Index to be description
    mars_facts = mars_facts.set_index('Description')

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_facts.to_html(classes="table table-striped")

    
    ### Mars Hemispheres
    #--------------------
    # Scrape images of Mars' hemispheres from the Astrogeology USGS.gov
    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(5)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    
    ### Store Data
    #--------------------
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url":featured_image_url,
        "featured_jpl_image_url": featured_jpl_image_url,
        "mars_weather_tweet_url": mars_weather_tweet_url,
        #"mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    ### Finish Tasks
    #--------------------
    # Close the browser after scraping
    browser.quit()


    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()