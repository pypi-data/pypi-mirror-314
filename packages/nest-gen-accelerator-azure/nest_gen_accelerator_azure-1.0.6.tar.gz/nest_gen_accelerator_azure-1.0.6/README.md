# NestGen Accelerator Promptflow Tool

This document describes how to create the connection to Nesgen from promptflow and install the Nestgen Promptflow Tool using the generated `.whl` file, as well as how to install the required dependencies.

## Prerequisites

Before installing the tool, ensure that you meet the following prerequisites:

- **Python 3.9**: The tool requires a modern version of Python.
- **pip**: The Python package manager.
- **Virtual Environment (Optional but Recommended)**: It is recommended to install the tool in a virtual environment to avoid dependency conflicts.

## Installation

### 1. Create a Virtual Environment (Optional)

It's a good practice to create a virtual environment to keep your project dependencies isolated:

```python -m venv venv```

Activate the Virtual environment:
On Linux/macOS:
```source venv/bin/activate```

On Windows:
```venv\Scripts\activate```

### 2. Install Requirements

Install all required dependencies listed in requirements.txt:
```pip install -r requirements.txt```

### 3. Verify the installation
```pip list```

### 4. Build the package
```python setup.py sdist bdist_wheel```

### 5. Install the Tool Wheel (locally)
```pip install dist/azure_llm_package-0.0.1-py3-none-any.whl --force-reinstall```

### 6. Test the package
```pytest tests```

### 7. Publish the library to pypi
```twine upload dist/*```

## Create CustomConnection
First, we need to create a Custom Connection to be able to connect to **Nest Acceleretor**. For this, there is a connection file called *nesgen_accelerator_connection.yaml* that contains the connection information. 

To create the connection, we have to run this promptflow command:

```pf connection create -f nesgen_accelerator_connection.yaml```

As the key params are not contained in the file, the user will be asked for:  `client_id` and `client_secret` after running the command.

Once the connection has been created, we will be able to see it at our promptflow UI as a Custom Connection called **NestGen Accelerator Azure LLM Tool**.


## Usage
After successful installation of the package, your custom “tool” will show up in VSCode extension as below: 
![alt text](https://microsoft.github.io/promptflow/_images/custom-tool-list-in-extension.png)
source: https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/create-and-use-tool-package.html
