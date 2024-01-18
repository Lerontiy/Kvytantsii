import sqlite3
from icecream import ic
from google_sheets import gs

class Database:
    def __init__(self):
        gs_all_citizens_data = gs.get_values()
        db_all_citizens_names = self.get_all_citizens_id_and_names()
        for iter in range(len(gs_all_citizens_data)):
            if gs_all_citizens_data[iter][1] not in db_all_citizens_names[iter][1]:
                self._sql_update(f"INSERT INTO жителі(ПІБ) VALUES ('{gs_all_citizens_data[iter][1]}')")
        return


    def _sql_connect(self, db_name="database.db"):
        return sqlite3.connect(db_name)
    
    def _sql_select(self, request:str):
        return_cur = None
        with self._sql_connect() as con:
            cur = con.cursor()
            return_cur = cur.execute(request)
        return return_cur
    
    def _sql_update(self, request:str):
        with self._sql_connect() as con:
            cur = con.cursor()
            cur.execute(request)
            con.commit()
        return
    
    def check_user_in_db(self, user_id):
        db_user_id = self._sql_select(f"SELECT user_id FROM жителі WHERE user_id='{user_id}'").fetchone()
        if db_user_id==None:
            self._sql_update(f"INSERT INTO жителі(user_id) VALUES ('{user_id}')")
        return
    
    def is_admin(self, user_id):
        return bool(self._sql_select(f"SELECT is_admin FROM жителі WHERE user_id='{user_id}'").fetchone())

    def get_all_citizens_id_and_names(self):
        return self._sql_select(f"SELECT id, ПІБ FROM жителі WHERE ПІБ is not NULL").fetchall()
    
    def get_userId_and_name_by_dbId(self, db_id):
        return self._sql_select(f"SELECT user_id, ПІБ FROM жителі WHERE id='{db_id}'").fetchone()

db = Database()