import logging
import os
import textwrap
import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)


class CodeImprover:
    DEFAULT_MODEL_NAME = "gpt-4o-mini"  # Default model name for the LLM
    DEFAULT_TEMPERATURE = 0.4  # Default temperature for LLM responses
    INPUT_LIMIT = 9999  # Maximum input length for code
    GENERATED_FILE_EXTENSION = "llm"  # Extension for generated files

    def __init__(
        self,
        file_path: str,
        openai_api_key: str = None,
        model_name: str = None,
        temperature: float = None,
    ):
        """
        Initializes the CodeImprover instance.

        Args:
            file_path (str): The path to the source code file to be improved.
            openai_api_key (str, optional): OpenAI API key for authentication. Defaults to None.
            model_name (str, optional): Name of the model to use. Defaults to None.
            temperature (float, optional): Temperature setting for the model's output. Defaults to None.

        Returns:
            None
        """
        self.file_path = file_path  # Path to the source code file
        self.llm = self._initialize_llm(
            openai_api_key, model_name, temperature
        )  # LLM instance
        self.generated_file_path = (
            self._generate_output_file_path()
        )  # Path for the generated output file

    def _initialize_llm(
        self, openai_api_key: str, model_name: str, temperature: float
    ) -> ChatOpenAI:
        """
        Initializes the ChatOpenAI instance with the provided parameters.

        Args:
            openai_api_key (str): OpenAI API key for authentication.
            model_name (str): Name of the model to use.
            temperature (float): Temperature setting for the model's output.

        Returns:
            ChatOpenAI: An instance of the ChatOpenAI class.
        """
        api_key = openai_api_key or os.getenv(
            "OPEN_AI_API_KEY"
        )  # Get API key from environment if not provided
        model = (
            model_name or self.DEFAULT_MODEL_NAME
        )  # Use default model name if not provided
        temp = (
            temperature or self.DEFAULT_TEMPERATURE
        )  # Use default temperature if not provided
        return ChatOpenAI(
            model_name=model, openai_api_key=api_key, temperature=float(temp)
        )

    @property
    def _prompts_action_map(self) -> dict:
        """
        Provides a mapping of actions to their corresponding prompt templates.

        Returns:
            dict: A dictionary mapping action names to prompt templates.
        """
        return {
            "clean": PromptTemplates.clean_code_prompt,
            "docstrings": PromptTemplates.docstrings_prompt,
            "tests": PromptTemplates.tests_prompt,
            "readme": PromptTemplates.readme_prompt,
        }

    def improve_code(self, action: str):
        """
        Improves the code based on the specified action.

        Args:
            action (str): The action to perform (e.g., 'clean', 'docstrings', 'tests', 'readme').

        Returns:
            None
        """
        prompt_template = self._get_prompt_template(
            action
        )  # Get the corresponding prompt template
        output_str = self._generate_improved_code(
            prompt_template
        )  # Generate improved code based on the prompt

        if output_str:
            self._save_improved_code(output_str)  # Save the improved code to a file
        else:
            logger.error(
                "No response received from LLM"
            )  # Log an error if no response is received

    def _get_prompt_template(self, action: str) -> str:
        """
        Retrieves the prompt template for the specified action.

        Args:
            action (str): The action for which to retrieve the prompt template.

        Returns:
            str: The corresponding prompt template.

        Raises:
            NotImplementedError: If the action is not implemented.
        """
        prompt_template = self._prompts_action_map.get(
            action
        )  # Get the prompt template from the action map
        if not prompt_template:
            raise NotImplementedError(
                f"Action '{action}' is not implemented."
            )  # Raise error if action is not found
        return prompt_template

    def _generate_improved_code(self, prompt_template: str) -> str:
        """
        Generates improved code using the provided prompt template.

        Args:
            prompt_template (str): The template to use for generating improved code.

        Returns:
            str: The improved code as a string.
        """
        code = self._read_code_from_file()  # Read the original code from the file
        prompt_input = {"code": code}  # Prepare the input for the LLM
        processed_template = self._process_template_string(
            prompt_template
        )  # Process the prompt template
        return self._invoke_llm_with_prompt(
            processed_template, prompt_input
        )  # Invoke the LLM with the prompt

    def _read_code_from_file(self) -> str:
        """
        Reads the code from the specified file.

        Returns:
            str: The code read from the file.

        Raises:
            RuntimeError: If the code exceeds the input length limit.
        """
        with open(self.file_path, 'r') as file:
            code = file.read()  # Read the content of the file
        self._validate_code_length(code)  # Validate the length of the code
        return code

    def _validate_code_length(self, code: str):
        """
        Validates the length of the code to ensure it is within the allowed limit.

        Args:
            code (str): The code to validate.

        Raises:
            RuntimeError: If the code exceeds the input length limit.
        """
        if len(code) >= self.INPUT_LIMIT:
            raise RuntimeError(
                f"File {self.file_path} is too big for processing. Limit is {self.INPUT_LIMIT} chars"
            )

    @staticmethod
    def _process_template_string(template: str) -> str:
        """
        Processes the template string by removing indentation.

        Args:
            template (str): The template string to process.

        Returns:
            str: The processed template string.
        """
        return textwrap.dedent(
            template
        )  # Remove leading whitespace from the template string

    def _invoke_llm_with_prompt(self, prompt_template: str, prompt_input: dict) -> str:
        """
        Invokes the LLM with the given prompt template and input.

        Args:
            prompt_template (str): The template to use for the prompt.
            prompt_input (dict): The input data for the prompt.

        Returns:
            str: The response from the LLM.
        """
        prompt = ChatPromptTemplate.from_template(
            prompt_template
        )  # Create a prompt from the template
        chain = (
            prompt | self.llm | StrOutputParser()
        )  # Create a chain of prompt, LLM, and output parser
        return chain.invoke(prompt_input)  # Invoke the chain with the prompt input

    def _generate_output_file_path(self) -> str:
        """
        Generates a file path for the output file based on the original file path and current timestamp.

        Returns:
            str: The generated output file path.
        """
        timestamp = int(time.time())  # Get the current timestamp
        return f"{self.file_path}.{self.GENERATED_FILE_EXTENSION}{timestamp}"  # Construct the output file path

    def _save_improved_code(self, output_str: str):
        """
        Saves the improved code to a file.

        Args:
            output_str (str): The improved code to save.

        Returns:
            None
        """
        output_file = self._generate_output_file_path()  # Generate the output file path
        with open(output_file, 'w') as file:
            file.write(output_str)  # Write the improved code to the output file
