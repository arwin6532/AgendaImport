import sys
from db_table import db_table

AGENDA_SCHEMA = {
    "id": "integer PRIMARY KEY AUTOINCREMENT",
    "date": "text",
    "time_start": "text",
    "time_end": "text",
    "session_type": "text",
    "title": "text",
    "location": "text",
    "description": "text",
    "speakers": "text"
}

def find_sessions(db, column, value):
    sessions = db.select(where={column: value})
    return sessions


def main():
    if len(sys.argv) != 3:
        print("Usage: ./lookup_agenda.py <column> <value>")
        sys.exit(1)

    column = sys.argv[1]
    value = sys.argv[2]

    db = db_table("agenda", AGENDA_SCHEMA)
    results = find_sessions(db, column, value)

    for result in results:
        print(result)

    db.close()


if __name__ == "__main__":
    main()