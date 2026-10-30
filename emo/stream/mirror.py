"""Card job and §11 aggregates (session 3.4; LOOP_CARD_PROTOCOL §1, §11).

Runs only inside a GitHub Action holding EMO_STREAM_KEY. Builds every card with
emo/stream/cards.py and returns only what §11 allows: safe_aggregate, edge-rule counts and
run times. Per-event cards never leave this module (no file, no print).
"""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path

from emo.stream.cards import (
    build_card,
    build_nodes,
    card_population,
    join,
    safe_aggregate,
)
from emo.stream.store import MANIFEST, STREAM_DIR, read_run

MIRROR_VERSION = "mirror-0.1"
SOURCES = ("gdacs", "usgs", "cems", "ifrc_go")
UTC = dt.UTC


def manifest_lines(root: Path) -> list[dict]:
    p = root / STREAM_DIR / MANIFEST
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def load_runs(root: Path) -> list[dict]:
    return [read_run(root / m["file"]) for m in manifest_lines(root)]


def source_gaps(lines: list[dict], today: dt.date) -> dict[str, set[dt.date]]:
    """§1: a source-day is lost when no run that day has the source without error."""
    ok: dict[str, set[dt.date]] = {s: set() for s in SOURCES}
    days = []
    for m in lines:
        d = dt.date.fromisoformat(str(m["run_id"])[:10])
        days.append(d)
        for s, info in (m.get("sources") or {}).items():
            if s in ok and info.get("error") is None:
                ok[s].add(d)
    if not days:
        return {s: set() for s in SOURCES}
    span = [min(days) + dt.timedelta(days=i) for i in range((today - min(days)).days + 1)]
    return {s: {d for d in span if d not in ok[s]} for s in SOURCES}


def build_cards(runs: list[dict], now: dt.datetime, gaps: dict) -> tuple[list[dict], list[dict]]:
    cards, edges, _ = build_cards_with_components(runs, now, gaps)
    return cards, edges


def build_cards_with_components(runs: list[dict], now: dt.datetime, gaps: dict):
    """As build_cards, plus each card's node component and earliest-seen time (session 3.6:
    the H8 caller needs them to match a card across runs and for its earliest-seen rule)."""
    nodes = build_nodes(runs)
    comps, edges = join(nodes)
    pop = card_population(comps, nodes)
    initial = [build_card(c, nodes, now, gaps) for c in pop]
    order = sorted(range(len(pop)), key=lambda i: initial[i]["onset"] or "9999")
    prior: dict = {}
    cards, extra = [], []
    for i in order:                          # §7 "learned": earlier closed cards only
        c = build_card(pop[i], nodes, now, gaps, prior_lags=dict(prior))
        cards.append(c)
        seen = [nodes[k]["earliest_seen"] for k in pop[i] if nodes[k]["earliest_seen"]]
        extra.append({"component": sorted("|".join(map(str, k)) for k in pop[i]),
                      "first_seen": min(seen) if seen else None})
        if c["closed"] and c["lag_onset_decision_days"] is not None and c["hazard"]:
            for iso in c["iso3"]:
                k = (iso, c["hazard"])
                prior[k] = min(prior.get(k, c["lag_onset_decision_days"]),
                               c["lag_onset_decision_days"])
    return cards, edges, extra


def edge_counts(edges: list[dict]) -> dict[str, int]:
    cnt: Counter = Counter()
    for e in edges:
        cnt[f"{e['rule']}{'|tie' if e.get('note') == 'tie' else ''}"] += 1
    return dict(sorted(cnt.items()))


def aggregates(root: Path, now: dt.datetime) -> dict:
    lines = manifest_lines(root)
    runs = [read_run(root / m["file"]) for m in lines]
    gaps = source_gaps(lines, now.date())
    cards, edges = build_cards(runs, now, gaps)
    return {
        "version": MIRROR_VERSION,
        "built_at": now.isoformat(timespec="seconds"),
        "last_ingestion_run": lines[-1]["run_id"] if lines else None,
        "ingestion_runs_read": len(lines),
        "safe_aggregate": safe_aggregate(cards),
        "edge_rule_counts": edge_counts(edges),
        "source_days_lost": {s: len(v) for s, v in gaps.items()},
        "evidence_class": "infrastructure",
        "note": "Counts only (LOOP_CARD_PROTOCOL §11). No per-event card is published until "
                "written reuse terms from GDACS (EC legal notice) and IFRC GO are recorded.",
    }
