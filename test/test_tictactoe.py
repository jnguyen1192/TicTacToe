import unittest

import tictactoe


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.ttt = tictactoe.tictactoe()

    def test_constructor_tictactoe(self):
        from pprint import pprint
        pprint(self.ttt.board)
        assert (True==True)

    def test_run_predefine_game_1(self):
        """
        Test if function run works with the predefine moves
        XXX
        OO.
        ...
        """
        player_1_moves = [(0, 0), (0, 1), (0, 2)]
        player_2_moves = [(1, 0), (1, 1), (1, 2)]
        self.ttt.print_board_state(self.ttt.run(player_1_moves=player_1_moves, player_2_moves=player_2_moves))

    def test_run_predefine_game_2(self):
        """
        Test if function run works with the predefine moves
        X..
        OXO
        ..X
        """
        player_1_moves = [(0, 0), (1, 1), (2, 2)]
        player_2_moves = [(1, 0), (1, 2), (2, 1)]
        self.ttt.print_board_state(self.ttt.run(player_1_moves=player_1_moves, player_2_moves=player_2_moves))

    def test_run_predefine_game_3(self):
        """
        Test if function run works with the predefine moves
        0..
        X0X
        ..0
        """
        player_1_moves = [(1, 0), (1, 2), (2, 1)]
        player_2_moves = [(0, 0), (1, 1), (2, 2)]
        self.ttt.print_board_state(self.ttt.run(player_1_moves=player_1_moves, player_2_moves=player_2_moves))


if __name__ == '__main__':
    unittest.main()