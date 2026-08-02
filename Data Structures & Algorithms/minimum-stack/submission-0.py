class MinStack:
    def __init__(self) -> None:
        """Initialize the main stack and its synchronized minimum stack."""
        self.stack: list[int] = []
        self.min_stack: list[int] = []

    def push(self, val: int) -> None:
        """Push val and record the minimum for the resulting stack state."""
        self.stack.append(val)
        if not self.min_stack:
            # The first value is automatically the current minimum.
            self.min_stack.append(val)
        else:
            # Preserve the smaller of val and the previous minimum.
            current_minimum = self.min_stack[-1]
            self.min_stack.append(min(val, current_minimum))

    def pop(self) -> None:
        """Remove the top value and its corresponding minimum state."""
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """Return the top value without removing it."""
        return self.stack[-1]

    def getMin(self) -> int:
        """Return the minimum value currently in the stack."""
        return self.min_stack[-1]