import random

class tictactoe:
    """
    A class that represent the game
    """
    def __init__(self, player_1="player_1", player_2="player_2", width=3, height=3):
        """
        The game will have two players with names, a board and a score
        """
        self.width = width
        self.height = height
        self.board = self.init_board()  # init to 0
        self.players = [player_1, player_2]
        self.current_player = 0
        self.end = False

    def init_board(self):
        """
        For a board 3x3, we will instanciate each cell with 0
        0 0 0
        0 0 0
        0 0 0
        The lines are from 0 to 2
        The columns are from 0 to 2

        :return: the board as a list with list
        """
        board = []
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(-1)
            board.append(line)
        return board

    def print_board_state(self, board):
        """
        Print the current state
        :return: 0 if it works else -1
        """
        try:
            str_board = ""
            for y in range(self.height):
                for x in range(self.width):
                    if board[y][x] == 0:
                        str_board += "X"
                    if board[y][x] == 1:
                        str_board += "O"
                    if board[y][x] == -1:
                        str_board += "."
                str_board += "\n"
            print(str_board)
            return 0
        except Exception as e:
            print(e)
            return -1

    def is_current_player_win(self):
        """
        Check if the current player have a line
        :return: True if it wins else False
        """
        # horizontal
        for y in range(self.height):
            is_end = True
            for x in range(self.width):
                if self.board[y][x] != self.current_player:
                    is_end = False
            if is_end:
                return True
        # vectical
        for x in range(self.width):
            is_end = True
            for y in range(self.height):
                if self.board[y][x] != self.current_player:
                    is_end = False
            if is_end:
                return True
        # diag left
        is_end = True
        # we admit width equals height
        for i in range(self.width):
            if self.board[i][i] != self.current_player:
                is_end = False
        if is_end:
            return True
        # diag right
        for i in range(self.width):
            if self.board[self.width - 1 - i][i] != self.current_player:
                is_end = False
        if is_end:
            return True
        return False

    def get_random_move(self):
        """
        Return an available move on the board
        :return: the coordinate of the move as (y, x)
        """
        available_moves = []
        for i_lines, lines in enumerate(self.board):
            for i_columns, columns in enumerate(lines):
                if columns == -1:
                    available_moves.append((i_lines, i_columns))
        # Get a random int between 0 and the size of available_moves less one
        random_int = random.randint(0, len(available_moves) - 1)
        return available_moves[random_int]

    def run_normal_game(self):
        """
        Run the game using input
        """
        print("Welcome to tic tac toe")
        while not self.end:
            print("Player", self.players[self.current_player], "need to play")
            self.print_board_state(self.board)
            # give input
            new_input = input()
            y, x = [int(_) for _ in new_input.split(" ")]
            # put in board
            self.board[y][x] = self.current_player
            # check if it wins
            if self.is_current_player_win():
                self.end = True
                break
            self.current_player = (self.current_player + 1) % 2
        print("Player", self.players[self.current_player], "wins")

    def run_predefine_game(self, player_1_moves, player_2_moves):
        """
        Run the game using predefine moves
        """
        next_moves = []
        for index, player_1_move in enumerate(player_1_moves):
            next_moves.append(player_1_moves[index])
            next_moves.append(player_2_moves[index])
        #print("Welcome to tic tac toe using predefine moves")
        i = 0
        while not self.end:
            y, x = next_moves[i]
            # put in board
            self.board[y][x] = self.current_player
            # check if it wins
            if self.is_current_player_win():
                self.end = True
                break
            i += 1
            self.current_player = (self.current_player + 1) % 2
        #self.print_board_state(self.board)
        #print("Player", self.players[self.current_player], "will win with those predefine moves")

    def run(self, player_1_moves=[], player_2_moves=[]):
        """
        The function that launch a game
        :return: 0 if it works else -1
        """
        try:
            if len(player_1_moves) == 0:
                self.run_normal_game()
            else:
                self.run_predefine_game(player_1_moves, player_2_moves)
            return self.board
        except Exception as e:
            print(e)
            return -1

