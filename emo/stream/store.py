"""Encrypted, append-only storage of the daily stream log, with a plain-text manifest.

Layout (all under data/stream/):
  log/<run_id>.json.gz.enc  one file per run, never changed after it is written:
                            gzip of {"run": {...}, "sources": {name: {"records": [...],
                            "requests": [...], "error": str|null}}}, encrypted with
                            `openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 -salt`
                            and the passphrase in the EMO_STREAM_KEY secret.
  MANIFEST.jsonl            one line per run, only appended: run id and times, file,
                            SHA-256 of ciphertext and plaintext, per source the SHA-256 of
                            its canonical JSON, whether it had any record (yes/no), error
                            class, and every request (URL,
                            status, start, end; for latency). No record counts or sizes.

Decrypt (any machine with openssl, e.g. Termux):
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 -pass env:EMO_STREAM_KEY \
      -in data/stream/log/<run_id>.json.gz.enc | gunzip > run.json
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

KEY_ENV = "EMO_STREAM_KEY"
OPENSSL = ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-md",
           "sha256", "-pass", f"env:{KEY_ENV}"]
STREAM_DIR = Path("data/stream")
MANIFEST = "MANIFEST.jsonl"


class MissingKey(RuntimeError):
    pass


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _key_env() -> dict:
    if not os.environ.get(KEY_ENV):
        raise MissingKey(f"{KEY_ENV} is not set; refusing to write (the log is never "
                         "stored unencrypted)")
    return dict(os.environ)


def encrypt(plain: bytes) -> bytes:
    p = subprocess.run(OPENSSL + ["-salt"], input=plain, capture_output=True,
                       env=_key_env(), check=True)
    return p.stdout


def decrypt(cipher: bytes) -> bytes:
    p = subprocess.run(OPENSSL + ["-d"], input=cipher, capture_output=True,
                       env=_key_env(), check=True)
    return p.stdout


def write_run(root: Path, run: dict, sources: dict) -> dict:
    """Encrypt and write one run; append its manifest line. Returns the manifest line."""
    _key_env()                                   # fail before anything is touched
    d = root / STREAM_DIR
    (d / "log").mkdir(parents=True, exist_ok=True)
    rel = STREAM_DIR / "log" / f"{run['run_id']}.json.gz.enc"
    path = root / rel
    if path.exists():
        raise FileExistsError(f"append-only: {rel} already exists")
    plain = gzip.compress(canonical({"run": run, "sources": sources}), mtime=0)
    cipher = encrypt(plain)
    path.write_bytes(cipher)
    line = {
        **run,
        "file": str(rel),
        "sha256_cipher": sha256(cipher),
        "sha256_plain_gz": sha256(plain),
        "sources": {name: {"sha256_records": sha256(canonical(s["records"])),
                           "has_records": bool(s["records"]),
                           "error": s["error"], "requests": s["requests"]}
                    for name, s in sources.items()},
    }
    with open(d / MANIFEST, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, sort_keys=True) + "\n")
    return line


def read_run(path: Path) -> dict:
    return json.loads(gzip.decompress(decrypt(path.read_bytes())))


def verify_append_only(root: Path, base: str = "HEAD") -> list[str]:
    """Problems with the staged changes under data/stream versus `base` (run after git add).

    Allowed: new files under data/stream/log/; MANIFEST.jsonl changed only by appending.
    """
    out = subprocess.run(["git", "diff", "--cached", "--name-status", base, "--",
                          str(STREAM_DIR)],
                         cwd=root, capture_output=True, text=True, check=True).stdout
    problems = []
    for row in filter(None, out.splitlines()):
        status, name = row.split("\t", 1)
        if name == str(STREAM_DIR / MANIFEST):
            if status == "A":
                continue
            old = subprocess.run(["git", "show", f"{base}:{name}"], cwd=root,
                                 capture_output=True, check=True).stdout
            new = subprocess.run(["git", "show", f":{name}"], cwd=root,
                                 capture_output=True, check=True).stdout
            if not new.startswith(old):
                problems.append(f"{name}: earlier lines changed")
        elif not (status == "A" and name.startswith(str(STREAM_DIR / "log") + "/")):
            problems.append(f"{status} {name}: only new log files may be added")
    return problems
