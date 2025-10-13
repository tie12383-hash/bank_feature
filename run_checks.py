"""Script to run all code quality checks and tests."""

import subprocess
import sys


def run_command(command, description):
    """Run a shell command and print result."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"{'='*50}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {description} failed!")
        return False
    print(f"✅ {description} passed!")
    return True


def main():
    """Run all code quality checks and tests."""
    checks = [
        ("black --check .", "Code formatting check (Black)"),
        ("isort --check-only .", "Import sorting check (isort)"),
        ("flake8", "Code linting (flake8)"),
        ("mypy .", "Type checking (mypy)"),
        ("pytest", "Running tests"),
    ]

    all_passed = True
    for command, description in checks:
        if not run_command(command, description):
            all_passed = False

    if all_passed:
        print(f"\n{'🎉'*20}")
        print("All checks passed! You're good to go!")
        print(f"{'🎉'*20}")
        return 0
    else:
        print(f"\n{'❌'*20}")
        print("Some checks failed! Please fix the issues.")
        print(f"{'❌'*20}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
