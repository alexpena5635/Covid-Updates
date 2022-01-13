import json

from typing import List

# Class structure containing covid data fields for any State, County
class CovidData:
    # Constructor
    def __init__(self, state, county, population, cases, deaths, last_seven, rate):
        self.state = state
        self.county = county
        self.cases = cases
        self.deaths = deaths
        self.last_seven = last_seven
        self.population = population
        self.rate = rate

    def print(self):
        print("State, County: ", self.state + ", " + self.county)
        print(" * Cases: ", self.cases)
        print(" * Deaths: ", self.deaths)
        print(" * LastSeven: ", self.last_seven)
        print(" * Population: ", self.population)
        print(" * Rate: ", self.rate)


# Take a json formatted string, and return a list of CovidData objects
def json_to_covid_data(state: str, counties_string: str) -> List[CovidData]:
    try:
        counties_object = json.loads(counties_string)

        covid_data = []

        for county in counties_object:
            covid_data.append(
                CovidData(
                    state,
                    county["County"],
                    county["Population"],
                    county["Confirmed"],
                    county["Deaths"],
                    county["Last Seven"],
                    county["Rate"],
                )
            )
    except Exception as error:
        print("Cause: Error converting to CovidData object - {}".format(error))

    # return a list of CovidData objects
    return covid_data


# Takes an object, returns a dictionary representing it
def obj_dict(obj):
    return obj.__dict__


# Take a list of CovidData objects, and returns a json formatted string
def covid_data_to_json(covid_data: List[CovidData]) -> str:
    try:
        # Load the CovidData object as a dictionary, then makes a string representation of it
        counties_string = str(json.dumps(covid_data, default=obj_dict))
    except Exception as error:
        print(
            "Cause: Error converting CovidData object to json formatted string - {}".format(
                error
            )
        )

    # return a json formatted string of counties
    return counties_string
