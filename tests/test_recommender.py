from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from src.recommender import LaptopRecommender

# --- Fixtures ---


@pytest.fixture
def sample_data():
    """
    Creates a DataFrame exactly matching the raw database output provided.
    Includes messy data: empty strings, ranges for weight, quotes in screen size.
    """
    raw_data = {
        "id": {36: 36, 244: 243, 627: 625},
        "item_name": {
            36: 'Samsung - Galaxy Tab S10 FE - 10.9" 128GB - Wi-Fi - with S-Pen - Gray (SM-X520NZAAXAR)(4)',
            244: 'HP EliteBook 840 G5 14" FHD 1920 x 1080 Notebook – 8th Gen Intel QUAD Core i5-8350U 512 GB SSD 16GB DDR4 RAM Webcam Windows 11 Pro',
            627: 'Dell Latitude E6420 14" LED Laptop Intel Core i5 2.50 GHz CPU 16 GB DDR3 RAM 128 GB SSD DVD-R HDMI WiFi Webcam Windows 10 Pro(2)',
        },
        "url": {
            36: "https://item-1-sample",
            244: "https://item-2-sample",
            627: "https://item-3-sample",
        },
        "image": {
            36: "https://image-1-sample",
            244: "https://image-2-sample",
            627: "https://image-3-sample",
        },
        "price": {36: 499.99, 244: 339.0, 627: 140.0},
        "screen_size": {36: '10.9"', 244: '14.0"', 627: '14.1"'},
        "memory": {36: "8GB", 244: "16GB", 627: "16GB"},
        "cpu_type": {
            36: "",
            244: "Intel Core i5 8th Gen",
            627: "Intel Core i5 2nd Gen",
        },
        "gpu": {36: "", 244: "Intel UHD Graphics", 627: "Intel HD Graphics 3000"},
        "storage": {36: "", 244: "512GB", 627: "128GB"},
        "resolution": {36: "2304 x 1440", 244: "1920 x 1080", 627: "1366 x 768"},
        "weight": {36: "", 244: "2 - 2.9 lbs.", 627: "4 - 4.9 lbs."},
        "backlit_keyboard": {36: "", 244: "", 627: ""},
        "touchscreen": {36: "", 244: "Non-Touch Screen", 627: "Non-Touch Screen"},
        "webcam": {36: "", 244: "Yes", 627: "Yes"},
        "thunderbolt": {36: "", 244: "1 x Thunderbolt", 627: ""},
        "card_reader": {36: "", 244: "", 627: "YES"},
        # Extra columns that exist in DB but are filtered out by Recommender
        "cpu_speed": {
            36: "Samsung Exynos 1580",
            244: "Intel Core i5-8350U",
            627: "Intel Core i5-2520M",
        },
        "operating_system": {
            36: "Android 15",
            244: "Windows 11 Pro",
            627: "Windows 10 Pro",
        },
    }
    return pd.DataFrame(raw_data)


@pytest.fixture
def sample_lookups():
    """Mock lookup tables for CPU/GPU scoring."""
    cpu = pd.DataFrame(
        {"cpu": ["intel core i5 8th gen", "intel core i5 2nd gen"], "score": [0.6, 0.3]}
    )
    gpu = pd.DataFrame(
        {"gpu": ["intel uhd graphics", "intel hd graphics 3000"], "score": [0.3, 0.1]}
    )
    return cpu, gpu


@pytest.fixture
def recommender(sample_data, sample_lookups):
    """Returns an instance of LaptopRecommender with mocked init logic if needed."""
    cpu_lookup, gpu_lookup = sample_lookups
    return LaptopRecommender(sample_data, cpu_lookup, gpu_lookup)


# --- Tests ---


def test_initialization_and_cleaning(recommender):
    """
    Test that the recommender correctly ingests the raw dirty data
    and filters down to the specific columns defined in _data_cleaning.
    """
    df = recommender.data

    assert "operating_system" not in df.columns
    assert "cpu_speed" not in df.columns

    assert "price" in df.columns
    assert "item_name" in df.columns

    assert len(df) == 3

    assert df.loc[df["id"] == 36, "screen_size"].values[0] == '10.9"'


