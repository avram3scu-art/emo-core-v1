"""Session 3.6: H8 scoring, once only (docs/SELF_MODEL_PROTOCOL.md §6). Inside the Action only.

    python scripts/selfmodel_score.py     # -> data/selfmodel/h8_score.json, or refuses

Refuses (exit 2, nothing written) while protocol.may_score() is false. Needs EMO_STREAM_KEY.
Prints only the verdict or the refusal: the Action logs of this public repository are public.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("data/selfmodel/h8_score.json")


def main(root: Path = ROOT, now: dt.datetime | None = None) -> int:
    from emo.selfmodel import ledger as L
    from emo.selfmodel.score import ScoringRefused, score
    from emo.stream.mirror import (
        build_cards_with_components,
        load_runs,
        manifest_lines,
        source_gaps,
    )
    now = now or dt.datetime.now(dt.UTC)
    if (root / OUT).exists():
        print("refused: H8 was already scored (once only)")
        return 2
    ledgers = L.merge([L.read_ledger(p) for p in L.ledger_files(root)])
    ends = [L._t(f["window_end_utc"]) for f in ledgers["forecasts"]]
    from emo.selfmodel.protocol import may_score
    if not may_score(now.date(), ends, len(ledgers["forecasts"])):
        print("refused: may_score() is false")
        return 2
    gaps = source_gaps(manifest_lines(root), now.date())
    cards, _, extra = build_cards_with_components(load_runs(root), now, gaps)
    try:
        res = score(ledgers, list(zip(cards, extra, strict=True)), now.date())
    except ScoringRefused:
        print("refused: may_score() is false")
        return 2
    (root / OUT).write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    print(f"wrote {OUT}; verdict {res['pooled']['verdict']}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 - a traceback could print a record value
        print(f"failed: {type(e).__name__} (message withheld)")
        sys.exit(1)
