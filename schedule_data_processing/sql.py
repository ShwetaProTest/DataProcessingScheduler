import sqlite3
import pandas as pd
import json

# Create SQLite connection and cursor
conn = sqlite3.connect('airline_data.db')
cursor = conn.cursor()

# Create Schedule table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schedule (
        aircraft_registration TEXT PRIMARY KEY,
        departure_airport TEXT,
        arrival_airport TEXT,
        scheduled_departure_time TEXT,
        scheduled_takeoff_time TEXT,
        scheduled_landing_time TEXT,
        scheduled_arrival_time TEXT,
        flight_number TEXT
    )
''')

# Load data from schedule.json
with open('data_files/schedule.json') as f:
    schedule_data = json.load(f)

# Insert data into Schedule table
for entry in schedule_data:
    cursor.execute('''
        INSERT OR REPLACE INTO Schedule (
            aircraft_registration, departure_airport, arrival_airport,
            scheduled_departure_time, scheduled_takeoff_time,
            scheduled_landing_time, scheduled_arrival_time, flight_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry['aircraft_registration'],
        entry['departure_airport'],
        entry['arrival_airport'],
        entry['scheduled_departure_time'],
        entry['scheduled_takeoff_time'],
        entry['scheduled_landing_time'],
        entry['scheduled_arrival_time'],
        entry['flight_number']
    ))

# Commit changes
conn.commit()

# Create Fleet table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Fleet (
        IATATypeDesignator TEXT PRIMARY KEY,
        TypeName TEXT,
        F INTEGER,
        C INTEGER,
        E INTEGER,
        M INTEGER,
        Total INTEGER,
        Reg TEXT,
        RangeLower INTEGER,
        RangeUpper INTEGER,
        Hub TEXT,
        Haul TEXT
    )
''')

# Load data from fleet.csv
fleet_data = pd.read_csv('data_files/fleet.csv')

# Insert data into Fleet table
fleet_data.to_sql('Fleet', conn, if_exists='replace', index=False)

# Create Airports table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Airports (
        AirportCode TEXT PRIMARY KEY,
        City TEXT,
        Country TEXT,
        Name TEXT,
        CityName TEXT,
        CountryName TEXT,
        Lat REAL,
        Lon REAL,
        Alt INTEGER,
        UTCOffset INTEGER
    )
''')

# Load data from airports.csv
airports_data = pd.read_csv('data_files/airports.csv')

# Insert data into Airports table
airports_data.to_sql('Airports', conn, if_exists='replace', index=False)

# Close connection
conn.close()