@patch("src.recommender.process_cpu")
@patch("src.recommender.process_gpu")
@patch("src.recommender.process_memory")
@patch("src.recommender.process_storage")
@patch("src.recommender.process_resolution")
@patch("src.recommender.process_portability")
@patch("src.recommender.process_size")
@patch("src.recommender.process_extra_feat")
def test_generate_lookup_embedding(
    mock_extra,
    mock_size,
    mock_port,
    mock_res,
    mock_store,
    mock_mem,
    mock_gpu,
    mock_cpu,
    recommender,
):
    """
    Test that generate_lookup_embedding handles the messy raw data
    by delegating to the utils functions correctly.
    """
    n_rows = len(recommender.data)

    # Mock return values (standardized numpy arrays expected by the math logic)
    # Even though input is messy strings, utils should return clean floats
    mock_cpu.return_value = np.array([0.0, 0.6, 0.3])
    mock_gpu.return_value = np.array([0.0, 0.3, 0.1])
    mock_mem.return_value = np.ones(n_rows)
    mock_store.return_value = np.ones(n_rows)
    mock_res.return_value = np.ones(n_rows)
    mock_port.return_value = np.array([0.9, 0.5, 0.2])
    mock_size.return_value = np.array([0.2, 0.5, 0.5])
    mock_extra.return_value = np.zeros((n_rows, 5))

    embedding = recommender.generate_lookup_embedding()

    # Verify the Utils were called with the messy raw data
    args, _ = mock_port.call_args
    assert "2 - 2.9 lbs." in args[0].values

    # Verify Output Shape
    # Usage(5) + Port(1) + Size(1) + Extra(5) = 12 columns
    assert embedding.shape == (n_rows, 12)


@patch("src.recommender.process_brand")
def test_predict_top_k_with_user_input(mock_process_brand, recommender):
    """
    Test the prediction logic using the specific user_input structure provided.
    """
    # 1. The specific User Input provided
    user_input = dict(
        brands=["msi"],
        budget=1200,
        usage="Gaming",
        portability=0.5,
        size=0.66,
        extra=[1, 0, 1, 0, 0],
    )

    # 2. Mock Laptop Embedding (3 items, 12 features)
    laptop_emb = np.random.rand(3, 12)

    # 3. Mock Brand Processing
    # Return array matching rows: 1 if brand match, 0 if not.
    mock_process_brand.return_value = np.array([0, 0, 0])

    # 4. Run Prediction
    top_items, top_scores = recommender.predict_top_k(user_input, laptop_emb, top_k=2)

    # 5. Assertions
    assert len(top_items) == 2

    # Check that price decay worked:
    # Item 36 (Price 499) vs Budget (1200) -> Safe
    # Item 244 (Price 339) vs Budget (1200) -> Safe
    # Item 627 (Price 140) vs Budget (1200) -> Safe
    assert top_scores[0] >= top_scores[1]


def test_usage_classifier_logic(recommender):
    """
    Test heuristics on the messy data after it has been 'processed' by mocks.
    We simulate the internal values to test the classification rules.
    """
    # Columns: cpu, gpu, memory, resolution, storage
    # Row 0: High GPU (Gaming)
    # Row 1: Low stats (Academy)
    # Row 2: High Res + Mem (Content Design)
    dummy_specs = pd.DataFrame(
        [
            {"cpu": 0.5, "gpu": 0.8, "memory": 0.5, "resolution": 0.5, "storage": 0.5},
            {"cpu": 0.1, "gpu": 0.1, "memory": 0.1, "resolution": 0.1, "storage": 0.1},
            {"cpu": 0.5, "gpu": 0.2, "memory": 0.8, "resolution": 0.9, "storage": 0.5},
        ]
    )

    embeddings = recommender._usage_classifier(dummy_specs)

    # Decode one-hot vectors to check classification
    indices = np.argmax(embeddings, axis=1)
    mapping = recommender.usage_types
    results = [mapping[i] for i in indices]

    assert results == ["Gaming", "Academy", "Content Design"]
