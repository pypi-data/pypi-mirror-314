class Error(Exception):
    def __init__(self, message):
        self.message = message


class BadlySpecifiedTemplateError(Error):
    pass

class EmptyStackException(Exception):
  pass
