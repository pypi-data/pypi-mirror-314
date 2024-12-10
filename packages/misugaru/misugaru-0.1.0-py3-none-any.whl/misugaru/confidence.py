__all__ = ['confidence']

from mokapot.confidence import assign_confidence
from pathlib import Path
from .data import Data
from .train import train_models
from .score import score
from .core import *

def confidence(scores, data: Data, dest_dir: Path, eval_fdr: float=0.01):
    assign_confidence(
        datasets=[data.psms],
        scores_list=[scores],
        max_workers=MAX_WORKERS,
        eval_fdr=eval_fdr,
        dest_dir=dest_dir,
        write_decoys=True,
        deduplication=False,
        do_rollup=True,
        prefixes=[""],
        rng=RNG,
        peps_error=False,
        peps_algorithm="hist_nnls",
        qvalue_algorithm="tdc",
        stream_confidence=True
    )
