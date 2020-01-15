import sql_queries as sqt
import db_tools as dbt


class RL_scratch:
    """
    A class to modelize RL behavior from scratch
    """
    def insert_new_state(self, states, winner, port=5432):
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
                dbt.query_with_parameters(sqt.INSERT_ON_STATE, parameters, port)
                print(index_state + 1, state)
            # TODO il faudrait que l'algo puisse rapidement comprendre que le triangle rend un match nul et que le plateau possede plusieurs symétries
            print("insert on table all states")