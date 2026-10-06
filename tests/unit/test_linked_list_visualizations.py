"""Tests for :mod:`src.visualizations.linked_lists`."""

from __future__ import annotations

import pytest

from src.visualizations.linked_lists import format_merge_trace, merge_frames

EXAMPLE_LIST1 = [1, 2, 4]
EXAMPLE_LIST2 = [1, 3, 5]


@pytest.mark.unit
def test_example_merge_order_matches_dummy_head_walk() -> None:
    frames = merge_frames(EXAMPLE_LIST1, EXAMPLE_LIST2)

    assert frames[0].source == "start"
    assert frames[0].merged == ()
    assert frames[-1].source == "done"
    assert frames[-1].merged == (1, 1, 2, 3, 4, 5)

    attached = [frame.merged[-1] for frame in frames if frame.source in {"list1", "list2"}]
    assert attached == [1, 1, 2, 3, 4]
    assert frames[-2].source == "rest2"
    assert frames[-2].merged == (1, 1, 2, 3, 4, 5)
    # Splice hangs 5 off tail->next but does not walk tail onto 5.
    assert frames[-3].merged == (1, 1, 2, 3, 4)
    assert frames[-3].tail_index == 4
    assert frames[-2].tail_index == 4


@pytest.mark.unit
def test_equal_heads_take_list1() -> None:
    # 1 <= 1 must attach list1, matching the C++ `<=` test.
    frames = merge_frames([1], [1])
    first_attach = next(frame for frame in frames if frame.source in {"list1", "list2"})
    assert first_attach.source == "list1"
    assert first_attach.merged == (1,)
    assert first_attach.remaining2 == (1,)


@pytest.mark.unit
def test_both_empty_splices_null_and_returns_empty() -> None:
    frames = merge_frames([], [])

    assert [frame.source for frame in frames] == ["start", "rest2", "done"]
    assert frames[-1].merged == ()
    assert frames[0].tail_index is None
    assert frames[1].tail_index is None


@pytest.mark.unit
def test_one_list_empty_splices_the_other() -> None:
    frames = merge_frames([], [1, 2])

    assert frames[0].merged == ()
    splice = frames[1]
    assert splice.source == "rest2"
    assert splice.merged == (1, 2)
    assert frames[-1].merged == (1, 2)


@pytest.mark.unit
def test_all_of_one_list_smaller_then_splice() -> None:
    frames = merge_frames([1, 2], [5, 6])

    attached = [frame.source for frame in frames if frame.source in {"list1", "list2"}]
    assert attached == ["list1", "list1"]
    assert frames[-2].source == "rest2"
    assert frames[-1].merged == (1, 2, 5, 6)


@pytest.mark.unit
def test_trace_table_renders_aligned_rows() -> None:
    frames = merge_frames(EXAMPLE_LIST1, EXAMPLE_LIST2)
    trace = format_merge_trace(frames)
    lines = trace.splitlines()

    assert lines[0].split()[:4] == ["step", "list1", "list2", "merged"]
    assert set(lines[1]) <= {"-", " "}
    assert "attach list1" in trace
    assert "splice the rest of list2" in trace
    assert len({len(line.rstrip()) > 0 for line in lines}) == 1
