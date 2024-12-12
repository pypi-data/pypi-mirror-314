class NoLogException(Exception):
    def __init__(self):
        super().__init__("No movie in the collection")
