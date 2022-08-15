# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import requests
import selenium


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# set up html parser and parent element
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Featured Images -JPL space image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# Convert to html to put into a website
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

browser = init_browser()
url = 'https://marshemispheres.com/'
browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.

# 3b. Set up the soup object
html = browser.html
hemi_soup = soup(html, 'html.parser')

# 3b. Find (almost) all h3 tags
main = hemi_soup.find_all('h3')[0:4]

# 3d.  Iterate over the h3 tags in the soup object and pull out the titles and image links
for hemi in main:
    hemispheres = {}
    
    # Click on the link for each hemishphere
    page = browser.find_by_text(hemi.text)
    page.click()
    
    # Create a soup object for the new page
    html = browser.html
    new_soup = soup(html, 'html.parser')
    
    # Find the Div with class downloads
    section = new_soup.find('div', class_='downloads')
    
    # Find and pull the image and create a full URL for it
    img_section = section.find('a', target='_blank')
    href = img_section['href']
    img_url = f'https://marshemispheres.com/{href}'
    
    # Find and pull the title
    pretitle = new_soup.find('div', class_='cover')
    title = pretitle.find('h2').get_text()
    
    # Add the img and url to the dictionary
    hemispheres['URL'] = img_url
    hemispheres['Title'] = title
    
    # Append the dict to the list
    hemisphere_image_urls.append(hemispheres)
    
    # Go back to the original page
    browser.back()



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


browser.quit()



