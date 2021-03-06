IS_TABLE_EXISTS = """SELECT EXISTS (
   SELECT 1
   FROM   information_schema.tables 
   WHERE  table_name = %s
   );"""

SELECT_STAR_FROM_STATE = """SELECT *
FROM public."State";"""

SELECT_STAR_FROM_STATE_WHERE_BOARD = """SELECT *
FROM public."State" 
WHERE board = %s;"""

""" TODO a request that will write:

For example :
 pos = 100,200
 move_cursor(pos)
 double_click(pos)
 
 The xml will be for the previous example :
 Action : move_cursor
<pos>100,200</pos>
 Action : double_click
<pos>100,200</pos>

"""
#TODO A test will need to be do to know if we need to wait each actions
INSERT_ON_STRATEGIE = """"""

INSERT_ON_ACTION = """INSERT INTO public."Action"(
	name)
	VALUES (%s);"""

DELETE_ON_ACTION = """DELETE FROM public."Action"
	WHERE name = %s;"""

IS_RAW_EXISTS_ON_ACTION = """SELECT EXISTS (
   SELECT 1
   FROM   "Action" 
   WHERE  name = %s
   );"""

IS_BOARD_EXISTS_ON_STATE = """SELECT EXISTS (
   SELECT 1
   FROM   "State" 
   WHERE  board = %s
   );"""

INSERT_ON_STATE = """INSERT INTO public."State"(
    board, "n° move", method)
    VALUES (%s, %s, %s)"""