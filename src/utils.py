import logging
import re
import sys
from typing import List

import numpy as np
import pandas as pd
import rapidfuzz as rf
from sklearn.preprocessing import MinMaxScaler

LOG_FORMAT = "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"


def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger


def fuzzy_search_mark(value: str, lookup: pd.DataFrame, extract: str, threshold=55):
    if pd.isna(value) or value == "":
        return np.nan

    match = rf.process.extractOne(
        value, lookup[extract], scorer=rf.fuzz.token_sort_ratio
    )

    if match:
        _, score, idx = match
        if score >= threshold:
            return float(lookup.loc[idx, f"{extract}_mark"])

    return np.nan


def min_max_scaling(feat: np.ndarray):
    scaler = MinMaxScaler()
    feat = scaler.fit_transform(feat.reshape(-1, 1))

    return feat.flatten()


def process_brand(item_names: pd.Series, input_brands: List[str]):
    def check_brand(x):
        for brand in input_brands:
            if brand in x:
                return 1.0

        return 0.0

    item_names = item_names.str.lower()
    feat = item_names.apply(check_brand).to_numpy()

    return feat


def process_memory(memory: pd.Series):
    memory = memory.str.extract(r"(\d+)").astype(float)
    median_val = memory.median()
    feat = memory.fillna(median_val).to_numpy()
    feat = min_max_scaling(feat)

    return feat


def process_cpu(cpu_name: pd.Series, cpu_lookup: pd.DataFrame):
    feat = cpu_name.apply(lambda x: fuzzy_search_mark(x, cpu_lookup, extract="cpu"))

    median_val = feat.median()
    feat = feat.fillna(median_val).to_numpy()
    feat = min_max_scaling(feat)

    return feat


def process_gpu(gpu_name: pd.Series, gpu_lookup: pd.DataFrame):
    feat = gpu_name.apply(lambda x: fuzzy_search_mark(x, gpu_lookup, extract="gpu"))

    median_val = feat.median()
    feat = feat.fillna(median_val).to_numpy()

    feat = min_max_scaling(feat)

    return feat


def process_storage(storage: pd.Series):
    def clean_storage(x):
        if pd.isna(x) or x == "":
            return np.nan

        x = str(x).lower()
        mul = 1000 if "tb" in x else 1

        match = re.search(r"(\d+)", x)

        if match:
            return float(match.group(1)) * mul
        else:
            return np.nan

    feat = storage.apply(clean_storage)
    mode_val = feat.mode()
    feat = feat.fillna(mode_val).to_numpy()
    feat = min_max_scaling(feat)

    return feat


def process_resolution(resolution: pd.Series):
    def encode_resolution(value):
        base = 1.0 / 5

        if pd.isna(value) or value == "":
            return base * 3  # FHD

        match = re.search(r"(\d+)", value)

        if match:
            reso = int(match.group(1))

            if reso <= 1280:
                value = base * 1  # SD
            elif reso <= 1600:
                value = base * 2  # HD
            elif reso <= 2200:
                value = base * 3  # FHD
            elif reso <= 3200:
                value = base * 4  # QHD
            else:
                value = base * 5  # UHD

        return value

    feat = resolution.apply(encode_resolution).to_numpy()

    return feat


def process_portability(weight: pd.Series):
    def clean_weight(x):
        if pd.isna(x) or x == "":
            return np.nan

        x = str(x).lower()
        matches = re.findall(r"(\d+(?:\.\d+)?)", x)

        if len(matches) == 2:
            low = float(matches[0])
            high = float(matches[1])
            return (low + high) / 2

        elif len(matches) == 1:
            return float(matches[0])

        else:
            return np.nan

    feat = weight.apply(clean_weight)
    median_val = feat.median()
    feat = feat.fillna(median_val)
    feat = feat.apply(lambda x: 1 / x).to_numpy()

    return feat


def process_size(screen_size: pd.Series):
    def encode_size(x):
        base = 1.0 / 3

        if pd.isna(x) or x == "":
            return base * 2  # medium

        match = re.search(r"\d+\.\d+", x)
        if match:
            x = float(match.group())

            if x <= 13:
                return base * 1  # small
            elif x <= 16:
                return base * 2  # medium
            else:
                return base * 3  # large

        return base * 2  # medium

    feat = screen_size.apply(encode_size).to_numpy()

    return feat


def process_extra_feat(extra_feat: pd.DataFrame):
    def is_available(x):
        if pd.isna(x) or x == "" or "non" in x.lower() or "no" in x.lower():
            return 0
        else:
            return 1

    feat_list = [
        "webcam",
        "thunderbolt",
        "backlit_keyboard",
        "card_reader",
        "touchscreen",
    ]

    columns = extra_feat.columns.to_list()
    assert columns == feat_list, "Wrong feature list for extra feature"

    for col in columns:
        extra_feat.loc[:, col] = extra_feat[col].apply(is_available)

    feat = extra_feat.to_numpy()

    return feat


def price_decay(price: float, budget, alpha=0.001):
    return 1 / np.exp(alpha * max(0, price - budget))
