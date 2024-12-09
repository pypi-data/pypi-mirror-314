import argparse
import logging
import sys

from py_code_improver.code_improver import CodeImprover

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser for command-line arguments.

    This function initializes an ArgumentParser object that will handle
    command-line arguments for the Code Improver Tool.

    It defines two required arguments:
    - `--file` or `-f`: The path to the file to be processed.
    - `--action` or `-a`: The action to perform on the file.

    and optional argument:
    - `--openai-api-key`: If passed, this key will be used in requests to OpenAI API.


    Returns:
        argparse.ArgumentParser: Configured argument parser.

    """
    parser = argparse.ArgumentParser(description="Code Cleaner Tool using LLM")
    parser.add_argument("--file", "-f", required=True, help="File to process")
    parser.add_argument("--action", "-a", required=True, help="Action to perform")
    parser.add_argument("--openai-api-key", required=False, help="OpenAI API key to use")
    return parser


def parse_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """
    Parses command-line arguments using the provided parser.

    This function takes an ArgumentParser object and parses the command-line
    arguments provided by the user.
    It returns the parsed arguments as a Namespace object.

    Args:
        parser (argparse.ArgumentParser): The argument parser to use for parsing.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.

    """
    return parser.parse_args()


def execute_code_improvement(file_path: str, action: str, openai_api_key: str) -> None:
    """
    Implements the code improvement process for the specified file and action.

    This function creates an instance of the CodeImprover class using the
    specified file path and calls its `improve_code` method with the given
    action.

    Args:
        file_path (str): The path to the file to be improved.
        action (str): The specific action to perform on the code.
        openai_api_key (str): The api key to use in requests to OpenAI API

    Returns:
        None: This function does not return a value.

    """
    code_improver = CodeImprover(file_path=file_path, openai_api_key=openai_api_key)
    code_improver.improve_code(action=action)


def main() -> None:
    """
    Main entry point for the Code Improver tool.

    This function orchestrates the execution of the Code Improver Tool by
    setting up the argument parser, parsing the command-line arguments,
    and executing the code improvement process based on the provided
    arguments.

    Returns:
        None: This function does not return a value.
    """
    parser = setup_argument_parser()
    args = parse_arguments(parser)
    execute_code_improvement(file_path=args.file, action=args.action, openai_api_key=args.openai_api_key)


if __name__ == "__main__":
    main()
