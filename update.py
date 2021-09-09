import vars
import storage

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver


# Chrome options specific to Heroku
chrome_options = vars.setChromeOptions(Options())

driver = webdriver.Chrome(
    executable_path=vars.CHROMEDRIVER_PATH, chrome_options=chrome_options
)

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
        sesID = request.response.headers['x-session-id']
        if(sesID.strip() != "None"): # Added this check!
            break
    except:
        continue
driver.quit()
# Go to download url with session ID, and download csv
print(sesID)
Download_url = ('https://public.tableau.com/vizql/w/DPHIdahoCOVID-19Dashboard/v/County/vudcsv/sessions/'
    + str(sesID) + 
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
jsonString = storage.makeJSON(vars.csvFilePath, vars.jsonFilePath)

#storage.postgresInsertIdahoData(jsonString)
storage.postgresUpdateIdahoData(jsonString)
