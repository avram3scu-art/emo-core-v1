"""Offline tests for the validation rules in scripts/refresh_open_data.py."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("refresh", ROOT / "scripts/refresh_open_data.py")
refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(refresh)

OLD_CSV = b"Entity,Code,Year,Value\nWorld,OWID_WRL,2020,1\nWorld,OWID_WRL,2021,2\n"


HURDAT_SAMPLE = (
    b"AL092017,             HARVEY,     3,\n"
    b"20170825, 1800,  , HU, 27.4N,  96.6W, 110,  941,\n"
    b"20170826, 0300, L, HU, 28.0N,  97.1W, 115,  937,\n"
    b"20170830, 0800, L, TS, 29.8N,  93.5W,  40,  993,\n"
    b"AL012025,             ALPHA,      1,\n"
    b"20250701, 0000,  , TD, 20.0N,  80.0W,  30, 1008,\n"
)


class _Resp:
    def __init__(self, content: bytes):
        self.content = content

    def json(self):
        return json.loads(self.content)


def _setup(tmp_path, monkeypatch, owid_new: bytes, oa_new: dict):
    data = tmp_path / "data"
    data.mkdir()
    monkeypatch.setattr(refresh, "DATA", data)
    for f in refresh.OWID:
        refresh.path_for(f).parent.mkdir(parents=True, exist_ok=True)
        refresh.path_for(f).write_bytes(OLD_CSV)
    old_oa = {"meta": {}, "group_by": [{"key": "2020", "count": 10}, {"key": "2021", "count": 11}]}
    for f in refresh.OPENALEX:
        refresh.path_for(f).parent.mkdir(parents=True, exist_ok=True)
        refresh.path_for(f).write_text(json.dumps(old_oa))

    def fake_get(url):
        if "nhc.noaa.gov" in url:
            return _Resp(HURDAT_SAMPLE)
        if "ourworldindata" in url:
            return _Resp(owid_new)
        return _Resp(json.dumps(oa_new).encode())

    monkeypatch.setattr(refresh, "_get", fake_get)
    return data


def test_valid_update_is_written(tmp_path, monkeypatch):
    new_csv = OLD_CSV + b"World,OWID_WRL,2022,3\n"
    new_oa = {"meta": {"notice": "x"}, "group_by": [{"key": "2020", "count": 10},
                                                     {"key": "2021", "count": 12}]}
    data = _setup(tmp_path, monkeypatch, new_csv, new_oa)
    res = refresh.refresh()
    assert all(s["status"] == "ok" and s["changed"] for s in res["sources"])
    f = next(iter(refresh.OWID))
    assert refresh.path_for(f).read_bytes() == new_csv
    g = json.loads(refresh.path_for(next(iter(refresh.OPENALEX))).read_text())
    assert "notice" not in g["meta"]


def test_header_change_keeps_committed_file(tmp_path, monkeypatch):
    bad = b"Entity,Code,Year,Other\nWorld,OWID_WRL,2020,9\nWorld,OWID_WRL,2021,9\n"
    data = _setup(tmp_path, monkeypatch, bad, {"group_by": []})
    res = refresh.refresh()
    assert all(s["status"] == "failed" for s in res["sources"])
    assert refresh.path_for(next(iter(refresh.OWID))).read_bytes() == OLD_CSV


def test_large_row_loss_is_rejected(tmp_path, monkeypatch):
    shrunk = b"Entity,Code,Year,Value\nWorld,OWID_WRL,2020,1\n"
    oa = {"group_by": [{"key": "2020", "count": 10}]}
    _setup(tmp_path, monkeypatch, shrunk, oa)
    res = refresh.refresh()
    assert all(s["status"] == "failed" and "retained" in s["detail"] for s in res["sources"])


def test_unchanged_content_is_not_rewritten(tmp_path, monkeypatch):
    oa = {"meta": {"cost_usd": 0.0001}, "group_by": [{"key": "2020", "count": 10},
                                                       {"key": "2021", "count": 11}]}
    _setup(tmp_path, monkeypatch, OLD_CSV, oa)
    res = refresh.refresh()
    assert all(s["status"] == "ok" and not s["changed"] for s in res["sources"])
    man = json.loads((tmp_path / "data/MANIFEST.json").read_text())
    assert all(v["last_changed_at"].startswith("2026-10-20") for v in man.values())


@pytest.mark.parametrize("secret", ["KEY123"])
def test_api_key_never_reaches_manifest(tmp_path, monkeypatch, secret):
    _setup(tmp_path, monkeypatch, OLD_CSV, {})
    monkeypatch.setenv("OPENALEX_API_KEY", secret)

    def boom(url):
        raise RuntimeError(f"failed {url}")

    monkeypatch.setattr(refresh, "_get", boom)
    refresh.refresh()
    assert secret not in (tmp_path / "data/MANIFEST.json").read_text()


def test_hurdat_check_and_gwi_event_rule(tmp_path):
    assert refresh._hurdat_check(HURDAT_SAMPLE) == (2, None)
    assert refresh._hurdat_check(b"nothing")[1] is not None
    spec = importlib.util.spec_from_file_location("gwi_h", ROOT / "analysis/gwi_hurricanes.py")
    gwi_h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gwi_h)
    f = tmp_path / "h.txt"
    f.write_bytes(HURDAT_SAMPLE)
    ev = gwi_h.landfall_events(f)
    assert [(str(d.date()), n) for d, n in ev] == [("2017-08-26", "Harvey (AL092017)")]
