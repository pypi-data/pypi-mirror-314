# Code Cleaner Tool

## Overview

The **Code Cleaner Tool** is a Python application that leverages OpenAI's language models to enhance code quality.

It can perform various actions such as cleaning code, adding docstrings, generating tests, and creating README files based on the provided source code. This tool is designed for developers who want to automate the improvement of their codebases efficiently.

## Features

- **Code Cleaning**: Automatically refines the code for better readability and performance.
- **Docstring Generation**: Adds meaningful docstrings to functions and classes for improved documentation.
- **Test Generation**: Creates unit tests to ensure code reliability.
- **README Generation**: Generates a README file to provide an overview of the project.

## Requirements

- Python 3.9 or higher
- `langchain_core`
- `langchain_openai`
- Access to OpenAI API

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in your environment variables:
   ```bash
   export OPEN_AI_API_KEY='your_openai_api_key'
   ```

## Usage

To use the Code Cleaner Tool, run the script from the command line with the required arguments:

```bash
python code_cleaner.py --file <path_to_your_code_file> --action <action_type>
```

### Arguments

- `--file` or `-f`: The path to the code file that you want to process (required).
- `--action` or `-a`: The action you want to perform. Options include:
  - `clean`: Clean the code.
  - `docstrings`: Add docstrings to the code.
  - `tests`: Generate tests for the code.
  - `readme`: Create a README file for the project.

### Example

To clean a Python file named `example.py`, you would run:

```bash
python code_cleaner.py --file example.py --action clean
```

## Output

The tool generates a new file with the same name as the input file, appended with a timestamp and the extension `.llm`. For example, if you process `example.py`, the output file will be named `example.py.llm<timestamp>`.

## Logging

The application logs its activities to the console. You can adjust the logging level in the code if you want more or less verbosity.

## Error Handling

The tool includes error handling for the following scenarios:
- If the specified file exceeds the character limit (9999 characters).
- If an unrecognized action is provided.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For questions or feedback, please reach out to [alex.polovinko+git@gmail.com].
