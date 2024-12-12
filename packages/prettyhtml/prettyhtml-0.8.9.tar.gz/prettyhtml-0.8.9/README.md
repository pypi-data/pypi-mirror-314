# PrettyHTML

## Overview

PrettyHTML is a Python library designed to refactor HTML code into a pretty dictionary format. It allows users to easily parse and structure HTML content, making it more readable and accessible for further processing or analysis. The library utilizes the BeautifulSoup parser to extract HTML elements and their attributes, effectively organizing the code into a user-friendly format.

## Features

- Conversion of HTML code into a dictionary format
- Recursive element path extraction for easy navigation through the document structure
- Handling of HTML elements without class attributes
- Customizable element searching with optional class filtering

## Structure

The PrettyHTML library consists of three main Python files:

1. `html_handler.py`: Contains the `HandlerBlock` class that takes HTML code as input and refactors it into a dictionary structure.
2. `utillites.py`: Houses the `Finder` class, which uses BeautifulSoup to find elements in a given HTML code and provides methods for finding elements with or without class attributes.
3. `__init__.py`: Initializes the PrettyHTML library by importing necessary functions and classes.

## Usage

To use PrettyHTML in your project, you need to follow these steps:

1. Install PrettyHTML using pip: `pip install prettyhtml`

2. Import the required files in your Python script:
   ```python
   from handler_html.PrettyHTML import HandlerBlock
   from handler_html.utillites import Finder
   ```

3. Create an instance of the `HandlerBlock` class and pass the HTML code as input:
   ```python
   block_code = """
   <div>
       <h1>Hello, World!</h1>
       <p>This is some text inside a paragraph</p>
   </div>
   """
   hb = HandlerBlock(block_code=block_code)
   ```

4. Call the `Handler` method of the `HandlerBlock` instance to obtain the refactored HTML code in dictionary format:
   ```python
   output = hb.Handler()
   print(output)
   ```

By following these steps, users can easily reshape their HTML code into a more accessible and organized dictionary structure using the PrettyHTML library.
# html_handler.py

This file provides a class for handling HTML content. The main goal is to parse HTML content and organize the elements into a dictionary structure.

## Usage

To use the `html_handler.py` class, follow these steps:

1. Import the necessary utility classes from the same module by using either a local or absolute import. In this example, import the `utillites` class.

   ```python
   try:
       import utillites
   except:
       from . import utillites
   ```

2. Create an instance of the `HandlerBlock` class initialized with the HTML content as the block code.

   ```python
   block_html = ""
   with open("test.txt", "r") as file:
       block_html = file.read()
   HB = HandlerBlock(block_code=block_html)
   ```

3. Invoke the `Handler()` method on the `HandlerBlock` instance to process the HTML content and get a dictionary containing the organized elements.

   ```python
   out = HB.Handler()
   ```

## Methods

### `__init__(self, block_code: str)`

- Description: Initializes the `HandlerBlock` class with the HTML content as the `block_code`.
- Parameters:
  - `block_code` (str): The HTML content to be parsed.

### `Handler(self) -> dict`

- Description: Processes the HTML content using the `__handler_element()` method and returns a dictionary containing organized elements.
- Parameters: None.
- Returns:
  - `dict`: A dictionary containing the organized elements.

### `__handler_element(self) -> dict`

- Description:Processes the HTML content, finding the elements without a class, and organizes them into a dictionary.
- Parameters: None.
- Returns:
  - `dict[str, list]`: A dictionary containing the organized elements.

### `__get_item_path(self, finder: utillites.Finder, item) -> str`

- Description: Recursively traverses the HTML content to determine the element's path and return it.
- Parameters:
  - `finder` (`utillites.Finder`): A `Finder` object provided for traversing the HTML content.
  - `item` (`object`): The current item being processed.
- Returns:
  - `str`: The item's path based on the parent/child relationships in the given HTML content.

## Example

The `__main__` section in the file demonstrates how to use the `HandlerBlock` class by reading HTML content from a file (test.txt), processing it, and printing its top-level keys. To use this example, replace `"test.txt"` with the path to your HTML file containing the content you would like to process.

```python
if __name__ == "__main__":
    block_html = ""
    with open("test.txt", "r") as file:
        block_html = file.read()
    HB = HandlerBlock(block_code=block_html)
    out = HB.Handler()
    print(list(out.keys()))
```
# utilities.py

