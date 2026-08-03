from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack: list[int] = []

        for token in tokens:
            if token not in {"+", "-", "*", "/"}:
                # The token is an integer operand.
                stack.append(int(token))
                continue

            # The second value popped is the left operand because
            # the stack follows last-in, first-out order.
            right: int = stack.pop()
            left: int = stack.pop()

            if token == "+":
                result: int = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                # Integer-only implementation of truncation toward zero.
                sign: int = -1 if (left < 0) != (right < 0) else 1
                result = sign * (abs(left) // abs(right))

            stack.append(result)

        return stack.pop()