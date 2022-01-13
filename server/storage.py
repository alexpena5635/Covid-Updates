import os
import psycopg2
import csv
import json

from covid_data import CovidData

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
    counties = []
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()

        sql = """ SELECT * FROM coviddatadb.idaho_data """
            
        cur.execute(sql)
    
        con.commit()

        data = cur.fetchall()

        for row in data:
            #print(row)
            r = CovidData(*row)
            counties.append(r)
            #r.print()

        #for county in counties:
            #county.print()


        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')

  
    def obj_dict(obj):
        return obj.__dict__

    test = str(json.dumps(counties, default=obj_dict))
    obj = json.loads(test)
    formatted  = json.dumps(obj, indent=2)
    #print(formatted)


    #return json.dumps(counties, default=obj_dict)
    return formatted