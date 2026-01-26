from scraper import WebScraper
from src.database import SupabaseManager


def main():
    scraper = WebScraper()
    db = SupabaseManager()

    # scraping newegg laptop/notebook product details
    newegg_data = []
    pages = scraper.newegg_scraper(n_page=20)
    for page in pages:
        for item in page:
            newegg_data.append(scraper.newegg_html_parser(item))

    db.insert_bulk_from_dict(table_name="items", data=newegg_data)

    # scraping passmark cpu benchmark
    cpu_data = []
    cpu_list = scraper.cpu_benchmark_scraper()

    for cpu in cpu_list:
        cpu_data.append(scraper.cpu_benchmark_html_parser(cpu))

    db.insert_bulk_from_dict(table_name="cpu_benchmark", data=cpu_data)

    # scraping passmark gpu benchmark
    gpu_data = []
    gpu_list = scraper.gpu_benchmark_scraper()

    for gpu in gpu_list:
        gpu_data.append(scraper.gpu_benchmark_html_parser(gpu))

    db.insert_bulk_from_dict(table_name="gpu_benchmark", data=gpu_data)


if __name__ == "__main__":
    main()
