from typing import Dict

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import (
    process_brand,
    process_cpu,
    process_extra_feat,
    process_gpu,
    process_memory,
    process_portability,
    process_resolution,
    process_size,
    process_storage,
    setup_logger,
)

logger = setup_logger(__name__)


class LaptopRecommender:
    def __init__(
        self, data: pd.DataFrame, cpu_lookup: pd.DataFrame, gpu_lookup: pd.DataFrame
    ):
        self.data = self._data_cleaning(data)

        self.cpu_lookup = cpu_lookup
        self.cpu_lookup["cpu"] = cpu_lookup.cpu.str.lower()

        self.gpu_lookup = gpu_lookup
        self.gpu_lookup["gpu"] = gpu_lookup.gpu.str.lower()

        self.usage_types = [
            "Personal",
            "Business",
            "Gaming",
            "Content Design",
            "Academy",
        ]

    def predict_top_k(self, user_input: Dict, laptop_embedding: np.ndarray, top_k=5):
        # Get input brands and add the vector to lookup emb
        user_brands = user_input["brands"]
        user_budget = user_input["budget"]
        brand_feat = process_brand(self.data.item_name, user_brands)
        user_lookup_emb = np.hstack((laptop_embedding, brand_feat.reshape(-1, 1)))

        # Calculate the price decay with the input budget
        price_decays = self.data.price.apply(
            lambda x: self._calculate_price_decay(x, user_budget)
        )

        # Calculate similarity (UsesVector, LaptopEmbedding)
        user_vec = self._generate_user_vector(**user_input)
        sim_scores = self._similarity_score(user_vec, user_lookup_emb)

        # Calculate overall score and sorting
        sim_scores = sim_scores * price_decays
        top_indices = sim_scores.argsort()[-top_k:][::-1]

        return self.data.iloc[top_indices], sim_scores[top_indices]

    def generate_lookup_embedding(self):
        # Specs component
        usage_df = pd.DataFrame(
            dict(
                cpu=process_cpu(self.data.cpu_type, self.cpu_lookup),
                gpu=process_gpu(self.data.gpu, self.gpu_lookup),
                memory=process_memory(self.data.memory),
                storage=process_storage(self.data.storage),
                resolution=process_resolution(self.data.resolution),
            )
        )
        usage_embedding = self._usage_classifier(usage_df)

        # Portability
        portability = process_portability(self.data.weight)

        # Screen size
        size = process_size(self.data.screen_size)

        # Additional features
        feat_list = [
            "webcam",
            "thunderbolt",
            "backlit_keyboard",
            "card_reader",
            "touchscreen",
        ]
        extra_feat = process_extra_feat(self.data[feat_list])

        feat_embedding = np.hstack(
            (
                usage_embedding,
                portability.reshape(-1, 1),
                size.reshape(-1, 1),
                extra_feat,
            )
        )

        return feat_embedding

    def _generate_user_vector(self, **kwargs):
        brand = np.array([1])
        usage_vec = self._encode_usage(kwargs["usage"])

        return np.concatenate(
            (
                usage_vec,
                np.array([kwargs["portability"]]),
                np.array([kwargs["size"]]),
                np.array(kwargs["extra"]),
                brand,
            )
        ).reshape(1, -1)

    def _data_cleaning(self, data: pd.DataFrame) -> pd.DataFrame:
        filter_features = [
            # brands
            "id",
            "item_name",
            # item pricing
            "price",
            # spces --> pricig
            "memory",
            "cpu_type",
            "gpu",
            "storage",
            "resolution",
            # portability
            "weight",
            # screen size
            "screen_size",
            # extra feat
            "backlit_keyboard",
            "touchscreen",
            "webcam",
            "thunderbolt",
            "card_reader",
        ]

        df = data[filter_features].copy()
        df = df.drop_duplicates(subset=["item_name"])
        df = df.dropna(subset=["price", "item_name"])

        return df.reset_index()

    def _usage_classifier(self, usage_df: pd.DataFrame) -> np.ndarray:
        def heuristic_classifier(x):
            if x.gpu >= 0.4:
                return "Gaming"

            if x.resolution > 0.6 and x.memory >= 0.45:
                return "Content Design"

            if x.cpu >= 0.25 and x.memory >= 0.2 and x.gpu < 0.4:
                return "Business"

            if x.cpu < 0.2:
                return "Academy"

            return "Personal"

        classified_usage = usage_df.apply(heuristic_classifier, axis=1)
        usage_embedding = classified_usage.apply(self._encode_usage).to_list()

        return np.stack(usage_embedding)

    def _encode_usage(self, usage_type: str) -> np.ndarray:
        vector = np.zeros(len(self.usage_types), dtype=int)

        try:
            idx = self.usage_types.index(usage_type)
            vector[idx] = 1
        except ValueError:
            logger.warning(
                f"Category {usage_type} not found. Returning zeros vector instead."
            )

        return vector

    def _calculate_price_decay(self, price: float, budget, alpha=0.001):
        return 1 / np.exp(alpha * max(0, price - budget))

    def _similarity_score(self, user_vector, laptop_embedding):
        scores = cosine_similarity(user_vector, laptop_embedding)[0]
        return scores
