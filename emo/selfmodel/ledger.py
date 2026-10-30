"""H8 forecast caller and ledger (session 3.6; docs/SELF_MODEL_PROTOCOL.md §2-§5, §8).

Runs only inside the GitHub Action "Self-model daily", after Mirror daily, holding
EMO_STREAM_KEY (and ANTHROPIC_API_KEY when Adrian has added it). Every protocol rule comes
from emo/selfmodel/protocol.py; this module only applies it run by run:

- one ledger run per new stream run; card state as at that run (snapshot replay);
- training rows (§5): each non-EU27 anchored card, at its earliest run where a target was
  eligible (any onset since the stream began), with its features at that run; used only
  once its outcome is known before the forecast time;
- forecasts (§2): every H8-eligible (card, target) at its earliest caller run, one stateless
  call each, until N_TARGET; a (card, target) is matched across runs by any shared node, so
  it is never forecast twice;
- an eligible (card, target) that cannot be sent (no key, or an account-level API error:
  authentication, permission, billing) is recorded as "missed" and never forecast later:
  the model was not asked. Any other failure (timeout, overload, rate limit after three
  attempts, unparseable or refused answer) is a forecast row with p_ai empty, scored 0.5
  (§4). This split is fixed here before any forecast is committed.

Output per run: one encrypted file under data/selfmodel/ledger/ and one public line in
data/selfmodel/ledger_index.csv (counts and hashes only, §4, §8.7). Nothing prints a record.
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import io
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from emo.selfmodel import protocol as P
from emo.stream import store

UTC = dt.UTC
LEDGER_DIR = Path("data/selfmodel/ledger")
INDEX = Path("data/selfmodel/ledger_index.csv")
PROTOCOL_FILE = Path("docs/SELF_MODEL_PROTOCOL.md")
LEDGER_VERSION = "ledger-0.1"

MODEL = "claude-haiku-5-5"                   # Adrian's choice, session 3.6 (STATUS)
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2026-10-21"                   # Messages API reference, opened 30 Oct 2026
MAX_TOKENS = 16000                           # adaptive thinking counts toward it
API_SETTINGS = {"model": MODEL, "max_tokens": MAX_TOKENS, "temperature": "omitted (the "
                "model does not accept it)", "thinking": "default (adaptive)",
                "effort": "default", "tools": "none", "anthropic_version": API_VERSION}
ACCOUNT_ERRORS = {401, 402, 403}
RETRY_STATUS = {408, 429, 500, 502, 503, 504, 529}

INDEX_FIELDS = ("ledger_run_id", "run_utc", "stream_runs", "status", "n_forecasts",
                "n_ai_unusable", "n_missed", "forecasts_total", "n_train_D", "n_train_B",
                "run_digest", "sha256_cipher", "model_requested", "model_returned",
                "prompt_version", "prompt_sha256", "protocol_sha256")


# --- card state -------------------------------------------------------------------------
def _t(s):
    return P._t(s)


def cluster(card: dict) -> str:
    """§6 cluster: ISO3 set, hazard, onset month (LOOP_CARD_PROTOCOL §9)."""
    return f"{'+'.join(card.get('iso3') or [])}|{card.get('hazard')}|{(card.get('onset') or '')[:7]}"


def training_targets(card: dict, now: dt.datetime) -> list[str]:
    """§5: targets eligible at `now` for a training row: §2 rules without the onset and
    earliest-seen dates (any onset since the stream began) and without the forecast cap."""
    if card.get("eu27") or card.get("closed") or not card.get("anchored"):
        return []
    if _t(card.get("onset")) is None:
        return []
    r = card.get("rungs", {})
    out = []
    if r.get("D") == "not yet":
        out.append("D")
    if r.get("D") == "present" and r.get("B") == "not yet":
        out.append("B")
    return [t for t in out if (P.window_end(card, t) or now) > now]


def features(card: dict, target: str, now: dt.datetime) -> dict:
    """§5 features of one (card, target) at `now`: the payload's hazard, stage, days."""
    p = P.payload(card, target, now)
    return {"hazard": p["hazard"], "stage": int(card.get("stage") or 0),
            "days": float(p["days_since_reference"])}


class Seen:
    """Node keys already used per (kind, target); a card sharing any node is the same card."""

    def __init__(self):
        self.keys: dict = {}

    def has(self, kind: str, target: str, comp) -> bool:
        return bool(self.keys.get((kind, target), set()) & set(comp))

    def add(self, kind: str, target: str, comp) -> None:
        self.keys.setdefault((kind, target), set()).update(comp)


def match(comp, states: list[tuple[dict, dict]]):
    """The current card sharing a node with `comp` (largest overlap), or None."""
    best, score = None, 0
    s = set(comp)
    for card, extra in states:
        k = len(s & set(extra["component"]))
        if k > score:
            best, score = card, k
    return best


