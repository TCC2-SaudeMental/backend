from functools import wraps
from sqlalchemy.exc import ProgrammingError


# Eventually treat and log each type of ProgrammingError
def DB_error_resistant(func):

    @wraps(func)
    def resistant_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProgrammingError:
            raise Exception('Erro na estrutura do Banco de Dados')

    return resistant_function
