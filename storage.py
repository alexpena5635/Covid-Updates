import os
import psycopg2
import csv
import json 

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

    # read database connection url from the enivron variable we just set.
    DATABASE_URL = os.environ['DATABASE_URL']
    con = None
    try:
        # create a new database connection by calling the connect() function
        print("Here is the URL ---> " + DATABASE_URL)
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