#!/usr/bin/env python3

import requests
import csv
import json 
import os

import flask;

from flask import Flask, request, send_file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

###### 

app = flask.Flask(__name__)
app.config["DEBUG"] = True



#$env:Path += ";C:\Users\unst0\Desktop\chromeDriver" -- need to set the path variable to add this every time

# Takes a csv file and a primary key within; converts to json
def make_json(csvFilePath, jsonFilePath): 
      
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
          



@app.route('/api/v1/byCounty/Idaho', methods=['GET'])
def api_byCounty_ID():


    #### For Heroku only
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    #############################################################

    # Actually Call The Function.
    # Decide the two file paths according to your  
    # computer system 
    csvFilePath = r'Data/ID-data.csv'
    jsonFilePath = r'Data/ID-dataF.json'
        ##### Setting up chrome to launch headless, setting the download path
    chrome_options = Options()

    ### For heroku only
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    chrome_options.add_argument("--headless")
    

    #driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    ###############################################

    ## commented out for heroku only
    #chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(chrome_options=chrome_options)

    # Use webdriver to load cookies and get a valid sesssion ID
    url = "https://public.tableau.com/profile/idaho.division.of.public.health#!/vizhome/DPHIdahoCOVID-19Dashboard/County"
    driver.get(url)
    print("\nLoading Webpage...")

    # Wait for something on the page to load, so that the session ID can be validated
    # (we wait for the iframe which contains all of the data)
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
    except:
        print("Error: Page Could Not Be Loaded/Found")
        quit()

    # Switch to the iframe which contains the table data
    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    
    # Look inside the iframe, and wait for an element of the table to appear
    # (waiting for sesssionID to be validated)
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tab-tvTLSpacer.tvimagesNS"))
        )
    except:
        print("Error: Page Could Not Be Loaded/Found")
        quit()


    # Check all response headers until we find session id, set it into sesID
    for request in driver.requests:
        try:
            #print( request.response.headers['X-Session-Id'] )
            sesID = request.response.headers['X-Session-Id']
            break
        except:
            continue

    driver.quit()

    # Go to download url with session ID, and download csv
    Download_url = ('https://public.tableau.com/vizql/w/DPHIdahoCOVID-19Dashboard/v/County/vudcsv/sessions/'
        + sesID + 
        '/views/15949333231900855173_797453858498711719?'
        'showall=true&underlying_table_id=Migrated%20Data&underlying_table_caption=Full%20Data')

    #print(Download_url)
    d = requests.get(Download_url, allow_redirects=True)
    print(d.status_code)

    # Convert the content of the request (the file) into a string
    # And store it in 'content'
    content = str(d.content)

    # Write the content to a file in csv format
    # Get rid of extra junk in string, and replace literal \n with their escape characters (so it prints correctly)
    filename = 'Data/ID-data.csv'
    fcont = content.replace("b\'\\xef\\xbb\\xbf",'').replace('\\n\'', '\n').replace('\\n', '\n').replace('\\t', '\t')
    open(filename, "w").write(fcont)

    make_json(csvFilePath, jsonFilePath)


    return send_file('Data/ID-dataF.json')

#app.run()
#For heroku
port = int(os.environ.get("PORT", 5000))
if __name__ == "main":
    app.run(host='0.0.0.0', port=port)