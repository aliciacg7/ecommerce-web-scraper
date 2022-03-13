import re
import argparse
from bs4 import BeautifulSoup

from pricescraper import ProductsScraper



# Parse command line argument and extract the searchterm
parser = argparse.ArgumentParser()
parser.add_argument("--product", help="Enter the product you want to compare. Words must be separated by .")
args = parser.parse_args()

searchterm = args.product

pscraper = ProductsScraper()

pscraper.scrapping(searchterm)







