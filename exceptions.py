class RequestBlankException(Exception):
    def __init__(self, url):
        super().__init__(url + " returns blank results.")

class FutureYearException(Exception):
    def __init__(self, year):
        super().__init__("Year {} is in the future. No data exists yet.".format(
            year
        ))

class InvalidSurveyYear(Exception):
    def __init__(self, name, year):
        super().__init__("{} is not available in year {}.".format(
            name, year
        ))

class UnknownDataSource(Exception):
    def __init__(self, name):
        super().__init__("{} has not been built into this wrapper yet or is an unknown data source".format(
            name
        ))

class TooManyFields(Exception):
    def __init__(self):
        super().__init__("Number of fields exceeds API limit.")