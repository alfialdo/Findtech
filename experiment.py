# %%
import random
import re
import time
from typing import List

import bs4
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# %%
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


def newegg_web_scraper(
    base_url="https://www.newegg.com/tools/laptop-finder?page={}", n_page=20
) -> List[List[bs4.element.Tag]]:
    pages = []

    with sync_playwright() as p:
        # setting headless browser configurtion
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1500, "height": 800})
        page = context.new_page()
        page.set_extra_http_headers(HEADERS)

        # parse HTML per page (up to 20 pages)
        for i in range(1, n_page + 1):
            url = base_url.format(str(i))
            print(f"Scraping: {url}")

            page.goto(url, timeout=10000)
            page.mouse.wheel(0, 2200)
            time.sleep(random.uniform(2, 5))

            soup = BeautifulSoup(page.content(), "html.parser")
            table = soup.find("table", class_="table-vertical")

            assert table is not None
            rows = table.find_all("tr")[1:]
            pages.append(rows)

        browser.close()

    return pages


# TODO: add parsing verification
def newegg_html_parser(html_content) -> dict:
    data = {}

    data["item_data"] = html_content.find("div", class_="goods-title").text.strip()
    data["url"] = html_content.find("a", class_="goods-info").get("href", "")
    data["image"] = html_content.find("img").get("src", "")
    price = html_content.find("span", class_="goods-price-value").text.strip()
    data["price"] = float(price.replace(",", ""))

    specs = html_content.find_all("td", class_="td-spec")
    for s in specs:
        col = s.find("div", class_="hid-text").text
        col = col.lower().replace(" ", "_")
        val = s.find("span").text
        data[col] = val

    return data


def cpu_benchmark_scraper(
    base_url="https://www.cpubenchmark.net/cpu-list/all",
) -> List[bs4.element.Tag]:
    with sync_playwright() as p:
        # setting headless browser configurtion
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1200, "height": 1000})
        page = context.new_page()
        page.set_extra_http_headers(HEADERS)
        page.goto(base_url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        page.mouse.wheel(0, 5200)
        time.sleep(random.uniform(2, 5))

        soup = BeautifulSoup(page.content(), "html.parser")
        table_content = soup.find("table", class_="cpulist")

        if table_content is not None:
            table_content = table_content.find_all("tr", id=re.compile("cpu*"))
        else:
            table_content = []

    return table_content


def cpu_benchmark_parser(cpu_list) -> List[dict]:
    data = []

    for cpu in cpu_list:
        temp = {}
        title_tag = cpu.find("a")
        mark_tag = cpu.find_all("td")[1]

        if title_tag is None or mark_tag is None:
            continue

        temp["cpu"] = title_tag.get_text().strip()
        mark_tag = mark_tag.get_text().replace(",", "")
        temp["mark"] = float(mark_tag)
        data.append(temp)

    return data


def gpu_benchmark_scraper(base_url=""):
    pass


def gpu_benchmark_parser(gpu_list) -> dict:
    pass


# %% Sraping newegg website data
start_time = time.time()
pages = newegg_web_scraper(n_page=1)
for rows in pages:
    for r in rows:
        print(newegg_html_parser(r))

print(f"Exec time: {time.time() - start_time:.3f}")

# %% Scraping cpu benchmarks web
html_content = cpu_benchmark_scraper()
cpu_list = cpu_benchmark_parser(html_content)
print(cpu_list)


# %%
