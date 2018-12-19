from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    #get latest news title and paragraph 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    listings["news_title"] = soup.find('div', class_='content_title').get_text()
    listings["news_p"] = soup.find('div', class_='article_teaser_body').get_text()

    #get mars featured image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    listings["featured_image_url"] = "https://www.jpl.nasa.gov"+str(soup.find('article',class_='carousel_item')['style'].split('\'')[1])

    #get mars weather
    url3="https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html = browser.html
    soup = bs(html, 'html.parser')
    listings["mars_weather"] = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
 
    #create mars table
    url4="https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Description', 'Data']
    df=df.set_index("Description")
    df = df.to_html(classes='df')
    df =df.replace('\n', ' ')
    # Add the Mars facts table to the dictionary
    listings["table"]=df
   
    #get mars hemispheres
    
    url5="https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    response = requests.get(url5)
    soup = bs(response.text, 'lxml') 
    hemisphere_image_urls = []
    Cerberus_title=soup.find('h2',class_="title").text
    Cerberus_img="https://astrogeology.usgs.gov"+str(soup.find('img',class_="wide-image")['src'])
    listings["Cerberus_img"]=Cerberus_img
    listings["Cerberus_title"]=Cerberus_title

    url6="https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    response = requests.get(url6)
    soup = bs(response.text, 'lxml') 
    Schiaparelli_title=soup.find('h2',class_="title").text
    Schiaparelli_img="https://astrogeology.usgs.gov"+str(soup.find('img',class_="wide-image")['src'])
    listings["Schiaparelli_img"]=Schiaparelli_img
    listings["Schiaparelli_title"]=Schiaparelli_title

    url7="https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    response = requests.get(url7)
    soup = bs(response.text, 'lxml') 
    Syrtis_title=soup.find('h2',class_="title").text
    Syrtis_img="https://astrogeology.usgs.gov"+str(soup.find('img',class_="wide-image")['src'])
    listings["Syrtis_img"]=Syrtis_img
    listings["Syrtis_title"]=Syrtis_title

    url8="https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    response = requests.get(url8)
    soup = bs(response.text, 'lxml') 
    valles_title=soup.find('h2',class_="title").text
    valles_img="https://astrogeology.usgs.gov"+str(soup.find('img',class_="wide-image")['src'])
    listings["valles_img"]=valles_img
    listings["valles_title"]=valles_title

    listings["mars_hemispheres"]=hemisphere_image_urls
    
    return listings
