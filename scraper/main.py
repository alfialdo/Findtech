from argparse import ArgumentParser

from scraper import WebScraper
from src.database import SupabaseManager

ap = ArgumentParser()
ap.add_argument("--item", action="store_true", help="Enable newegg scraper")
ap.add_argument("--cpu", action="store_true", help="Enable passmark CPU scraper")
ap.add_argument("--gpu", action="store_true", help="Enable passmark GPU scraper")


def main():
    args = ap.parse_args()
    scraper = WebScraper()
    db = SupabaseManager()

    # scraping newegg laptop/notebook product details
    if args.item:
        newegg_data = []
        pages = scraper.newegg_scraper(n_page=20)
        for page in pages:
            for item in page:
                newegg_data.append(scraper.newegg_html_parser(item))

        db.insert_bulk_from_dict(table_name="items", data=newegg_data)

    # scraping passmark cpu benchmark
    if args.cpu:
        cpu_data = []
        cpu_list = scraper.cpu_benchmark_scraper()

        for cpu in cpu_list:
            cpu_data.append(scraper.cpu_benchmark_html_parser(cpu))

        db.insert_bulk_from_dict(table_name="cpu_benchmark", data=cpu_data)

    # scraping passmark gpu benchmark
    if args.gpu:
        gpu_data = []
        gpu_list = scraper.gpu_benchmark_scraper()

        for gpu in gpu_list:
            gpu_data.append(scraper.gpu_benchmark_html_parser(gpu))

        db.insert_bulk_from_dict(table_name="gpu_benchmark", data=gpu_data)


if __name__ == "__main__":
    main()
