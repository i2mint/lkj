"""Tests for ``lkj.importing``: ``import_object`` and namespace forwarding."""

import sys

import pytest

from lkj.importing import (
    NamespaceForwardingFinder,
    NamespaceForwardingLoader,
    import_object,
    register_namespace_forwarding,
)


def test_import_object_errors():
    assert import_object("os.path.join").__name__ == "join"
    with pytest.raises(ImportError, match="does not contain a module path"):
        import_object("nodots")
    with pytest.raises(ImportError, match="is not found in"):
        import_object("os.path.no_such_thing")


def test_finder_only_claims_source_namespace():
    finder = NamespaceForwardingFinder("fwd_src", "json")
    assert finder.find_spec("something_else", None) is None
    spec = finder.find_spec("fwd_src.decoder", None)
    assert spec is not None and spec.name == "fwd_src.decoder"


def test_loader_forwards_to_target_module():
    loader = NamespaceForwardingLoader("fwd_src.decoder", "fwd_src", "json")
    try:
        module = loader.load_module("fwd_src.decoder")
        import json.decoder

        assert module is json.decoder  # already loaded target is returned as is
    finally:
        sys.modules.pop("fwd_src.decoder", None)


def test_loader_missing_target_raises():
    loader = NamespaceForwardingLoader("fwd_src.nope", "fwd_src", "json")
    with pytest.raises(ImportError):
        loader.load_module("fwd_src.nope")


def test_register_namespace_forwarding_inserts_finder_first():
    before = list(sys.meta_path)
    try:
        register_namespace_forwarding("fwd_ns_src", "json")
        first = sys.meta_path[0]
        assert isinstance(first, NamespaceForwardingFinder)
        assert (first.source_base, first.target_base) == ("fwd_ns_src", "json")
    finally:
        sys.meta_path[:] = before
