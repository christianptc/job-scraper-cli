from pathlib import Path
import sqlite3
from typing import List
from datetime import datetime


# Path to main directory 
BASE_DIR = Path(__file__).resolve().parent.parent

# Creates database file if not exists in main directory
DB_PATH = BASE_DIR / "internships.db"

tablename = "internships"
temptablename = "scraped_internships"
settings_table_name = "settings"

def table_create() -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            command = "CREATE TABLE IF NOT EXISTS"
            table_columns = (
                "id INTEGER NOT NULL PRIMARY KEY",
                "company_name TEXT NOT NULL",
                "position TEXT NOT NULL",
                "location TEXT NOT NULL",
                "link TEXT NOT NULL UNIQUE",
                "date_posted TEXT NOT NULL",
                "status TEXT NOT NULL DEFAULT 'fetched'",
                "last_update TEXT"   
            )
            temp_columns = (
                "id INTEGER NOT NULL PRIMARY KEY",
                "company_name TEXT NOT NULL",
                "position TEXT NOT NULL",
                "location TEXT NOT NULL",
                "link TEXT NOT NULL UNIQUE",
                "date_posted TEXT NOT NULL",  
            )
            user_settings = (
                "search TEXT",
                "ort TEXT",
                "umkreis INTEGER",
                "search_amount INTEGER"
            )
            insert_default_settigs = f"INSERT INTO {settings_table_name}(search, ort, umkreis, search_amount) VALUES(?, ?, ?, ?)"
            default_settings = ("Softwareentwickler", "Kiel", "25", "20")
            fields = ",".join(table_columns)
            tempfields = ",".join(temp_columns)
            settings = ",".join(user_settings)

            #creates if not exists main table where all user prefered jobs
            cur.execute(f"{command} {tablename} ({fields})")

            #creates if not exists temp table to show all scraped jobs
            cur.execute(f"{command} {temptablename} ({tempfields})")

            # create settings table + add default settings
            cur.execute(f"{command} {settings_table_name} ({settings})")

            cur.execute(f"SELECT count(*) FROM {settings_table_name}")
            count = cur.fetchone()[0]
            # print(count)
            if count == 0:
                cur.execute(insert_default_settigs, default_settings)

            return
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return

def update_check() -> int:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT MAX(id) FROM {tablename}")
            maxID = cur.fetchone()[0]
            if maxID is not None:
                return maxID
            return 0
    except sqlite3.Error as e:
        print(f"Error:{e}")
        return 0
    
def add_internship(company_name, position, location, link, date_posted) -> bool | int:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            sql = f"INSERT INTO {tablename}(company_name, position, location, link, date_posted, last_update) VALUES(?, ?, ?, ?, ?, ?)"
            data = (company_name, position, location, link, date_posted, datetime.now().date())
            cur.execute(sql, data)
            idCount = cur.lastrowid

            return True, idCount
    except sqlite3.Error as e:
        print(f"Error:{e}")
        return False, 0

def scrape_internship(company_name, position, location, link, date_posted) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            sql = f"INSERT INTO {temptablename}(company_name, position, location, link, date_posted) VALUES(?, ?, ?, ?, ?)"
            data = (company_name, position, location, link, date_posted)
            cur.execute(sql, data)
            return True
    except sqlite3.Error as e:
        return False


def move_internship(targetID) -> bool | int:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT MAX(id) FROM {temptablename}")
            maxtempID = cur.fetchone()[0]

            if maxtempID is not None:
                if int(maxtempID) < int(targetID):
                    return False, 0
                
                cur.execute(f'SELECT * FROM {temptablename} WHERE id =?', (targetID,))

                id, company_name, position, location, link, date_posted = cur.fetchone()
                # print(type(id))
                check, id = add_internship(company_name, position, location, link, date_posted)
                if check:
                    return True, id
            
            return False, 0
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return False, 0

def get_all_internships() -> List[tuple] | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {tablename} ORDER BY date_posted DESC')
            rowData: List[tuple] = cur.fetchall()

            return rowData, None
    except sqlite3.Error as e:
        return [], e

def get_all_scrapes() -> List[tuple] | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {temptablename} ORDER BY date_posted ASC')
            rowData: List[tuple] = cur.fetchall()
            if rowData == []:
                return [None], None
            return rowData, None
    except sqlite3.Error as e:
        return [None], e

def get_all_settings() -> List[tuple] | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {settings_table_name}')
            rowData: tuple = cur.fetchone()

            return rowData, None
    except sqlite3.Error as e:
        return [], e

def get_internship_by_id(targetID) -> tuple | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {tablename} WHERE id =?', (targetID,))
            rowData: tuple = cur.fetchone()
            return [rowData], None
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return [], e

def update_status(internship_id: int, new_status: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            current_date = datetime.now() 
            cur.execute(f"UPDATE {tablename} SET status=?, last_update=? WHERE id=?", (new_status, current_date.date(), internship_id))

            return
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return

def update_setting(setting: str, new_setting: str | int) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE {settings_table_name} SET {setting}=?", (new_setting,))
            return True
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return False

def clear_temp_database() -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {temptablename}")
            return True
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return False

def delete_internship(targetID) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {tablename} WHERE id=?", (targetID,))
            return True
    except sqlite3.OperationalError as e:
        print(f"Error:{e}")
        return False

# add_internship()
# print("added")

# move_internship(1)