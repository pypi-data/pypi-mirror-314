import argparse
import logging
import sys

from .code_improver import CodeImprover

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)


def setup_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser."""
    parser = argparse.ArgumentParser(description="Code Cleaner Tool using LLM")
    parser.add_argument("--file", "-f", required=True, help="File to process")
    parser.add_argument("--action", "-a", required=True, help="Action to perform")
    return parser


def parse_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parses command-line arguments using the provided parser."""
    return parser.parse_args()


def execute_code_improvement(file_path: str, action: str) -> None:
    """Executes the code improvement process."""
    code_improver = CodeImprover(file_path=file_path)
    code_improver.improve_code(action=action)


def main() -> None:
    """Main entry point for the Code Improver tool."""
    parser = setup_argument_parser()
    args = parse_arguments(parser)
    execute_code_improvement(file_path=args.file, action=args.action)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
