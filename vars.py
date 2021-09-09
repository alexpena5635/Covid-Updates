#!/usr/bin/env python3
local = False

if local:
    #CHROMEDRIVER_PATH = r'C:/Users/unst0/Desktop/chromeDriver/chromedriver.exe' #local path laptop
    CHROMEDRIVER_PATH = r'C:/Users/alexp/Desktop/cdriver/chromedriver.exe' #local path for desktop
    GOOGLE_CHROME_PATH= r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe' #local path
else:
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

csvFilePath = r'Data/ID-data.csv'
jsonFilePath = r'Data/ID-data.json'

# Returns an Options() object from selenium chrome options
def setChromeOptions(Options):
    ops = Options
    ops.binary_location = GOOGLE_CHROME_PATH
    ops.add_argument('--no-sandbox')
    ops.add_argument("--headless")
    ops.add_argument('--disable-gpu')
    return ops
