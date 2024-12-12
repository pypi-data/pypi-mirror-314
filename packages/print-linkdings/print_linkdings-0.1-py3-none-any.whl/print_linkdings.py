#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import requests
from courlan import extract_links, is_navigation_page, is_not_crawlable


def main():

    if len(sys.argv) != 2:
        exit("Usage: print-linkdings INSTANCE_URL")

    api_url = f"{sys.argv[1]}/api/bookmarks/"
    linkding_api_key = (
        Path("/usr/local/etc/linkding_api_key.txt").read_text().strip("\n")
    )
    headers = {"Authorization": f"Token {linkding_api_key}"}
    response = requests.get(api_url, headers=headers)
    json_data = json.loads(response.text)

    linkding_urls = []
    for item in json_data["results"]:
        linkding_urls.append(item.get("url"))

    for url in linkding_urls:
        text = requests.get(url).text
        links = set(extract_links(text, url))

        for link in links:
            if not is_navigation_page(link) and not is_not_crawlable(link):
                print(link)


if __name__ == "__main__":
    main()
