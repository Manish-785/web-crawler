import requests
import argparse
from bs4 import BeautifulSoup
import matplotlib

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',help="Specify the URL with http/https",required=True)
    parser.add_argument('-d','--depth',type=int,default=1,help='Specify depth of recursion')
    return parser.parse_args()

urls = []

def scrape(site,depth):
    if depth < 1:
        return
    try:
        request = requests.get(site,timeout=3,allow_redirects=True)
        text = BeautifulSoup(request.text,"html.parser")
    except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            return  
    for anchor in text.find_all('a'):
        href = anchor.get('href')
        if href is None:
            return
        if href.startswith('/'):
            nextLink = site + href
            if nextLink not in urls:
                urls.append(nextLink)
                scrape(nextLink,depth-1)
                print(nextLink)
        elif href.startswith('https://') or href.startswith('http://'):
            if href not in urls:
                urls.append(href)
                print(href)
                scrape(href,depth-1)

if __name__ == "__main__":
    args = get_args()
    link = args.url
    depth = args.depth
    scrape(link,depth)