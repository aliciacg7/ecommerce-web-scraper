import re
import argparse
from bs4 import BeautifulSoup

from pricescraper import ProductsScraper



# Parse command line argument and extract the searchterm
parser = argparse.ArgumentParser()
parser.add_argument("--product", help="Enter the product you want to compare. Words must be separated by .")
parser.add_argument("--link", help="Enter the link of the product you want to compare")
args = parser.parse_args()

searchterm = args.product
searchlink = args.link

pscraper = ProductsScraper()


#pscraper.scrappingProduct(searchlink)
pscraper.scrappingProductsListEci(searchterm)







