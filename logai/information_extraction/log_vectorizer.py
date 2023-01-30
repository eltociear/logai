#
# Copyright (c) 2023 Salesforce.com, inc.
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
    """Config class for Vectorizer. 
    """
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
    Implement Log Vectorizer to transform raw log data to vectors. It Currently supports various statistical 
    (e.g. TfIdfVectorizer) and neural (Word2Vec, FastText, LogBERT) vectorizer models 
    """

    def __init__(self, config: VectorizerConfig):
        name = config.algo_name.lower()
        config_class = factory.get_config_class("vectorization", name)
        algorithm_class = factory.get_algorithm_class("vectorization", name)
        self.vectorizer = algorithm_class(
            config.algo_param if config.algo_param else config_class()
        )

    def fit(self, loglines: pd.Series):
        """fit method for LogVectorizer, to train the vectorizer model on the training data
        Args:
            loglines (pd.Series): pandas Series object containing the training raw log data 
        """
        self.vectorizer.fit(loglines)

    def transform(self, loglines: pd.Series) -> pd.Series:
        """transform method for LogVectorizer, to transform the raw log text data to vectors

        Args:
            loglines (pd.Series): pandas Series object containing the test raw log data 

        Returns:
            pd.Series: pandas Series object containing the vectorized log data 
        """
        return self.vectorizer.transform(loglines)
