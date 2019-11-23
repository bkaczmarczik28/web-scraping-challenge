#!/usr/bin/env python
# coding: utf-8

# # Scrape NASA Mars Site - Collect Latest News Title and Paragraph text

#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.


#import dependcies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pymongo
import time

def scrape_mars():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #url for NASA site:
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #allow page to load in chrome
    time.sleep(1)

    # Retrieve page with the requests module
    # HTML object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    #desired text is in a <div class="content_title">
    #pull the latest title of an article
    latest_title = soup.find('div', class_='content_title').text
    print(latest_title)

    #pull the latest paragraph of an article
    latest_paragraph = soup.find('div', class_="article_teaser_body").text
    print(latest_paragraph)


    # # JPL Mars Space Images - Featured Image


    #use splinter to pull html off webpage with featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #allow page to load in chrome
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #url for featured image is in <article> tag
    featured_img_url = soup.find('article', class_='carousel_item')['style']
    #featured_img_url=featured_img_url.find({"style" : "background-image url"})
    #split the splintered text to extract just the url for the jpg
    featured_img_url=featured_img_url.split("url('")
    featured_img_url=featured_img_url[1]
    featured_img_url=featured_img_url.split("')")
    featured_img_url=featured_img_url[0]
    #create the final url
    featured_img_url="https://www.jpl.nasa.gov{0}".format(featured_img_url)
    print(featured_img_url)


    # # Mars Weather

    #use splinter to pull html off webpage with featured image
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #allow page to load in chrome
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    text = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    #cut out unnecessary part of text from find
    text=text.split('pic.')
    mars_weather=text[0]
    print(mars_weather)


    # # Mars Facts

    #import pandas dependencies
    import pandas as pd


    #create empty lists to store Mars facts
    header_list=[]
    facts_list=[]


    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    #allow page to load in chrome
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #extract table of facts on page
    facts_table = soup.find('tbody')

    #from tbody, extract all tr rows in the table
    keys=facts_table.find_all('td', class_='column-1')

    facts=facts_table.find_all('td', class_='column-2')

    #loop through each list to extract only the facts in text
    fact_list=[]

    for fact in facts:
        item=fact.text.strip()
        fact_list.append(item)


    #loop through each list to extract only the text for the table keys
    key_list=[]

    for key in keys:
        item=key.text.strip()
        key_list.append(item)

    #put the two lists into a dataframe
    data=zip(key_list, fact_list)
    mars_facts_df=pd.DataFrame(data, columns=['Key', 'Fact'])
    mars_facts_df.head()

    #convert to html table string
    mars_facts_html=mars_facts_df.to_html(header=False, index=False)

    # # Mars Hemispheres
    url = 'https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #allow page to load in chrome
    time.sleep(1)

    #through the <a> tag, will reach the <h3> tag 
    atags=browser.find_by_css("a.product-item h3")

    #create empty list for img urls
    hemisphere_list=[]

    for i in range(len(atags)):
        #create an empty dictionary for each picture url hemisphere
        hemisphere={}
        
        #click on the link to reach the full-resolution picture
        browser.find_by_css("a.product-item h3")[i].click()

        #allow page to load in chrome
        time.sleep(1)
        
        #each full-resolution picture is tied to a "Sample" text. Use to capture link
        item=browser.find_link_by_text('Sample').first
        
        #save with a img_url key
        hemisphere['img_url']=item['href']
        
        #store the title of the hemisphere picture. Tied to h2 tag, class='title'
        hemisphere['title']=browser.find_by_css('h2.title').text
        
        #add iteration to the list
        hemisphere_list.append(hemisphere)
        
        #back out of the page 
        browser.back()

    print(hemisphere_list)

    # Close the browser after scraping
    browser.quit()

    mars_dictionary={}
    mars_dictionary['latest_news_title']=latest_title
    mars_dictionary['latest_news_paragraph']=latest_paragraph
    mars_dictionary['featured_image_url']=featured_img_url
    mars_dictionary['mars_weather']=mars_weather
    mars_dictionary['mars_facts']=mars_facts_html
    mars_dictionary['hemispheres']=hemisphere_list

    return mars_dictionary
    
