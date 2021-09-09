import os
import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import sys
import json

from covid_data import CovidData

from flask import jsonify

# Takes a csv file and a primary key within; converts to json
def makeJSON(csvFilePath, jsonFilePath): 
    # create a dictionary 
    data = {} 
      
    # Open a csv reader called DictReader 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
          
        # Convert each row into a dictionary  
        # and add it to data 
        for rows in csvReader: 
              
            # Assuming a column named 'County' to 
            # be the primary key 
            key = rows['County'] 
            data[key] = rows 
  
    # Open a json writer, and use the json.dumps()  
    # function to dump data 
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonf.write(json.dumps(data, indent=4))
    
    return json.dumps(data, indent=4)

def testPostgres():
    # read database connection url from the enivron variable we just set.
    DATABASE_URL = os.environ['DATABASE_URL']
    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        
        # execute an SQL statement to get the HerokuPostgres database version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        
        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')


def postgresInsertIdahoData(jsonString):
    # read database connection url from the enivron variable we just set.
    DATABASE_URL = os.environ['DATABASE_URL']
    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()

        sql = """ INSERT INTO coviddatadb.idaho_data("Cases", "Deaths", "LastSeven", "Population", "Rate", "County")
           VALUES (%s, %s, %s, %s, %s, %s) """

        County = Cases = Deaths = LastSeven = Population = Rate = ""
        jsonObject = json.loads(jsonString)
        for object in jsonObject:
            value = jsonObject[object]
            
            County = Cases = Deaths = LastSeven = Population = Rate = ""
            for key in value:
               if(key == "County"):
                  County = value[key]
               elif(key == "Confirmed"):
                   Cases = value[key]
               elif(key == "Deaths"):
                   Deaths = value[key]
               elif(key == "LastSeven"):
                   LastSeven = value[key]
               elif(key == "Population"):
                   Population = value[key]
               elif(key == "Rate"):
                   Rate = value[key]

               #print("The key and value are ({}) = ({})".format(key, value[key]))
            
            cur.execute(sql, (Cases, Deaths, LastSeven, Population, Rate, County,))
    

        con.commit()

        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')

####### Move the call to actually do the whole selenium thing to a seperate function/file?
####### This will run on a cron job, and only be called once a day at say 6:00 am
####### That file will update the database
####### The regular api will only go and get the database itself, it wont query with selenium each time!!!!!!
####### Once this is in place, it will make subsequent calls to the api much much faster, and stage one of the refactor will be in minumum viable forms


def postgresUpdateIdahoData(jsonString):
    # read database connection url from the enivron variable we just set.
    DATABASE_URL = os.environ['DATABASE_URL']
    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()

        sql = """ UPDATE coviddatadb.idaho_data
                SET "Cases" = %s, "Deaths" = %s, "LastSeven" = %s, "Population" = %s, "Rate" = %s
                WHERE "County" = %s
            """

        County = Cases = Deaths = LastSeven = Population = Rate = ""
        jsonObject = json.loads(jsonString)
        for object in jsonObject:
            value = jsonObject[object]
            
            County = Cases = Deaths = LastSeven = Population = Rate = ""
            for key in value:
               if(key == "County"):
                  County = value[key]
               elif(key == "Confirmed"):
                   Cases = value[key]
               elif(key == "Deaths"):
                   Deaths = value[key]
               elif(key == "LastSeven"):
                   LastSeven = value[key]
               elif(key == "Population"):
                   Population = value[key]
               elif(key == "Rate"):
                   Rate = value[key]

               #print("The key and value are ({}) = ({})".format(key, value[key]))
            
            cur.execute(sql, (Cases, Deaths, LastSeven, Population, Rate, County,))
    

        con.commit()

        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')


def postgresGETIdahoData():
    # read database connection url from the enivron variable we just set.
    DATABASE_URL = os.environ['DATABASE_URL']
    con = None
    data = ""
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor(cursor_factory=RealDictCursor)

        sql = """ SELECT * FROM coviddatadb.idaho_data """
            
        cur.execute(sql)
    
        con.commit()

        data = cur.fetchall()
        #print(data)

        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')

    print(json.dumps(data))
    return json.dumps(data)