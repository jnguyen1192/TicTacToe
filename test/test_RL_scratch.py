import unittest

import db_tools as dbt
import sql_queries as sqt

import tictactoe
import RL_scratch


class TestRL_scratch(unittest.TestCase):

    def setUp(self):
        self.rs = RL_scratch.RL_scratch()
        self.ttt = tictactoe.tictactoe()
        self.port = 5433
        # create image db
        name = "postgres"
        assert dbt.create_image_using_dockerfile(name) == 0
        # check if image exist
        assert dbt.dtt.is_image_exist("c_ttt_" + name)
        # run container db on port 5433
        assert dbt.run_db(port=self.port) == 0
        # wait db connection
        assert dbt.wait_db_connection(port=self.port) == 0

    def tearDown(self):
        name = "postgres"
        # stop and remove container db
        assert dbt.dtt.clean_container("c_ttt_" + name) == 0
        # remove image db
        assert dbt.dtt.clean_image("c_ttt_" + name) == 0
        assert not dbt.dtt.is_image_exist("c_ttt_" + name)

    def test_insert_new_state(self):
        """
        Test if function insert_new_state works with an entire random game
        """
        for i in range(10):
            states, winner = self.ttt.run(random_game=True)
            assert self.rs.insert_new_state(states, winner, self.port) == 0
        #print(dbt.select_star_without_parameters(sqt.SELECT_STAR_FROM_STATE, self.port))

    def test_run_game_using_choose_next_position_using_current_state(self):
        """
        Test if function choose_next_move_using_current_state
        """
        # fufill db with states
        for i in range(100000):
            self.ttt = tictactoe.tictactoe()
            states, winner = self.ttt.run(random_game=True)
            assert self.rs.insert_new_state(states, winner, self.port) == 0
        # TODO Export the csv using the db
        self.ttt = tictactoe.tictactoe()
        print("Test run npucs", self.ttt.board)
        self.ttt.play((1, 0))
        print("Test run npucs after first move", self.ttt.board)
        print(self.rs.choose_next_position_using_board(self.ttt, self.port))
        # TODO
        #   Launch a game
        #   While game not end
        #       choose next position using the current board
        #       execute with next position using play()
        #       get the current board


if __name__ == '__main__':
    unittest.main()
