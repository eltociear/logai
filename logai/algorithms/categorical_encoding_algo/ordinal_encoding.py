#
# Copyright (c) 2023 Salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
#
import numpy as np
import pandas as pd
from attr import dataclass
from sklearn.preprocessing import OrdinalEncoder

from logai.algorithms.algo_interfaces import CategoricalEncodingAlgo
from logai.config_interfaces import Config


@dataclass
class OrdinalEncodingParams(Config):
    """
    Configuration of OrdinalEncoding.
    """

    categories: str = "auto"
    dtype: np.float64 = np.float64
    handle_unknown: str = "error"
    unknown_value: object = None


class OrdinalEncoding(CategoricalEncodingAlgo):
    """
    Implementation of ordinal encoder.
    """

    def __init__(self, params: OrdinalEncodingParams):
        self.model = OrdinalEncoder(
            categories=params.categories,
            dtype=params.dtype,
            handle_unknown=params.handle_unknown,
            unknown_value=params.unknown_value,
        )

    def fit_transform(self, log_attributes: pd.DataFrame) -> pd.DataFrame:
        """
        Fit and transform log attributes into ordinal encoding categories.
        :param log_attributes: list of log attributes in text format.
        :return: pd.DataFrame: ordinal encoding categories
        """
        self.model.fit(log_attributes)
        res_column_names = ["{}-categorical".format(c) for c in log_attributes.columns]
        res = pd.DataFrame(
            self.model.transform(log_attributes), index=log_attributes.index
        )
        res.columns = res_column_names
        return res
