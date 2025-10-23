"""Module containing decorators for function logging and monitoring."""

import functools
from typing import Any, Callable, Optional, Union
from datetime import datetime


def log(filename: Optional[str] = None) -> Callable:
    """Decorator that logs function execution details."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)

                log_message = f"{timestamp} - {func_name} ok\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as error:
                error_type = type(error).__name__
                args_str = ", ".join(repr(arg) for arg in args)
                kwargs_str = ", ".join(f"{k}: {v!r}" for k, v in kwargs.items())
                inputs = f"({args_str})"
                if kwargs_str:
                    inputs += f", {{{kwargs_str}}}"

                log_message = f"{timestamp} - {func_name} error: {error_type}. Inputs: {inputs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message)
                else:
                    print(log_message, end="")

                raise

        return wrapper

    return decorator