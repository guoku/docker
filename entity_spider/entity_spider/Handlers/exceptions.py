class LinkHandlerException(Exception):
    def __init__(self, message=u''):
        self.message = message
