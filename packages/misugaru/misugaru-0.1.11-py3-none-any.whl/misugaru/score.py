__all__ = ['score']

from pathlib import Path
from typing import List

from mokapot.model import PercolatorModel
from mokapot.brew import _predict_with_ensemble

from .data import Data
from .core import *

def score(data: Data, models: List[PercolatorModel]):          
    scores = _predict_with_ensemble(
        dataset=data.psms,
        models=models,
        max_workers=MAX_WORKERS,
    )
    return scores
