import requests
from bs4 import BeautifulSoup
import html.parser
from urllib.parse import urljoin
from textwrap import wrap

def get_all_urls(url, amt):
    """Gets all URLs from a given domain."""

    urls = []
    visited = []
    x = 0

    def crawl(url, amt):
        
        print(f"#{len(urls)}:  {url}")
        if url in visited or len(urls) > amt:
            return
        sites_stored = open('./src/python/embeddings/sites.csv', "r")
        sites_stored_arr = sites_stored.read()
        if url not in sites_stored:
            visited.append(url)
        else: return
        sites_stored.close()


        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = urljoin(url, href)
                if href.startswith(url):
                    urls.append(href)
                    crawl(href, amt)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")

    crawl(url, amt)
    return urls

#if __name__ == '__main__':
#    domain = "https://www.example.com/"
#    all_urls = get_all_urls(domain, amt)
#    for url in all_urls:
#        print(url)

def web_scrape_all(domain:str, amt):
    site = get_all_urls(domain, amt)
    f = open('./src/python/embeddings/sites.csv', 'a')
    for i in site:
        f.write(i)
    f.close()
    soup = []
    z = 0
    for i in site:
        z += 1
        print(f"{z} {i}")
        r = requests.get(i)
        x = BeautifulSoup(r.content, 'html.parser').get_text()
        f = open('./src/python/embeddings/research.csv', 'a')
        f.write(x)
        f.close()
    
    return soup

    

scraped_data = web_scrape_all("https://finance.yahoo.com/", 1)