import unittest

import db_tools as dbt
import sql_queries as sqt

import tictactoe


class TestDbTools(unittest.TestCase):

    def setUp(self):
        self.ttt = tictactoe.tictactoe()

    def test_create_image_postgres(self):
        """
        Test if image postgres correctly created
        """
        image_name = "postgres"
        # create postgres image
        assert dbt.create_image_using_dockerfile(image_name) == 0
        # check if image exist
        assert dbt.dtt.is_image_exist("c_ttt_" + image_name)
        # remove image
        assert dbt.dtt.clean_image("c_ttt_" + image_name) == 0
        assert not dbt.dtt.is_image_exist("c_ttt_" + image_name)

    def generic_db_tools_all_tables_created(self, tables_name):
        """
        Function to test if tables exist
        :return:
        """
        for name in tables_name:
            res = dbt.select_one_with_parameters(sqt.IS_TABLE_EXISTS, (name,), port="5435")
            assert(res != -1)
            assert res

    def test_run_db(self):
        """
        Test if the db works
        """
        name = "postgres"
        # Create postgres image
        assert dbt.create_image_using_dockerfile(name) == 0
        # Launch the db
        assert dbt.run_db(port=5435) == 0
        assert dbt.wait_db_connection(port=5435) == 0
        # Check if the tables exist
        tables_name = ['State']
        self.generic_db_tools_all_tables_created(tables_name)
        # Remove container and image
        assert dbt.dtt.clean_container("c_ttt_" + name) == 0
        # Remove image
        assert dbt.dtt.clean_image("c_ttt_" + name) == 0
        assert not dbt.dtt.is_image_exist("c_ttt_" + name)

    def test_insert_new_state(self):
        """
        Test if function insert_new_state works
        """
        method = ""
        states, winner = self.ttt.run(random_game=True)
        for index_state, state in enumerate(states):
            parameters = (state,)
            dbt.query_with_parameters(sqt.INSERT_ON_STATE, )
            print(index_state + 1, state)

        if winner == 0:
            method = "reward"
            print("reward")
        if winner == 1:
            method = "penalize"
            print("penalize")
        if method != "":
            # TODO il faudrait que l'algo puisse rapidement comprendre que le triangle rend un match nul et que le plateau possede plusieurs symétries

            print("insert on table state")


"""
    def test_create_backup(self):
        name = "postgres"
        # create postgres image
        assert dbt.create_image_using_dockerfile(name) == 0
        #   Launch the db
        assert dbt.run_db(port=5435) == 0

    def test_first_backup(self):
        #Create a backup with the table state
        name = "backup"
        # create postgres image
        assert dbt.create_image_using_dockerfile(name) == 0
        #   Launch the db
        assert dbt.run_backup() == 0
        # TODO launch backup
        assert dbt.new_backup() != -1
        #   Remove container and image
        assert dbt.dtt.clean_container("c_ttt_" + name) == 0
        # remove image
        assert dbt.dtt.clean_image("c_ttt_" + name) == 0
        assert not dbt.dtt.is_image_exist("c_ttt_" + name)
"""


if __name__ == '__main__':
    unittest.main()
