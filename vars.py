#!/usr/bin/env python3
import os
import flask

#### For Heroku only
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# Decide the two file paths according to your system 
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
