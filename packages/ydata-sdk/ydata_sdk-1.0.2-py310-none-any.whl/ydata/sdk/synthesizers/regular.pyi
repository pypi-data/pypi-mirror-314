from pandas import DataFrame as pdDataFrame
from typing import Dict, List, Optional, Union
from ydata.datascience.common import PrivacyLevel
from ydata.sdk.datasources import DataSource
from ydata.sdk.datasources._models.metadata.data_types import DataType
from ydata.sdk.synthesizers.synthesizer import BaseSynthesizer

class RegularSynthesizer(BaseSynthesizer):
    def sample(self, n_samples: int = ..., condition_on: Optional[dict] = ...) -> pdDataFrame: ...
    def fit(self, X: Union[DataSource, pdDataFrame], privacy_level: PrivacyLevel = ..., entities: Optional[Union[str, List[str]]] = ..., generate_cols: Optional[List[str]] = ..., exclude_cols: Optional[List[str]] = ..., dtypes: Optional[Dict[str, Union[str, DataType]]] = ..., target: Optional[str] = ..., anonymize: Optional[dict] = ..., condition_on: Optional[List[str]] = ...) -> None: ...
