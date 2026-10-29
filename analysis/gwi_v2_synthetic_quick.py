"""Quick GWI v2 synthetic check for the weekly frozen runs (session 2.6 review).

Runs analysis/gwi_v2_synthetic.py with --quick (~1 min); its output is frozen in
analysis/gwi_v2_synthetic_quick_output.txt, so any change to emo/gwi_v2.py that alters the
method shows up in the weekly run before the 2027-11-15 scoring.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "--quick"]
runpy.run_path(str(Path(__file__).with_name("gwi_v2_synthetic.py")), run_name="__main__")
