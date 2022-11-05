import random

random.seed()


class DominoesGame:

    DOMINOES_ALL = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                    [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                    [3, 3], [3, 4], [3, 5], [3, 6],
                    [4, 4], [4, 5], [4, 6],
                    [5, 5], [5, 6],
                    [6, 6]]

    def __init__(self):
        self.stock = DominoesGame.DOMINOES_ALL
        self.domino_snake = []
        self.players_hand = sorted(self.take_dominoes(7))
        self.computers_hand = sorted(self.take_dominoes(7))
        self.status = None

    def take_dominoes(self, quantity):
        hand = []
        for x in range(quantity):
            if self.stock:
                domino = random.choice(self.stock)
                self.stock.remove(domino)
                hand.append(domino)
        return hand

    def get_doubles(self):
        counter = 6
        while counter >= 0:
            double_domino = [counter, counter]
    
            for hand, name in (
                [self.players_hand, "bot"],
                [self.computers_hand, "player"],
            ):
                
                if double_domino in hand:
                    self.domino_snake.append(double_domino)
                    hand.remove(double_domino)
                    return name

            else:
                counter -= 1
                if counter == -1:
                    return "restart"

    def switch_player(self):
        self.status = "bot" if self.status == "player" else "player"
        return self.gameplay()
    
    def inverse_domino(self, domino):
        return [domino[1], domino[0]]  # reversal

    def gameplay(self):
        # making sure it's not draw!
        if self.domino_snake[0][0] == self.domino_snake[-1][1]:  # compare left & right side
            snake_elements = [x for x in str(self.domino_snake) if x.isdigit()]
            if snake_elements.count(str(self.domino_snake[0][0])) == 8:
                exit(print("Status: The game is over. It's a draw!"))

        # print CLI interface
        print(
            f"{'=' * 70}\n"
            f"Stock size: {len(self.stock)}\n"
            f"Computer pieces: {len(self.computers_hand)}\n"
        )
        if len(self.domino_snake) > 6:
            print(
                f"{self.domino_snake[0]}{self.domino_snake[1]}{self.domino_snake[2]}..."
                f"{self.domino_snake[-3]}{self.domino_snake[-2]}{self.domino_snake[-1]}"
            )
        else:
            print(*self.domino_snake, sep="")
        print("\nYour pieces:")
        for n, domino in enumerate(self.players_hand, start=1):
            print(f"{n}:{domino}")

        # checking if game is won!
        if not self.computers_hand:
            exit(print("Status: The game is over. The computer won!"))
        elif not self.players_hand:
            exit(print("Status: The game is over. You won!"))

        # CLI prompt
        elif self.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
            self.players_move()
        elif self.status == "bot":
            _ = input(
                "Status: Computer is about to make a move. Press Enter to continue...\n"
            )
            self.bot_move()

    def is_valid_move(self, move, side="both") -> bool:
        current_hand = self.computers_hand if self.status == "bot" else self.players_hand
        domino_number = abs(move) - 1
        domino = current_hand[domino_number]
        # the move is valid if dominoes side matches the 'snake' side

        # left side // right side
        snake_side_values = {
            "left": self.domino_snake[0][0],
            "right": self.domino_snake[-1][1],
            "both": self.domino_snake[0][0] + self.domino_snake[-1][1],
        }
        return any(
            (
                snake_side_values[side] in domino,
                move == 0,
            )
        )

    def players_move(self):
        move = input()
        if move.lstrip("-").isdigit() and abs(int(move)) <= len(self.players_hand):
            move = int(move)
            domino_number = (abs(move) - 1)  # decreasing because enumerate numbers increased by 1
            domino = self.players_hand[domino_number]

            if move == 0:
                self.players_hand += self.take_dominoes(1)

            else:
                if move > 0 and self.is_valid_move(move, "right"):
                    self.domino_snake.append(
                        domino
                        if domino[0] == self.domino_snake[-1][1]
                        else self.inverse_domino(domino)
                    )
                    del self.players_hand[domino_number]

                elif move < 0 and self.is_valid_move(move, "left"):
                    self.domino_snake.insert(
                        0,
                        domino
                        if domino[1] == self.domino_snake[0][0]
                        else self.inverse_domino(domino),
                    )
                    del self.players_hand[domino_number]

                else:
                    print("Illegal move. Please try again.")
                    return self.players_move()

        else:
            print("Invalid input. Please try again.")
            self.players_move()
        return self.switch_player()

    def bot_move(self):
        def get_best_moves() -> list:
            domino_scores = {
                0: 0,
            }
            for i in range(len(self.computers_hand)):
                domino_scores[i + 1] = sum(self.computers_hand[i])
            keys_list = sorted(domino_scores, reverse=True)
            return keys_list

        left_side: list = self.domino_snake[0][0]
        right_side: list = self.domino_snake[-1][1]
        best_moves: list = get_best_moves()
        if len(best_moves) > 0:
            for move in best_moves:
                domino_number = abs(move) - 1
                domino = self.computers_hand[domino_number]

                if move == 0:
                    self.computers_hand += self.take_dominoes(1)
                    break

                # check if domino can be put to the tail
                elif self.is_valid_move(move, "right"):
                    self.domino_snake.append(
                        domino if domino[0] == right_side else self.inverse_domino(domino)
                    )
                    del self.computers_hand[domino_number]
                    break

                # check if domino can be put to the head
                elif self.is_valid_move(-move, 'left'):
                    self.domino_snake.insert(
                        0, self.inverse_domino(domino) if domino[0] == left_side else domino
                    )
                    del self.computers_hand[domino_number]
                    break
        else:
            self.computers_hand += self.take_dominoes(1)
        return self.switch_player()


if __name__ == "__main__":
    game = DominoesGame()
    game.status = game.get_doubles()

    while True:
        if game.status != "restart":
            game.gameplay()
        continue
