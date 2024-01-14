import requests
import argparse
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',help="Specify the URL with http/https",required=True)
    parser.add_argument('-d','--depth',type=int,default=1,help='Specify depth of recursion')
    return parser.parse_args()

urls = []
urlsVisited = [0]
timestamp = [0]
timeBeforecrawling = 0
uniqueDomains = []
depthURL = []
xaxis = []

def generateTimeChart():
    plt.subplot(2,1,1)
    plt.title('Crawl History Over Time')
    plt.xlabel('Time in second')
    plt.ylabel('Number of URLs Crawled')
    global timestamp
    plt.plot(timestamp,urlsVisited)

def generateDepthChart():
    plt.subplot(2,1,2)
    plt.title('Depth of Crawling')
    plt.xlabel('Depth from Main Source')
    plt.ylabel('Number of URLs Crawled')
    plt.bar(xaxis,depthURL)

def generateCharts():
    generateTimeChart()
    generateDepthChart()
    plt.tight_layout(pad=1.0)
    plt.show()

def extractDomain(url):
    uniqueDomain1 = url.split('//')[1].split('/')[0]
    uniqueDomain2 = url.split('//')[1].split('//')[0]
    uniqueDomain = ''
    if len(uniqueDomain2)>len(uniqueDomain1):
        uniqueDomain = uniqueDomain1
    else:
        uniqueDomain = uniqueDomain2
    if uniqueDomain not in uniqueDomains:
        uniqueDomains.append(uniqueDomain)

def scrape(site,depth):
    global timeBeforecrawling
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
        depthURL[depth-1]+=1
        if href.startswith('/'):
            nextLink = site + href
            if nextLink not in urls:
                urls.append(nextLink)

                timeAftercrawling = time.time()
                timestamp.append(timeAftercrawling-timeBeforecrawling)
                urlsVisited.append(urlsVisited[-1]+1)
                
                print(nextLink)
                scrape(nextLink,depth-1)
       
        elif href.startswith('https://') or href.startswith('http://'):
            if href not in urls:
                extractDomain(href)
                urls.append(href)
                print(href)
                
                timeAftercrawling = time.time()
                timestamp.append(timeAftercrawling-timeBeforecrawling)
                urlsVisited.append(urlsVisited[-1]+1)
                
                scrape(href,depth-1)

def generateReport():
    print()
    print("----------------------------------------------------")
    print("Crawling Statistics ")
    print("----------------------------------------------------")
    print(f"1. Total Unique URLs Crawled: {len(urls)}")
    print(f"2. Total Execution Time: {executionTime} sec")
    print(f"3. Total Unique Domains: {len(uniqueDomains)}")
    print("----------------------------------------------------")

if __name__ == "__main__":
    args = get_args()
    link = args.url
    depth = args.depth
    depthURL = [0 for i in range(1,depth+1)]

    timeBeforecrawling = time.time()
    scrape(link,depth)
    timeAftercrawling = time.time()
    executionTime = timeAftercrawling - timeBeforecrawling
    xaxis = [i for i in range(1,depth+1)]

    print(uniqueDomains)
    generateReport()
    generateCharts() 