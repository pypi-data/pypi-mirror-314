# Architect Log

The **Architect Log** project helps document Architectural Decision Records (ADRs) following industry best practices. This makes it easy to reference, update, and maintain ADRs as the system evolves, providing a clear decision-making history for the development team.

## Setup and Installation

To set up the project, follow these steps:

1. **Generate Requirements File:**
   Ensure your environment has all dependencies and export them to a `requirements.txt` file:
   ```bash
   pip freeze > requirements.txt
   ```
2. **Install the Project Locally:**
   Install the project in your current environment:
   ```bash
   pip install .
   ```
3. **Build the Package:**
   Build the package using the Python build module
   ```bash
   rm -rf dist/* build/ src/architect_log.egg-info && python3 -m build
   ```
4. **Upload to Test PyPI:**
   Upload the built package to Test PyPI (make sure you have your credentials set up):
   ```bash
   python3 -m twine upload --repository testpypi dist/*
   ```

## Usage

   To create a new ADR, use the following command:
   ```bash
   architect_log add <title> --status <status> --template <template>
   ```
