"""
自定义异常类
"""


class LRunException(Exception):
    pass


class NoSuchNodeException(LRunException):
    """
    This is NoSuchNodeException
    """
    pass


class InvalidOperationException(LRunException):
    """
    This is InvalidOperationException
    """
    pass


class TargetTimeout(LRunException):
    """
    This is TargetTimeout
    """
    pass


class ConnectError(LRunException):
    """
    This is ConnectError
    """
    pass


class AdbError(LRunException):
    """
    This is AdbError
    """
    pass


class InvalidParamError(LRunException):
    """
    This is InvalidParamError
    """
    pass


class FilteredRectsNotEmpty(Exception):
    def __init__(self, message="疑似资源缺失"):
        self.message = message
        super().__init__(self.message)

    def handle(self):
        print(self.message)


class NotFoundPatch(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
