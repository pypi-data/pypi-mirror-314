__all__ = ['Data']

from functools import cached_property
from pathlib import Path
from pandas import DataFrame
import numpy as np

from mokapot.constants import CHUNK_SIZE_READ_ALL_DATA
from mokapot.dataset import (
    OnDiskPsmDataset,
)
from mokapot.parsers.pin import parse_in_chunks, read_percolator
from mokapot.brew import make_train_sets

from .core import *


class Data:
    def __init__(self, psm_file: Path):
        self.psms: OnDiskPsmDataset = read_percolator(psm_file, max_workers=MAX_WORKERS)
        if not self.size > 1:
            raise ValueError("Dataset contains no PSMs")
    
    def get_train_psms_splits(self, n_subset: int) -> [DataFrame, DataFrame, DataFrame]:

        # Mokapot functions often expect lists of datasets
        train_idx = list(make_train_sets(
            test_idx=[self.fold_idx],  # expects list
            subset_max_train=n_subset,
            data_size=[self.size],  # expects list
            rng=RNG,
        ))
        fold_a, fold_b, fold_c = parse_in_chunks(
            datasets=[self.psms],  # expects list
            train_idx=train_idx,
            chunk_size=CHUNK_SIZE_READ_ALL_DATA,
            max_workers=MAX_WORKERS, 
        )
        del train_idx
        return fold_a, fold_b, fold_c 

    @cached_property
    def fold_idx(self):
        return self.psms._split(N_FOLDS, RNG)
    
    @cached_property
    def n_decoys(self) -> np.int64:
        return (~self.psms.spectra_dataframe[self.psms.target_column]).sum()

    @cached_property
    def n_targets(self) -> np.int64:
        return (self.psms.spectra_dataframe[self.psms.target_column]).sum()

    @cached_property
    def size(self) -> np.int64:
        return len(self.psms.spectra_dataframe)
