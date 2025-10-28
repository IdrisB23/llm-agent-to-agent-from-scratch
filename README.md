# Introduction

I am building a mini framework for A2A communication (see https://a2a-protocol.org/latest/). Goal is to create a network of agents that connect and solve tasks together.

# System Diagram

![architecture](docs/architecture.drawio.png)

# Get Started
1. Create virtual environment `python -m venv .venv`.
2. Activate the virtual environment.
3. Install the dependencies. Example with pip: `pip install -r requirements.txt`
4. Run the entrypoint script: `python main_threads.py`

# Code Quality (desired)
- Linter: [ruff](https://github.com/astral-sh/ruff)
- Testing: [pytest](https://github.com/pytest-dev/pytest)