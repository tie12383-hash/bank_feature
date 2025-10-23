"""Demonstration of decorators module functionality."""

import os
from src.decorators import log


def main() -> None:
    """Demonstrate decorators module functionality."""
    print("=== Decorators Module Demo ===\n")

    if os.path.exists("demo_success.log"):
        os.remove("demo_success.log")
    if os.path.exists("demo_error.log"):
        os.remove("demo_error.log")

    print("1. Console Logging Demo:")
    print("-" * 30)

    @log()
    def console_function(a: int, b: int) -> int:
        """Function that logs to console."""
        return a * b

    result1 = console_function(5, 3)
    print(f"Result: {result1}\n")

    print("2. File Logging Demo - Success:")
    print("-" * 30)

    @log(filename="demo_success.log")
    def file_function_success(name: str, count: int) -> str:
        """Function that logs to file (success case)."""
        return f"Hello {name} repeated {count} times"

    result2 = file_function_success("World", 3)
    print(f"Result: {result2}")

    with open("demo_success.log", "r", encoding="utf-8") as f:
        print("Log file content:")
        print(f.read())

    print("3. File Logging Demo - Error:")
    print("-" * 30)

    @log(filename="demo_error.log")
    def file_function_error(data: list) -> float:
        """Function that logs to file (error case)."""
        if not data:
            raise ValueError("Empty data provided")
        return sum(data) / len(data)

    try:
        file_function_error([])
    except ValueError as e:
        print(f"Caught expected error: {e}")

    with open("demo_error.log", "r", encoding="utf-8") as f:
        print("Error log file content:")
        print(f.read())

    print("4. Mixed Arguments Demo:")
    print("-" * 30)

    @log()
    def mixed_args_function(x: int, y: int = 10, z: int = 20) -> int:
        """Function with mixed positional and keyword arguments."""
        return x + y + z

    result3 = mixed_args_function(5, y=15, z=25)
    print(f"Result: {result3}")

    print("\n=== Demo Completed ===")
    print("Check generated log files: demo_success.log and demo_error.log")


if __name__ == "__main__":
    main()