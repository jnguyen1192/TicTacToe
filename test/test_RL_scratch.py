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

    def train_naive_rl(self, nb_game=10):
        # fufill db with states
        for i in range(nb_game):
            self.ttt = tictactoe.tictactoe()
            states, winner = self.ttt.run(random_game=True)
            assert self.rs.insert_new_state(states, winner, self.port) == 0

    def test_run_game_using_choose_next_position_using_current_state(self):
        """
        Test if function choose_next_move_using_current_state
        """
        self.train_naive_rl()
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

    def test_run_normal_game_with_RL_1(self):
        """
        Test if function run_normal_game works
        """
        try:
            i = 0
            winner = -1
            while True:
                i += 1
                # game ininitialized with ttt
                # first player play using db with naive rl
                self.ttt.play(self.rs.choose_next_position_using_board(self.ttt, self.port))
                # check if game is ended
                winner = self.ttt.get_game_state()
                if winner != 3:
                    break
                # second player play using random move
                self.ttt.play(self.ttt.get_random_move())
                # check if game is ended
                winner = self.ttt.get_game_state()
                if winner != 3:
                    break
                if i == 1000:
                    assert False
            #winner_str = ["Joueur 1", "Joueur 2", "Personne"]
            #self.ttt.print_board_state(self.ttt.board)
            #print("Le gagnant est :", winner_str[winner])
            assert True
        except Exception as e:
            print(e)
            assert False

    def test_experience_to_plot_1(self):
        """
        Test if the experience to create a plot works correctly
        """
        # TODO to implement
        #   Use the test test_run_game_using_choose_next_position_using_current_state and test_run_normal_game_with_RL_1
        #       1) train the RL while fufill the db with 10/100/1000/10000 games
        #           1.a) train and record on db
        #           1.b) play 100 games versus the random player moves
        #           1.c) clean the table state
        #       2) get the number of win/loss/draw for each training versus a random player moves and get the time
        trains = [10, 100, 1000, 10000]
        for train in trains:
            # 1.a)
            self.train_naive_rl(train)
            # 1.b)
            # TODO refactor test_run_normal_game_with_RL_1 to have a game with a result



    def test_export_table_to_csv(self):
        """
        Test if the function export_table_to_csv works
        """

        # fufill db with states
        for i in range(10):
            self.ttt = tictactoe.tictactoe()
            states, winner = self.ttt.run(random_game=True)
            assert self.rs.insert_new_state(states, winner, self.port) == 0
        assert dbt.export_table_to_csv("State", test=True) == 0
        # TODO optionally:
        #   Test if the csv file contains header and some raw respecting the format of table "State" (int, str, int, str)

    def test_read_table_csv(self):
        """
        Test if the function read table csv works
        """
        # TODO to build a strategy it need to create an object with unknowing number of parameter and unknowing number of output
        import csv
        # @source: https://www.alexkras.com/how-to-read-csv-file-in-python/
        with open("State_20200219.csv") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            data = []
            for row in reader:
                data.append(row)
            print(data)



if __name__ == '__main__':
    unittest.main()
