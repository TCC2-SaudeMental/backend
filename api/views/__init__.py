class JSONFormatException(Exception):
    messages: str | dict[str, str | list[str]]
    status: int

    def __init__(self) -> None:
        self.status = 400
        self.messages = (
            'O corpo da request precisa ser no formato {chave: valor}'
        )


def response(data) -> tuple[dict, int, dict[str, str]]:
    return (
        {
            'status': "success",
            'data': data
        }, 200, {
            'Content-Type': 'application/json'
        }
    )


def error(status: int, data) -> tuple[dict, int, dict[str, str]]:
    return (
        {
            'status': "error",
            'data': data
        }, status, {
            'Content-Type': 'application/json'
        }
    )
