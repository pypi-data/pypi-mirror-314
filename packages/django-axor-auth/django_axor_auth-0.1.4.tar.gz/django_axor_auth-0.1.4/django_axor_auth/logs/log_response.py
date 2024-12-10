class LogResponse:
    def __init__(self, status, message=None):
        self.status_code = status
        self.message = message

    def serialize(self):
        result = {"status_code": self.status_code}
        if self.message:
            result["log_message"] = self.message
        return result
