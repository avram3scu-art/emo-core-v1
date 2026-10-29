"""Daily run of the global hazard stream (session 3.2; .github/workflows/stream_daily.yml).

  python scripts/stream_daily.py run              fetch all sources, write one encrypted run
  python scripts/stream_daily.py ran-today        exit 0 if a run dated today (UTC) exists
  python scripts/stream_daily.py verify           append-only check of staged changes
  python scripts/stream_daily.py counts [--out F] monthly counts from the log (needs the key)

Output never contains record content, record counts or sizes (E1: nothing can reveal what
was dropped). A source that fails is written with its error and the others are kept; the
exit code is then 2, after the run is written, so the commit still happens and the failure
shows in the Actions list.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from emo.stream import store  # noqa: E402
from emo.stream.counts import monthly_counts  # noqa: E402
from emo.stream.fetchers import FETCHERS, Http  # noqa: E402


def run(root: Path = ROOT) -> int:
    store._key_env()                       # refuse before any request if no key
    started = dt.datetime.now(dt.UTC)
    run_id = started.strftime("%Y-%m-%dT%H%M%SZ")
    today = started.date()
    sources, failed = {}, []
    for name, fetch in FETCHERS.items():
        http = Http()
        try:
            recs, err = fetch(http, today), None
            if not recs:                   # every source has records in any 7-day window
                err = "EmptyResponse"
                failed.append(name)
        except Exception as e:             # keep the other sources
            recs, err = [], f"{type(e).__name__}"
            failed.append(name)
        sources[name] = {"records": recs, "requests": http.log, "error": err}
        print(f"{name}: {'ok' if err is None else 'error ' + err}")
    meta = {"run_id": run_id, "started": started.isoformat(),
            "ended": dt.datetime.now(dt.UTC).isoformat(), "code_version": "stream-0.2"}
    line = store.write_run(root, meta, sources)
    print(f"wrote {line['file']} sha256 {line['sha256_cipher']}")
    return 2 if failed else 0


def ran_today(root: Path = ROOT) -> int:
    man = root / store.STREAM_DIR / store.MANIFEST
    today = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    if man.exists() and any(json.loads(x)["run_id"].startswith(today)
                            for x in man.read_text().splitlines() if x.strip()):
        return 0
    return 1


def verify(root: Path = ROOT) -> int:
    problems = store.verify_append_only(root)
    for p in problems:
        print("append-only:", p)
    return 1 if problems else 0


def counts(root: Path = ROOT, out: str | None = None) -> int:
    runs = [store.read_run(p)
            for p in sorted((root / store.STREAM_DIR / "log").glob("*.json.gz.enc"))]
    res = {"runs": len(runs), "monthly": monthly_counts(runs)}
    text = json.dumps(res, indent=1, sort_keys=True)
    if out:
        Path(out).write_text(text + "\n")
    print(text)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "ran-today", "verify", "counts"])
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "counts":
        return counts(out=a.out)
    return {"run": run, "ran-today": ran_today, "verify": verify}[a.cmd]()


if __name__ == "__main__":
    sys.exit(main())
