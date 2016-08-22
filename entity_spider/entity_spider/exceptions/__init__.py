class MessageException(Exception):
    def __init__(self, message='', *args, **kwargs):
        super(MessageException, self).__init__(*args, **kwargs)
        self._message = message