"""EMO-Core: metric functions used by the analyses in `analysis/` and the weekly run."""

from importlib.metadata import PackageNotFoundError, version

from emo.gwi import compute_gwi
from emo.info_time import compute_information_time
from emo.smf import compute_smf
from emo.synergy import compute_gaussian_synergy

try:
    __version__ = version("emo-core")
except PackageNotFoundError:  # local checkout without installation
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "compute_gaussian_synergy",
    "compute_gwi",
    "compute_information_time",
    "compute_smf",
]
