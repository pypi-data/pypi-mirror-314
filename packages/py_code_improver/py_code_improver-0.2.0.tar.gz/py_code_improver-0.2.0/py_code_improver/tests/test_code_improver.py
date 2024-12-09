import unittest
from unittest.mock import MagicMock, mock_open, patch

from py_code_improver.code_improver import CodeImprover


class TestCodeImprover(unittest.TestCase):

    @patch('py_code_improver.code_improver.ChatOpenAI')
    @patch('os.getenv')
    def test_initialize_llm_with_api_key(self, mock_getenv, mock_chat_openai):
        mock_getenv.return_value = None

        # Create a mock instance of ChatOpenAI
        mock_llm_instance = MagicMock()
        mock_llm_instance.model_name = 'gpt-4o-mini'
        mock_llm_instance.openai_api_key = 'test_key'
        mock_llm_instance.temperature = 0.4

        # Set the return value of the ChatOpenAI constructor to our mock instance
        mock_chat_openai.return_value = mock_llm_instance

        code_improver = CodeImprover(
            file_path='test_file.py', openai_api_key='test_key'
        )
        self.assertEqual(code_improver.llm.model_name, 'gpt-4o-mini')
        self.assertEqual(code_improver.llm.openai_api_key, 'test_key')
        self.assertEqual(code_improver.llm.temperature, 0.4)

    @patch('py_code_improver.code_improver.ChatOpenAI')
    @patch('os.getenv')
    def test_initialize_llm_without_api_key(self, mock_getenv, mock_chat_openai):
        mock_getenv.return_value = 'env_key'

        # Create a mock instance of ChatOpenAI
        mock_llm_instance = MagicMock()
        mock_llm_instance.openai_api_key = 'env_key'

        # Set the return value of the ChatOpenAI constructor to our mock instance
        mock_chat_openai.return_value = mock_llm_instance

        code_improver = CodeImprover(file_path='test_file.py')
        self.assertEqual(code_improver.llm.openai_api_key, 'env_key')

    @patch('py_code_improver.code_improver.ChatOpenAI')
    @patch('py_code_improver.code_improver.PromptTemplates')
    def test_prompts_action_map(self, mock_prompt_templates, mock_chat_openai):
        mock_prompt_templates.clean_code_prompt = 'clean prompt'
        mock_prompt_templates.docstrings_prompt = 'docstring prompt'
        mock_prompt_templates.tests_prompt = 'test prompt'
        mock_prompt_templates.readme_prompt = 'readme prompt'

        mock_llm_instance = MagicMock()
        # Set the return value of the ChatOpenAI constructor to our mock instance
        mock_chat_openai.return_value = mock_llm_instance

        code_improver = CodeImprover(file_path='test_file.py')
        expected_map = {
            "clean": 'clean prompt',
            "docstrings": 'docstring prompt',
            "tests": 'test prompt',
            "readme": 'readme prompt',
        }
        self.assertEqual(code_improver._prompts_action_map, expected_map)

    @patch('py_code_improver.code_improver.CodeImprover._get_prompt_template')
    @patch('py_code_improver.code_improver.CodeImprover._generate_improved_code')
    @patch('py_code_improver.code_improver.CodeImprover._save_improved_code')
    @patch('py_code_improver.code_improver.logger')
    def test_improve_code_success(
        self, mock_logger, mock_save, mock_generate, mock_get
    ):
        mock_get.return_value = 'clean prompt'
        mock_generate.return_value = 'improved code'
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        code_improver.improve_code('clean')
        mock_get.assert_called_once_with('clean')
        mock_generate.assert_called_once_with('clean prompt')
        mock_save.assert_called_once_with('improved code')
        mock_logger.error.assert_not_called()

    @patch('py_code_improver.code_improver.CodeImprover._get_prompt_template')
    @patch('py_code_improver.code_improver.CodeImprover._generate_improved_code')
    @patch('py_code_improver.code_improver.logger')
    def test_improve_code_no_response(self, mock_logger, mock_generate, mock_get):
        mock_get.return_value = 'clean prompt'
        mock_generate.return_value = None
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        code_improver.improve_code('clean')
        mock_get.assert_called_once_with('clean')
        mock_generate.assert_called_once_with('clean prompt')
        mock_logger.error.assert_called_once_with("No response received from LLM")

    @patch(
        'py_code_improver.code_improver.CodeImprover._prompts_action_map',
        new_callable=MagicMock,
    )
    def test_get_prompt_template_valid_action(self, mock_prompts):
        mock_prompts.get.return_value = 'prompt template'
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        result = code_improver._get_prompt_template('clean')
        self.assertEqual(result, 'prompt template')

    def test_get_prompt_template_invalid_action(self):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        with self.assertRaises(NotImplementedError):
            code_improver._get_prompt_template('invalid_action')

    @patch('py_code_improver.code_improver.CodeImprover._read_code_from_file')
    @patch('py_code_improver.code_improver.CodeImprover._process_template_string')
    @patch('py_code_improver.code_improver.CodeImprover._invoke_llm_with_prompt')
    def test_generate_improved_code(self, mock_invoke, mock_process, mock_read):
        mock_read.return_value = 'original code'
        mock_process.return_value = 'processed template'
        mock_invoke.return_value = 'improved code'
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        result = code_improver._generate_improved_code('prompt template')
        self.assertEqual(result, 'improved code')
        mock_read.assert_called_once()
        mock_process.assert_called_once_with('prompt template')
        mock_invoke.assert_called_once_with(
            'processed template', {'code': 'original code'}
        )

    @patch('builtins.open', new_callable=mock_open, read_data='some code')
    def test_read_code_from_file_success(self, mock_file):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        result = code_improver._read_code_from_file()
        self.assertEqual(result, 'some code')
        mock_file.assert_called_once_with('test_file.py', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='x' * 10000)
    def test_read_code_from_file_exceeds_limit(self, mock_file):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        with self.assertRaises(RuntimeError):
            code_improver._read_code_from_file()

    def test_validate_code_length_success(self):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        code_improver._validate_code_length('short code')

    def test_validate_code_length_failure(self):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        with self.assertRaises(RuntimeError):
            code_improver._validate_code_length('x' * 10000)

    def test_process_template_string(self):
        result = CodeImprover._process_template_string('    indented string')
        self.assertEqual(result, 'indented string')

    @patch('time.time', return_value=1234567890)
    def test_generate_output_file_path(self, mock_time):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        result = code_improver._generate_output_file_path()
        expected_path = 'test_file.py.llm1234567890'
        self.assertEqual(result, expected_path)

    @patch('time.time', return_value=1234567890)
    @patch('builtins.open', new_callable=mock_open)
    def test_save_improved_code(self, mock_file, mock_time):
        code_improver = CodeImprover(file_path='test_file.py', openai_api_key="test")
        code_improver._save_improved_code('improved code')
        mock_file.assert_called_once_with('test_file.py.llm1234567890', 'w')
        mock_file().write.assert_called_once_with('improved code')


if __name__ == '__main__':
    unittest.main()
