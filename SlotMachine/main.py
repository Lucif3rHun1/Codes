import random

MIN_LINES = 1
MAX_LINES = 3
MAX_BET_AMOUNT = 100
MIN_BET_AMOUNT = 10

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}
symbol_values = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol]*bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row],end=" | ")
            else:
                print(column[row])

def deposit():
    while True:
        amount = input("How much do you want to deposit: \n")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please enter a number greater then 0.")
        else:
            print("Please enter a numric value.")
    return amount

def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on ({MIN_LINES}-{MAX_LINES})?\n")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Please enter a number of lines.")
        else:
            print("Please enter a numric value.")
    return lines
def bet_amount():
    while True:
        bet = input("How much do you want to bet on each line?\n")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET_AMOUNT <= bet <= MAX_BET_AMOUNT:
                break
            else:
                print(f"Amount must be between {MIN_BET_AMOUNT} - {MAX_BET_AMOUNT}.")
        else:
            print("Please enter a numric value.")
    return bet
def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = bet_amount()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You don't have enough money. Your current balance is: {balance}")
        else:
            break
    print(f"You are betting {bet} on {lines} line. Total bet is equal to: {total_bet}.")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f"Your winnings are: {winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet
def main():
    balance = deposit()
    while True:
        print(f"Current balance is {balance}")
        answer = input("Press Enter to spin(q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"Your final balance is {balance}")
    
main()