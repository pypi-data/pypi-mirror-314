__all__ = ['RNG', 'N_FOLDS', 'train_models']

from joblib import Parallel, delayed
from typing import List
import copy
import numpy as np

from mokapot.model import PercolatorModel
from mokapot.brew import _fit_model

from .core import *
from .data import Data

RNG = np.random.default_rng(42)
N_FOLDS = 3

def train_models(
    data: Data,
    subset_max_train: int,
) -> List[PercolatorModel]:  
    
    model = PercolatorModel()
    model.rng = RNG
    psm_folds = data.get_train_psms_splits(n_subset=subset_max_train)
    
    # fitted looks like so:
    # `[(model_a: PercolatorModel, reset_a: bool), (model_b, reset_b), (model_c, reset_c)]`
    fitted = Parallel(n_jobs=N_FOLDS, require="sharedmem")(
        delayed(_fit_model)(x, [data.psms], copy.deepcopy(model), i)
        for i, x in enumerate(psm_folds)
    )
    # sort by fold for a deterministic order
    models, needs_reset = zip(*sorted(fitted, key=lambda x: x[0].fold))
    if any(needs_reset):
        # TODO: create specific exception
        raise ValueError("Model training failed")
    return models
