import os
import psycopg2
import csv
import json 

#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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