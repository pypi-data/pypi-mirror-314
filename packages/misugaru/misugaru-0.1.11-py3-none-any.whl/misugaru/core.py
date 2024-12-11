__all__ = ['N_FOLDS', 'MAX_WORKERS', 'RNG', 'TEST_FDR']

import numpy as np

N_FOLDS = 3
MAX_WORKERS = 8
RNG = np.random.default_rng(42)
TEST_FDR = 0.01

