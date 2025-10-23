"""Tests for decorators module."""

import os
import tempfile
from typing import Any, Callable
import pytest
from src.decorators import log


class TestLogDecorator:
    """Test class for log decorator functionality."""

    @pytest.fixture
    def temp_log_file(self) -> str:
        """Create a temporary log file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            temp_file = f.name
        yield temp_file
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    @pytest.fixture
    def sample_function(self) -> Callable[[int, int], int]:
        """Create a sample function for testing."""

        @log()
        def add_numbers(a: int, b: int) -> int:
            return a + b

        return add_numbers

    @pytest.fixture
    def error_function(self) -> Callable[[int, int], float]:
        """Create a function that raises an error."""

        @log()
        def divide_numbers(a: int, b: int) -> float:
            if b == 0:
                raise ValueError("Division by zero")
            return a / b

        return divide_numbers

    def test_log_to_console_success(self, capsys: pytest.CaptureFixture, sample_function: Callable) -> None:
        """Test logging successful function execution to console."""
        result = sample_function(3, 4)

        captured = capsys.readouterr()
        assert "add_numbers ok" in captured.out
        assert result == 7

    def test_log_to_console_error(self, capsys: pytest.CaptureFixture, error_function: Callable) -> None:
        """Test logging function error to console."""
        with pytest.raises(ValueError):
            error_function(10, 0)

        captured = capsys.readouterr()
        assert "divide_numbers error: ValueError" in captured.out
        assert "Inputs: (10, 0)" in captured.out

    def test_log_to_file_success(self, temp_log_file: str) -> None:
        """Test logging successful function execution to file."""

        @log(filename=temp_log_file)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(5, 6)

        with open(temp_log_file, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "multiply ok" in log_content
        assert result == 30

    def test_log_to_file_error(self, temp_log_file: str) -> None:
        """Test logging function error to file."""

        @log(filename=temp_log_file)
        def risky_operation(x: int) -> int:
            if x < 0:
                raise TypeError("Negative values not allowed")
            return x * 2

        with pytest.raises(TypeError):
            risky_operation(-5)

        with open(temp_log_file, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "risky_operation error: TypeError" in log_content
        assert "Inputs: (-5)" in log_content

    def test_log_preserves_function_metadata(self) -> None:
        """Test that decorator preserves original function metadata."""

        @log()
        def original_function(x: int) -> int:
            """Original function docstring."""
            return x * 2

        assert original_function.__name__ == "original_function"
        assert original_function.__doc__ == "Original function docstring."

    def test_log_with_keyword_arguments(self, capsys: pytest.CaptureFixture) -> None:
        """Test logging with keyword arguments."""

        @log()
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = greet(name="Alice", greeting="Hi")

        captured = capsys.readouterr()
        assert "greet ok" in captured.out
        assert result == "Hi, Alice!"

    def test_log_with_mixed_arguments_error(self, capsys: pytest.CaptureFixture) -> None:
        """Test logging error with mixed positional and keyword arguments."""

        @log()
        def problematic_function(a: int, b: int = 0) -> float:
            if a + b == 0:
                raise ZeroDivisionError("Sum is zero")
            return 10 / (a + b)

        with pytest.raises(ZeroDivisionError):
            problematic_function(0, b=0)

        captured = capsys.readouterr()
        assert "problematic_function error: ZeroDivisionError" in captured.out
        assert "Inputs: (0), {b: 0}" in captured.out

    def test_multiple_calls_to_same_file(self, temp_log_file: str) -> None:
        """Test multiple function calls logging to the same file."""

        @log(filename=temp_log_file)
        def counter() -> int:
            return 42

        counter()
        counter()
        counter()

        with open(temp_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert all("counter ok" in line for line in lines)

    @pytest.mark.parametrize("a, b, expected_result", [
        (1, 2, 3),
        (0, 0, 0),
        (-5, 10, 5),
        (100, 200, 300),
    ])
    def test_log_with_parameterized_success(
            self, capsys: pytest.CaptureFixture, a: int, b: int, expected_result: int
    ) -> None:
        """Test successful function execution with parameterized inputs."""

        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(a, b)

        captured = capsys.readouterr()
        assert "add ok" in captured.out
        assert result == expected_result

    @pytest.mark.parametrize("input_value, expected_exception", [
        (0, ZeroDivisionError),
        ("string", TypeError),
        ([], TypeError),
    ])
    def test_log_with_parameterized_errors(
            self, capsys: pytest.CaptureFixture, input_value: Any, expected_exception: type
    ) -> None:
        """Test function errors with parameterized inputs."""

        @log()
        def dangerous_operation(x: Any) -> float:
            return 10 / x

        with pytest.raises(expected_exception):
            dangerous_operation(input_value)

        captured = capsys.readouterr()
        assert "dangerous_operation error:" in captured.out
        assert f"Inputs: ({input_value!r})" in captured.out


def test_file_creation_and_appending() -> None:
    """Test that log file is created and content is appended correctly."""
    import uuid
    test_filename = f"test_log_{uuid.uuid4().hex[:8]}.log"

    try:
        if os.path.exists(test_filename):
            os.unlink(test_filename)

        @log(filename=test_filename)
        def test_func() -> None:
            pass

        test_func()
        assert os.path.exists(test_filename)

        test_func()

        with open(test_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert all("test_func ok" in line for line in lines)

    finally:
        if os.path.exists(test_filename):
            os.unlink(test_filename)


def test_log_output_format(capsys: pytest.CaptureFixture) -> None:
    """Test the exact format of log output."""

    @log()
    def test_function(x: int, y: int, z: str = "default") -> str:
        return f"result: {x + y} {z}"

    result = test_function(5, 3, z="custom")

    captured = capsys.readouterr()
    assert "test_function ok" in captured.out
    assert result == "result: 8 custom"


def test_log_error_format(capsys: pytest.CaptureFixture) -> None:
    """Test the exact format of error log output."""

    @log()
    def failing_function(a: int, b: int, c: str = "test") -> None:
        raise RuntimeError("Something went wrong")

    with pytest.raises(RuntimeError):
        failing_function(1, 2, c="error_test")

    captured = capsys.readouterr()
    assert "failing_function error: RuntimeError" in captured.out
    assert "Inputs: (1, 2), {c: 'error_test'}" in captured.out


def test_log_with_different_exception_types(capsys: pytest.CaptureFixture) -> None:
    """Test logging with different exception types."""

    @log()
    def multi_error_function(choice: int) -> None:
        if choice == 1:
            raise ValueError("Value error")
        elif choice == 2:
            raise TypeError("Type error")
        elif choice == 3:
            raise KeyError("Key error")
        else:
            return "success"

    with pytest.raises(ValueError):
        multi_error_function(1)
    captured = capsys.readouterr()
    assert "multi_error_function error: ValueError" in captured.out

    with pytest.raises(TypeError):
        multi_error_function(2)
    captured = capsys.readouterr()
    assert "multi_error_function error: TypeError" in captured.out

    result = multi_error_function(0)
    captured = capsys.readouterr()
    assert "multi_error_function ok" in captured.out
    assert result == "success"