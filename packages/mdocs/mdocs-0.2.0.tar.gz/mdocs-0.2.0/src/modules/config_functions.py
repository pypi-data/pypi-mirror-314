import os
import json
import logging


def validate_required_fields(message):
    """
    Prompts the user for input and ensures that a value is provided.

    This function repeatedly prompts the user for input until a non-empty
    value is provided. It is used for required fields where user input is mandatory.

    Args:
        message (str): The message to display to the user when asking for input.

    Returns:
        str: The non-empty input provided by the user.
    """
        
    value = input(message)

    while not value:
        print("Warning: This field is required!")
        value = input(message)

    return value


def starter_config(filename):
    """
    Creates an initial configuration file with user-provided project details.

    This function:
    1. Checks if a configuration file already exists at the specified location.
    2. If a file exists, asks the user if they want to overwrite it.
    3. Prompts the user for various required and optional project information such as project name, description, developer/company name, contact email, and repository link.
    4. Writes the collected data to the specified configuration file in JSON format.

    Args:
        filename (str): The name of the configuration file to create or overwrite.

    Returns:
        None
    """

    if os.path.exists(filename):

        overwrite = input(
            f"A configuration file already exists. Do you want to overwrite it? (yes/no): ").strip().lower()

        if overwrite != 'yes' and overwrite != 'y':
            logging.warning("Operation cancelled.")
            return

    print('Starter config...')

    try:

        title = validate_required_fields("Project name (required): ")

        description = validate_required_fields("Project description (required): ")

        developer = input("Developer or company name [default empty]: ")

        mail = input("Contact e-mail [default empty]: ")

        link = input("Repository link [default empty]: ")

    except Exception as e:
        logging.error(f"An error occurred while gathering input: {e}")
        return

    data = {
        "title": title,
        "description": description,
        "developer": developer,
        "mail": mail,
        "link": link
    }

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)
        
        logging.info('Initial configuration file created successfully...')
        
        print('usage: mdocs [filename]')
    
    except IOError as e:
        logging.error(f"An error occurred while writing to the file: {e}")
