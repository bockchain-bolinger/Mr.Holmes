import json
from pathlib import Path

from Core.Support.FileIO import Json


def test_write_atomic_writes_payload(tmp_path):
    target = tmp_path / "result.json"
    payload = {"List": [{"site": "https://example.com"}], "ok": True}

    Json.write_atomic(str(target), payload)

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data == payload


def test_write_atomic_replaces_existing_file(tmp_path):
    target = tmp_path / "result.json"
    target.write_text('{"stale": true}', encoding="utf-8")

    Json.write_atomic(str(target), {"fresh": 1})

    assert json.loads(target.read_text(encoding="utf-8")) == {"fresh": 1}
