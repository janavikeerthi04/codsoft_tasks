"""Play up to five rounds of Rock, Paper, Scissors against the computer."""

import random


CHOICES = ("rock", "paper", "scissors")
BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}
MAX_ROUNDS = 5


def get_user_choice() -> str:
    while True:
        choice = input("Choose rock, paper, or scissors: ").strip().lower()
        if choice in CHOICES:
            return choice
        print("Please enter rock, paper, or scissors.")


def get_round_result(user_choice: str, computer_choice: str) -> str:
    """Return 'user', 'computer', or 'tie' for a round."""
    if user_choice not in CHOICES or computer_choice not in CHOICES:
        raise ValueError("Both choices must be rock, paper, or scissors.")
    if user_choice == computer_choice:
        return "tie"
    if BEATS[user_choice] == computer_choice:
        return "user"
    return "computer"


def ask_to_play_again() -> bool:
    while True:
        answer = input("Play another round? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def main() -> None:
    user_score = 0
    computer_score = 0
    ties = 0

    print("Welcome to Rock, Paper, Scissors!")
    print(f"Play up to {MAX_ROUNDS} rounds.")
    print("Rock beats scissors, scissors beat paper, and paper beats rock.")

    for round_number in range(1, MAX_ROUNDS + 1):
        print(f"\n--- Round {round_number} of {MAX_ROUNDS} ---")
        user_choice = get_user_choice()
        computer_choice = random.choice(CHOICES)
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        result = get_round_result(user_choice, computer_choice)
        if result == "tie":
            ties += 1
            print("It's a tie!")
        elif result == "user":
            user_score += 1
            print("You win this round!")
        else:
            computer_score += 1
            print("The computer wins this round.")

        print(
            f"Score — You: {user_score} | Computer: {computer_score} "
            f"| Ties: {ties}"
        )

        if round_number < MAX_ROUNDS and not ask_to_play_again():
            break

    print("\n--- Final score ---")
    print(f"You: {user_score} | Computer: {computer_score} | Ties: {ties}")
    if user_score > computer_score:
        print("You won the game!")
    elif computer_score > user_score:
        print("The computer won the game.")
    else:
        print("The game is a tie!")


if __name__ == "__main__":
    main()