import re
from bs4 import BeautifulSoup
import whois
import requests
import json
import re



class ProductsScraper():

    def __init__(self):
        self.headers ={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
            37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        self.cookie = {
            "version":0,
            "name":'COOKIE_NAME',
            "value":'true',
            "port":None,
            "domain":'www.mydomain.com',
            "path":'/',
            "secure":False,
            "expires":None,
            "discard":True,
            "comment":None,
            "comment_url":None,
            "rest":{},
            "rfc2109":False
            }

    def constructLinkAmazon(self, searchterm):
        searchitem_parsed = ("+").join(searchterm.split("."))
        return f"https://www.amazon.es/s?k={searchitem_parsed}"

    def constructLinkECI(self, searchterm):
        searchitem_parsed = ("%20").join(searchterm.split("."))
        return f"https://www.elcorteingles.es/search/?s={searchitem_parsed}"

    def scrappingProduct(self, prodlink):
        session = requests.Session()
        session.cookies.set(**self.cookie)

        page = session.get(prodlink, headers=self.headers)
        #if page.status_code == 200:
        soup = BeautifulSoup(page.content, features="html.parser")
        #prod_data = soup.find_all('div', attrs={"class": 's-card-container'})


        #for pd in prod_data:

        price_discount = soup.find('span', attrs={"class": 'a-price', "data-a-strike": "true"})
        product_name = soup.find('span', attrs={"id": 'productTitle'})
        #rating_whole = soup.find('i', attrs={"class": 'a-icon a-icon-star'})
        rating_whole = soup.find('span', attrs={"class": 'a-icon-alt'})
        n_comments = soup.find('span', attrs={"id": 'acrCustomerReviewText'})
        image = soup.find('img', attrs={"id": 'landingImage'})
        is_express = False


        # Treating prices
        price_num = None
        price_topay = None
        discount_percent = None
        currency = None

        for p in soup.select('span[class*="PriceToPay"]'):
            price_topay = p.find('span', attrs={"class": 'a-offscreen'}).string

        if price_topay:
            price_num = float(price_topay[:-1].replace(',', '.'))
            symbol = price_topay[-1]
            
            currency = "EUR" if u"\N{euro sign}" in symbol else "USD"
        
        if price_discount and price_num:
            price_disc_str = price_discount.find('span', attrs={"class": 'a-offscreen'}).string
            price_before_discount = float(price_disc_str[:-1].replace(',', '.'))
            discount_percent = round((price_before_discount - price_num) / price_before_discount *100, 0)
            
        # Treating is_express
        scripts = soup.find_all("script", attrs={"type": "text/javascript"})
        for s in scripts:
            if re.search(r"var bbopData", s.string): is_express = True


        # Treating rating
        rating = None
        if rating_whole:
            if 'de 5 estrellas' in rating_whole.string:
                rating_str = rating_whole.string.split('de')[0].replace(',', '.')
                rating = float(rating_str)
                
        print({
            "products": product_name.string.lstrip().rstrip() if product_name else "",
            "price": price_num if price_num else 0.0,
            "discount_percent": discount_percent,
            "rating": rating,
            "n_comments": int(("").join([s for s in n_comments.string.replace('.', '').split() if s.isdigit()])) if n_comments else 0,
            "image": image.get('src') if image else "",
            "currency": currency,
            "is_express": is_express
        })


        
    def scrappingProductsList(self, url):

        session = requests.Session()
        session.cookies.set(**self.cookie)


        #try:
        page = session.get(url, headers=self.headers)
        #if page.status_code == 200:
        soup = BeautifulSoup(page.content, features="html.parser")

        prod_data = soup.find_all('div', attrs={"class": 's-card-container'})
        
        json_l = []


        for pd in prod_data:

            prices = pd.find('span', attrs={"class": 'a-price-whole'})
            price_discount = pd.find("span", attrs={"class": "a-price a-text-price", "data-a-strike": "true"})
            products = pd.find('span', attrs={"class": 'a-size-base-plus a-color-base a-text-normal'})
            brand = pd.find('span', attrs={"class": "a-size-base-plus a-color-base"})
            rating = pd.find('span', attrs={"class": 'a-icon-alt'})
            n_comments = pd.find('span', attrs={"class": 'a-size-base s-underline-text'})
            image = pd.find('img', attrs={"class": 's-image'})


            # Treating prices
            price_num = None
            discount_percent = None

            if prices:
                maketrans = prices.string.maketrans
                price_num = float(prices.string.translate(maketrans(',.', '.,', ' ')).replace(',', ''))

            

        
            if price_discount and price_num:
                price_disc_str = price_discount.find('span', attrs={"class": 'a-offscreen'}).string
                price_before_discount = float(price_disc_str[:-1].replace(',', '.'))
                discount_percent = round((price_before_discount - price_num) / price_before_discount *100, 0)


            json_l.append({
                "product": products.string if products else None,
                "brand": brand.string if brand else None,
                "price": price_num,
                "discount_percent": discount_percent,
                "rating": float(rating.string.split('de')[0].replace(',', '.')) if rating and 'de 5 estrellas' in rating.string else None,
                "n_comments": int(n_comments.string.replace('.', '')) if n_comments else 0,
                "image": image.get('src') if image else None
            })

        return json_l
            
