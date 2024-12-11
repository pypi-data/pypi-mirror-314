class UserDataFunctionError(Exception):
    def __init__(self, error_code: str, message: str = "Known User Data Function Exception Thrown", properties: dict = None):
        self.error_code = error_code
        self.message = message
        if (properties is None):
            self.properties = {}
        else:
            self.properties = properties
        super().__init__(self.message)


class UserDataFunctionInternalError(UserDataFunctionError):
    def __init__(self, message: str = "An internal execution error occured during function execution", properties: dict = None):
        super().__init__("InternalError", message, properties)


class UserDataFunctionInvalidInputError(UserDataFunctionError):
    def __init__(self, message: str = "Something went wrong when parsing an input to this function. This could be because the provided data couldn't be constructed as the data type provided, or the provided data isn't valid JSON.", properties: dict = None):
        super().__init__("InvalidInput", message, properties)


class UserDataFunctionMissingInputError(UserDataFunctionError):
    def __init__(self, message: str = "Parameter does not exist in binding data", properties: dict = None):
        super().__init__("MissingInput", message, properties)


class UserDataFunctionResponseTooLargeError(UserDataFunctionError):
    def __init__(self, limit_in_megabytes: int, properties: dict = None):
        super().__init__("ResponseTooLarge", f"Function's response size is larger than the {limit_in_megabytes} megabyte limit.", properties)


class UserDataFunctionTimeoutError(UserDataFunctionError):
    def __init__(self, timeout: int, properties: dict = None):
        super().__init__("Timeout", f"Function hit a timeout limit after {timeout} seconds but may still be running. Please check the logs for more information.", properties)


class UserThrownError(UserDataFunctionError):
    def __init__(self, message: str = "User Exception Thrown", properties: dict = None):
        super().__init__("UserThrown", message, properties)
