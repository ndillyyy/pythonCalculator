import random

def guessing_game():
    print("=" * 35)
    print("      Number Guessing Game")
    print("=" * 35)
    print("\nI've picked a number between 1 and 100.")

    secret_number = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        print(f"\nAttempts remaining: {remaining}")

        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print(" Please enter a valid whole number.")
            continue

        attempts += 1

        if guess < 1 or guess > 100:
            print("  Please guess a number between 1 and 100.")
            attempts -= 1  # Don't count out-of-range guesses
        elif guess < secret_number:
            print(" Too low! Try higher.")
        elif guess > secret_number:
            print(" Too high! Try lower.")
        else:
            print(f"\n Correct! The number was {secret_number}.")
            print(f"You got it in {attempts} attempt(s)!")
            break
    else:
        print(f"\n😞 Oops, You're out of attempts! The number was {secret_number}.")

    print("\nThanks for playing along! ")

if __name__ == "__main__":
    guessing_game()
