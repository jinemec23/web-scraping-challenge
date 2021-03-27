#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import re
import json


# ## NASA Mars News 
# * Scrape the NASA [Mars News Site]('https://mars.nasa.gov/news/') and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[2]:


url = 'https://mars.nasa.gov/news/'


# In[3]:


response = requests.get(url)


# In[4]:


soup = bs(response.text, 'html.parser')


# In[5]:


print(soup.prettify())


# In[6]:


news_title = soup.find('div', class_='content_title').find('a').text
news_p = soup.find('div', class_='rollover_description_inner').text
print(f'Title:{news_title}')
print(f'Paragraph Text: {news_p}')


# ## JPL Mars Space Images - Featured Image
# * Visit the url for JPL Featured Space Image [here]('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html').
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# * Make sure to find the image url to the full size .jpg image.
# * Make sure to save a complete url string for this image.

# In[7]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(image_url)
image_html = browser.html
image_soup = bs(image_html, 'html.parser')
images = image_soup.find(class_="headerimage fade-in")


# In[9]:


images.attrs


# In[10]:


image_string = images['src']
image_string


# In[11]:


image_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
featured_image_url = image_base_url + image_string
print(featured_image_url)


# ## Mars Facts
# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# * Use Pandas to convert the data to a HTML table string.

# In[12]:


facts_url = 'https://space-facts.com/mars/'
facts_table= pd.read_html(facts_url)
facts_table


# In[13]:


mars_table = facts_table[0]
mars_table.columns = ['Description','Value']
mars_table.set_index('Description',inplace=True)
mars_table


# In[14]:


marstable_html = mars_table.to_html()
marstable_html


# In[15]:


marstable_html.replace('\n','')
print(marstable_html)


# ## Mars Hemispheres
# * Visit the USGS Astrogeology site [here]('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars') to obtain high resolution images for each of Mar's hemispheres.
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[16]:


mars_hemisphere_html = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hemisphere_html)
hemisphere_html = browser.html
hemisphere_bs = bs(hemisphere_html,'html.parser')


# In[17]:


hemisphere_img_links = hemisphere_bs.find_all('img', class_='thumb')
hemisphere_img_links[0].attrs


# In[18]:


hemisphere_image_urls = []

for each_link in hemisphere_img_links:
    title = each_link.attrs['alt']
    img_src = each_link.attrs['src']
    hemi_base = 'https://astrogeology.usgs.gov'
    img_url = hemi_base + img_src
    hemisphere_image_urls.append({'title': title, 'img_url': img_url, 'img_src': img_src})

hemisphere_image_urls 


# In[19]:


browser.quit()


# In[ ]:




