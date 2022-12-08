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