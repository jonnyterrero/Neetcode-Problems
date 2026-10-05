"""Tests for :mod:`src.visualizations.stacks`."""

from __future__ import annotations

import pytest

from src.visualizations import (
    format_min_stack_trace,
    min_stack_states,
)

EXAMPLE_OPS: list[tuple[str, int | None]] = [
    ("push", 1),
    ("push", 2),
    ("push", 0),
    ("pop", None),
]


@pytest.mark.unit
def test_states_include_initial_empty_state() -> None:
    states = min_stack_states(EXAMPLE_OPS)

    assert len(states) == len(EXAMPLE_OPS) + 1
    assert states[0].stack == ()
    assert states[0].min_stack == ()
    assert states[0].top is None
    assert states[0].minimum is None


@pytest.mark.unit
def test_states_match_the_worked_example() -> None:
    states = min_stack_states(EXAMPLE_OPS)

    assert states[3].stack == (1, 2, 0)
    assert states[3].min_stack == (1, 1, 0)
    assert states[3].minimum == 0

    # After the pop, the earlier minimum must be recovered.
    assert states[4].stack == (1, 2)
    assert states[4].top == 2
    assert states[4].minimum == 1


@pytest.mark.unit
def test_both_stacks_always_have_equal_height() -> None:
    for state in min_stack_states(EXAMPLE_OPS):
        assert len(state.stack) == len(state.min_stack)


@pytest.mark.unit
def test_minimum_matches_brute_force_at_every_step() -> None:
    for state in min_stack_states([("push", 3), ("push", 5), ("push", -2), ("pop", None)]):
        expected = min(state.stack) if state.stack else None
        assert state.minimum == expected


@pytest.mark.unit
def test_duplicate_minimums_survive_a_pop() -> None:
    states = min_stack_states([("push", 2), ("push", 1), ("push", 1), ("pop", None)])

    assert states[-1].stack == (2, 1)
    assert states[-1].minimum == 1


@pytest.mark.unit
@pytest.mark.parametrize(
    "operations, message",
    [
        ([("pop", None)], "empty stack"),
        ([("push", None)], "requires a value"),
        ([("peek", 1)], "Unknown operation"),
    ],
)
def test_invalid_operations_raise(operations: list[tuple[str, int | None]], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        min_stack_states(operations)


@pytest.mark.unit
def test_trace_table_renders_aligned_rows() -> None:
    trace = format_min_stack_trace(min_stack_states(EXAMPLE_OPS))
    lines = trace.splitlines()

    # Header, underline, then one row per state.
    assert len(lines) == len(EXAMPLE_OPS) + 3
    assert lines[0].split() == ["step", "operation", "stack", "min_stack", "top", "getMin"]
    assert set(lines[1]) <= {"-", " "}
    assert "push(1)" in lines[3]
    assert len({len(line.rstrip()) > 0 for line in lines}) == 1


@pytest.mark.unit
def test_trace_marks_empty_state_with_dashes() -> None:
    trace = format_min_stack_trace(min_stack_states([]))

    assert "init" in trace
    assert "[]" in trace
