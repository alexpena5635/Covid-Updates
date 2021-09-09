class CovidData:

    def __init__(self, cases, deaths, lastseven, population, rate, county):
        self.cases = cases
        self.deaths = deaths
        self.lastseven = lastseven
        self.population = population
        self.rate = rate
        self.county = county


    def print(self):
        print("County: ", self.county)
        print(" * Cases: ", self.deaths)
        print(" * Deaths: ", self.deaths)
        print(" * LastSeven: ", self.deaths)
        print(" * Population: ", self.deaths)
        print(" * Rate: ", self.deaths)