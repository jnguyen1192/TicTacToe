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
        # TODO implement
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
        # TODO implement
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
        # TODO implement
        player_1_moves = [(1, 0), (1, 2), (2, 1)]
        player_2_moves = [(0, 0), (1, 1), (2, 2)]
        self.ttt.print_board_state(self.ttt.run(player_1_moves=player_1_moves, player_2_moves=player_2_moves))

    def test_get_random_move(self):
        """
        Test if function get_random_move works
        """
        for i in range(1000):
            y, x = self.ttt.get_random_move()
            assert (y < self.ttt.height)
            assert (x < self.ttt.height)


if __name__ == '__main__':
    unittest.main()
