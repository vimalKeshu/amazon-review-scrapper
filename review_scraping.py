from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

amazon_product = "https://www.amazon.in/product-reviews/{}?pageNumber={}"
product_code = "B01FM7GIR4"


def get_data(url):
    reviews=[]
    browser = webdriver.Chrome()
    try:            
        browser.get(url)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        divs = soup.find_all("div",attrs={"data-hook":"review"})        
        for div in divs:
            rating = ""
            review = ""    
            rating_div = div.div.find('span', class_ = 'a-icon-alt')
            if rating_div is not None:
                rating = rating_div.text
            review_body_div = div.div.find('span', attrs={"data-hook":"review-body"})
            if review_body_div is not None:
                review = review_body_div.text.encode("utf-8")
            reviews.append((rating,review))
    except Exception as ex:
        print(ex)        
    finally:
        browser.close()             
    return reviews

def get_total_pages(url):
    page_size = "10"
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        lis = soup.find_all("li",attrs={"data-reftag":"cm_cr_arp_d_paging_btm"})
        for li in lis:
            if li.a is not None:
                page_size = li.a.text
    except Exception as ex:
        print(ex)
    finally:
        browser.close()              
    return int(page_size)
   
pagination_start = 1
pagination_end = 10
pagination_end = get_total_pages(amazon_product.format(product_code,str(pagination_start)))

print("Total pages {}".format(pagination_end))

for i in range(pagination_start,pagination_end):
    url = amazon_product.format(product_code,str(i))
    reviews = get_data(url)
    print(url)
    print(reviews)
    print("-------------------------------------------------")
    