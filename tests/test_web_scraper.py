import pytest
from bs4 import BeautifulSoup

from scraper import WebScraper


@pytest.fixture
def sample_newegg_html():
    return """
    <tr><td class=td-item><a class=goods-info data-target=#modal-pc-builder-pdp data-toggle=modal href="https://www.newegg.com/msi-crosshair-a16-hx-16-0-geforce-rtx-5060-laptop-gpu-2-4-5-3ghz-qhd-32gb-memory-1tb-nvme-ssd-gen4x4-ssd/p/N82E16834156876?Item=N82E16834156876"><div class=goods-img><img alt='MSI CROSSHAIR A16 - 16" QHD+ 240H -z AMD Ryzen 9-8940HX - GeForce RTX 5060 - 32GBDDR5 1TB NVMe SSD - Win 11 Gaming Laptop (D8WFKG-015US)'src=https://c1.neweggimages.com/ProductImageCompressAll125/34-156-876-13.jpg></div><div class=goods-title><div class=goods-title-content>MSI CROSSHAIR A16 - 16" QHD+ 240H -z AMD Ryzen 9-8940HX - GeForce RTX 5060 - 32GBDDR5 1TB NVMe SSD - Win 11 Gaming Laptop (D8WFKG-015US)</div><div class=goods-rating><i aria-label="rated 5 out of 5"class="rating rating-5"></i> <span class="font-s goods-rating-num text-gray">(3)</span></div></div></a><td class=td-spec><div class=hid-text>Screen Size</div><span>16.0"</span><td class=td-spec><div class=hid-text>CPU type</div><span>AMD Ryzen 9 8000 Series</span><td class=td-spec><div class=hid-text>Memory</div><span>32GB</span><td class=td-spec><div class=hid-text>Storage</div><span>1TB NVMe</span><td class=td-spec><div class=hid-text>GPU</div><span>GeForce RTX 5060 Laptop GPU</span><td class=td-spec><div class=hid-text>Resolution</div><span>2560 x 1600</span><td class=td-spec><div class=hid-text>Weight</div><span>5 - 5.9 lbs.</span><td class=td-spec><div class=hid-text>Backlit Keyboard</div><span></span><td class=td-spec><div class=hid-text>Touchscreen</div><span>Non-Touch Screen</span><td class=td-spec><div class=hid-text>CPU Speed</div><span>AMD Ryzen 9 8940HX</span><td class=td-spec><div class=hid-text>Number of Cores</div><span></span><td class=td-spec><div class=hid-text>Color</div><span></span><td class=td-spec><div class=hid-text>Display Type</div><span>QHD+</span><td class=td-spec><div class=hid-text>Graphic Type</div><span></span><td class=td-spec><div class=hid-text>Operating System</div><span>Windows 11 Home</span><td class=td-spec><div class=hid-text>Webcam</div><span>720p HD</span><td class=td-spec><div class=hid-text>Thunderbolt</div><span></span><td class=td-spec><div class=hid-text>Card Reader</div><span></span><td class=td-action><div class="col-w-3 grid item-action"><div class=goods-price-current><div class="font-s goods-price"><div class=goods-price-current><span class=goods-price-label></span> <span class=goods-price-symbol>$ </span><span class=goods-price-value><strong>1,499 </strong><sup>.99</sup></span></div></div></div><div class="goods-operate xxs-hide"><div class=goods-button-area><button class="bg-orange button button-s"title='Add MSI CROSSHAIR A16 - 16" QHD+ 240H -z AMD Ryzen 9-8940HX - GeForce RTX 5060 - 32GBDDR5 1TB NVMe SSD - Win 11 Gaming Laptop (D8WFKG-015US) to cart'><span>Add to cart</span></button></div></div></div>
    """


@pytest.fixture
def sample_cpu_benchmark_html():
    return """
    <tr class="alt" id="cpu2416"><td><a href="/cpu_lookup.php?cpu=AMD+A10+PRO-7850B+APU&amp;id=2416">AMD A10 PRO-7850B APU</a></td><td>3,441</td><td>2777</td><td class="vLink" style="cursor: pointer;">23.25</td><td class="pLink" style="cursor: pointer;">$148.02*</td></tr>
    """


@pytest.fixture
def sample_gpu_benchmark_html():
    return """
    <tr class="odd" role="row"><td class="details-control"></td><td class="sorting_1"><a href="video_lookup.php?gpu=Quadro+M1000M&amp;id=3349">Quadro M1000M</a></td><td>2,836</td><td>309</td><td>40</td><td>4096 MB</td><td>Mobile, Workstation</td></tr>
    """


@pytest.fixture
def scraper_instance() -> WebScraper:
    return WebScraper()


def test_newegg_parser(scraper_instance, sample_newegg_html):
    soup = BeautifulSoup(sample_newegg_html, "html.parser")

    result = scraper_instance.newegg_html_parser(soup)

    assert "MSI CROSSHAIR A16" in result["item_name"]

    assert result["price"] == 1499.99

    assert "newegg.com" in result["url"]

    assert "c1.neweggimages.com" in result["image"]

    assert result["screen_size"] == '16.0"'
    assert result["memory"] == "32GB"
    assert result["cpu_type"] == "AMD Ryzen 9 8000 Series"
    assert result["weight"] == "5 - 5.9 lbs."
    assert result["storage"] == "1TB NVMe"
    assert result["gpu"] == "GeForce RTX 5060 Laptop GPU"
    assert result["resolution"] == "2560 x 1600"
    assert result["backlit_keyboard"] == ""
    assert result["touchscreen"] == "Non-Touch Screen"
    assert result["cpu_speed"] == "AMD Ryzen 9 8940HX"
    assert result["number_of_cores"] == ""
    assert result["color"] == ""
    assert result["display_type"] == "QHD+"
    assert result["graphic_type"] == ""
    assert result["operating_system"] == "Windows 11 Home"
    assert result["webcam"] == "720p HD"
    assert result["thunderbolt"] == ""
    assert result["card_reader"] == ""


def test_cpu_benchmark_parser(scraper_instance, sample_cpu_benchmark_html):
    soup = BeautifulSoup(sample_cpu_benchmark_html, "html.parser")

    result = scraper_instance.cpu_benchmark_html_parser(soup)

    assert result["cpu"] == "AMD A10 PRO-7850B APU"
    assert result["score"] == 3441.0


def test_gpu_benchmark_parser(scraper_instance, sample_gpu_benchmark_html):
    soup = BeautifulSoup(sample_gpu_benchmark_html, "html.parser")

    result = scraper_instance.gpu_benchmark_html_parser(soup)

    assert result["gpu"] == "Quadro M1000M"

    assert result["score"] == 2836.0

    assert result["vram"] == "4096 MB"

    assert result["categories"] == "Mobile, Workstation"
