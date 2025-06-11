import random
import string

def generate_password(length):
    if length < 4:
        return "Password length should be at least 4 characters."

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Combine all character sets
    all_chars = lowercase + uppercase + digits + symbols

    # Ensure password contains at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the rest of the password length
    password += random.choices(all_chars, k=length - 4)

    # Shuffle the password list to remove predictability
    random.shuffle(password)

    # Convert list to string
    return ''.join(password)

# --- Main Program ---
try:
    user_input = int(input("Enter desired password length: "))
    password = generate_password(user_input)
    print(f"Generated Password: {password}")
except ValueError:
    print("Please enter a valid number.")
