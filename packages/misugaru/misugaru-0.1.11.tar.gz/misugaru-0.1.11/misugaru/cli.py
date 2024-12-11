__all__ = ['main']

from pathlib import Path
import typer

from .data import Data
from .train import train_models
from .score import score
from .confidence import confidence
from .core import *


app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    path_psm: Path = typer.Argument(..., help="Path to PSM parquet file"),
    out_dir: Path = typer.Argument(..., help="Output directory"),
    subset_max_train: int = typer.Option(10000, help="Maximum number of training examples to train PercolatorModels"),
):
    """Train a PercolatorModel on a subset of the given PSMs, then score all PSMs and estimate confidence values."""
    if ctx.invoked_subcommand is None:
        data = Data(path_psm)
        models = train_models(data, subset_max_train=subset_max_train)
        scores = score(data, models)
        confidence(scores, data, out_dir)

@app.command()
def train(
    path_psm: Path = typer.Argument(..., help="Path to PSM parquet file"),
    out_dir: Path = typer.Argument(..., help="Output directory"),
    subset_max_train: int = typer.Option(10000, help="Maximum number of training examples to train PercolatorModels"),
):
    """Train a PercolatorModel on a subset of the given PSMs, and save the model to the given output directory."""
    data = Data(path_psm)
    models = train_models(data, subset_max_train=subset_max_train)
    print(models[0], out_dir)


