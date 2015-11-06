class AlreadyRunException(Exception):
    def __init__(self, message):
        super(AlreadyRunException, self).__init__(message)