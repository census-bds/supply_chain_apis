class RequestBlankException(Exception):
    def __init__(self, url):
        super().__init__(url + " returns blank results.")