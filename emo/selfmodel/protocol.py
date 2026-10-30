"""H8 self-model protocol in code (docs/SELF_MODEL_PROTOCOL.md). Every constant is part of it.

Nothing here calls a model or opens a stream record. Session 3.6 adds the caller, which runs
inside a GitHub Action holding EMO_STREAM_KEY and uses only these functions.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import math
import re

import numpy as np

UTC = dt.UTC

# --- §2 eligibility -------------------------------------------------------------------
CUTOFF_UTC = dt.datetime(2026, 10, 31, 0, 0, tzinfo=UTC)   # after the protocol commit
ONSET_LAST_UTC = dt.datetime(2027, 12, 1, 0, 0, tzinfo=UTC)  # onsets before 1 Dec 2027
N_TARGET = 120             # forecasting stops at the 120th forecast (or ONSET_LAST_UTC)
SCORE_LATEST = dt.date(2028, 4, 1)
TARGETS = ("D", "B")
HAZARDS = ("EQ", "TS", "TC", "FL", "VO", "DR", "WF")

# --- §5 baselines ---------------------------------------------------------------------
MIN_TRAIN, MIN_CLASS, MIN_HAZARD_ROWS, RIDGE = 20, 5, 5, 1.0

# --- §6 scoring -----------------------------------------------------------------------
ALPHA, MARGIN, MIN_N, MIN_CLUSTERS = 0.05, 0.01, 30, 20
N_FLIPS, N_BOOT, SCORE_SEED = 10_000, 10_000, 20261030
P_UNUSABLE = 0.5            # an unparseable, refused or missing AI answer is scored as 0.5

PROMPT_VERSION = "h8-v1"
SYSTEM_PROMPT = (
    "You are a forecasting model of how humanity's response systems behave after natural "
    "hazards. You describe; you do not recommend. Answer only with one JSON object."
)
USER_TEMPLATE = (
    "Event state (no names, no dates):\n{payload}\n\n"
    "Question: {question}\n"
    'Reply exactly as {{"p": <probability between 0 and 1>, "coherent_whole": '
    '"<one sentence: what a coherent whole that knows what humanity knows would do>"}}'
)
QUESTIONS = {
    "D": "What is the probability that an IFRC appeal (DREF or Emergency Appeal) or a "
         "Copernicus EMS activation is recorded for this event within {days_left} days?",
    "B": "What is the probability that IFRC money (a DREF or appeal funding above zero) is "
         "recorded for this event within {days_left} days?",
}


def _t(s):
    if s is None:
        return None
    t = dt.datetime.fromisoformat(s)
    return t if t.tzinfo else t.replace(tzinfo=UTC)


def window_end(card: dict, target: str):
    """End of the rung window (LOOP_CARD_PROTOCOL §5): D onset+60 d; B decision+60 d."""
    if target == "D":
        on = _t(card.get("onset"))
        return on + dt.timedelta(days=60) if on else None
    d = _t(card.get("t_decision"))
    return d + dt.timedelta(days=60) if d else None


def eligible_targets(card: dict, now: dt.datetime, first_seen: dt.datetime,
                     n_so_far: int = 0) -> list[str]:
    """§2: targets this card may be forecast for at `now` (once each, at the earliest such run)."""
    if card.get("eu27") or card.get("closed") or n_so_far >= N_TARGET:
        return []
    on = _t(card.get("onset"))
    if on is None or on < CUTOFF_UTC or on >= ONSET_LAST_UTC or first_seen < CUTOFF_UTC:
        return []
    if not card.get("anchored"):
        return []
    r = card.get("rungs", {})
    out = []
    if r.get("D") == "not yet":
        out.append("D")
    if r.get("D") == "present" and r.get("B") == "not yet":
        out.append("B")
    return [t for t in out if (window_end(card, t) or now) > now]


def payload(card: dict, target: str, now: dt.datetime) -> dict:
    """§3: the only data sent to the model. No identifier, title, date, value or record."""
    ref = _t(card["onset"]) if target == "D" else _t(card["t_decision"])
    days_left = (window_end(card, target) - now).total_seconds() / 86400
    rungs = card.get("rungs", {})
    return {
        "hazard": card.get("hazard"),
        "countries_iso3": sorted(card.get("iso3") or []),
        "stage_so_far": card.get("stage_label"),
        "rungs": {k: rungs.get(k) for k in ("W", "R", "D", "B")},
        "decision_systems": sorted(card.get("decision_systems") or []),
        "days_since_reference": round((now - ref).total_seconds() / 86400, 1),
        "reference": "onset" if target == "D" else "earliest decision record",
        "days_left": round(days_left, 1),
    }


def prompt(card: dict, target: str, now: dt.datetime) -> tuple[str, str]:
    p = payload(card, target, now)
    q = QUESTIONS[target].format(days_left=int(math.floor(p["days_left"])))
    return SYSTEM_PROMPT, USER_TEMPLATE.format(payload=canonical(p), question=q)


def prompt_sha256() -> str:
    return sha256(canonical({"v": PROMPT_VERSION, "s": SYSTEM_PROMPT, "u": USER_TEMPLATE,
                             "q": QUESTIONS}))


_NUM = re.compile(r'"p"\s*:\s*([0-9]*\.?[0-9]+(?:[eE][-+]?\d+)?)')


def parse_probability(text: str | None) -> float | None:
    """§4: p from the reply; None (scored as 0.5) unless one number in [0, 1] is found."""
    if not text:
        return None
    try:
        obj = json.loads(text.strip().strip("`").removeprefix("json").strip())
        p = obj.get("p") if isinstance(obj, dict) else None
        p = float(p) if isinstance(p, int | float) and not isinstance(p, bool) else None
    except (ValueError, AttributeError):
        m = _NUM.findall(text)
        p = float(m[0]) if len(m) == 1 else None
    return p if p is not None and 0.0 <= p <= 1.0 and math.isfinite(p) else None


def may_score(today: dt.date, window_ends: list[dt.datetime], n_forecasts: int) -> bool:
    """§6: one scoring only, after every window has closed (+7 days for late records) and
    either the target is reached or forecasting has ended; never before 1 Apr 2028 otherwise."""
    if not window_ends:
        return False
    closed = today >= (max(window_ends) + dt.timedelta(days=7)).date()
    ended = n_forecasts >= N_TARGET or today >= SCORE_LATEST
    return closed and ended


# --- §4 ledger --------------------------------------------------------------------------
def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(s: str | bytes) -> str:
    return hashlib.sha256(s.encode() if isinstance(s, str) else s).hexdigest()


def forecast_id(card_id: str, target: str, key: bytes) -> str:
    """Keyed hash: stable per (card, target), not reversible without EMO_STREAM_KEY."""
    return hmac.new(key, f"{card_id}|{target}".encode(), hashlib.sha256).hexdigest()[:32]


LEDGER_FIELDS = ("forecast_id", "card_id", "target", "forecast_utc", "window_end_utc",
                 "cluster", "payload", "prompt_version", "prompt_sha256", "model_requested",
                 "model_returned", "response_id", "response_text", "p_ai", "coherent_whole",
                 "p_base", "p_logit", "baseline_train_n", "protocol_sha256")


def ledger_row(**kw) -> dict:
    missing = set(LEDGER_FIELDS) - set(kw)
    if missing:
        raise ValueError(f"ledger row lacks {sorted(missing)}")
    row = {k: kw[k] for k in LEDGER_FIELDS}
    row["row_sha256"] = sha256(canonical(row))
    return row


def run_digest(rows: list[dict]) -> str:
    """Public commitment for one run: hash of the sorted row hashes."""
    for r in rows:
        body = {k: r[k] for k in LEDGER_FIELDS}
        if sha256(canonical(body)) != r["row_sha256"]:
            raise ValueError("row hash mismatch")
    return sha256("\n".join(sorted(r["row_sha256"] for r in rows)))


# --- §5 baselines -----------------------------------------------------------------------
def base_rate(ys) -> float:
    ys = list(ys)
    return (sum(ys) + 0.5) / (len(ys) + 1.0)


def _design(rows: list[dict], hazards: list[str]) -> np.ndarray:
    cols = [np.ones(len(rows))]
    for h in hazards:
        cols.append(np.array([1.0 if r["hazard"] == h else 0.0 for r in rows]))
    cols.append(np.array([1.0 if r.get("stage", 0) >= 2 else 0.0 for r in rows]))
    cols.append(np.array([math.log1p(max(r["days"], 0.0)) for r in rows]))
    return np.column_stack(cols)


def fit_logistic(train: list[dict]) -> dict:
    """§5: ridge logistic on hazard (rare → pooled), stage ≥ 2, log1p(days). Newton steps.

    train rows: {'hazard', 'stage', 'days', 'y'}; one target only.
    """
    ys = np.array([r["y"] for r in train], dtype=float)
    br = base_rate(ys)
    if len(train) < MIN_TRAIN or ys.sum() < MIN_CLASS or (len(ys) - ys.sum()) < MIN_CLASS:
        return {"kind": "base", "p": br, "n": len(train)}
    counts: dict = {}
    for r in train:
        counts[r["hazard"]] = counts.get(r["hazard"], 0) + 1
    common = sorted(h for h, c in counts.items() if c >= MIN_HAZARD_ROWS and h is not None)
    hazards = common[1:]                       # earliest common hazard + pooled rare = reference
    x = _design(train, hazards)
    w = np.zeros(x.shape[1])
    pen = np.full(x.shape[1], RIDGE)
    pen[0] = 0.0
    for _ in range(50):
        p = 1 / (1 + np.exp(-(x @ w)))
        g = x.T @ (p - ys) + pen * w
        h = (x * (p * (1 - p))[:, None]).T @ x + np.diag(pen)
        step = np.linalg.solve(h, g)
        w -= step
        if np.max(np.abs(step)) < 1e-9:
            break
    return {"kind": "logit", "w": w.tolist(), "hazards": hazards, "n": len(train)}


def predict(model: dict, row: dict) -> float:
    if model["kind"] == "base":
        return float(model["p"])
    x = _design([row], model["hazards"])[0]
    return float(1 / (1 + math.exp(-float(x @ np.array(model["w"])))))


# --- §6 outcome and score ---------------------------------------------------------------
def outcome(card_at_score: dict, target: str, forecast_utc: dt.datetime) -> int | None:
    """1/0 from records via the card rules; None = excluded (not scored for anyone)."""
    if card_at_score.get("eu27"):
        return None
    st = card_at_score.get("rungs", {}).get(target)
    if st == "present":
        t = _t(card_at_score.get("t_decision" if target == "D" else "t_money"))
        end = window_end(card_at_score, target)
        if t is None or end is None:
            return None
        if t <= forecast_utc:
            return None                          # happened before the forecast: excluded
        return 1 if t <= end else 0
    if st == "absent":
        return 0
    return None                                  # not yet, missing, withheld, no source


def _flip_p(sums: np.ndarray, rng) -> float:
    """One-sided sign-flip p-value for mean of cluster sums > 0 (exact if ≤ 15 clusters)."""
    k = len(sums)
    obs = sums.sum()
    if k <= 15:
        signs = ((np.arange(2 ** k)[:, None] >> np.arange(k)) & 1) * 2 - 1
        return float(np.mean(signs @ sums >= obs - 1e-12))
    signs = rng.choice([-1.0, 1.0], size=(N_FLIPS, k))
    return float((1 + np.sum(signs @ sums >= obs - 1e-12)) / (N_FLIPS + 1))


def h8_score(rows: list[dict], seed: int = SCORE_SEED) -> dict:
    """rows: {'y', 'p_ai' (None → 0.5), 'p_base', 'p_logit', 'cluster'}; scored rows only."""
    rng = np.random.default_rng(seed)
    rows = [r for r in rows if r["y"] in (0, 1)]
    n = len(rows)
    clusters = sorted({r["cluster"] for r in rows}, key=str)
    out: dict = {"n": n, "clusters": len(clusters)}
    if n < MIN_N or len(clusters) < MIN_CLUSTERS:
        out["verdict"] = "not testable at this size"
        return out
    y = np.array([r["y"] for r in rows], float)
    pa = np.array([P_UNUSABLE if r["p_ai"] is None else r["p_ai"] for r in rows], float)
    bs = {"ai": (pa - y) ** 2,
          "base": (np.array([r["p_base"] for r in rows]) - y) ** 2,
          "logit": (np.array([r["p_logit"] for r in rows]) - y) ** 2}
    idx = {c: i for i, c in enumerate(clusters)}
    ci = np.array([idx[r["cluster"]] for r in rows])
    for k, v in bs.items():
        out[f"brier_{k}"] = float(v.mean())
    out["ai_unusable"] = int(sum(r["p_ai"] is None for r in rows))
    for ref in ("base", "logit"):
        gain = bs[ref] - bs["ai"]
        sums = np.bincount(ci, weights=gain, minlength=len(clusters))
        out[f"gain_{ref}"] = float(gain.mean())
        out[f"p_{ref}"] = _flip_p(sums, rng)
    # cluster bootstrap upper bound of the mean gain over the statistical model
    gain = bs["logit"] - bs["ai"]
    sums = np.bincount(ci, weights=gain, minlength=len(clusters))
    cnt = np.bincount(ci, minlength=len(clusters)).astype(float)
    pick = rng.integers(0, len(clusters), size=(N_BOOT, len(clusters)))
    boot = sums[pick].sum(1) / cnt[pick].sum(1)
    out["gain_logit_upper95"] = float(np.quantile(boot, 1 - ALPHA))
    if out["p_base"] < ALPHA and out["p_logit"] < ALPHA:
        out["verdict"] = "PASS"
    elif out["gain_logit_upper95"] < MARGIN:
        out["verdict"] = "FAIL"
    else:
        out["verdict"] = "not shown at this size"
    return out
