# unic4py

`unic4py` is a Python module intended as an adapter
for transforming non-interactive command-line analysis tools to
OSLC-compliant web services

---

## Installation

To use `unic4py`, install it using pip:

```bash
pip install unic4py
```

Additionally, ensure that the `oslc4py-client` and `oslc4py-domains-auto` dependencies are installed:

```bash
pip install oslc4py-client oslc4py-domains-auto
```

---

## Features

The `unic4py` module includes the following main classes:

1. `UniteAnalyser`: A utility class for registering, compiling, and analyzing systems under test (SUTs).
2. `SUT`: A resource representation of a system under test, designed with OSLC principles.

---

## Example Usage

### Using `UniteAnalyser` for Compilation and Analysis

```python
from unic4py.UniteAnalyser import UniteAnalyser

# Initialize the UniteAnalyser with the server's base URL and ports
analyser = UniteAnalyser("http://example.com", "8081", "8080")

# Set up compilation and analysis arguments
analyser.add_compilation_argument("sourceBase64", "encoded_source_code_here")
analyser.add_analysis_argument("SUT", "http://example.com:8080/compilation/services/resources/sUTs/155")

# Specify the analysis tool to use
analyser.pass_data['analysis_tool'] = "infer"

# Run the analysis
analyser.analyse()
```

## `UniteAnalyser` Class

The `UniteAnalyser` class automates the process of registering, compiling, and analyzing SUTs. It uses the `OSLCPythonClient` for communicating with OSLC servers.

### Methods

#### `__init__`
```python
def __init__(self, unite_url, compilation_port, analysis_port)
```
- Initializes the analyser with the base URL and ports for compilation and analysis services.

#### `add_compilation_argument`
```python
def add_compilation_argument(self, name, value)
```
- Adds an argument for the compilation process.

#### `add_analysis_argument`
```python
def add_analysis_argument(self, name, value)
```
- Adds an argument for the analysis process.

#### `analyse`
```python
def analyse(self)
```
- Executes the full pipeline: registering the SUT, checking its registration, performing the analysis, and retrieving the result.

#### `register_sut`
```python
def register_sut(self)
```
- Registers the system under test (SUT) using a compilation request.

#### `check_sut_registration`
```python
def check_sut_registration(self)
```
- Verifies the SUT registration by polling the compilation results.

#### `perform_analysis`
```python
def perform_analysis(self)
```
- Sends an analysis request for the registered SUT.

#### `get_analysis_result`
```python
def get_analysis_result(self)
```
- Retrieves the results of the analysis.

---

## `SUT` Class

The `SUT` class represents a System Under Test resource and provides properties for working with OSLC-compliant resources.

### Key Properties

- **`launch_command`**: The command used to launch the system under test.
- **`build_command`**: The command used to build the system under test.
- **`title`**: The title of the system under test.
- **`description`**: A description of the system under test.
- **`identifier`**: A unique identifier for the system under test.
- **`sut_directory_path`**: Path to the directory containing the SUT.
- **`compiled`**: Indicates whether the SUT has been compiled.
- **`produced_by_automation_request`**: Link to the automation request that produced this SUT.


## Notes

- Ensure the `OSLC4PY_ACTIVE_INSTALLED_DOMAINS` or `OSLC4PY_EXTRA_DOMAINS_DIR` environment variables are set if additional class discovery is needed.
- Dependencies:
  - `oslc4py-client`
  - `oslc4py-domains-auto`

Install dependencies using:
```bash
pip install oslc4py-client oslc4py-domains-auto
```
