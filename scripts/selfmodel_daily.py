"""Session 3.6: H8 forecast caller, one ledger run per new stream run (inside the Action only).

    python scripts/selfmodel_daily.py run      # needs EMO_STREAM_KEY; ANTHROPIC_API_KEY optional
    python scripts/selfmodel_daily.py verify   # index lines match their encrypted files

Without ANTHROPIC_API_KEY the run still writes its ledger (training rows, and every eligible
card recorded as missed with reason "no key"); no forecast is written. Prints only counts and
paths: the Action logs of this public repository are public. Protocol:
docs/SELF_MODEL_PROTOCOL.md; code: emo/selfmodel/protocol.py, emo/selfmodel/ledger.py.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def states_for(root: Path, done: set[str], now: dt.datetime) -> list[dict]:
    """Card states as at each stream run not yet in a ledger (the last at `now`)."""
    from emo.stream.mirror import (
        build_cards_with_components,
        manifest_lines,
        source_gaps,
    )
    from emo.stream.store import read_run
    lines = manifest_lines(root)
    new = [i for i, m in enumerate(lines) if str(m["run_id"]) not in done]
    if not new:
        return []
    runs = [read_run(root / m["file"]) for m in lines[:new[-1] + 1]]
    out = []
    for i in new:
        last = i == new[-1]
        t = now if last else _run_time(lines[i])
        gaps = source_gaps(lines[:i + 1], t.date())
        cards, _, extra = build_cards_with_components(runs[:i + 1], t, gaps)
        out.append({"stream_run_id": str(lines[i]["run_id"]), "t": t,
                    "cards": list(zip(cards, extra, strict=True))})
    return out


def _run_time(m: dict) -> dt.datetime:
    for k in ("ended", "started"):
        if m.get(k):
            t = dt.datetime.fromisoformat(str(m[k]).replace("Z", "+00:00"))
            return t if t.tzinfo else t.replace(tzinfo=dt.UTC)
    rid = str(m["run_id"])                    # e.g. 2026-10-30T072241Z
    return dt.datetime.strptime(rid[:17], "%Y-%m-%dT%H%M%S").replace(tzinfo=dt.UTC)


def run(root: Path, now: dt.datetime, model_fn=None) -> dict | None:
    from emo.selfmodel import ledger as L
    from emo.selfmodel import protocol as P
    from emo.stream.store import KEY_ENV
    key = os.environ[KEY_ENV].encode()
    prior = L.merge([L.read_ledger(p) for p in L.ledger_files(root)])
    states = states_for(root, set(prior["stream_runs"]), now)
    if not states:
        print("no new stream run: nothing written")
        return None
    if model_fn is None and os.environ.get("ANTHROPIC_API_KEY"):
        api_key = os.environ["ANTHROPIC_API_KEY"]

        def model_fn(system, user):
            return L.call_model(system, user, api_key)
    protocol_sha = P.sha256((root / L.PROTOCOL_FILE).read_bytes())
    out = L.process(states, prior, now, model_fn, key, protocol_sha)
    rid = now.strftime("%Y-%m-%dT%H%M%SZ")
    line = L.write_ledger(root, out, rid)
    print(f"wrote {L.LEDGER_DIR / (rid + '.json.gz.enc')}; status {line['status']}; "
          f"forecasts {line['n_forecasts']} (total {line['forecasts_total']}); "
          f"missed {line['n_missed']}")
    return line


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "verify"])
    a = ap.parse_args(argv)
    if a.cmd == "verify":
        from emo.selfmodel.ledger import verify_index
        problems = verify_index(ROOT)
        print(f"index problems: {len(problems)}")
        return 1 if problems else 0
    run(ROOT, dt.datetime.now(dt.UTC))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 - a traceback could print a record value to a public log
        print(f"failed: {type(e).__name__} (message withheld: it may hold a record value)")
        sys.exit(1)
