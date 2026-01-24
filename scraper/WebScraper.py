import random
import re
import time
from typing import List

from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


class WebScraper:
    # hanlde html data extraction safely
    def _fetch_data(self, tag, selector, class_name=None, attribute=None):
        if not tag:
            return ""

        element = (
            tag.find(selector, class_=class_name) if class_name else tag.find(selector)
        )

        if not element:
            return ""

        if attribute:
            return element.get(attribute, "")
        else:
            return element.text.strip()

    # Scraper for newegg laptop/notebook product detail
    def newegg_scraper(
        self, base_url="https://www.newegg.com/tools/laptop-finder?page={}", n_page=20
    ) -> List[List[Tag]]:
        pages = []

        with sync_playwright() as p:
            # setting headless browser configurtion
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1500, "height": 800})
            page = context.new_page()
            page.set_extra_http_headers(HEADERS)

            # parse HTML per page (up to 20 pages)
            for i in range(1, n_page + 1):
                try:
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
                except Exception as e:
                    print(f"Error scraping newegg laptop/notebook page [{i}]: {e}")

            browser.close()

        return pages

    # Content parser for newegg html doc
    def newegg_html_parser(self, html_content: Tag) -> dict:
        data = {}

        try:
            data["item_data"] = self._fetch_data(
                html_content, "div", class_name="goods-title"
            )

            data["url"] = self._fetch_data(
                html_content, "a", class_name="goods-info", attribute="href"
            )

            data["image"] = self._fetch_data(html_content, "img", attribute="src")

            raw_price_text = self._fetch_data(
                html_content, "span", class_name="goods-price-value"
            )

            try:
                clean_price = raw_price_text.replace("$", "").replace(",", "")
                data["price"] = float(clean_price) if clean_price else 0.0
            except ValueError:
                data["price"] = 0.0

            specs = html_content.find_all("td", class_="td-spec")
            for s in specs:
                try:
                    col = (
                        self._fetch_data(s, "div", class_name="hid-text")
                        .lower()
                        .replace(" ", "_")
                    )
                    val = self._fetch_data(s, "span")

                    if col:
                        data[col] = val
                except Exception:
                    continue

        except Exception as e:
            print(f"Error parsing newegg HTML content: {e}")
            return {}

        return data

    def cpu_benchmark_scraper(
        self,
        base_url="https://www.cpubenchmark.net/cpu-list/all",
    ) -> List[Tag]:
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

            print("Scraping: ", base_url)
            soup = BeautifulSoup(page.content(), "html.parser")
            table_content = soup.find("table", class_="cpulist")

            if table_content is not None:
                table_content = table_content.find_all("tr", id=re.compile("cpu*"))
            else:
                table_content = []

        return table_content

    def cpu_benchmark_html_parser(self, html_content) -> List[dict]:
        data = []

        for cpu in html_content:
            temp = {}
            temp["cpu"] = self._fetch_data(cpu, "a")
            score = cpu.find_all("td")[1].get_text()

            try:
                clean_score = score.replace(",", "")
                temp["score"] = float(clean_score) if clean_score else 0.0
            except ValueError:
                temp["score"] = 0.0

            data.append(temp)

        return data
