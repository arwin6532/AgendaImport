from db_table import db_table
import sys
import pandas as pd
import xlrd
import json


# Declare schema at the top for clarity!
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

def load_agenda(filename):
    # Open the workbook using xlrd and obtain sheet index! 
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    
    # Define the column names
    columns = ['Date', 'Start Time', 'End Time', 'Session Type', 'Title', 'Location', 'Description', 'Speakers']
    
    # Initialize an empty list to hold the rows
    data = []
    subsMapIdx = {}
    subsMapStrFormat = {}
    # Iterate over the rows, starting from the 14th row (index 13)
    for row_idx in range(15, sheet.nrows):
        prime_key = row_idx-14
        row = sheet.row(row_idx)
        data.append([cell.value for cell in row])
        if row[3].value == 'Session':
            lastSession = prime_key
            subsMapIdx[prime_key] = []
            subsMapStrFormat[prime_key] = ""
        elif row[3].value == 'Sub':
            subsMapIdx[lastSession].append(prime_key)
            outputString = ""
            for cell in row:
                outputString += str(cell.value) + " "
            subsMapStrFormat[lastSession] += outputString


    with open('subsession.json', 'w') as json_file:
        json.dump(subsMapIdx, json_file, indent=4)
    
    # Precalculates every result with subsessions, can be slightly faster than calculating during execution
    with open('subsMapStrFormat.json', 'w') as json_file:
        json.dump(subsMapStrFormat, json_file, indent=4)

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
            "location": row['Location'],
            "description": row['Description'],
            "speakers": row['Speakers']
        }
        # Insert into agenda table
        agenda_table.insert(agenda_row)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Less than or more than 2 given arguments. Please provide command line input as \"./import_agenda.py <filename>\"")
        sys.exit(1)
    else:
        agenda = load_agenda(sys.argv[1])
        create_agenda(agenda)
    
