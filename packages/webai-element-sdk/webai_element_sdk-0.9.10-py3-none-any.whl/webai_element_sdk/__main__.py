import builtins
import importlib
import json
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock

import click

from .element import Element


@contextmanager
def change_directory(new_dir: Path):
    """A context manager to temporarily change the current working directory and add to sys.path."""
    old_dir = os.getcwd()
    old_sys_path = sys.path[:]

    try:
        os.chdir(new_dir)
        sys.path.insert(0, str(new_dir))
        yield
    finally:
        os.chdir(old_dir)
        sys.path = old_sys_path


def get_package_name_from_setup(dir_path: Path):
    with open(dir_path / "setup.py", "r") as file:
        setup_content = file.read()

    # Regular expression to match the name parameter in setup()
    name_match = re.search(r'name\s*=\s*["\']([^"\']+)', setup_content)

    if name_match:
        return name_match.group(1)
    else:
        raise ValueError("Unable to find package name in setup.py")


@click.group()
def cli():
    pass


@cli.command()
@click.option("--path", required=False, default=".")
def generate(path: str):
    # Dictionary to store mocked modules
    mocked_modules = {}
    original_import = builtins.__import__

    def mock_module(name):
        """Create a mock module and all its parent modules."""
        parts = name.split(".")
        for i in range(1, len(parts) + 1):
            partial_name = ".".join(parts[:i])
            if partial_name not in mocked_modules:
                mocked_modules[partial_name] = MagicMock()
                sys.modules[partial_name] = mocked_modules[partial_name]
        return mocked_modules[name]

    # Custom import function
    def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
        try:
            # Attempt the original import
            return original_import(name, globals, locals, fromlist, level)
        except ImportError as e:
            print(f"Mocking import of {name} due to {str(e)}")
            return mock_module(name)

    # Replace the built-in __import__ function with our custom one
    builtins.__import__ = mock_import

    with change_directory(Path(path).resolve()):
        # Code inside this block will execute with the new directory as the current working directory
        print("Current working directory:", os.getcwd())
        element = get_package_name_from_setup(Path("."))
        module = importlib.import_module(element)
        module_vars = list(module.__dict__.values())
        for var in module_vars:
            if isinstance(var, Element):
                metadata = var.generate_metadata()
                with open("publish.json", "w") as f:
                    json.dump(metadata, f, indent=4)
                print(f"publish.json successfully generated here: {os.getcwd()}")
                exit(0)
        print("Something went wrong.")
        exit(1)


cli()
