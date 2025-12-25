from pathlib import Path
import sqlite3
from typing import List


# Path to database file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "test.db"

idCount = 0

def table_create():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    tablename = "internships"
    command = "CREATE TABLE IF NOT EXISTS"
    fieldslist = (
        "id INTEGER NOT NULL PRIMARY KEY",
        "company_name TEXT NOT NULL",
        "position TEXT NOT NULL",
        "location TEXT NOT NULL",
        "link TEXT NOT NULL UNIQUE",
        "tech_stack TEXT",
        "date_posted TEXT NOT NULL",
        "status TEXT NOT NULL DEFAULT 'fetched'"       
   )
    fields = ",".join(fieldslist)
    cur.execute(f"{command} {tablename} ({fields})")
    conn.commit()
    conn.close()


def add_internship():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM internships")
            maxID = cur.fetchone()[0]
            if maxID is not None:
                idCount = maxID + 1
            print(f"idcount == {idCount}")
            sql = "INSERT INTO internships(id, company_name, position, location, link, date_posted) VALUES(?, ?, ?, ?, ?, ?)"
            data = (idCount, "CAU Kiel", "Student", "Kiel", "https://www.test2.de", "23.12.2025")
            cur.execute(sql, data)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
        return e

def get_all_internships() -> List[tuple]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM internships ORDER BY id DESC')
            rowData: List[tuple] = cur.fetchall()

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

def update_status(internship_id, new_status):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE internships SET status=? WHERE id=?", (new_status, internship_id))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)

# add_internship()
# print("added")