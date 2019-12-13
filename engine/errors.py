class Basic(Exception):
    def __init__(self):
        pass


class Cheating:
    def __init__(self, msg, reason):
        self.msg = msg
        self.reason = reason
