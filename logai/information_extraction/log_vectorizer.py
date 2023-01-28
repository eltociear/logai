#
# Copyright (c) 2022 Salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
#
import pandas as pd
from attr import dataclass

from logai.config_interfaces import Config
from logai.algorithms.factory import factory


@dataclass
class VectorizerConfig(Config):
    algo_name: str = "word2vec"
    algo_param: object = None
    custom_param: object = None

    @classmethod
    def from_dict(cls, config_dict):
        config = super(VectorizerConfig, cls).from_dict(config_dict)
        config.algo_param = factory.get_config(
            "vectorization", config.algo_name.lower(), config.algo_param
        )
        return config


class LogVectorizer:
    """
    Implement Log Vectorizer. Support Word2Vec and FastText vectorization.
    """

    def __init__(self, config: VectorizerConfig):
        name = config.algo_name.lower()
        config_class = factory.get_config_class("vectorization", name)
        algorithm_class = factory.get_algorithm_class("vectorization", name)
        self.vectorizer = algorithm_class(
            config.algo_param if config.algo_param else config_class()
        )

    def fit(self, loglines: pd.Series):
        self.vectorizer.fit(loglines)

    def transform(self, loglines: pd.Series) -> pd.Series:
        return self.vectorizer.transform(loglines)
