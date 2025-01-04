# -*- coding: utf-8 -*-

"""
把 https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
中的所有文档的 HTML 页面下载下来, 保存到 tmp 目录下.
"""

import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from diskcache import Cache

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
dir_cache = dir_here.joinpath(".cache")


def reset_dir_tmp():
    if dir_tmp.exists():
        shutil.rmtree(dir_tmp)
    dir_tmp.mkdir()


def reset_dir_cache():
    if dir_cache.exists():
        shutil.rmtree(dir_cache)
    dir_cache.mkdir()


cache = Cache(str(dir_cache))


def get_html_by_url(url: str) -> str:
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def get_html_by_url_with_cache(
    url: str,
    use_cache: bool = True,
) -> str:
    if use_cache:
        if url in cache:
            return cache[url]
    html = get_html_by_url(url)
    cache[url] = html
    return html


def extract_the_main_div(soup: BeautifulSoup) -> BeautifulSoup:
    """
    从文档页面中找到关键文档所在的 div, 剔除无关元素.
    """
    found_div = None
    for div in soup.find_all("div"):
        for child in div.children:
            if child.name == "h1":
                found_div = div
                break
        if found_div is not None:
            break
    if found_div is None:
        raise Exception("Can not find the correct div")
    return found_div


def write_webpage(div: BeautifulSoup, title: str):
    path = dir_tmp.joinpath(f"{title}.html")
    text = str(div.prettify())
    path.write_text(text)


def main():
    reset_dir_tmp()

    html = get_html_by_url_with_cache(
        "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/",
    )
    soup = BeautifulSoup(html, "html.parser")
    main_div = extract_the_main_div(soup)
    write_webpage(main_div, "Atlassian Document Format")

    # 找到左边导航栏的所有链接
    div = soup.find("div", class_="sideNavLinksScrollable")
    for a in div.find_all("a"):
        href = a["href"]
        url = f"https://developer.atlassian.com{href}"
        print(f"Crawl: {a.text}")
        # time.sleep(1)
        html = get_html_by_url_with_cache(url)
        soup = BeautifulSoup(html, "html.parser")
        main_div = extract_the_main_div(soup)
        write_webpage(main_div, a.text)


if __name__ == "__main__":
    main()
