#!/usr/bin/env python3

import sys

import requests
from courlan import extract_links, is_navigation_page, is_not_crawlable


def main():
    if len(sys.argv) != 2:
        exit("Usage: print-links URL")

    url = sys.argv[1]
    text = requests.get(url).text
    links = set(extract_links(text, url))

    for link in links:
        if not is_navigation_page(link) and not is_not_crawlable(link):
            print(link)


if __name__ == "__main__":
    main()
