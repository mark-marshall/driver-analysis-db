from pymongo import MongoClient
import csv

connection  = MongoClient(f"mongodb+srv://mm260:UlChjqXiYBzRkJVb@driver-analysis-1hurl.mongodb.net/production?retryWrites=true")
db = connection.production

records = []
careers = {}

def formatFL(fl):
    '''
    This method takes a fastest lap in the form of a string, returns NULL
    for any laps if Non-Type is provided or if the float(string) value is 
    less than 50, and returns the float(string) value for any other values
    of fl.
    '''
    formated_fl = fl
    if not fl:
        formated_fl = 'NULL'
    elif ((not fl ==  'NULL') and (float(fl) < 50)):
        formated_fl = 'NULL'
    elif not fl == 'NULL':
        formated_fl = float(fl)
    return formated_fl

def teammateFL(driver, team, event, session):
    '''
    This method takes a 3-letter driver acronym, a team name, an event  ID,
    and a session type. It returns the fastest lap of the teammates driver
    in the given session.
    '''
    # open and read csv
    with open('dbLaptime.csv') as teammates_csv:
        teammates = csv.reader(teammates_csv, delimiter=',')
        line = 0
        # loop over rows
        for row in teammates:
            # skip the headers
            if line == 0:
                line += 1
            # find row that links to the drivers teammate
            elif row[1] == event and row[2] == session and row[3] == team and row[4] != driver:
                return row[5]

with open('dbLaptime.csv') as laps_csv:
    # open and read csv
    laps = csv.reader(laps_csv, delimiter=',')
  # loop to populate driver data
    line = 0
    for row in laps:
      # skip the headers
      if line == 0:
        line += 1
      # append data from subsequent rows
      else:
        if row[4] not in careers:
            careers[row[4]] =  {}
            records.append(row[4])
        if row[0] not in careers[row[4]]:
            careers[row[4]][row[0]] = []
        careers[row[4]][row[0]].append({
            "event": row[1],
            "session": row[2],
            "team": row[3],
            "fl": formatFL(row[5]),
            "teammate_fl": formatFL(teammateFL(row[4],row[3],row[1],row[2]))
        })

# populate the database
for record in records:
    db.data.insert_one({
        "name": record,
        "career": careers[record]
    })
