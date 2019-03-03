# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time


# Choose the executable path to driver 

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Defining scrape & dictionary
def scrape():
    final_data = {}
    news_data = marsNews()
    final_data["mars_news"] = news_data[0]
    final_data["mars_paragraph"] = news_data[1]
    final_data["mars_image"] = marsUrl()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHemisphere()

    return final_data
    
# ### NASA Mars News
def marsNews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    news_data = [news_title,news_p]
    return news_data
    


# ### JPL Mars Space Images - Featured Image

def marsUrl():
    browser = init_browser()
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    html_img = browser.html
    soup = BeautifulSoup(html_img, 'html.parser')
    base_img_url = soup.find('article', class_='carousel_item')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_img_url = f'https://www.jpl.nasa.gov{base_img_url}'
    
    return featured_img_url


# ### Mars Weather

def marsWeather():
    browser = init_browser()
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass
    
    
    return weather_tweet
    # browser.quit()


# ### Mars Facts

def marsFacts():
    browser = init_browser()
    mf_url = 'http://space-facts.com/mars/'
    browser.visit(mf_url)
    time.sleep(10)
    table = pd.read_html(mf_url)
    mars_df = table[0]
    mars_df.columns = ['Fact','Value']
    mars_df.set_index('Fact', inplace=True)
    mars_facts = mars_df.to_html(index = True, header =True)

    # browser.quit()
    return mars_facts
    

# ### Mars Hemispheres

def marsHemisphere():
    browser = init_browser()
    site = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(site)
    html_hemi = browser.html
    soup = BeautifulSoup(html_hemi, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    browser.quit()
    
    return mars_hemisphere