from ast import keyword
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# initialize the set of links (unique links)
internal_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url`
    """
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.content, "html.parser")
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # obtain only the scheme://netloc/ of the link
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `internal_urls` global set variable.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total URLs:", len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    domain_name = urlparse(url).netloc

    # save the internal links to a file
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
             print(internal_link.strip(), file=f)
        
