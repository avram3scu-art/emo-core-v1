"""
RDL backtest engine: one generic intervention library for all domains, plus problem-structure
inputs. See docs/RDL_BACKTEST_PROTOCOL.md (pre-registered at commit 1b84f12).

Everything here is the same for every domain. Labels and structure rules are documented
assumptions (see the protocol change log); they were written without consulting the ozone or
climate outcomes, but by authors who know those outcomes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from emo.models.bottleneck_profile import BottleneckProfile
from emo.remedy.simulation import has_measured_data, measured_gap

_DELIVERY = {"low": 0.2, "medium": 0.5, "high": 0.8}               # size of behaviour change, not speed
_CAPACITY = {"low": 0.9, "medium": 0.65, "high": 0.4}               # feasibility from capacity (as v0.1)


@dataclass(frozen=True)
class GenericInstrument:
    option_id: str
    name: str
    target_bottlenecks: tuple[str, ...]
    required_capacity: str
    time_to_effect: str
    evidence_level: str
    binding: bool
    delivery_effect: str


GENERIC_LIBRARY: tuple[GenericInstrument, ...] = (
    GenericInstrument("binding_regulation", "Binding regulation or ban with deadlines",
                      ("translation", "deployment", "persistence"), "high", "medium", "strong", True, "high"),
    GenericInstrument("price_instrument", "Price instrument (tax, levy, permit trading)",
                      ("translation", "budget", "contradiction"), "high", "medium", "strong", True, "high"),
    GenericInstrument("substitute_support", "Subsidy or public investment in substitutes",
                      ("deployment", "budget"), "medium", "long", "moderate", False, "medium"),
    GenericInstrument("finance_transfer", "Finance transfer to lower-income parties",
                      ("budget", "deployment"), "medium", "medium", "moderate", False, "medium"),
    GenericInstrument("trade_measures", "Trade measures against non-participants",
                      ("persistence", "contradiction"), "medium", "medium", "moderate", True, "medium"),
    GenericInstrument("voluntary_pledges", "Voluntary targets or pledges",
                      ("translation",), "low", "short", "conceptual", False, "low"),
    GenericInstrument("information_reporting", "Information, labelling and reporting",
                      ("validation", "persistence"), "low", "short", "moderate", False, "low"),
    GenericInstrument("research_monitoring", "Research and monitoring",
                      ("validation",), "medium", "long", "moderate", False, "low"),
)


@dataclass(frozen=True)
class StructureInputs:
    """
    Problem structure at the decision date (values must come from dated sources).
    n_major_actors: number of major producers/emitters whose action is needed.
    substitutes: 0 = no substitute known; 1 = substitutes available at similar cost.
    economic_share: share of the world economy directly affected by the restriction (0-1).
    """
    n_major_actors: int
    substitutes: float
    economic_share: float
    sources: dict[str, str] = field(default_factory=dict)


def _concentration(n: int) -> float:
    return 1.0 / (1.0 + math.log10(max(n, 1)))          # 1 actor -> 1.0; 10 -> 0.5; 100 -> 0.33


def _political_ease(share: float) -> float:
    return 1.0 / (1.0 + 10.0 * max(share, 0.0))         # 1% -> 0.91; 10% -> 0.5; 80% -> 0.11


def structure_multiplier(inst: GenericInstrument, s: StructureInputs | None) -> tuple[float, float]:
    """(feasibility multiplier, effect multiplier). None = structure ignored (RDL v0.2 behaviour)."""
    if s is None:
        return 1.0, 1.0
    c, p, sub = _concentration(s.n_major_actors), _political_ease(s.economic_share), s.substitutes
    rules = {
        "binding_regulation": ((c + p + sub) / 3.0, 1.0),
        "price_instrument": ((c + p) / 2.0, 0.5 + 0.5 * sub),
        "substitute_support": (1.0, 0.5 + 0.5 * sub),
        "finance_transfer": (1.0, 0.5 + 0.5 * sub),
        "trade_measures": (c, 1.0),
        "voluntary_pledges": (1.0, 1.0),
        "information_reporting": (1.0, 1.0),
        "research_monitoring": (1.0, 1.0),
    }
    return rules[inst.option_id]


@dataclass
class BacktestResult:
    gap: float
    top3: list[tuple[str, float]]
    predicted_gain: float
    used_structure: bool
    refused: bool = False
    note: str = ""


def run_backtest(profile: BottleneckProfile, structure: StructureInputs | None) -> BacktestResult:
    if not has_measured_data(profile):
        return BacktestResult(0.0, [], 0.0, structure is not None, refused=True,
                              note="All inputs zero: missing data, not measured failure.")
    gap = measured_gap(profile)
    dominant = set(profile.dominant_bottlenecks)
    scored = []
    for inst in GENERIC_LIBRARY:
        fm, em = structure_multiplier(inst, structure)
        feas = _CAPACITY[inst.required_capacity] * fm
        eff = _DELIVERY[inst.delivery_effect] * em
        relevance = 1.0 if dominant.intersection(inst.target_bottlenecks) else 0.5
        scored.append((inst.option_id, round(feas * eff * relevance, 4), feas * eff))
    scored.sort(key=lambda t: t[1], reverse=True)
    top = scored[:3]
    gain = round(gap * sum(v for _, _, v in top) / len(top), 3)
    return BacktestResult(gap, [(k, v) for k, v, _ in top], gain, structure is not None)


# ---------------------------------------------------------------- RDL v0.3
# See docs/RDL_V03_PROTOCOL.md. Same library, labels and structure rules as v0.2.
# Changes: (1) tractability and remaining gap reported separately;
#          (2) ranking by feasibility x effect only; stage link kept for explanation.

@dataclass
class BacktestResultV03:
    remaining_gap: float
    tractability: float
    predicted_gain: float                      # continuity only; not used in criteria
    top3: list[tuple[str, float]]
    repairs: dict[str, list[str]]              # instrument -> dominant stages it targets
    fallback: list[tuple[str, float]] = field(default_factory=list)  # low-effect: cannot close the gap
    refused: bool = False
    note: str = ""


def run_backtest_v03(profile: BottleneckProfile, structure: StructureInputs) -> BacktestResultV03:
    if not has_measured_data(profile):
        return BacktestResultV03(0.0, 0.0, 0.0, [], {}, refused=True,
                                 note="All inputs zero: missing data, not measured failure.")
    gap = measured_gap(profile)
    dominant = set(profile.dominant_bottlenecks)
    scored = []
    for inst in GENERIC_LIBRARY:
        fm, em = structure_multiplier(inst, structure)
        scored.append((inst, round(_CAPACITY[inst.required_capacity] * fm * _DELIVERY[inst.delivery_effect] * em, 4)))
    scored.sort(key=lambda t: t[1], reverse=True)
    # Development change 1 (logged): a recommended remedy must be able to close a material part of
    # the gap, so only medium/high delivery-effect instruments enter the top 3.
    eligible = [t for t in scored if t[0].delivery_effect != "low"]
    top = eligible[:3]
    tract = round(sum(v for _, v in top) / 3, 3)
    return BacktestResultV03(
        fallback=[(i.option_id, v) for i, v in scored if i.delivery_effect == "low"],
        remaining_gap=gap, tractability=tract, predicted_gain=round(gap * tract, 3),
        top3=[(i.option_id, v) for i, v in top],
        repairs={i.option_id: sorted(dominant.intersection(i.target_bottlenecks)) for i, _ in top},
    )
