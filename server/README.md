# Covid App
This is an application that uses a python api and a java android app to create a system of informing the user about the covid data of the current county and state they are located in. 

# Setup


## Heroku

To setup this app to run in production mode on the heroku server, follow all the neccesary heroku steps first.

Then, **env** in *config.json* should be set to **prod**..

*Procfile*
web: gunicorn -t 45 app:app


## Local

To setup this app to run locally, **env** in *config.json* should be set to **dev**. 

Then, on local console, run: 
**heroku local web -f Procfile.windows**

Where Procfile.windows is a special file you must create if you are on windows to run your main app.

*Procfile.windows*
web: py app.py runserver 0.0.0.0:5000

# Other Details

Every time a user makes a request to the api, the database is hit. The only time the database is updated, is by an automatic scheduler script at 6:00am every day. This is what updates the db. 

Use *black* autoformatter to conform to PEP8 and make as consitent as possible

# Sample `config.json`
      {
          "env": "prod",

          "databaseURL": "postgres://....",
          "dev": {
              "chromeDriverPath": "C:/Users/user1/chromeDriver/chromedriver.exe",
              "googleChromePath": "C:/Program Files(x86)/Google/Chrome/Application/chrome.exe"
          },
          "prod": {
              "chromeDriverPath": "/app/.chromedriver/bin/chromedriver",
              "googleChromePath": "/app/.apt/usr/bin/google-chrome"
          }
      }
