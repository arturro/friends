class UserException(Exception):
    def __init__(self, message=None):
        self.message = message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return unicode(self).encode('utf8')


class IncorrectUID(UserException):
    pass