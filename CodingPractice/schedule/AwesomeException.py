class AwesomeException(Exception):

    def __init__(self, *arg, **kwargs):
        Exception.__init__(self, *args, **kwargs)


raise AwesomeException('somehow, this is an awesome exception')