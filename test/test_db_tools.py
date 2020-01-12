import unittest

import db_tools


class TestDbTools(unittest.TestCase):

    def test_create_image_postgres(self):
        """
        Test if image postgres correctly created
        """
        image_name = "postgres"
        # create postgres image
        assert db_tools.create_image_using_dockerfile(image_name) == 0
        # check if image exist
        assert db_tools.dtt.is_image_exist("c_ttt_" + image_name)
        # remove image
        assert db_tools.dtt.clean_image("c_ttt_" + image_name) == 0
        assert not db_tools.dtt.is_image_exist("c_ttt_" + image_name)

    def test_run_db(self):
        """
        Test if the db works
        """
        assert True



if __name__ == '__main__':
    unittest.main()
