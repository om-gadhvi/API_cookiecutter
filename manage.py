#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Determine the path to the .env file in your project's root directory
BASE_DIR = Path(__file__).parent.resolve()
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Optionally, print a message if .env is not found
    print("No .env file found in the project root; proceeding without it.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
        ) from exc

    # Allow easy placement of apps within the inner demo_cookiecutter directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "demo_cookiecutter"))

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
