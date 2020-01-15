import sql_queries as sqt
import db_tools as dbt


class RL_scratch:
    """
    A class to modelize RL behavior from scratch
    """
    def insert_new_state(self, states, winner, port=5432):
        """
        Insert the states and the winner of the game on the db
        :param states: the different states to the game
        :param winner: if the player win or lose
        :param port: the port to connect on the db
        :return: 0 if it works else -1
        """
        try:
            method = ""
            if winner == 0:
                method = "reward"
                #print("reward")
            if winner == 1:
                method = "penalize"
                #print("penalize")
            if method != "":
                for index_state, state in enumerate(states):
                    parameters = (state, index_state + 1, method)
                    # TODO check if state already exist before insert on db
                    dbt.query_with_parameters(sqt.INSERT_ON_STATE, parameters, port)
                    #print(index_state + 1, state)
                # TODO il faudrait que l'algo puisse rapidement comprendre que le triangle rend un match nul et que le plateau possede plusieurs symétries
                #print("insert on table all states")
            return 0
        except Exception as e:
            print(e)
            return -1
