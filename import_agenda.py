from db_table import db_table
import sys
import pandas as pd
import xlrd


# Declare schema at the top for clarity!
AGENDA_SCHEMA = {
    "id": "integer PRIMARY KEY AUTOINCREMENT",
    "date": "text",
    "time_start": "text",
    "time_end": "text",
    "session_type": "text",
    "title": "text",
    "room": "text",
    "description": "text",
    "speakers": "text"
}


def load_agenda(filename):
    # Open the workbook using xlrd and obtain sheet index! 
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    
    # Define the column names
    columns = ['Date', 'Start Time', 'End Time', 'Session Type', 'Title', 'Room', 'Description', 'Speakers']
    
    # Initialize an empty list to hold the rows
    data = []
    
    # Iterate over the rows, starting from the 14th row (index 13)
    for row_idx in range(15, sheet.nrows):
        row = sheet.row(row_idx)
        data.append([cell.value for cell in row])
    
    # Create a DataFrame (I'm more familiar with this library)
    agenda_df = pd.DataFrame(data, columns=columns)
    
    return agenda_df


def create_agenda(agenda) -> None:
    # Create empty SQLite3 database
    agenda_table = db_table("agenda", AGENDA_SCHEMA)

    # For each row in agenda's 
    for _, row in agenda.iterrows():
        # Create object to insert into agenda table
        agenda_row = {
            "date": row['Date'],
            "time_start": row['Start Time'],
            "time_end": row['End Time'],
            "session_type": row['Session Type'],
            "title": row['Title'],
            "room": row['Room'],
            "description": row['Description'],
            "speakers": row['Speakers']
        }
        # Insert into agenda table
        agenda_table.insert(agenda_row)
        # Debug statement
        print(_, row)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Less than or more than 2 given arguments. Please provide command line input as \"./import_agenda.py <filename>\"")
    else:
        agenda = load_agenda(sys.argv[1])
        create_agenda(agenda)
