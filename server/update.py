import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

from bs4 import BeautifulSoup
import json

import storage
from utils import get_config

config = get_config()
env = config["env"]

# Takes an Options() object from selenium chrome options
# Returns the same object with arguments set
def set_chrome_options(Options):
    ops = Options
    ops.binary_location = config[env]["googleChromePath"]  # google chrome path

    # Arguments for running selenium with chrome on server with no gui
    ops.add_argument("--no-sandbox")
    ops.add_argument("--headless")
    ops.add_argument("--disable-gpu")
    return ops


def update_idaho():
    # Chrome options specific to Heroku
    chrome_options = set_chrome_options(Options())

    # Create a new webdriver
    driver = webdriver.Chrome(
        executable_path=config[env]["chromeDriverPath"], chrome_options=chrome_options
    )

    url = "https://public.tableau.com/profile/idaho.division.of.public.health#!/vizhome/DPHIdahoCOVID-19Dashboard/County"

    # Use the webdriver to request the webpage
    driver.get(url)
    print("\nLoading Webpage...")

    # We need to get a session ID from the webpage, so we can download the data later
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
    iframe = driver.find_elements_by_tag_name("iframe")[0]
    driver.switch_to.frame(iframe)

    # Look inside the iframe, and wait for an element of the table to appear
    # (waiting for sesssionID to be validated)
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tab-tvTLSpacer.tvimagesNS")
            )
        )
    except:
        print("Error: Page Could Not Be Loaded/Found")
        quit()

    # Check all response headers for each request the webdriver made, until we find the session id
    for request in driver.requests:
        try:
            # Try getting the session id header
            ses_id = request.response.headers["x-session-id"]

            # If there was no session id header, ses_id will be "None"
            # Otherwise, the session id is found, so break out of the loop
            if ses_id.strip() != "None":
                break
        except:
            continue

    driver.quit()

    print(ses_id)

    # Create download url with session ID
    download_url = (
        "https://public.tableau.com/vizql/w/DPHIdahoCOVID-19Dashboard/v/County/vudcsv/sessions/"
        + str(ses_id)
        + "/views/15949333231900855173_797453858498711719?"
        "showall=true&underlying_table_id=Migrated%20Data&underlying_table_caption=Full%20Data"
    )

    # Request the url, and downlaod the csv file containing the data
    response = requests.get(download_url, allow_redirects=True)
    print(response.status_code)

    # Get the body of the response, and convert it to a string
    # The content should be a csv formatted string
    content = str(response.content)

    # Get rid of extra junk in the string, and replace literal \n with their escape characters (so it prints correctly)
    content_as_csv = (
        content.replace("b'\\xef\\xbb\\xbf", "")
        .replace("\\n'", "\n")
        .replace("\\n", "\n")
        .replace("\\t", "\t")
    )

    # Convert the csv string to a json string
    content_as_json = storage.csv_to_json(content_as_csv)

    # Update Idaho's covid data in the database
    storage.update_state_data("Idaho", content_as_json)


def update_washington():
    # Chrome options specific to Heroku
    chrome_options = set_chrome_options(Options())

    # Create a new webdriver
    driver = webdriver.Chrome(
        executable_path=config[env]["chromeDriverPath"], chrome_options=chrome_options
    )

    url = "https://www.doh.wa.gov/Emergencies/COVID19/DataDashboard#downloads"

    # Use the webdriver to request the webpage
    driver.get(url)
    print("\nLoading Webpage...")

    soup = BeautifulSoup()

    # Wait for the table element containing the case/death data to load
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "pnlConfirmedCasesDeathsTbl"))
        )

        # Once it loads, create soup of the HTML of the table
        soup = BeautifulSoup(element.get_attribute("innerHTML"), features="html.parser")

    except:
        print("Error: Page Could Not Be Loaded/Found")
        quit()

    driver.quit()

    table = soup.get_text().strip()

    # Identify the starting and stopping index of data in the string representing the table
    start_index = table.find("Adams")
    end_index = table.find("Total")

    # Shorten the string to the only neccesary table data
    table_condensed = table[start_index:end_index].strip()

    county_list = []

    # Split the string into a list, each item being a county with its data
    # The delimiter is two newliens
    county_strings = table_condensed.split("\n\n")

    # Loop through each county with all of its data "string"
    for c in county_strings:

        # Split each field of the county into its own seperate space
        c = c.strip().split("\n")

        # Append the list of county with data to a list of all counties with data
        county_list.append(c)

    county_data = []

    # Loop through each county data "list" in the overarching list
    for c in county_list:

        # Create a representative dictioanry with keys for the county
        county = {
            "County": c[0],
            "Confirmed": c[1].replace(",", ""),
            "Deaths": c[3].replace(",", ""),
            "Population": 0,
            "Last Seven": 0,
            "Rate": 0,
        }

        # Add this to a list of all counties translated into this format
        county_data.append(county)

    # Convert the list of counties as dictionaries, into a json formatted string
    content_as_json = str(json.dumps(county_data))

    # Update Washingtons's covid data in the database
    storage.update_state_data("Washington", content_as_json)


def update_oregon():

    url = "https://govstatus.egov.com/OR-OHA-COVID-19"

    raw_data = ""

    try:
        res = requests.get(url)

        # Create soup from the html of the webpage
        soup = BeautifulSoup(str(res.content), features="html.parser")

        # Get the text from the HTML of the table with data
        raw_data = soup.find(id="collapseDemographics").get_text().strip()
    except:
        print("ERROR: Page data could not load/be found for Oregon\n")
        quit()

    # Identify the starting and stopping index of data in the string representing the table
    start_index = raw_data.find("Baker")
    end_index = raw_data.find("Total")

    # Slice the data to only the relavant part of the string
    condensed_data = raw_data[start_index:end_index].strip()

    # Split the string representing data into a list of strings with no distincition between each county
    list_data = condensed_data.split("\\r\\n")

    county_list = []

    # Loop through the list of counties, cases, deaths, etc
    # Create new lists which hold the data for each specific county
    # Append this to the county_list "list"
    # Iterate by 3 because each county has 3 pieces of the list with it corresponding
    for i in range(0, len(list_data), 3):
        county_list.append(list_data[i : i + 3])

    county_data = []

    # For each county in the list
    for c in county_list:

        # If there is only item in the list, then this is the very last item, we dont need to do this
        if len(c) == 1:
            continue

        # Create a dictioanry-formatted item for the list
        county = {
            "County": c[0],
            "Confirmed": c[1],
            "Deaths": c[2],
            "Population": 0,
            "Last Seven": 0,
            "Rate": 0,
        }

        # Add it
        county_data.append(county)

    # Convert the list of entires into a json formatted string
    content_as_json = str(json.dumps(county_data))

    # Update Oregon's covid data in the database
    storage.update_state_data("Oregon", content_as_json)


update_idaho()
update_washington()
update_oregon()
