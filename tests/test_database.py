from unittest.mock import MagicMock, patch

import pytest

from src.database import SupabaseManager


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://fake.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "random-key-456")


@pytest.fixture
def sample_scraped_items():
    return [
        {
            "item_name": "MSI CROSSHAIR A16",
            "price": 1499.99,
            "url": "https://newegg.com/msi",
            "image": "https://c1.neweggimages.com/test.jpg",
            "screen_size": '16.0"',
            "memory": "32GB",
            "cpu_type": "AMD Ryzen 9 8000 Series",
            "gpu": "GeForce RTX 5060 Laptop GPU",
            "backlit_keyboard": "",
            "thunderbolt": "",
        }
    ]


@pytest.fixture
def sample_benchmark_data():
    return [
        {"cpu": "AMD A10 PRO-7850B APU", "score": 3441.0},
        {"cpu": "Intel Core i9-13900K", "score": 60000.0},
    ]


@patch("src.database.create_client")
def test_init_success(mock_create_client, mock_env):
    manager = SupabaseManager()

    assert manager.url == "https://fake.supabase.co"
    assert manager.key == "random-key-456"
    mock_create_client.assert_called_once_with(
        "https://fake.supabase.co", "random-key-456"
    )


def test_init_fails_without_env(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)

    with pytest.raises(ValueError, match="SUPABASE Credentials not initialized"):
        SupabaseManager()


@patch("src.database.create_client")
def test_insert_items_success(mock_create_client, mock_env, sample_scraped_items):
    manager = SupabaseManager()
    mock_instance = mock_create_client.return_value

    expected_response = MagicMock()
    expected_response.data = [{"id": 101, "status": "inserted"}]
    mock_instance.table.return_value.insert.return_value.execute.return_value = (
        expected_response
    )

    response = manager.insert_bulk_from_dict("items", sample_scraped_items)

    assert response == expected_response

    # check if data structure passed correctly
    called_args = mock_instance.table.return_value.insert.call_args[0][0]
    assert called_args[0]["item_name"] == "MSI CROSSHAIR A16"
    assert called_args[0]["price"] == 1499.99


@patch("src.database.create_client")
def test_insert_benchmarks_success(mock_create_client, mock_env, sample_benchmark_data):
    manager = SupabaseManager()
    mock_instance = mock_create_client.return_value

    manager.insert_bulk_from_dict("cpu_benchmark", sample_benchmark_data)

    mock_instance.table.assert_called_with("cpu_benchmark")
    args, _ = mock_instance.table.return_value.insert.call_args
    assert args[0][0]["cpu"] == "AMD A10 PRO-7850B APU"
    assert args[0][0]["score"] == 3441.0


@patch("src.database.create_client")
def test_get_table_wrapper(mock_create_client, mock_env):
    # arrange
    manager = SupabaseManager()
    mock_instance = mock_create_client.return_value

    # act
    manager.table("items")

    # assert
    mock_instance.table.assert_called_once_with("items")
