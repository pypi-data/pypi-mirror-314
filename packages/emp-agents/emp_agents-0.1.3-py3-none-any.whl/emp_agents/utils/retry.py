from asyncio import iscoroutinefunction

from emp_agents.exceptions import TooManyTriesException


def retry(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    if iscoroutinefunction(f):
                        return await f(*args, **kwargs)
                    return f(*args, **kwargs)
                except Exception as _exc:
                    exc = _exc
            raise TooManyTriesException() from exc

        return wrapper

    return func_wrapper
