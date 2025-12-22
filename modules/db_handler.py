from pathlib import Path
import sqlite3

# Path to database file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "test.db"

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


def get_all_internships():
    return 0


def get_internship_by_id(targetID):
    return 0