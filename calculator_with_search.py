"""A basic calculator that solves equations by brute-force search.

Week 2 assignment. The solver deliberately does no algebra: it tries every
candidate value of x and keeps whichever one lands closest to the target.
"""

import ast
import math


# The search space: -100 to 100 in steps of 0.1, stored as tenths.
# Tenths are kept as whole numbers so the loop can use range(); see
# _candidate_values() for why that matters.
_SEARCH_START = -1000
_SEARCH_END = 1000


def basic_calculate(num1, num2, operator):
    """Apply one of +, -, *, / to two numbers."""
    if operator == "+":
        return num1 + num2
    if operator == "-":
        return num1 - num2
    if operator == "*":
        return num1 * num2
    if operator == "/":
        # Returning a message instead of raising keeps the menu loop alive.
        if num2 == 0:
            return "Error: Division by zero is undefined."
        return num1 / num2
    return "Error: Invalid operator."


# Only these pieces of Python may appear in an expression the user types.
# Anything else - a function call, an attribute lookup, an import - is rejected
# before it is ever run. This matters because the expression ends up going
# through eval(), and eval() on unchecked input will run whatever it is given.
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
)


def _compile_expression(expression_str):
    """Parse an expression and reject anything that is not arithmetic on x."""
    tree = ast.parse(expression_str, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError("Expression contains an unsupported operation.")
        if isinstance(node, ast.Name) and node.id != "x":
            raise ValueError("Expression may only use the variable x.")
    return compile(tree, "<calculator expression>", "eval")


def _candidate_values(start_tenths=_SEARCH_START, end_tenths=_SEARCH_END, step_tenths=1):
    """Yield candidate x values, counting in whole tenths.

    Counting in tenths and dividing by 10 at the last moment avoids adding 0.1
    over and over, which drifts: 0.1 added thirty times is 3.0000000000000004,
    not 3.0.
    """
    for tenths in range(start_tenths, end_tenths + 1, step_tenths):
        yield tenths / 10


def _search(expression_str, target_val, candidates, report=False):
    """Try every candidate, keep the closest. Optionally print each attempt."""
    try:
        compiled_expression = _compile_expression(expression_str)
    except (SyntaxError, ValueError):
        compiled_expression = None

    best_x = None
    best_difference = None

    for x in candidates:
        difference = None
        if compiled_expression is not None:
            try:
                result = eval(compiled_expression, {"__builtins__": {}}, {"x": x})
                # Guard against inf/nan, which compare strangely and would
                # otherwise win the "closest" contest.
                if isinstance(result, (int, float)) and math.isfinite(result):
                    difference = abs(result - target_val)
            except (ArithmeticError, TypeError, ValueError, OverflowError):
                pass

        if report:
            if difference is None:
                print(f"Trying x = {x:>6.1f} | distance from target: unavailable")
            else:
                print(f"Trying x = {x:>6.1f} | distance from target: {difference:.4f}")

        # Strict "<" means the first candidate wins a tie. For x * x = 16 that
        # returns -4.0 rather than 4.0 - both are correct answers.
        if difference is not None and (
            best_difference is None or difference < best_difference
        ):
            best_x = x
            best_difference = difference

    return best_x, best_difference


def solve_for_x(expression_str, target_val):
    """Return the tenth-step x in [-100, 100] that comes closest to the target.

    This is exhaustive on purpose: 2001 candidates, no rearranging, no
    shortcuts. It is the slow way, and that is the point of the exercise.
    """
    return _search(expression_str, target_val, _candidate_values())


# Why this prints a narrower range than solve_for_x actually searches:
# solve_for_x checks all 2001 candidates from -100 to 100. Printing every one of
# them floods the terminal - the useful part scrolls away before you can read it.
# So the walkthrough defaults to -10 to 10 in steps of 0.5, which is 41 lines and
# fits on one screen, while still showing the distance shrink toward zero and
# grow again on the far side. The solver itself is untouched; only this printed
# demonstration is narrowed.
def visualize_search(expression_str, target_val, start_tenths=-100, end_tenths=100, step_tenths=5):
    """Run the same search as solve_for_x, printing every value it tries."""
    candidates = _candidate_values(start_tenths, end_tenths, step_tenths)
    return _search(expression_str, target_val, candidates, report=True)


def equation_solver_menu():
    """Ask for an expression and a target, solve it, print the answer."""
    expression = input("Enter an expression containing x: ")
    target = float(input("Enter the target value: "))
    best_x, difference = solve_for_x(expression, target)

    if best_x is None:
        print("Could not evaluate the expression.")
        return

    print(f"Closest match: x = {best_x}, difference = {difference}")


def explain_search():
    """Option 4: what a search algorithm is, in plain language."""
    print()
    print("A brute-force search solves a problem by trying every possibility it is")
    print("allowed to try, measuring how wrong each one is, and keeping the best.")
    print("It never reasons about the problem - it just checks, one at a time.")
    print()
    print("That is why it is slow. Solving x + 5 = 12 here costs 2001 guesses, even")
    print("though the distance to the target shrinks steadily the whole way and then")
    print("grows again - information a smarter method would have used. Widening the")
    print("range or using finer steps makes the cost grow in direct proportion.")
    print()
    print("A smarter approach is binary search. When the expression moves in one")
    print("direction only (as x + 5 does), you can check the middle of the range and")
    print("throw away the half the answer cannot be in. That turns roughly 2000")
    print("guesses into about 11, because each guess halves what is left.")
    print()


def main():
    while True:
        print("\nSmart Calculator")
        print("1. Basic calculation")
        print("2. Equation solver")
        print("3. Search visualisation")
        print("4. What is a search algorithm?")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
            except ValueError:
                print("Error: Please enter valid numbers.")
                continue

            operator = input("Enter an operator (+, -, *, /): ").strip()
            print(f"Result: {basic_calculate(num1, num2, operator)}")
        elif choice == "2":
            try:
                equation_solver_menu()
            except ValueError:
                print("Error: Please enter a valid target value.")
        elif choice == "3":
            print("\nVisualising a brute-force search for x + 5 = 12:")
            best_x, difference = visualize_search("x + 5", 12)
            print(f"\nClosest match: x = {best_x}, difference = {difference}")
        elif choice == "4":
            explain_search()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    main()
