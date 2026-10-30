"""Session 3.4: field-presence check and daily card aggregates (run inside the Action only).

    python scripts/stream_cards.py presence   # -> data/mirror/field_presence.json
    python scripts/stream_cards.py cards      # -> data/mirror/aggregates.json

Needs EMO_STREAM_KEY. Prints nothing about records (Action logs of this public repository
are public); only the output path. Protocols: docs/FIELD_PRESENCE_CHECK.md,
docs/LOOP_CARD_PROTOCOL.md §10-§11.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("data/mirror")


def _write(name: str, obj: dict) -> None:
    p = ROOT / OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n")
    print(f"wrote {OUT / name}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["presence", "cards"])
    a = ap.parse_args(argv)
    from emo.stream.mirror import load_runs, manifest_lines
    now = dt.datetime.now(dt.UTC)
    if a.cmd == "presence":
        from emo.stream.presence import PRESENCE_VERSION, presence, verdicts
        agg = presence(load_runs(ROOT))
        _write("field_presence.json", {
            "version": PRESENCE_VERSION, "built_at": now.isoformat(timespec="seconds"),
            "runs_read": [m["run_id"] for m in manifest_lines(ROOT)],
            "protocol": "docs/FIELD_PRESENCE_CHECK.md", "groups": agg, "verdicts": verdicts(agg),
            "evidence_class": "infrastructure"})
        return 0
    from emo.stream.mirror import aggregates
    _write("aggregates.json", aggregates(ROOT, now))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 - a traceback could print a record value to a public log
        print(f"failed: {type(e).__name__} (message withheld: it may hold a record value)")
        sys.exit(1)
