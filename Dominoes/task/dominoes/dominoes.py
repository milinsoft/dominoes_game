import random

random.seed()

domino_all = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
              [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
              [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
              [3, 3], [3, 4], [3, 5], [3, 6],
              [4, 4], [4, 5], [4, 6],
              [5, 5], [5, 6],
              [6, 6]]


def take_dominoes(quantity):
    global stock
    hand = []
    for x in range(quantity):
        domino = random.choice(stock)
        hand.append(domino)
        stock.remove(domino)
    return hand


def doubles():
    counter = 6
    while counter >= 0:
        if [counter, counter] in players_hand:
            domino = [counter, counter]
            domino_snake.append(domino)
            players_hand.remove(domino)
            return 'computer'
        elif [counter, counter] in computers_hand:
            domino = [counter, counter]
            domino_snake.append(domino)
            computers_hand.remove(domino)
            return 'player'
        else:
            counter -= 1
            if counter == -1:
                return "restart"


def reorient_domino(domino):
    new_domino = [domino[1], domino[0]]
    return new_domino


def gameplay():
    gameover_check()
    line = ("=" * 70)
    print(f"""{line}
Stock size: {len(stock)}
Computer pieces: {len(computers_hand)}\n""")
    if len(domino_snake) > 6:
        print(f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}")
    else:
        print("".join(str(x) for x in domino_snake))
    print()
    print("Your pieces:")
    for n, domino in enumerate(players_hand, start=1):
        print("{}:{}".format(n, domino))
    print()


def game_status():
    gameplay()
    if status == "computer won":
        print("Status: The game is over. The computer won!")
        exit()
    elif status == "player won":
        print("Status: The game is over. You won!")
        exit()
    elif status == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
        players_move()
    elif status == 'computer':
        print("Status: Computer is about to make a move. Press Enter to continue...")
        _ = input()
        computers_move()
    elif status == 'draw':
        print("Status: The game is over. It's a draw!")
        exit()
    else:
        print("UNKNOWN STATUS ERROR")


def next_player():
    global status, domino_snake
    gameover_check()
    if status == "player":
        status = "computer"
    elif status == "computer":
        status = "player"
    elif status == "draw":
        print("Status: The game is over. It's a draw!")
        exit()
    return game_status()


def ai_module():
    global domino_snake, computers_hand
    dom = domino_snake[:]
    comp = computers_hand[:]
    dom.extend(comp)
    domino_scores = {0: 0, }
    for i in range(len(computers_hand)):
        domino_scores[i+1] = computers_hand[i][0] + computers_hand[i][1]
    sorted_x = dict(sorted(domino_scores.items(), reverse=True))
    keys_list = []
    for k in sorted_x.keys():
        keys_list.append(k)
    return keys_list


def move_validation(move):
    global status, computers_hand, players_hand, domino_snake
    left_side = domino_snake[0][0]
    right_side = domino_snake[-1][1]
    if status == "computer":
        current_hand = computers_hand
    elif status == "player":
        current_hand = players_hand
    domino_number = abs(move) - 1
    domino = current_hand[domino_number]
    is_legal = False
    if domino[0] == right_side:
        is_legal = True
    elif domino[1] == right_side:
        is_legal = True
    elif domino[0] == left_side:
        is_legal = True
    elif domino[1] == left_side:
        is_legal = True
    elif move == 0:
        is_legal = True
    else:
        is_legal = False
    return is_legal


def players_move():
    global stock, players_hand, domino_snake
    left_side = domino_snake[0][0]
    right_side = domino_snake[-1][1]
    move = input()
    if move.lstrip("-").isdigit() and abs(int(move)) <= len(players_hand):
        move = int(move)
        if move > 0:
            domino_number = abs(move) - 1  # decreasing because enumerate numbers increased by 1
            domino = players_hand[domino_number]
            if domino[0] == right_side:
                domino_snake.append(domino)
                del players_hand[domino_number]
            elif domino[1] == right_side:
                domino_snake.append(reorient_domino(domino))
                del players_hand[domino_number]
            else:
                print("Illegal move. Please try again.")
                return players_move()
        elif move < 0:
            domino_number = abs(move) - 1  # decreasing because enumerate numbers increased by 1
            domino = players_hand[domino_number]
            if domino[0] == left_side:
                reoriented_domino = reorient_domino(players_hand[domino_number])
                domino_snake.insert(0, reoriented_domino)
                del players_hand[domino_number]
            elif domino[1] == left_side:
                domino_snake.insert(0, players_hand[domino_number])
                del players_hand[domino_number]
            else:
                print("Illegal move. Please try again.")
                return players_move()
        elif move == 0:
            if len(stock) > 0:
                players_hand += take_dominoes(1)
            else:
                pass
    else:
        print("Invalid input. Please try again.")
        players_move()
    return next_player()


def computers_move():
    global computers_hand, domino_snake
    left_side = domino_snake[0][0]
    right_side = domino_snake[-1][1]
    # move = random.randint(0 - len(computers_hand), len(computers_hand))
    best_moves = ai_module()  # issue is here
    if len(best_moves) > 0:
        for move in best_moves:
            domino_number = abs(move) - 1
            domino = computers_hand[domino_number]
            if move_validation(move):
                if move > 0:
                    if domino[0] == right_side:
                        domino_snake.append(computers_hand[domino_number])
                        del computers_hand[domino_number]
                        break
                    elif domino[1] == right_side:
                        domino_snake.append(reorient_domino(computers_hand[domino_number]))
                        del computers_hand[domino_number]
                        break
                elif move < 0:
                    if domino[0] == left_side:
                        reoriented_domino = reorient_domino(computers_hand[domino_number])
                        domino_snake.insert(0, reoriented_domino)
                        del computers_hand[domino_number]
                        break
                    elif domino[1] == left_side:
                        domino_snake.insert(0, computers_hand[domino_number])
                        del computers_hand[domino_number]
                        break
                elif move == 0:
                    if len(stock) > 0:
                        computers_hand += take_dominoes(1)
                    else:
                        pass
            elif move_validation(-move):
                if -move > 0:
                    if domino[0] == right_side:
                        domino_snake.append(computers_hand[domino_number])
                        del computers_hand[domino_number]
                        break
                    elif domino[1] == right_side:
                        domino_snake.append(reorient_domino(computers_hand[domino_number]))
                        del computers_hand[domino_number]
                        break
                elif -move < 0:
                    if domino[0] == left_side:
                        reoriented_domino = reorient_domino(computers_hand[domino_number])
                        domino_snake.insert(0, reoriented_domino)
                        del computers_hand[domino_number]
                        break
                    elif domino[1] == left_side:
                        domino_snake.insert(0, computers_hand[domino_number])
                        del computers_hand[domino_number]
                        break
                return next_player()
    else:
        move = 0
    return next_player()


def gameover_check():
    global stock, status, domino_snake, players_hand, computers_hand, player_is_out_of_moves, pc_is_out_of_moves
    left_side = domino_snake[0][0]
    right_side = domino_snake[-1][1]
    if len(computers_hand) == 0:
        status = "computer won"
    elif len(players_hand) == 0:
        status = "player won"
    if left_side == right_side:
        snake_elements = [x for x in str(domino_snake) if x.isdigit()]
        if snake_elements.count(str(left_side)) == 8:
            status = "draw"



if __name__ == '__main__':

    while True:
        stock = list(domino_all)
        domino_snake = []
        players_hand = take_dominoes(7)
        players_hand.sort()
        computers_hand = take_dominoes(7)
        computers_hand.sort()
        status = doubles()
        pc_is_out_of_moves = None
        player_is_out_of_moves = None
        if status == 'restart':
            continue
        else:
            game_status()
