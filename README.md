# Curser Analytics

A Python toolkit for data analysis and experimentation.

## Overview

This project provides a flexible Python environment equipped with a wide range of libraries for data manipulation, visualization, exploratory data analysis (EDA), machine learning, and database connectivity. The environment is managed using a `Makefile` for easy setup and common development tasks.

## Features

- **Comprehensive Python Environment**: Pre-configured with popular data science libraries (see `requirements.txt`).
- **Simplified Setup**: Use `make` to create your virtual environment and install dependencies.
- **Development Tools**: Includes commands for linting (Black, iSort, Flake8, Mypy) and testing (Pytest).

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `make` utility (common on Linux/macOS; can be installed on Windows)

### Environment Setup with Makefile

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Set up the Python virtual environment and install dependencies:**
    This command will create a virtual environment named `venv` in the project root and install all packages listed in `requirements.txt`.
    ```bash
    make setup_env
    ```

3.  **Activate the virtual environment:**
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows (Git Bash or similar):
        ```bash
        source venv/Scripts/activate
        ```

### Makefile Targets

The `Makefile` provides several useful targets:

-   `make setup_env`: (Default) Creates the `venv` and installs dependencies from `requirements.txt`.
-   `make lint`: Runs linters (Black, iSort, Flake8, Mypy) to check code formatting and quality. Ensure the environment is activated or run as `make lint VENV_NAME=venv` if tools are not on PATH.
-   `make test`: Runs tests using Pytest (expects tests to be in a `tests/` directory).
-   `make clean`: Removes the virtual environment (`venv/`), Python cache files (`__pycache__`, `*.pyc`, `*.pyo`), and coverage reports.
-   `make help`: Displays a list of available targets and their descriptions.

You can run these commands from the project's root directory.

## Project Structure

-   `Makefile`: Defines commands for environment setup, linting, testing, and cleaning.
-   `requirements.txt`: Lists all Python dependencies for the project.
-   `README.md`: This file, providing an overview and instructions.
-   (Your source code, notebooks, scripts, and `tests/` directory will reside here)

## Installed Packages

The environment includes the following packages categorized by functionality:

### Core Data & Manipulation
- **pandas** (≥1.3.0): Data manipulation and analysis library providing DataFrame structures.
- **numpy** (≥1.20.0): Fundamental package for scientific computing with support for arrays and matrices.
- **polars** (≥0.17.0): Fast DataFrame library implemented in Rust with a pandas-like API.

### Data Visualization
- **matplotlib** (≥3.5.0): Comprehensive library for creating static, animated, and interactive visualizations.
- **seaborn** (≥0.11.0): Statistical data visualization based on matplotlib with a high-level interface.
- **plotly** (≥5.5.0): Interactive graphing library for creating web-based visualizations.

### Exploratory Data Analysis (EDA)
- **ydata-profiling** (≥4.1.0): Generates profile reports from pandas DataFrames, including statistics and visualizations.
- **sweetviz** (≥2.1.0): Creates beautiful, high-density visualizations for EDA with a single line of code.

### Dashboards / Tableau-style Apps
- **dash** (≥2.6.0): Framework for building web-based analytical applications with React components.
- **streamlit** (≥1.12.0): App framework that turns data scripts into shareable web apps quickly.

### SQL & Database Connectivity
- **sqlalchemy** (≥1.4.0): SQL toolkit and Object-Relational Mapping (ORM) library.
- **duckdb** (≥0.6.0): In-process SQL OLAP database management system with pandas integration.
- **pandasql** (≥0.7.0): Allows querying pandas DataFrames using SQL syntax.

### Database Connectors
- **mysql-connector-python** (≥8.0.0): Official MySQL driver for Python.
- **snowflake-connector-python** (≥2.8.0): Connector for the Snowflake data warehouse.
- **python-dotenv** (≥0.19.0): Reads key-value pairs from .env files and sets them as environment variables.

### LLMs / Prompt Interfaces
- **openai** (≥0.27.0): Python client for the OpenAI API, enabling access to GPT models.
- **langchain** (≥0.0.200): Framework for developing applications powered by language models.
- **llama-index** (≥0.6.0): Data framework for connecting custom data sources to LLMs.

### Jupyter & Interactivity
- **jupyterlab** (≥3.4.0): Web-based interactive development environment for notebooks, code, and data.
- **ipython** (≥8.4.0): Enhanced interactive Python shell.
- **ipywidgets** (≥8.0.0): Interactive HTML widgets for Jupyter notebooks.

### Utilities
- **tqdm** (≥4.62.0): Fast, extensible progress bar for loops and CLI applications.
- **click** (≥8.0.0): Package for creating command-line interfaces with minimal code.
- **tabulate** (≥0.8.9): Pretty-print tabular data in Python.

### Development Dependencies
- **pytest** (≥6.2.5): Framework for writing and running tests.

## Analytics Playground
We provide an interactive Jupyter notebook that demonstrates the key features of many data science packages available in this environment:

```bash
# After activating your environment, launch Jupyter Lab
jupyter lab
```

Then open `analytics_playground.ipynb` in the Jupyter interface. This notebook includes examples of:

