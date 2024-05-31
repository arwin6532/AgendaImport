import sys
from db_table import db_table
import json

with open('subsession.json') as json_file:
    SUBSESSION_DICT = json.load(json_file)

AGENDA_SCHEMA = {
    "id": "integer PRIMARY KEY AUTOINCREMENT",
    "date": "text NOT NULL",
    "time_start": "text NOT NULL",
    "time_end": "text NOT NULL",
    "session_type": "text NOT NULL",
    "title": "text NOT NULL",
    "location": "text",
    "description": "text",
    "speakers": "text"
}
# Need to add "NOT NULL" for required fields (Date, Time Start, Time End, Session_Type, Title)


def find_sessions(column, value):
    
    db = db_table("agenda", AGENDA_SCHEMA)
    columns = [k for k in AGENDA_SCHEMA]

    if column == "speakers":
        query = f"SELECT * FROM agenda WHERE speakers LIKE ?"
        param = ("%" + value + "%",)
        sessions = []
        for row in db.db_conn.execute(query, param):
            result = {}
            for key, value in zip(columns, row):
                result[key] = value
            sessions.append(result)
    else:
        query = {column: value}
        sessions = db.select(where=query)
    
    subsession_list = []
    for session in sessions:
        if session["session_type"] == "Session":
            if (len(SUBSESSION_DICT[str(session["id"])]) != 0):
                for subsession_id in SUBSESSION_DICT[str(session["id"])]:
                    subsession_list.extend(db.select(where={"id": subsession_id}))
                
    return sessions + subsession_list


def parse_args(argv):
    if len(argv) != 3:
        print("Proper Usage: ./lookup_agenda.py <column> <value>. Please try again.")
        sys.exit(1)

    column = argv[1]
    value = argv[2]

    # Check for room input instead of location. Convert to location
    if column == "room":
        column = "location"
    
    elif column == "speaker":
        column = "speakers" # db_table[7]=Speakers, but valid column is 'speaker'. Must convert

    # Check for valid column. Terminate otherwise
    if column.lower() not in ["date", "time_start", "time_end", "title", "location", "description", "speakers"]: # speaker, not speakers
        print("Error: Column is not one of the valid columns. Please try again.")
        sys.exit(1)
    
    return column, value


def print_sessions(sessions):
    for row in sessions:
        print("------------Session Separator------------")

        for key, value in row.items():
            print(f"{key}: {value}")

        print("\n")


if __name__ == "__main__":
    column, value = parse_args(sys.argv)
    sessions = find_sessions(column, value)
    print_sessions(sessions)