# --- model call -------------------------------------------------------------------------
def call_model(system: str, user: str, api_key: str, timeout: int = 120) -> dict:
    """One stateless Messages API call. Returns {'kind': 'answer'|'failed'|'account',
    'model_returned', 'response_id', 'response_text', 'error'} (error: class only)."""
    body = json.dumps({"model": MODEL, "max_tokens": MAX_TOKENS, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json", "anthropic-version": API_VERSION,
        "Authorization": f"Bearer {api_key}"})
    err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                obj = json.loads(r.read())
            text = "".join(b.get("text", "") for b in obj.get("content", [])
                           if b.get("type") == "text") or None
            return {"kind": "answer", "model_returned": obj.get("model"),
                    "response_id": obj.get("id"), "response_text": text,
                    "error": None if text else f"no text (stop_reason {obj.get('stop_reason')})"}
        except urllib.error.HTTPError as e:
            if e.code in ACCOUNT_ERRORS:
                return {"kind": "account", "model_returned": None, "response_id": None,
                        "response_text": None, "error": f"HTTP {e.code}"}
            err = f"HTTP {e.code}"
            if e.code not in RETRY_STATUS:
                break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            err = type(e).__name__
        time.sleep(10 * (attempt + 1))
    return {"kind": "failed", "model_returned": None, "response_id": None,
            "response_text": None, "error": err}


def coherent_whole(text: str | None) -> str | None:
    if not text:
        return None
    try:
        obj = json.loads(text.strip().strip("`").removeprefix("json").strip())
        v = obj.get("coherent_whole") if isinstance(obj, dict) else None
        return v if isinstance(v, str) else None
    except ValueError:
        return None


# --- one ledger run -------------------------------------------------------------------
def process(states: list[dict], prior: dict, now: dt.datetime, model_fn, key: bytes,
            protocol_sha: str) -> dict:
    """states: new stream runs in order, each {'stream_run_id', 't', 'cards': [(card, extra)]};
    the last is the current state (its 't' is the caller time `now`). prior: merged earlier
    ledgers (`merge`). model_fn(system, user) -> call_model-like dict, or None (no key)."""
    seen = Seen()
    for s in prior["snapshots"]:
        seen.add("train", s["target"], s["component"])
    for f in prior["forecasts"]:
        seen.add("h8", f["target"], prior["components"][f["forecast_id"]])
    for m in prior["missed"]:
        seen.add("h8", m["target"], m["component"])
    snapshots, missed, forecasts, comps = [], [], [], {}
    n_total = len(prior["forecasts"])
    account_down = False
    for i, st in enumerate(states):
        t = st["t"]
        current = i == len(states) - 1
        for card, extra in st["cards"]:
            for tg in training_targets(card, t):
                if not seen.has("train", tg, extra["component"]):
                    seen.add("train", tg, extra["component"])
                    snapshots.append({"component": extra["component"], "target": tg,
                                      "t": t.isoformat(), "stream_run_id": st["stream_run_id"],
                                      **features(card, tg, t)})
        todo = []
        for card, extra in st["cards"]:
            fs = extra["first_seen"] or t
            for tg in P.eligible_targets(card, t, fs, n_total):
                if not seen.has("h8", tg, extra["component"]):
                    seen.add("h8", tg, extra["component"])
                    todo.append((P.forecast_id(card["card_id"], tg, key), tg, card, extra))
        for fid, tg, card, extra in sorted(todo, key=lambda x: x[0]):
            if n_total >= P.N_TARGET:
                break
            reason = ("no caller run" if not current else "no key" if model_fn is None
                      else "api_unavailable" if account_down else None)
            if reason is None:
                row, kind = forecast(card, extra, tg, fid, t, prior, snapshots, states,
                                     model_fn, protocol_sha)
                if kind == "account":
                    account_down, reason = True, "api_unavailable"
                else:
                    forecasts.append(row)
                    comps[fid] = extra["component"]
                    n_total += 1
                    continue
            missed.append({"component": extra["component"], "target": tg, "t": t.isoformat(),
                           "reason": reason})
    status = ("forecasts" if forecasts else "no key" if model_fn is None and missed else
              "api_unavailable" if account_down else "no eligible card")
    return {"version": LEDGER_VERSION, "run_utc": now.isoformat(timespec="seconds"),
            "stream_runs": [s["stream_run_id"] for s in states], "status": status,
            "api_settings": API_SETTINGS, "forecasts": forecasts, "components": comps,
            "snapshots": snapshots, "missed": missed, "forecasts_total": n_total,
            "protocol_sha256": protocol_sha}


def training_rows(target: str, now: dt.datetime, snapshots: list[dict],
                  current: list[tuple[dict, dict]]) -> list[dict]:
    """§5: snapshots of `target` taken before `now` whose outcome (§6 rule, current card
    state) is known before `now`."""
    rows = []
    for s in snapshots:
        if s["target"] != target or _t(s["t"]) >= now:
            continue
        card = match(s["component"], current)
        if card is None:
            continue
        y = P.outcome(card, target, _t(s["t"]))
        if y is None:
            continue
        rows.append({"hazard": s["hazard"], "stage": s["stage"], "days": s["days"], "y": y})
    return rows


