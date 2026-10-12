#!/usr/bin/env python3
import argparse
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def extract_text(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else base_url

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text_blocks = []
    for p in soup.find_all(["p", "h1", "h2", "h3", "li"]):
        text = " ".join(p.get_text(" ", strip=True).split())
        if text:
            text_blocks.append(text)

    content = " ".join(text_blocks)
    if not content:
        content = " ".join(soup.get_text(" ", strip=True).split())

    return {
        "title": title,
        "url": base_url,
        "content": content[:5000],
        "site": base_url.split("//")[-1].split("/")[0],
        "source": "crawler",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl and index a site into the private search API.")
    parser.add_argument("--url", required=True, help="URL to crawl")
    parser.add_argument("--api-url", default="http://localhost:8000", help="Search API base URL")
    parser.add_argument("--api-key", default="change-me", help="Search API key")
    args = parser.parse_args()

    html = fetch_page(args.url)
    page = extract_text(html, args.url)
    payload = [
        {
            "id": page["url"],
            "title": page["title"],
            "url": page["url"],
            "content": page["content"],
            "site": page["site"],
            "source": page["source"],
        }
    ]

    response = requests.post(
        f"{args.api_url}/documents",
        json=payload,
        headers={"x-api-key": args.api_key},
        timeout=20,
    )

    if response.status_code != 200:
        print(f"Indexing failed: {response.status_code} {response.text}")
        raise SystemExit(1)

    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
