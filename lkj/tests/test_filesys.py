"""Tests for ``lkj.filesys`` (no real ripgrep or user data directory is touched)."""

import json
import os
import subprocess

import pytest

from lkj import filesys
from lkj.filesys import (
    _ripgrep_json_parser,
    do_nothing,
    enable_sourcing_from_file,
    get_app_data_dir,
    get_watermarked_dir,
    has_watermark,
    rename_file,
    search_folder_fast,
    simple_jsonl_parser,
    watermark_dir,
)


def _match_line(path="a.py", n=3, text="foo\n", sub="foo"):
    return json.dumps(
        {
            "type": "match",
            "data": {
                "path": {"text": path},
                "line_number": n,
                "lines": {"text": text},
                "submatches": [{"match": {"text": sub}, "start": 0, "end": 3}],
            },
        }
    )


def test_simple_jsonl_parser():
    assert simple_jsonl_parser('{"a": 1}\n{"b": 2}') == [{"a": 1}, {"b": 2}]


def test_ripgrep_json_parser_keeps_only_matches_and_skips_junk():
    out = "\n".join(
        [json.dumps({"type": "begin"}), "not json", "", _match_line(), '{"type":"end"}']
    )
    assert _ripgrep_json_parser(out) == [
        {
            "path": "a.py",
            "line_number": 3,
            "line_text": "foo\n",
            "submatches": [{"match_text": "foo", "start": 0, "end": 3}],
        }
    ]


class _Done:
    def __init__(self, stdout=""):
        self.stdout = stdout


def test_search_folder_fast_without_rg_returns_none(monkeypatch, capsys):
    monkeypatch.setattr(filesys.shutil, "which", lambda name: None)
    assert search_folder_fast("x") is None
    assert "ripgrep" in capsys.readouterr().out


def test_search_folder_fast_parses_output_and_raw_egress(monkeypatch):
    monkeypatch.setattr(filesys.shutil, "which", lambda name: "/usr/bin/rg")
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return _Done(_match_line())

    monkeypatch.setattr(filesys.subprocess, "run", fake_run)
    (hit,) = search_folder_fast("foo", "some/dir")
    assert hit["path"] == "a.py"
    assert calls[0][-2:] == ["foo", "some/dir"]
    assert search_folder_fast("foo", egress=None) == _match_line()


def test_search_folder_fast_no_match_and_real_error(monkeypatch, capsys):
    monkeypatch.setattr(filesys.shutil, "which", lambda name: "/usr/bin/rg")

    def no_match(cmd, **kw):
        raise subprocess.CalledProcessError(1, cmd, stderr="")

    monkeypatch.setattr(filesys.subprocess, "run", no_match)
    assert search_folder_fast("foo") == []

    def bad(cmd, **kw):
        raise subprocess.CalledProcessError(2, cmd, stderr="boom")

    monkeypatch.setattr(filesys.subprocess, "run", bad)
    assert search_folder_fast("foo") is None
    assert "boom" in capsys.readouterr().out

    def missing(cmd, **kw):
        raise FileNotFoundError

    monkeypatch.setattr(filesys.subprocess, "run", missing)
    assert search_folder_fast("foo") is None


def test_enable_sourcing_from_file(tmp_path):
    @enable_sourcing_from_file
    def shout(s):
        return s.upper()

    f = tmp_path / "in.txt"
    f.write_text("abc")
    assert shout("abc") == "ABC"  # not a path: used as is
    assert shout(str(f)) == "ABC"  # a path: content is read
    assert f.read_text() == "abc"

    out = tmp_path / "out.txt"
    assert shout(str(f), write_output=str(out)) == "ABC"
    assert out.read_text() == "ABC"
    assert shout(str(f), write_output=True) == "ABC"
    assert f.read_text() == "ABC"


def test_enable_sourcing_from_file_factory_form(tmp_path):
    @enable_sourcing_from_file(write_output=True)
    def shout(s):
        return s.upper()

    f = tmp_path / "in.txt"
    f.write_text("abc")
    shout(str(f))
    assert f.read_text() == "ABC"


def test_do_nothing():
    assert do_nothing(1, a=2) is None


def test_get_app_data_dir_callbacks(tmp_path):
    root = str(tmp_path) + os.sep
    made = get_app_data_dir("new", rootdir=root)
    assert os.path.isdir(made)
    seen = []
    again = get_app_data_dir("new", rootdir=root, if_exists=seen.append)
    assert again == made and seen == [made]
    # None callbacks are allowed
    assert get_app_data_dir("other", rootdir=root, if_does_not_exist=None)
    assert not os.path.isdir(os.path.join(root, "other"))


def test_watermark_roundtrip_and_validation_failure(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    assert not has_watermark(str(d))
    watermark_dir(str(d))
    assert has_watermark(str(d))

    root = str(tmp_path) + os.sep
    p = get_watermarked_dir("wm", rootdir=root)
    assert has_watermark(p)
    assert get_watermarked_dir("wm", rootdir=root) == p  # second call validates
    os.remove(os.path.join(p, ".lkj"))
    with pytest.raises(ValueError, match="not watermarked"):
        get_watermarked_dir("wm", rootdir=root)


def test_rename_file_dry_run_and_real(tmp_path, capsys):
    f = tmp_path / "a.txt"
    f.write_text("x")
    rename_file(str(f), lambda p: p + ".bak")  # dry run by default
    assert f.exists()
    assert "Renaming" in capsys.readouterr().out
    rename_file(str(f), lambda p: p + ".bak", dry_run=False, verbose=False)
    assert not f.exists() and (tmp_path / "a.txt.bak").exists()
