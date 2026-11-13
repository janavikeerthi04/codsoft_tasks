"""Simple command-line calculator for basic arithmetic."""


def calculate(first_number: float, second_number: float, operation: str) -> float:
    """Return the result of applying an arithmetic operation."""
    if operation == "+":
        return first_number + second_number
    if operation == "-":
        return first_number - second_number
    if operation == "*":
        return first_number * second_number
    if operation == "/":
        if second_number == 0:
            raise ValueError("Cannot divide by zero.")
        return first_number / second_number
    raise ValueError("Choose +, -, *, or /.")


def read_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    print("Simple Calculator")
    first_number = read_number("Enter the first number: ")
    second_number = read_number("Enter the second number: ")
    operation = input("Choose an operation (+, -, *, /): ").strip()

    try:
        result = calculate(first_number, second_number, operation)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Result: {result:g}" if result.is_integer() else f"Result: {result}")


if __name__ == "__main__":
    main()
