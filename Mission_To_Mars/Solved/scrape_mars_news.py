from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import time 


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #01 
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    #soup = BeautifulSoup(response.text, 'html.parser')
    
    results = soup.find_all('div', class_='list_text')[0]
    news_title = results.find('div', class_='content_title').text
    news_p = results.find('div', class_='article_teaser_body').text
    news_date = results.find('div', class_='list_date').text
    
    # news_date = soup.find_all('div', class_='list_date').text
    
    
    
    
    #02
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    # browser.links.find_by_partial_text("FULL IMAGE").click()
    html = browser.html
    soup = bs(html, "html.parser")
    #soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(1)
    # featured_image = soup.find('img', class_= "headerimage fade-in" )["src"]
    # featured_image = url + featured_image
    # featured_image = soup.find('img', class_='fancybox-image')['src']
    # featured_image = url + featured_image
    featured_image = soup.find('img', class_= "headerimage fade-in" )
    featured_img = url + str(featured_image['src'])
  
    #03
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    # read_mars = pd.read_html(url)[0]
    read_table = pd.read_html(url)
    #convert data to a html table string 

    table_df= read_table[0]
    mars_facts = table_df.to_html()
    


    url = "https://marshemispheres.com/"

    hemisphere_image_urls = []

    #using splinter documentation "Clicking Links" under "interacting with elements on a page"

    #go to the url 
    browser.visit(url)
    time.sleep(1)
    
    #collect the first image 
    for i in range(4): 
        time.sleep(1)
        print(i)
        browser.links.find_by_partial_text('Hemisphere')[i].click()
        
        html = browser.html
        soup = bs(html, 'html.parser')

        drill_url = soup.find('img', class_="wide-image")['src']
       
        drill_title = soup.find('h2', class_='title').get_text()
 
        dict = {"title": drill_title , "img_url" : drill_url}

        hemisphere_image_urls.append(dict)
       
        print(hemisphere_image_urls)

        browser.back()
 

    scraped_data = {
        "Headline": news_title,
        "Summary": news_p,
        "Feautured_Mars_Image": featured_img,
        "Mars_Data":  mars_facts,
        "Mars Date": news_date, 
        "hemisphere_image_1": hemisphere_image_urls[0]["img_url"],
        "hemisphere_image_2": hemisphere_image_urls[1]["img_url"],
        "hemisphere_image_3": hemisphere_image_urls[2]["img_url"],
        "hemisphere_image_4": hemisphere_image_urls[3]["img_url"],
        "image_1_title": hemisphere_image_urls[0]["title"],
        "image_2_title": hemisphere_image_urls[1]["title"],
        "image_3_title": hemisphere_image_urls[2]["title"],
        "image_4_title": hemisphere_image_urls[3]["title"]
    }

    browser.quit() 
    return scraped_data

   