- Data manipulation with pandas and polars
- Data visualization with matplotlib, seaborn, and plotly
- Exploratory data analysis with ydata-profiling and sweetviz
- SQL queries with various supported dbs


## Database Connectivity

If you plan to connect to databases, create a `.env` file in your project root with your database credentials. The environment variables will be loaded automatically by the Makefile.

**Example `.env.template` (copy to `.env` and fill in your details):**
```
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

## Saved Query Results

Query results are automatically saved to pickle files in the `outputs` directory. The file naming convention uses the query name and the current date:

```
outputs/query_name_YYYY-MM-DD.pkl
```

This allows you to:
- Keep a history of query results for comparison
- Load the saved data in other Python scripts without re-running the query
- Share results with team members

### Loading Pickle Files

```python
import pandas as pd

# Load a saved query result
results = pd.read_pickle('outputs/markets_2025-05-06.pkl')

# Display the data
print(results.head())
```

## Sample Schema Data

The package includes a comprehensive sample schema file (`full_schema.txt`) that contains a complete database schema for a sports trading management (STM) system with 110 tables. This sample can be used for exploring schema analysis features without connecting to a real database.

### Accessing the Sample Schema

```python
from curser_analytics.samples import get_sample_path

# Get the path to the full schema sample
schema_path = get_sample_path('full_schema.txt')

# Read the schema file
with open(schema_path, 'r') as f:
    schema_data = f.read()
```

### Listing Available Samples

```python
from curser_analytics.samples import list_available_samples

# Get all available sample files
samples = list_available_samples()
print(samples)  # Includes 'full_schema.txt'
```

## Project Structure

The project's main Python package, `curser_analytics`, is structured as follows:

```
curser_analytics/
├── __init__.py         # Package initialization
├── analytics.py        # Main analytics module
├── run_schema.py       # Script to run schema analysis
├── config/             # Configuration module (e.g., settings)
│   └── (...)
├── db/                 # Database related modules (connection, schema)
│   └── (...)
├── examples/           # Example scripts and notebooks
│   └── (...)
├── output/             # Default directory for generated outputs (e.g., schema files, ERDs)
│   └── (...)
├── queries/            # SQL query files
│   └── (...)
├── samples/            # Sample data files
│   └── (...)
├── tests/              # Tests for the curser_analytics package
│   └── (...)
└── utils/              # Utility modules (e.g., logger)
    └── (...)
```

## Database Connectivity

The package supports connecting to the following databases:

- **MySQL**: Connect to MySQL databases and analyze schema
- **PostgreSQL**: (Coming soon) Connect to PostgreSQL databases
- **Snowflake**: (Coming soon) Connect to Snowflake data warehouses

Each database connection is implemented as a subclass of the `DatabaseConnection` base class, providing a consistent interface for connecting to different database types.

## Schema Analysis

The schema analysis module provides tools for extracting and analyzing database schemas, including:

- Table information: names, row counts, engines, etc.
- Column information: names, types, nullability, keys, etc.
- Foreign key relationships
- Table relationships: outgoing and incoming references

The analysis results can be saved to a file for further examination or used programmatically within your application.

## Development

### Setup Development Environment

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies

```bash
git clone https://github.com/your-username/curser-analytics.git
cd curser-analytics
./setup_dev.sh
```

### Cursor IDE Setup

This project includes configuration files specifically for the [Cursor](https://cursor.so/) IDE:

- `.cursor.json` - Project configuration for code style, linting rules, and AI assistant behavior
- `.cursorignore` - Files and directories that should be excluded from Cursor's indexing

If you're using Cursor IDE, these files will automatically configure your development environment with appropriate settings for this project.

### Code Standards

This project uses pre-commit hooks to enforce code quality standards:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

The pre-commit configuration includes:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking
- bandit for security checks

### Running Tests

```bash
pytest
```

## VSCode Extensions

For the best development experience with this project, we recommend installing the following VSCode extensions:

1. **Jupyter Notebook**: Essential for working with `.ipynb` notebook files. This extension allows you to create, edit, and run Jupyter notebooks directly within VSCode.
   - Extension ID: `ms-toolsai.jupyter`
   - [Install from VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

2. **Data Wrangler**: Provides interactive data exploration and transformation capabilities directly within VSCode. It's a powerful tool for quick data analysis.
   - Extension ID: `ms-toolsai.datawrangler`
   - [Install from VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler)

To install these extensions:
- Open VSCode
- Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac) to open the Extensions view
- Search for each extension by name
- Click "Install"

## Environment Files Consistency

This repository provides multiple ways to set up your development environment, with consistent package management across different methods:

1. **requirements.txt** - Core package list with versioned dependencies organized by category:
   - Core Data & Manipulation (pandas, numpy, polars)
   - Data Visualization (matplotlib, seaborn, plotly, etc.)
   - EDA Libraries (ydata-profiling, sweetviz, etc.)
   - Database Connectivity (sqlalchemy, connectors, etc.)
   - ML & Modeling (scikit-learn, xgboost, etc.)
   - And more specialized categories

All environment files are designed to provide consistent functionality while accommodating different workflow preferences. They include common special case handling:

- datatable: Commented out due to compilation requirements
- ibis-framework: Commented out unless Python 3.10+ is available
- snowflake-connector-python: Special handling due to complex dependencies 