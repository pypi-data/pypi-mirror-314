class PromptTemplates:
    """ """

    clean_code_prompt = """

    Act as a senior developer performing code review.
    Your task is to refactor this code to follow clean code principles while preserving its original functionality.

    To implement this:
    - Use descriptive names
    - Break down large functions into smaller ones, maintain a logical order for easier reading
    - Ensure each function has a single responsibility
    - Avoid unnecessary comments
    - Limit variable scope

    - **Code:**
    {code}

    """

    docstrings_prompt = """

        Act as a senior developer performing code review.
        Your task is to add docstrings to each method while preserving its original functionality.

        To implement this:
        - Add docstrings for each method and each variable
        - Describe return types
        - Describe method functionality in docstrings

        - **Code:**
        {code}

        """

    tests_prompt = """

        Act as a senior developer performing code review.
        Your task is to create unit test to each method while preserving its original functionality.

        To implement this:
        - Suggest unit test for each method and each code path

        - **Code:**
        {code}

        """

    readme_prompt = """

        Act as a technical writer, your task is to create README file
        to describe the purpose and usage of code.

        To implement this:
        - Suggest text for README file describing the code

        - **Code:**
        {code}

        """
