import io
import sys
import re

from lkj.strings import FindReplaceTool


def capture_print(func, *args, **kwargs):
    old_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_find_and_print_matches_highlight_under_match():
    text = "apple banana apple\nsome other line\n"
    tool = FindReplaceTool(text, line_mode=False)
    out = capture_print(tool.find_and_print_matches, r"apple")

    # We expect for the first match that the matched line appears, then the
    # highlight line directly under it, then following context lines. Ensure the
    # highlight caret appears on its own line immediately after the matched line.
    # Locate the first occurrence of the matched line and the caret line that follows.
    lines = out.splitlines()

    # Find the index of the line that contains the first printed snippet for match 0
    # It should contain 'apple banana apple'
    match0_idx = None
    for i, line in enumerate(lines):
        if "apple banana apple" in line:
            # Ensure the next non-empty line is the highlight
            match0_idx = i
            break

    assert match0_idx is not None, "Did not find the matched line in output"

    # The next line should be the caret highlight (contains at least one '^')
    assert any(
        c == "^" for c in lines[match0_idx + 1]
    ), "Highlight not directly under matched line"

    # For completeness, ensure that the text 'some other line' appears after the caret
    assert "some other line" in "\n".join(
        lines[match0_idx + 2 :]
    ), "Following context not printed after highlight"
