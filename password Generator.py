import random
import string

def get_password_requirements():
    """Prompt user for password requirements"""
    print("\nPassword Generator")
    print("-----------------")
    
    while True:
        try:
            length = int(input("Enter password length (8-32 characters): "))
            if 8 <= length <= 32:
                break
            print("Please enter a number between 8 and 32")
        except ValueError:
            print("Please enter a valid number")
    
    print("\nSelect character types to include:")
    lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    digits = input("Include digits? (y/n): ").lower() == 'y'
    symbols = input("Include symbols? (y/n): ").lower() == 'y'
    
    # At least one character type must be selected
    while not any([lowercase, uppercase, digits, symbols]):
        print("You must select at least one character type!")
        lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        digits = input("Include digits? (y/n): ").lower() == 'y'
        symbols = input("Include symbols? (y/n): ").lower() == 'y'
    
    return length, lowercase, uppercase, digits, symbols

def generate_password(length, lowercase, uppercase, digits, symbols):
    """Generate password based on requirements"""
    character_set = ""
    
    if lowercase:
        character_set += string.ascii_lowercase
    if uppercase:
        character_set += string.ascii_uppercase
    if digits:
        character_set += string.digits
    if symbols:
        character_set += string.punctuation
    
    # Ensure at least one character from each selected type is included
    password = []
    if lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if digits:
        password.append(random.choice(string.digits))
    if symbols:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest with random characters
    for _ in range(length - len(password)):
        password.append(random.choice(character_set))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def main():
    while True:
        # Get user requirements
        length, lowercase, uppercase, digits, symbols = get_password_requirements()
        
        # Generate password
        password = generate_password(length, lowercase, uppercase, digits, symbols)
        
        # Display password
        print("\nGenerated Password:")
        print(password)
        
        # Ask to generate another
        again = input("\nGenerate another password? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()