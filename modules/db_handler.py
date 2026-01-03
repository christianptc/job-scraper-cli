from pathlib import Path
import sqlite3
from typing import List
from datetime import datetime


# Path to database file 
BASE_DIR = Path(__file__).resolve().parent.parent
# Creates database file if not exists
DB_PATH = BASE_DIR / "internships.db"

def table_create():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    tablename = "internships"
    command = "CREATE TABLE IF NOT EXISTS"
    main_table_columns = (
        "id INTEGER NOT NULL PRIMARY KEY",
        "company_name TEXT NOT NULL",
        "position TEXT NOT NULL",
        "location TEXT NOT NULL",
        "link TEXT NOT NULL UNIQUE",
        "date_posted TEXT NOT NULL",
        "status TEXT NOT NULL DEFAULT 'fetched'",
        "last_update TEXT"   
   )
    settings_table_name = "settings"
    user_settings = (
        "search TEXT",
        "ort TEXT",
        "umkreis INTEGER",
        "search_amount INTEGER"
   )
    insert_default_settigs = f"INSERT INTO {settings_table_name}(search, ort, umkreis, search_amount) VALUES(?, ?, ?, ?)"
    default_settings = ("Softwareentwickler", "Kiel", "25", "20")
    fields = ",".join(main_table_columns)
    settings = ",".join(user_settings)
    
    cur.execute(f"{command} {tablename} ({fields})")

    # create settings table + add default data
    cur.execute(f"{command} {settings_table_name} ({settings})")
    cur.execute(f"SELECT count(*) FROM {settings_table_name}")
    count = cur.fetchone()[0]
    # print(count)
    if count == 0:
        cur.execute(insert_default_settigs, default_settings)
    conn.commit()
    conn.close()

def update_check():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM internships")
            maxID = cur.fetchone()[0]
            if maxID is not None:
                return maxID
            return 0
    except sqlite3.Error as e:
        print(e)
        return 0
    
def add_internship(company_name, position, location, link, date_posted) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM internships")
            maxID = cur.fetchone()[0]
            if maxID is not None:
                idCount = maxID + 1
            else:
                idCount = 1
            # print(f"idcount == {idCount}")
            sql = "INSERT INTO internships(id, company_name, position, location, link, date_posted) VALUES(?, ?, ?, ?, ?, ?)"
            data = (idCount, company_name, position, location, link, date_posted)
            cur.execute(sql, data)
            conn.commit()
            return True
    except sqlite3.Error as e:
        # print(f"Error:{e}")
        return False

def get_all_internships() -> List[tuple]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM internships ORDER BY date_posted DESC')
            rowData: List[tuple] = cur.fetchall()

            return rowData, None
    except sqlite3.Error as e:
        return [], e

def get_all_settings() -> List[tuple]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM settings')
            rowData: tuple = cur.fetchone()

            return rowData, None
    except sqlite3.Error as e:
        return [], e

def get_internship_by_id(targetID) -> tuple:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            # cur.execute('SELECT * FROM internships')
            cur.execute('SELECT * FROM internships WHERE id =?', (targetID,))
            rowData: tuple = cur.fetchone()
            return [rowData], None
    except sqlite3.OperationalError as e:
        # print(e)
        return [], e

def update_status(internship_id: int, new_status: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            current_date = datetime.now() 
            cur.execute("UPDATE internships SET status=?, last_update=? WHERE id=?", (new_status, current_date.date(), internship_id))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)
        return

def update_setting(setting: str, new_setting: str | int):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE settings SET {setting}=?", (new_setting,))
            return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

# add_internship()
# print("added")