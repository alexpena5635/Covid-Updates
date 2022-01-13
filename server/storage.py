import psycopg2
import csv
import json
import io

from typing import List


from covid_data import CovidData, json_to_covid_data, covid_data_to_json
from utils import get_config

config = get_config()

# Takes a csv formatted string, and returns json string
def csv_to_json(csv_string):

    csvReader = csv.DictReader(io.StringIO(csv_string))
    json_data = json.dumps(list(csvReader))

    return str(json_data)


# Opens connection to db, return connection and cursor
def open_db():
    # Retreives the postgres DB url from environment variable
    DATABASE_URL = config["databaseURL"]
    con = None

    try:
        # Create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

    except Exception as error:
        print("Database Connection Failed - Cause: {}".format(error))

    #  Create a new cursor
    cur = con.cursor()

    return con, cur


# Takes in a postgres DB connection and cursor, closes the connetion
def close_db(con, cur):
    try:
        # Commit any changes made by the current connection
        con.commit()

        # Close the communication with the HerokuPostgres db
        cur.close()
    except Exception as error:
        print("Cause: {}".format(error))

    # Close the communication with the server
    if con is not None:
        con.close()
        print("Database connection succesfully closed.")


# Inserts a string of all county data for the given state into the database
def insert_state_data(state: str, counties_data: str):
    # Open the connection to the database
    con, cur = open_db()
    try:
        sql = """ INSERT INTO coviddatadb.covid_data(state, county, population, cases, deaths, last_seven, rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s) """

        # Convert the json formatted counties into CovidData objects
        counties = json_to_covid_data(state, counties_data)

        # Add each county to the database
        # *county unpacks it into all of its members/arguments
        for county in counties:
            cur.execute(
                sql,
                (
                    state,
                    county.county,
                    county.population,
                    county.cases,
                    county.deaths,
                    county.last_seven,
                    county.rate,
                ),
            )

    except Exception as error:
        print("Cause: {}".format(error))

    # Close the connection to the database
    close_db(con, cur)


# Update all counties for the given state in the database
def update_state_data(state: str, counties_data: str):
    # Open the connection to the database
    con, cur = open_db()
    try:
        sql = """ UPDATE coviddatadb.covid_data
                SET population = %s, cases = %s, deaths = %s, last_seven = %s, rate = %s
                WHERE state = %s AND county = %s
            """

        # Convert the json formatted string of counties into a list of CovidData objects
        counties = json_to_covid_data(state, counties_data)

        # Update each county's fields in the database
        for county in counties:
            cur.execute(
                sql,
                (
                    county.population,
                    county.cases,
                    county.deaths,
                    county.last_seven,
                    county.rate,
                    county.state,
                    county.county,
                ),
            )

    except Exception as error:
        print("Cause: {}".format(error))

    # Close the connection to the database
    close_db(con, cur)


# Get all county data for the state, and return it
def get_state_data(state):
    # Open connection to the database
    con, cur = open_db()
    counties: List[CovidData] = []

    # Convert the state string to only the first letter uppercase, as is needed in the database
    state = state.title()
    try:
        sql = """ SELECT * FROM coviddatadb.covid_data 
                WHERE state = %s
                ORDER BY county """

        cur.execute(sql, (state,))

        # Get all rows from the query
        data = cur.fetchall()

        # Loop through each row/county and init a CovidData object with its data
        #  Then append it to the list of counties
        for row in data:
            r = CovidData(*row)
            counties.append(r)

    except Exception as error:
        print("Cause: {}".format(error))

    if not counties:
        return "No data found for state: " + state

    # Reformatting the list of data for each county into a json formatted string
    counties_json = covid_data_to_json(counties)

    # Close the connection to the database
    close_db(con, cur)

    return counties_json


# Get specifc county data for a state, and return it
def get_county_data(state, county):
    # Open connection to the database
    con, cur = open_db()

    # Convert the state and county strings to only the first letter uppercase, as is needed in the database
    state = state.title()
    county = county.title()
    try:
        sql = """ SELECT * FROM coviddatadb.covid_data
                WHERE state = %s AND county = %s """

        cur.execute(
            sql,
            (
                state,
                county,
            ),
        )

        # Get row from the query
        data = cur.fetchone()

        # Unpack the covid data in the row into a CovidData object and initialize it
        county = CovidData(*data)

    except Exception as error:
        print("Cause: {}".format(error))

    if not county:
        return "No data found for state, county: " + state + ", " + county

    # Reformatting the list of data for each county into json formatted string
    county_json = covid_data_to_json(county)

    # Close the connection to the database
    close_db(con, cur)

    return county_json
