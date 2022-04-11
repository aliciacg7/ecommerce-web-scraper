import re
from reprlib import recursive_repr
from bs4 import BeautifulSoup
import requests
import random
import json
import re
from time import sleep


class ProductsScraper():

    def __init__(self):
        self.headers ={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "*",
            "Cache-Control": "no-cache",
            "Cookie": "ocp=1; cookiesPolicy=11111; _gcl_au=1.1.425227982.1647185075; _fbp=fb.1.1647185076484.1085935914; _qubitTracker=04fgsk0qtj7-0l0pfgra8-i1y2gco; BVBRANDID=6da17aa1-8168-4e27-86ee-536fdf66afc2; qb_generic=:X+D4aEe:.elcorteingles.es; open_app=1; session_id=8f5ce7d5c52a665f49097ab46c256016482d506e00fc08aef1da11a475cbd019; _pin_unauth=dWlkPU5tVXpOemRoTnpJdFkyVmlZUzAwT1daaUxUZzBabUV0TXpBMk0yWTJZakJpTnpNMg; MADid=7f49ee90-2fa3-40e2-9016-74833aaa3958; tfc-l={\"a\":{\"v\":\"8d95a1fc-6260-4f27-9105-577cd9e77662\",\"e\":1647271709},\"k\":{\"v\":\"avv9f7hg0265n0uj5bhp93eduq\",\"e\":1710084510},\"c\":{\"v\":\"adult\",\"e\":1710084509}}; SSLB=1; popover_login=1; store=eciStore; centre=NULL; express=0; locale=es_ES; TLTSID=96622136634256064575185565822929; BVImplmain_site=4572; selectedSize=M; bm_sz=94AA65AA96404002915625F72BCAA35C~YAAQF7U+FxlY3Z9/AQAAb5OA8w9SLNcgI/VzvurNGk4yxD2aFiDowzfTdfWyE2aZeMIGO/f8slkqbJwC4MQli1QWxMATKsGiygSvlUvZ1CHkWQTdjyxNJFnL+yz+lqHo0kK5d78Cz5+XhJ/mJDjjoLO7lhg/nG6DI2zhKNjzIV+yFpM8Gv7lS90nAHsG6VydcAz9sMmn+rQS/TOH5r1DHeh8Z4Ztjnr2xnLR+I4z9cyJexE8uLxP5MkW9tPicjhtPVnHlrGr8R9xxafnKQYSKBwyz1HoPjzPkwt8a5mp5trfrr79XC3+7xU=~4605252~3617841; bm_mi=CD1BF6F1F9384A806093D8B0E7453ACF~LSymzMi4LF+Kq+TgUp5aVg+2XLnWnqvLtiHSkW+byeheFZOSVbPMnBF9OFD/7kSiMrw1Q4rVONvYC47eDdOoR42VrwrBMhEz6hqZewQwXnXKWxiT6LFSmEEL03y3ZbnWLPq4NZJNpnzeuvtbrpfR+4jfgqyxYy7aJhG6brEfZkDvzzUwtXWe+kk6DoEeBbpWUh3rObecIecLzznEmAtmEihR0BEnDgNA5g5GMFNDF02nWmYxAqdxIh0BVVJB8pUOITrBAqeLkZIpSrv8SD1r0w==; _gid=GA1.2.493578267.1649057769; _clck=1jdfpke|1|f0c|0; ak_bmsc=9DEA1AF8E0AF0A4183178853CD355B95~000000000000000000000000000000~YAAQF7U+FyVd3Z9/AQAA0dqA8w9vL6QDfM9k4pa59kW+wIrAQ5R6CnJ9gNw61OjUcY2L8Mz5t1w2BzkplAoreljhi7o5JbejLCPYeFu4SrPtLAdoicpQH1bjT+/qLuha8VB7GdJdGNuzcGdudpxg3nd0fjcA+LtUfceSQ6IqVs68pgzcR33XOoqz4RxR5Iv/xqed8mJ90DNYXEXgFg8Yq5C+Cjb5LrsijE39z4yrLSfRx+S8cmCENt9Txqd9+l6txsIRTbvs4DD9lXwLuKQx8sneM22dpuMC/8CYweQcdDvDnJGJ0lhQTt3TR44K7hMZ7cfX/Cgfjf2DnGz+tIVFj2OsV51CYiJOZ0CDLah6xGlS6mR47mY37y7aoO9h1kKpBAKHkOQodCqG1wCvYjISXM4SA0TqBTwWjDNu/AC+khFkiEnwsc/os2y6ONO/e2DAN3goIMgFBZiY331h1ANQAc3oxW5Dh/+6uYeXrbs=; babbc09f4fab077b4efb4cb013c3f704=1b40ed6a2e413c6184fb0e6cb5f9c921; SSID=CQC5ZR0cAAAAAABcXh5irADFDFxeHmIKAAAAAAAAAAAAJ7BKYgD53AIHAQG4-SIAJ7BKYgEApQYBAVbzIgAnsEpiAQA; SSSC=567.G7070192214462496940.10|67237.2290518:67330.2292152; SSRT=J7BKYgADAA; RT=\"z=1&dm=elcorteingles.es&si=9zozdj7bxl&ss=l1gnoa9q&sl=0&tt=0\"; _ga=GA1.2.1953228374.1646157412; qb_session=1:1:2::0:X/zwC/r:0:0:0:0:.elcorteingles.es; qb_permanent=04fgsk0qtj7-0l0pfgra8-i1y2gco:67:4:9:7:0::0:1:0:BiLgy1:BiSrAt:A:::::madrid:1715:spain:ES:::unknown:unknown:madrid:11413:migrated|1649061934037:EtrJ==E=CJQV=BW::X/zwDPV:X/zgKrY:0:0:0::0:0:.elcorteingles.es:0; rr_rcs=eF4Nx7kRgDAMBMDEEb2cR5-F1QF1-JshIAPqh802pacfIu5t2kIra8K4dpCJo8R_Wj6s2Xa99zkykzLYLcg5VEl3VIA_j10Rhg; _uetsid=e59ba240b3e911ec9ae64dd606fde177; _uetvid=b13933c0a2e111ecbc5349576776f44f; _abck=B905B88D010B19154B8378CCCD15933D~0~YAAQF7U+F2Hg4J9/AQAAhzXA8wdZlKRby9QJomuPHde7OXqvvsOnXbtkVJnB+gXNFWttl+xBLcpLinFChe6czORd1ThqS7241vLmp2G3jsdiV5qkdWjla6Yxk08vqGceVx5Kl+BXVaR+VqE0OTGlxnKuNdTZ/EfrMZ+ucvMq+obPRbQ98jqkLpMhD9HNX/eolrzPmvKN75rlFQw7bNsnm1V8KLxYIV6ds+xQifaEGLVxP2DTL7ojeqT/7R3Q/B4MCvSGZmBhiXOMnSDMNNPW0S//6bqdL0415mrqcK62baiCab4htTRJmWhSq2SAbRobkilQx5P1AykDa1NZPijYc5GwcQRpL8bwQnVqoa0bTStN349UmVdgnHkuDcBM4AASgljQXzuKY/PGdq+MX29t1TmPuGQx6YxnCidgBaS8~-1~||-1||~-1; SSPV=JgMAAAAAAAAAAwAAAAAAAAAAAAQAAAAAAAAAAAAA; _clsk=1oln4b4|1649061936834|2|0|f.clarity.ms/collect; BVBRANDSID=f87eb8b4-af2b-4bf6-a0ba-272bdb25fb20; _dc_gtm_UA-42384899-20=1; _ga_SWVN6ZZS8X=GS1.1.1649061927.5.1.1649061952.35",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.getUserAgent(),
            'x-test': 'true',
            'x-test2': 'true',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate"
        }
        
        self.cookie = {
            "version":4,
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

    # Método para elegir un User Agent diferente en cada llamada y evitar bloqueos
    def getUserAgent(self):
        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
        ]
        return random.choice(user_agent_list)    


    def scrappingProductsListEci(self, raw_results, item):

        soup = BeautifulSoup(raw_results, features='lxml')

        # Obtenemos la lista de productos tras la búsqueda
        prod_data = soup.find_all('li', attrs={"class": "products_list-item"})
        
        prod_csv = []

        for pd in prod_data:
            elem = pd.find('span', attrs={"class": 'dataholder'}).get('data-json', {})
            elem_object = json.loads(elem)

            rating = pd.find('meta', attrs={"itemprop": 'ratingValue'})
            n_comments = pd.find('meta', attrs={"itemprop": 'reviewCount'})
            image =  pd.find('img', attrs={"class": 'js_preview_image'})


            obj = {
                "product": elem_object.get("name").replace(',', ''),
                "brand": elem_object.get("brand").replace(',', ''),
                "price": elem_object.get("price").get("f_price"),
                "discount_percent": elem_object.get("price").get("discount_percent"),
                "rating": float(rating.get('content')) if rating else None,
                "n_comments": int(n_comments.get('content')) if n_comments else None,
                "image": 'https:' + image.get('data-src') if image else None,
                "express_delivery": elem_object.get("badges").get("express_delivery"),
                "ecommerce": "ECI"
            }

            prod_csv.append([item, obj['product'], obj['brand'], obj['price'], obj['discount_percent'], obj['rating'], obj['n_comments'], obj['image'], obj['express_delivery'], obj['ecommerce']])

        return prod_csv


        
    def scrappingProductsListAmz(self, url, item):

        session = requests.Session()
        session.cookies.set(**self.cookie)

        page = session.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, features='lxml')

         # Obtenemos la lista de productos tras la búsqueda
        prod_data = soup.find_all('div', attrs={"class": 's-card-container'})
        
        prod_csv = []


        for pd in prod_data:

            prices = pd.find('span', attrs={"class": 'a-price-whole'})
            price_discount = pd.find("span", attrs={"class": "a-price a-text-price", "data-a-strike": "true"})
            products = pd.find('span', attrs={"class": 'a-size-base-plus a-color-base a-text-normal'})
            brand = pd.find('span', attrs={"class": "a-size-base-plus a-color-base"})
            rating = pd.find('span', attrs={"class": 'a-icon-alt'})
            n_comments = pd.find('span', attrs={"class": 'a-size-base s-underline-text'})
            image = pd.find('img', attrs={"class": 's-image'})
            express_delivery = pd.find('i', attrs={"class": 'a-icon-prime'})


            # Treating prices
            price_num = None
            discount_percent = 0

            if prices:
                maketrans = prices.string.maketrans
                price_num = float(prices.string.translate(maketrans(',.', '.,', ' ')).replace(',', ''))

        
            if price_discount and price_num:
                price_disc_str = price_discount.find('span', attrs={"class": 'a-offscreen'}).string
                price_before_discount = float(price_disc_str[:-1].translate(maketrans(',.', '.,', ' ')).replace(',', ''))
                discount_percent = round((price_before_discount - price_num) / price_before_discount *100, 0)

            # Comprobamos si es un anuncio para no añadirlo a la lista
            if  products and price_num and rating and image:

                obj = {
                    "product": products.string.replace(',', '') if products else None,
                    "brand": brand.string.replace(',', '') if brand else None,
                    "price": price_num,
                    "discount_percent": discount_percent,
                    "rating": float(rating.string.split('de')[0].replace(',', '.')) if rating and 'de 5 estrellas' in rating.string else None,
                    "n_comments": int(n_comments.string.replace('.', '')) if n_comments else 0,
                    "image": image.get('src') if image else None,
                    "express_delivery": express_delivery.get("aria-label")=="Amazon Prime" if express_delivery else False,
                    "ecommerce": "AMZ"
                }

                prod_csv.append([item, obj['product'], obj['brand'], obj['price'], obj['discount_percent'], obj['rating'], obj['n_comments'], obj['image'], obj['express_delivery'], obj['ecommerce']])

        return prod_csv



    # def constructLinkAmazon(self, searchterm):
    #     searchitem_parsed = ("+").join(searchterm.split(" "))
    #     return f"https://www.amazon.es/s?k={searchitem_parsed}"

    # def constructLinkECI(self, searchterm):
    #     searchitem_parsed = ("%20").join(searchterm.split(" "))
    #     return f"https://www.elcorteingles.es/search/?s={searchitem_parsed}"

    # def scrappingProduct(self, prodlink):
    #     session = requests.Session()
    #     session.cookies.set(**self.cookie)

    #     page = session.get(prodlink, headers=self.headers)
    #     #if page.status_code == 200:
    #     soup = BeautifulSoup(page.content, features="html.parser")
    #     #prod_data = soup.find_all('div', attrs={"class": 's-card-container'})

    #     price_discount = soup.find('span', attrs={"class": 'a-price', "data-a-strike": "true"})
    #     product_name = soup.find('span', attrs={"id": 'productTitle'})
    #     #rating_whole = soup.find('i', attrs={"class": 'a-icon a-icon-star'})
    #     rating_whole = soup.find('span', attrs={"class": 'a-icon-alt'})
    #     n_comments = soup.find('span', attrs={"id": 'acrCustomerReviewText'})
    #     image = soup.find('img', attrs={"id": 'landingImage'})
    #     is_express = False


    #     # Treating prices
    #     price_num = None
    #     price_topay = None
    #     discount_percent = None
    #     currency = None

    #     for p in soup.select('span[class*="PriceToPay"]'):
    #         price_topay = p.find('span', attrs={"class": 'a-offscreen'}).string

    #     if price_topay:
    #         price_num = float(price_topay[:-1].replace(',', '.'))
    #         symbol = price_topay[-1]
            
    #         currency = "EUR" if u"\N{euro sign}" in symbol else "USD"
        
    #     if price_discount and price_num:
    #         price_disc_str = price_discount.find('span', attrs={"class": 'a-offscreen'}).string
    #         price_before_discount = float(price_disc_str[:-1].replace(',', '.'))
    #         discount_percent = round((price_before_discount - price_num) / price_before_discount *100, 0)
            
    #     # Treating is_express
    #     scripts = soup.find_all("script", attrs={"type": "text/javascript"})
    #     for s in scripts:
    #         if re.search(r"var bbopData", s.string): is_express = True


    #     # Treating rating
    #     rating = None
    #     if rating_whole:
    #         if 'de 5 estrellas' in rating_whole.string:
    #             rating_str = rating_whole.string.split('de')[0].replace(',', '.')
    #             rating = float(rating_str)
                
    #     print({
    #         "products": product_name.string.lstrip().rstrip() if product_name else "",
    #         "price": price_num if price_num else 0.0,
    #         "discount_percent": discount_percent,
    #         "rating": rating,
    #         "n_comments": int(("").join([s for s in n_comments.string.replace('.', '').split() if s.isdigit()])) if n_comments else 0,
    #         "image": image.get('src') if image else "",
    #         "currency": currency,
    #         "is_express": is_express
    #     })
            
