from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import re


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    facts_url = 'https://space-facts.com/mars/'
    mars_hemisphere_html = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    mars_data = {}

    browser.visit(url)
    
    browser.is_element_present_by_value('article_teaser_body', wait_time=5)

    news_html = browser.html
    soup = bs(news_html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    mars_data['news_title']= news_title
    mars_data['news_p']= news_p

    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    images = image_soup.find(class_="headerimage fade-in")
    image_string = images['src']
    image_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    featured_image_url = image_base_url + image_string
    mars_data['featured_image_url'] = featured_image_url

    
    facts_table= pd.read_html(facts_url)
    mars_table = facts_table[0]
    mars_table.columns = ['Description','Value']
    mars_table.set_index('Description',inplace=True)
    marstable_html = mars_table.to_html()

    mars_data['facts']= marstable_html

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
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    mars_data['hemi']= hemisphere_image_urls

    browser.quit()
    return mars_data



