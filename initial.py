import sqlite3
from pprint import pprint


# Create new database and cursor
conn = sqlite3.connect('users_info.db')
c = conn.cursor()

# Create answer table

create_answer_table = """
    CREATE TABLE IF NOT EXISTS users_info 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    date TEXT, 
    us_answer INTEGER, 
    is_correct INTEGER, 
    start_time INTEGER, 
    end_time INTEGER, 
    duration INTEGER)
"""

# c.execute(create_answer_table)
# conn.commit()
# c.close()
# conn.close()

# Check answer table

query = """
    SELECT * FROM users_info
"""
c.execute(query)
pprint(c.fetchall())
conn.commit()
c.close()
conn.close()

