def add(a, b):     
    return a + b  # addition of two numbers

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def calculator():
    print("=" * 35)
    print("       Simple Calculator")
    print("=" * 35)

    while True:
        print("\nOperations: + | - | * | /")
        print("Type 'exit' to quit.\n")

        try:
            num1 = input("Enter first number: ")
            if num1.lower() == 'exit':
                break
            num1 = float(num1)

            operator = input("Enter operator (+, -, *, /): ").strip()

            num2 = input("Enter second number: ")
            if num2.lower() == 'exit':
                break
            num2 = float(num2)

        except ValueError:
            print(" Invalid input. Please enter numeric values.")
            continue

        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)
        else:
            print(" Invalid operator. Please use +, -, *, or /.")
            continue

        print(f"\n Result: {num1} {operator} {num2} = {result}")

    print("\nGoodbye! 👋")

if __name__ == "__main__":
    calculator()