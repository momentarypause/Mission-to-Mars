#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    

    # Set news and paragraph variables
    news_title, news_paragraph = mars_news(browser)


    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }


    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # SCRAPEMARS NEWS
    # Visit the Mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # set up html parser and parent element
    html = browser.html
    news_soup = soup(html, 'html.parser')


    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    return news_title, news_p


# ## Featured Images -JPL Space Image

def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
            return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url




def mars_facts():

    # try:

    # Use read_html to scrape facts table into a df
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    # except BaseException:
        # return None


    # Assign columns and set index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)


    # Convert to html to put into a website
    return df.to_html(classes="table table-striped")




def mars_hemispheres(browser):

    def init_browser():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        return Browser('chrome', **executable_path, headless=False)
    
    browser = init_browser()
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    hemisphere_image_urls = []

    # Set up the soup object
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Find (almost) all h3 tags
    main = hemi_soup.find_all('h3')[0:4]

    # Iterate over the h3 tags in the soup object and pull out the titles and image links
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


    return hemisphere_image_urls



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

