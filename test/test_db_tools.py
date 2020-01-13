import unittest

import db_tools as dbt
import sql_queries as sqt


class TestDbTools(unittest.TestCase):

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



    def generic_db_tools_all_tables_created(self, test=False):
        """
        Function to test if tables exist
        :return:
        """
        tables_name = ['Strategie', 'Action', 'Has_action']
        for name in tables_name:
            res = dbt.select_one_with_parameters(sqt.IS_TABLE_EXISTS, (name,), test)
            assert(res != -1)
            assert res

    def test_db_tools_all_tables_created(self):
        """
        Test if all the tables are created
        """
        self.generic_db_tools_all_tables_created()

    def test_run_db(self):
        """
        Test if the db works
        """
        image_name = "postgres"
        # TODO implement
        #   Create image of the db
        # create postgres image
        assert dbt.create_image_using_dockerfile(image_name) == 0
        #   Launch the db
        assert dbt.run_db() == 0
        #   TODO Check if the tables exist
        #self.generic_db_tools_all_tables_created()
        #   Remove container and image
        # remove image
        assert dbt.dtt.clean_image("c_ttt_" + image_name) == 0
        assert not dbt.dtt.is_image_exist("c_ttt_" + image_name)

        assert True


if __name__ == '__main__':
    unittest.main()
