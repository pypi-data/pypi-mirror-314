import os
import re
import ast
import json
import fnmatch
import logging


def read_config_file(config_file):
    """
    Reads and parses a JSON configuration file.

    This function attempts to open and read the specified configuration file, 
    returning the parsed data if successful. It handles errors such as the file 
    not being found or invalid JSON format.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The parsed configuration data from the file, or None if an error occurs.

    Example:
        >>> read_config_file('mdocs_settings.json')
        INFO - 'The configuration file has been read successfully'
        DEBUG - {"title": "Test Project", "description": "This is a test project", "developer": "Your name", "mail": "Your email", "link": "Your link"}
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logging.info('The configuration file has been read successfully')
            logging.debug(data)
            return data
        
    except FileNotFoundError:
        logging.error(f"Error reading configuration file. usage: mdocs [-c]")
        return
    
    except json.JSONDecodeError:
        logging.error(f"Error: The file is not a valid JSON.")
        return
    
    except Exception as e:
        logging.error(f"Unexpected error {e}")
        return


def find_python_files(directory):
    """
    Recursively searches for Python files in the specified directory.

    This function scans the provided directory for `.py` files and returns
    a list of their paths.

    Args:
        directory (str): The directory path to search for Python files.

    Returns:
        list: A list of file paths to Python files in the directory, or None if the directory is invalid.
    """

    python_files = []

    if not os.path.isdir(directory):
        logging.error(f'Error: "{directory}" is not a valid directory.')
        return

    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.py'):
            python_files.append(os.path.join(root, filename))
            logging.debug(f'File "{filename}" found.')

    return python_files


def extract_functions_with_docstring(paths):
    """
    Extracts functions or class and their docstrings from a list of Python files.

    This function parses each Python file in the provided list, extracting the 
    function or class names and their associated docstrings, if available.

    Args:
        paths (list): A list of file paths to Python files.

    Returns:
        list: A list of tuples containing the module name and a list of function names with their docstrings.
    """

    mudules = []

    for file_path in paths:

        module_name = os.path.basename(file_path)

        functions = []

        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                class_name = node.name
                docstring = ast.get_docstring(node)
                functions.append((f"Class: {class_name}", docstring))

                logging.debug(
                    f'Class {class_name} from {module_name} extracted.')
                
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                docstring = ast.get_docstring(node)
                functions.append((func_name, docstring))

                logging.debug(
                    f'Function {func_name} from {module_name} extracted.')

        if functions:
            mudules.append((module_name, functions))

    logging.info('Functions extracted successfully...')

    return mudules


def format_section(section_name, docstring):
    """
    Formats a specific section (e.g., Args, Returns) in a function's docstring.

    This function searches for the specified section in the docstring and formats it 
    as a list, if found.

    Args:
        section_name (str): The name of the section to format (e.g., 'Args', 'Returns').
        docstring (str): The function's docstring to format.

    Returns:
        str: The formatted docstring with the specified section formatted as a list.
    """

    pattern = rf"({section_name}:)(.*?)(\n\S|$)"

    match = re.search(pattern, docstring, flags=re.DOTALL)

    if match:

        section_content = match.group(2).strip()

        formatted_section = "\n".join(
            [f"\n- {line.strip()}\n" for line in section_content.splitlines()])

        docstring = docstring[:match.start(
            2)] + formatted_section + docstring[match.end(2):]

    return docstring


def format_example(docstring):
    """
    Formats the 'Example' section in a docstring.

    This function looks for an 'Example:' section in the docstring and formats it
    within code blocks for better readability.

    Args:
        docstring (str): The function's docstring to format.

    Returns:
        str: The formatted docstring with the 'Example' section in code blocks.
    """

    if "Example:" in docstring:
        docstring = re.sub(r"(Example:)(.*)", r"\1\n```\2\n```", docstring, flags=re.DOTALL)

    return docstring


def write_to_md(source_file, config_file, output_file):
    """
    Generates a Markdown documentation file from Python files and configuration data.

    This function reads the configuration file, scans the source directory for Python 
    files, extracts the functions and their docstrings, and writes the formatted 
    documentation to the specified output file in Markdown format.

    Args:
        source_file (str): The path to the source directory containing Python files.
        config_file (str): The path to the JSON configuration file.
        output_file (str): The path to the output Markdown file.

    Returns:
        None
    """

    try:
        config = read_config_file(config_file)

        title = config.get('title', 'Title Default')

        description = config.get('description', 'Description Default')

        developer = config.get('developer', '')

        mail = config.get('mail', '')

        link = config.get('link', '')

        paths = find_python_files(source_file)

        modules = extract_functions_with_docstring(paths)

        with open(output_file, "w", encoding="utf-8") as file:

            if title != '':
                file.write(f"# {title}\n")      
            if description != '':
                file.write(f"{description}\n\n")
            if developer != '':
                file.write(f"#### Developed by {developer}\n\n")
                if link != '':
                    file.write(f"- GitHub: [{link}]({link})\n\n")
                if mail != '':
                    file.write(f"- Contact: [{mail}](mailto:{mail})\n\n")

            for module, functions in modules:

                file.write(f"## Module {module}\n")

                for func_name, docstring in functions:

                    file.write(f"### {func_name}( )\n")

                    if docstring:
                        docstring = format_section("Methods", docstring)
                        docstring = format_section("Args", docstring)
                        docstring = format_section("Returns", docstring)
                        docstring = format_section("Raises", docstring)
                        docstring = format_example(docstring)
                        file.write(f"\n{docstring}\n\n\n")

                        logging.debug(
                            f'Function {func_name} recorded correctly')

                    else:
                        file.write("_No docstring available_\n\n")

                        logging.warning(
                            f"Function {func_name} _No docstring available_")
                file.write(f"---\n\n")

        logging.info(
            f'The documentation was successfully generated in the file "{output_file}"')

    except AttributeError as e:
        logging.error(e)

    except FileNotFoundError as e:
        logging.error(e)

    except Exception as e:
        logging.error(f"Unexpected error {e}")