def simple_calculator():
    print("Simple Calculator")
    print("-----------------")
    print("Operations available:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Modulus (%)")
    print("6. Exponentiation (**)")
    print("-----------------")
    
    try:
        # Get user input
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Enter the operation (+, -, *, /, %, **): ").strip()
        
        # Perform calculation based on operation
        if operation == '+':
            result = num1 + num2
            print(f"Result: {num1} + {num2} = {result}")
        elif operation == '-':
            result = num1 - num2
            print(f"Result: {num1} - {num2} = {result}")
        elif operation == '*':
            result = num1 * num2
            print(f"Result: {num1} * {num2} = {result}")
        elif operation == '/':
            if num2 == 0:
                print("Error: Division by zero is not allowed!")
            else:
                result = num1 / num2
                print(f"Result: {num1} / {num2} = {result}")
        elif operation == '%':
            result = num1 % num2
            print(f"Result: {num1} % {num2} = {result}")
        elif operation == '**':
            result = num1 ** num2
            print(f"Result: {num1} ** {num2} = {result}")
        else:
            print("Invalid operation! Please choose from +, -, *, /, %, **")
    
    except ValueError:
        print("Error: Please enter valid numbers!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the calculator
if __name__ == "__main__":
    while True:
        simple_calculator()
        another_calculation = input("\nDo you want to perform another calculation? (yes/no): ").lower()
        if another_calculation != 'yes':
            print("Goodbye!")
            break