def forecast(card, extra, tg, fid, now, prior, new_snaps, states, model_fn, protocol_sha):
    current = states[-1]["cards"]
    train = training_rows(tg, now, prior["snapshots"] + new_snaps, current)
    ys = [r["y"] for r in train]
    p_base = P.base_rate(ys) if ys else 0.5
    p_logit = P.predict(P.fit_logistic(train), features(card, tg, now)) if train else 0.5
    system, user = P.prompt(card, tg, now)
    ans = model_fn(system, user)
    if ans["kind"] == "account":
        return None, "account"
    text = ans["response_text"]
    row = P.ledger_row(
        forecast_id=fid, card_id=card["card_id"], target=tg,
        forecast_utc=now.isoformat(timespec="seconds"),
        window_end_utc=P.window_end(card, tg).isoformat(timespec="seconds"),
        cluster=cluster(card), payload=P.payload(card, tg, now),
        prompt_version=P.PROMPT_VERSION, prompt_sha256=P.prompt_sha256(),
        model_requested=MODEL, model_returned=ans["model_returned"],
        response_id=ans["response_id"], response_text=text if text else ans["error"],
        p_ai=P.parse_probability(text), coherent_whole=coherent_whole(text),
        p_base=round(p_base, 6), p_logit=round(p_logit, 6), baseline_train_n=len(train),
        protocol_sha256=protocol_sha)
    return row, ans["kind"]


# --- files ----------------------------------------------------------------------------
def ledger_files(root: Path) -> list[Path]:
    d = root / LEDGER_DIR
    return sorted(d.glob("*.json.gz.enc")) if d.exists() else []


def read_ledger(path: Path) -> dict:
    return json.loads(gzip.decompress(store.decrypt(path.read_bytes())))


def merge(ledgers: list[dict]) -> dict:
    out: dict = {"forecasts": [], "components": {}, "snapshots": [], "missed": [],
                 "stream_runs": []}
    for lg in ledgers:
        for k in ("forecasts", "snapshots", "missed", "stream_runs"):
            out[k] += lg[k]
        out["components"].update(lg["components"])
    return out


def read_index(root: Path) -> list[dict]:
    p = root / INDEX
    if not p.exists():
        return []
    return list(csv.DictReader(io.StringIO(p.read_text())))


def write_ledger(root: Path, run: dict, ledger_run_id: str) -> dict:
    """Encrypt the run, write it (append-only), append its public index line."""
    plain = gzip.compress(store.canonical(run), mtime=0)
    cipher = store.encrypt(plain)
    rel = LEDGER_DIR / f"{ledger_run_id}.json.gz.enc"
    path = root / rel
    if path.exists():
        raise FileExistsError(f"append-only: {rel} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(cipher)
    fc = run["forecasts"]
    line = {
        "ledger_run_id": ledger_run_id, "run_utc": run["run_utc"],
        "stream_runs": ";".join(run["stream_runs"]), "status": run["status"],
        "n_forecasts": len(fc), "n_ai_unusable": sum(r["p_ai"] is None for r in fc),
        "n_missed": len(run["missed"]), "forecasts_total": run["forecasts_total"],
        "n_train_D": sum(s["target"] == "D" for s in run["snapshots"]),
        "n_train_B": sum(s["target"] == "B" for s in run["snapshots"]),
        "run_digest": P.run_digest(fc) if fc else "", "sha256_cipher": store.sha256(cipher),
        "model_requested": MODEL,
        "model_returned": ";".join(sorted({str(r["model_returned"]) for r in fc
                                           if r["model_returned"]})),
        "prompt_version": P.PROMPT_VERSION, "prompt_sha256": P.prompt_sha256(),
        "protocol_sha256": run.get("protocol_sha256", ""),
    }
    ip = root / INDEX
    new = not ip.exists()
    with open(ip, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=INDEX_FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow(line)
    return line


def verify_index(root: Path) -> list[str]:
    """Every index line matches its encrypted file (hash) and its digest (rows)."""
    problems = []
    for line in read_index(root):
        p = root / LEDGER_DIR / f"{line['ledger_run_id']}.json.gz.enc"
        if not p.exists():
            problems.append(f"{line['ledger_run_id']}: file missing")
            continue
        if store.sha256(p.read_bytes()) != line["sha256_cipher"]:
            problems.append(f"{line['ledger_run_id']}: cipher hash differs")
            continue
        lg = read_ledger(p)
        dg = P.run_digest(lg["forecasts"]) if lg["forecasts"] else ""
        if dg != line["run_digest"]:
            problems.append(f"{line['ledger_run_id']}: digest differs")
    return problems

