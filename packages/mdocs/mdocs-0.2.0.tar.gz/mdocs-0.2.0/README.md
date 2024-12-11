# mdocs

**mdocs** allows you to extract docstrings from Python functions to create a documentation file in Markdown format. It is designed as an alternative for projects that consist of just a few functions and do not require more sophisticated tools. We will obtain an MD file that can easily be linked to the README of our repository to present accessible and well-organized technical documentation to clients or users.

See the generated document of this same project as an example [here](docs/documentation.md).

## Install

It can be installed from the PyPI repository.
```bash
pip install mdocs
```
[https://pypi.org/project/mdocs/0.1.0/](https://pypi.org/project/mdocs/0.1.0/)

## Usage

### First use

On the first use, use `-c` to configure the project.
```bash
mdocs -c
```
This will initiate the configuration process for the project. Enter the project details and remember that Project name and Project description are required.
```bash
Starter config...
Project name (required): Test Project
Project description (required): This is a test project
Developer or company name [default empty]: Your name
Contact e-mail [default empty]: Your email
Repository link [default empty]: Your link
2024-10-19 00:02:06,010 - INFO - Initial configuration file created successfully...
usage: mdocs [source]
```
This will create a configuration file named **mdocs_settings.json** in the directory where the program was executed.

### Create documentation.

Use `mdocs [source]` to extract the documentation from your functions. `[source]` is the path to your source files.

For example.
```bash
mdocs ./src
```
This will create a file named **documentation.md** that will contain the documentation for your functions in the directory where the program was executed.

## For it to work.

For now, it only extracts docstrings from functions and class, but more functionality is expected to be added.

It is expected to find a docstring with the following structure:

```python
def calculate_rectangle_area(base, height):
    """
    Calculates the area of a rectangle.

    Args:
        base (float): The length of the rectangle's base.
        height (float): The height of the rectangle.

    Returns:
        float: The area of the rectangle calculated as base * height.

    Example:
        >>> calculate_rectangle_area(5, 3)
        15
    """
    return base * height
```

## Contributing

If you would like to contribute or share ideas for improvement, please feel free to contact me via email. I welcome all suggestions and contributions to enhance this project!
