# Function: basic_calculate
# Takes num1, num2, and an operator (+, -, *, /).
# Handles division by zero gracefully without crashing.
# Returns the calculated result or an error message.
def basic_calculate(num1, num2, operator):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            return "Error: Division by zero is not allowed."
        return num1 / num2
    else:
        return "Error: Invalid operator."

# Function: solve_for_x
# Solves an equation containing 'x' against a target value using brute-force search.
# Tests every value from -100 to 100 in increments of 0.1.
# Replaces 'x' in the expression, evaluates it, and finds the x value closest to target.
# Returns the best x rounded to one decimal place.
def solve_for_x(expression, target):
    best_x = 0
    best_diff = float('inf')

    for x in [i * 0.1 for i in range(-1000, 1001)]:
        try:
            result = eval(expression.replace('x', str(x)))
            diff = abs(result - target)
            if diff < best_diff:
                best_diff = diff
                best_x = x
        except:
            continue

    return round(best_x, 1)

# Function: visualize_search
# Runs the brute-force search and prints each attempted x and its difference from target.
# Uses a narrowed range (-10 to 15) to avoid flooding the terminal with 2,000 lines.
def visualize_search(expression, target):
    for x in [i * 0.1 for i in range(-100, 151)]:
        try:
            result = eval(expression.replace('x', str(x)))
            diff = abs(result - target)
            print(f"x = {x}, difference = {diff}")
        except:
            continue

# Function: equation_solver_menu
# Asks the user for an expression containing 'x' and the target value it should equal.
# Calls solve_for_x() and displays the calculated solution.
def equation_solver_menu():
    expression = input("Enter an expression containing 'x': ")
    target = float(input("Enter the target value: "))
    result = eval(expression.replace('x', f"({x})"))
    print(f"The solution is: {solution}")


# Function: main
# Interactive loop offering 5 choices:
# 1. Basic calculation
# 2. Equation solver
# 3. Search visualization
# 4. What is a search algorithm explanation
# 5. Exit
# Handles invalid inputs without crashing.
def main():
    while True:
        print("\n1. Basic calculation")
        print("2. Equation solver")
        print("3. Search visualization")
        print("4. What is a search algorithm explanation")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            operator = input("Enter the operator (+, -, *, /): ")
            result = basic_calculate(num1, num2, operator)
            print(f"The result is: {result}")
        elif choice == "2":
            equation_solver_menu()
        elif choice == "3":
            expression = input("Enter an expression containing 'x': ")
            target = float(input("Enter the target value: "))
            visualize_search(expression, target)
        elif choice == "4":
            print(
                "\nA brute-force search methodically tests every single possibility in a problem space "
                "until it finds a match. It is slow because it evaluates every wrong answer without "
                "prior knowledge or direction. Smarter approaches—like binary search or heuristic searches "
                "such as A*—use feedback or estimates to skip bad paths and find answers far more efficiently."
            )
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()