# Class/ data struct for covid data for any state (modeled after ID)
class CovidData:
    # Constructor
    def __init__(self, cases, deaths, lastseven, population, rate, county):
        self.county = county
        self.cases = cases
        self.deaths = deaths
        self.lastseven = lastseven
        self.population = population
        self.rate = rate

    def print(self):
        print("County: ", self.county)
        print(" * Cases: ", self.cases)
        print(" * Deaths: ", self.deaths)
        print(" * LastSeven: ", self.lastseven)
        print(" * Population: ", self.population)
        print(" * Rate: ", self.rate)