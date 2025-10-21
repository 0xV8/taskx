"""
Pytest configuration and fixtures for taskx tests.
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest

from taskx.core.config import Config
from taskx.core.task import Task


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_file(temp_dir: Path) -> Path:
    """Create a sample configuration file."""
    config_path = temp_dir / "pyproject.toml"
    config_path.write_text("""
[tool.taskx.env]
APP_NAME = "testapp"
VERSION = "1.0.0"

[tool.taskx.tasks]
hello = "echo 'Hello, World!'"
test = { cmd = "pytest tests/", description = "Run tests" }
build = { cmd = "python -m build", description = "Build package" }
deploy = { depends = ["test", "build"], cmd = "echo 'Deploying...'", description = "Deploy to production" }
""")
    return config_path


@pytest.fixture
def sample_config(sample_config_file: Path) -> Config:
    """Load a sample configuration."""
    config = Config(sample_config_file)
    config.load()
    return config


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task."""
    return Task(
        name="test_task",
        cmd="echo 'test'",
        description="A test task",
    )
