"""H8 scoring (session 3.6; docs/SELF_MODEL_PROTOCOL.md §6). Once only, by code only.

Refuses (ScoringRefused) unless protocol.may_score() is true. Outcomes come from the card
rules (emo/stream/cards.py via protocol.outcome) at the scoring date: IFRC GO and CEMS
records only. The AI's text and the coherent-whole sentence are never read here. Returns
only what §6 lets leave the Action: counts, mean Brier scores, gains, p-values, the upper
bound, unusable answers, verdict; per model as well when the model changed.
"""
from __future__ import annotations

import datetime as dt

from emo.selfmodel import ledger as L
from emo.selfmodel import protocol as P

SCORE_VERSION = "score-0.1"
READ_FIELDS = ("forecast_id", "target", "forecast_utc", "window_end_utc", "cluster",
               "model_returned", "model_requested", "p_ai", "p_base", "p_logit")


class ScoringRefused(RuntimeError):
    pass


def score(ledgers: dict, current: list[tuple[dict, dict]], today: dt.date) -> dict:
    """ledgers: merged (ledger.merge); current: [(card, extra)] built at the scoring date."""
    fc = ledgers["forecasts"]
    ends = [P._t(f["window_end_utc"]) for f in fc]
    if not P.may_score(today, ends, len(fc)):
        raise ScoringRefused("may_score() is false: windows still open or forecasting not "
                             "ended; no Brier score is computed before then (§6, §8.6)")
    rows = []
    for f in fc:
        f = {k: f[k] for k in READ_FIELDS}           # the AI's text is never read
        card = L.match(ledgers["components"][f["forecast_id"]], current)
        y = None if card is None else P.outcome(card, f["target"], P._t(f["forecast_utc"]))
        rows.append({"y": y, "p_ai": f["p_ai"], "p_base": f["p_base"],
                     "p_logit": f["p_logit"], "cluster": f["cluster"],
                     "model": f["model_returned"] or f["model_requested"]})
    out = {"version": SCORE_VERSION, "scored_on": today.isoformat(),
           "forecasts": len(fc), "excluded": sum(r["y"] is None for r in rows),
           "pooled": P.h8_score(rows)}
    models = sorted({r["model"] for r in rows if r["y"] is not None}, key=str)
    if len(models) > 1:
        out["per_model"] = {m: P.h8_score([r for r in rows if r["model"] == m])
                            for m in models}
    return out
