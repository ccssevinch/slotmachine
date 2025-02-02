import random 


class SlotMachine:
    def __init__(self, symbol_count, symbol_value):
        self.symbol_count = symbol_count
        self.symbol_value = symbol_value

    def choose_slot_size(self):
        SLOT_SIZES = {
            "3x3": (3, 3),
            "5x3": (5, 3)
        }

        while True:
            chosen_size = input("Choose slot size (3x3) or (5x3): ").strip()
            if chosen_size in SLOT_SIZES:
                return SLOT_SIZES[chosen_size]
            else:
                print("Invalid choice. Please choose a valid slot size (3x3 or 5x3).")
    
    def get_slot_machine_spin(self, rows, cols):
        weighted_list = []
        for symbol, count in self.symbol_count.items():
            weighted_list.extend([symbol] * count)

        grid = []
        for _ in range(cols):
            column = [random.choice(weighted_list) for _ in range(rows)]
            grid.append(column)
        
        return grid
    
    def check_winnings(self, grid, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = grid[0][line]
            if all(column[line] == symbol for column in grid):
                winnings += self.symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines
    
    @staticmethod
    def print_slot_machine(grid):
        for row in range(len(grid[0])):
            for i, column in enumerate(grid):
                if i != len(grid) - 1:
                    print(column[row], end=" | ")
                else:
                    print(column[row], end="")
            print()

class Player:
    MIN_BET = 1
    MAX_BET = 10000
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self):
        while True:
            amount = input("What would you like to deposit? $")
            if amount.isdigit():
                amount = int(amount)
                if amount > 0:
                    self.balance += amount
                    break
                else:
                    print("Amount must be greater than 0.")
            else:
                print("Please enter a number.")

    def get_number_of_lines(self, rows):
        while True:
            try:
                num_lines = int(input(f"Enter the number of lines to bet on (1-{rows}): "))
                # how does the program know what rows we're reffering to above
                if 1 <= num_lines <= rows:
                    return num_lines
                else:
                    print(f"Invalid input. Please enter a number between 1 and {rows}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def get_bet(self):
        while True:
            amount = input("What would you like to bet on each line? $")
            if amount.isdigit():
                amount = int(amount)
                if Player.MIN_BET <= amount <= Player.MAX_BET:
                    return amount
                else:
                    print(f"Amount must be between ${Player.MIN_BET} - ${Player.MAX_BET}.")
            else:
                print("Please enter a numnber.")
    
    def place_bet(self, bet, num_lines):
        total_bet = bet * num_lines # 
        if total_bet > self.balance:
            raise ValueError(
                f"You do not have enough to bet that amount. Your current balance is ${self.balance}.")
        self.balance -= total_bet 
        return total_bet
    
class Game:
    def __init__(self):
        self.symbol_count = {
            "A": 2,
            "B": 4,
            "C": 6, 
            "D": 8
        }

        self.symbol_value = {
            "A": 5,
            "B": 4, 
            "C": 3,
            "D": 2
        }
        self.slot_machine = SlotMachine(self.symbol_count, self.symbol_value)
        self.player = Player(balance=0)

    def play(self):
        self.player.deposit()
        while True:
            print(f"Current balance: ${self.player.balance}")
            rows, cols = self.slot_machine.choose_slot_size()
            num_lines = self.player.get_number_of_lines(rows)
            bet = self.player.get_bet()

            try:
                total_bet = self.player.place_bet(bet, num_lines)
                print(f"You are betting ${bet} on {num_lines} lines. Total bet is ${total_bet}.")

                # Spin the slot machine 
                grid = self.slot_machine.get_slot_machine_spin(rows, cols)
                self.slot_machine.print_slot_machine(grid)

                #Check winnings 
                winnings, winning_lines = self.slot_machine.check_winnings(grid, num_lines, bet)
                self.player.balance += winnings 
                print(f"You won ${winnings}. Winning lines:", winning_lines)

            except ValueError as e: #
                print(e)

            if self.player.balance <= 0:
                print("You have run out of money. Game over!")
                break

            play_again = input("Please enter to play again, or 'q' to quit: ").strip().lower()
            if play_again == 'q':
                break 
        
        print(f"You left with ${self.player.balance}")

game = Game()
game.play()
                      

