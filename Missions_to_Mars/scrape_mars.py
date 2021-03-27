import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import re

mars_data = {}
# ## NASA Mars News 
# * Scrape the NASA [Mars News Site]('https://mars.nasa.gov/news/') and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    mars_data['news_title']=news_title
    mars_data['news_p']=news_p


# ## JPL Mars Space Images - Featured Image


    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    images = image_soup.find(class_="headerimage fade-in")
    image_string = images['src']
    image_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = image_base_url + image_string
    mars_data['featured_image_url']= featured_image_url


# ## Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table= pd.read_html(facts_url)
    mars_table = facts_table[0]
    mars_table.columns = ['Description','Value']
    mars_table.set_index('Description',inplace=True)
    marstable_html = mars_table.to_html()
    mars_data['marstable_html']=marstable_html


# ## Mars Hemispheres
    browser.visit(mars_hemisphere_html)
    hemisphere_html = browser.html
    hemisphere_bs = bs(hemisphere_html,'html.parser')

    hemisphere_img_links = hemisphere_bs.find_all('img', class_='thumb')
    hemisphere_image_urls = []

    for each_link in hemisphere_img_links:
        title = each_link.attrs['alt']
        img_src = each_link.attrs['src']
        hemi_base = 'https://astrogeology.usgs.gov'
        img_url = hemi_base + img_src
        hemisphere_image_urls.append({'title': title, 'img_url': img_url, 'img_src': img_src})

    mars_data['hemisphere_image_urls'] =  hemisphere_image_urls

    browser.quit()
    return mars_data






