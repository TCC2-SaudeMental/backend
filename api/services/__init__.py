class ServiceError(Exception):
    messages: str | dict[str, str | list[str]]
    status: int

    def __init__(self, messages, status=400) -> None:
        self.messages = messages
        self.status = status
