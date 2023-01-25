class ServerError(Exception):
    status_code = 500

    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)


class MBTAUnreachable(ServerError):
    pass


class MBTAError(ServerError):
    pass


class InvalidStationName(ServerError):
    pass
