class MinStack:
    def __init__(self) -> None:
        """Create an empty stack that can report its minimum in O(1)."""

        # Every value pushed, in order.
        self.stack: list[int] = []

        # min_stack[i] is the smallest value among stack[0..i], so the last
        # entry is always the minimum of the whole stack.
        self.min_stack: list[int] = []

    def push(self, val: int) -> None:
        """Push val onto the stack."""

        self.stack.append(val)

        # The new minimum is either val itself or the previous minimum.
        current_min = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(current_min)

    def pop(self) -> None:
        """Remove the top element."""

        # Both stacks stay the same length, so they are popped together.
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """Return the top element without removing it."""

        return self.stack[-1]

    def getMin(self) -> int:
        """Return the smallest element currently in the stack."""

        return self.min_stack[-1]
