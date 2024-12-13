from functools import wraps

from classic.components import doublewrap


@doublewrap
def takes_connection(
        func, connect_attr='connect', connection_param='connection'
):
    """Декоратор для автоматического получения соединения из атрибута объекта.

    Args:
        connect_attr: имя атрибута с методом connect
        connection_param: имя параметра для передачи соединения
    """

    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        connect = getattr(obj, connect_attr)
        with connect() as conn:
            kwargs[connection_param] = conn
            return func(obj, *args, **kwargs)

    return wrapper