This file contains a `Finder` class which is used to search for HTML elements within a provided HTML string. It utilizes the `BeautifulSoup` library to parse and extract HTML elements based on specified criteria.

## Finder Class

The `Finder` class is initialized with an HTML code string, which is then parsed using the `BeautifulSoup` library.

### Methods

#### `__init__(self, html_code: str) -> None`

- Initializes the `Finder` class with the provided `html_code` parameter.
- The `html_code` is parsed using the `BeautifulSoup` library with the 'html.parser'.

#### `find_classes(self, type_item, class_name) -> list`

- Searches for HTML elements with the specified `type_item` and `class_name`.
- The `type_item` parameter accepts either 'div', 'span', 'p', 'button', etc.
- The `class_name` parameter is the class name of the desired HTML element.
- Returns a list of matching HTML elements.

#### `find_without_class(self) -> list`

- Searches for all HTML elements without a class name.
- Returns a list of all matching HTML elements.


# PrettyHTML: \_\_init\_\_.py

This module contains the main class for the PrettyHTML library, which primarily focuses on helping users format their HTML content in a more readable way by automating the process of adding indentation, line breaks, and additional formatting to HTML code. The main class is named `PrettyHTML`, created with an intention to be both developer-friendly and versatile, supporting a wide range of HTML generation and formatting scenarios.

## Usage

To use the PrettyHTML module, you need to follow these simple steps:

1. Import the `PrettyHTML` class from the module.
2. Create an instance of the `PrettyHTML` class.
3. Add HTML content using various built-in methods and properties.
4. Generate formatted HTML by accessing the `formatted` property of the class instance.

Here's a brief example:

```python
from PrettyHTML import PrettyHTML

# Create an instance of PrettyHTML class
pretty_html = PrettyHTML()

# Add HTML content using built-in methods and properties
pretty_html.add_head('<meta charset="utf-8">')
pretty_html.add_script('src')

# Add arbitrary HTML content
pretty_html.add_html('<h1>Welcome to PrettyHTML!</h1>')

# Generate formatted HTML content
formatted_html = pretty_html.formatted
```

In this example, we created an instance of the `PrettyHTML` class, added content (head, script, and arbitrary HTML) using its methods, and accessed the formatted HTML content through the `formatted` property.

## Methods and Properties

### Constructor: __init__(self)

The `__init__` constructor initializes a new `PrettyHTML` instance, setting up the template for HTML content. This method ensures that the class maintains its structure and formatting settings during object creation.

### add_head(self, head_content: str)

After creating an instance of the `PrettyHTML` class, the `add_head` method enables users to insert content corresponding to the HTML `<head>` element. The `head_content` argument should be a valid HTML head content string.

### add_script(self, script_content: str)

The `add_script` method facilitates adding JavaScript `<script>` content to the HTML `head` section. The `script_content` argument should be a valid JS script string.

### add_html(self, html_content: str)

The `add_html` method allows users to add arbitrary HTML content to the class instance. Its `html_content` argument must be a valid string containing HTML code.

### formatted(self) -> str

Finally, the `formatted` property returns a formatted string containing all added content (head, script, and HTML) in a properly formatted, readable manner.

By accessing the `formatted` property on the `PrettyHTML` instance, you obtain the complete, formatted, and styled HTML content, ready for usage in your projects or further manipulation as required.

# pyproject.toml

This file describes the project's build requirements and dependencies. It is used by tools like Poetry to manage project's dependencies and build system.

## Usage

To create a new `pyproject.toml` file with the basic structure, you can use the following command:

```bash
touch pyproject.toml
```

Then, open the `pyproject.toml` file and add the necessary fields. For example:

```toml
[tool.poetry]
name = "prettyhtml"
version = "0.8.5"
description = "This code can refactor your html in pretty dict"
authors = ["dima-on <sinica911@gmail.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
bs4 = "^0.0.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Make sure to replace the content with the appropriate information for your project.

## Methods

This file does not contain any methods, but it is essential for declaring dependencies and build requirements for your project.

- `[tool.poetry]`: This section contains general project configuration fields like name, version, description, authors, license, and readme.
- `[tool.poetry.dependencies]`: This section specifies the dependencies your project requires, listing the package names and their specific versions or version ranges.
- `[build-system]`: This section describes the build system used for your project, specifying the required packages and the build-backend.

Make sure to refer to the official [PyPA's pyproject-toml documentation](https://python-poetry.org/docs/pyproject) for more information regarding the available fields and configurations for this file.
