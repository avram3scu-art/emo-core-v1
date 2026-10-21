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


class _Resp:
    def __init__(self, content: bytes):
        self.content = content

    def json(self):
        return json.loads(self.content)


def _setup(tmp_path, monkeypatch, owid_new: bytes, oa_new: dict):
    data = tmp_path / "data"
    data.mkdir()
    for f in refresh.OWID:
        (data / f).write_bytes(OLD_CSV)
    old_oa = {"meta": {}, "group_by": [{"key": "2020", "count": 10}, {"key": "2021", "count": 11}]}
    for f in refresh.OPENALEX:
        (data / f).write_text(json.dumps(old_oa))
    monkeypatch.setattr(refresh, "DATA", data)

    def fake_get(url):
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
    assert (data / f).read_bytes() == new_csv
    g = json.loads((data / next(iter(refresh.OPENALEX))).read_text())
    assert "notice" not in g["meta"]


def test_header_change_keeps_committed_file(tmp_path, monkeypatch):
    bad = b"Entity,Code,Year,Other\nWorld,OWID_WRL,2020,9\nWorld,OWID_WRL,2021,9\n"
    data = _setup(tmp_path, monkeypatch, bad, {"group_by": []})
    res = refresh.refresh()
    assert all(s["status"] == "failed" for s in res["sources"])
    assert (data / next(iter(refresh.OWID))).read_bytes() == OLD_CSV


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
