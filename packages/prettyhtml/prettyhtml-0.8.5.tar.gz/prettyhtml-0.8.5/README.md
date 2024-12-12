# PrettyHTML

PrettyHTML is a Python library that allows you to refactor HTML code into a pretty dictionary format. This code can be useful when working with web development and needing to manipulate or process HTML elements easily.

## Overview

The primary objective of PrettyHTML is to provide an efficient way to navigate and extract information from HTML code. It converts HTML code into a hierarchical dictionary structure, making it more convenient to access and modify specific elements.

## Features

- **Easy-to-use API**: Utilize a simple and intuitive API to work with HTML code seamlessly.
- **Refactor HTML**: Transform HTML into a hierarchical dictionary format for better manipulation.
- **Find Elements**: Locate specific elements in the HTML code based on their classes or tags without using classes.
- **Customizable**: Adapt the functionality to fit your specific project requirements.

## Structure

PrettyHTML consists of several components, including:

- `HandlerBlock`: Responsible for handling the HTML code and converting it into a hierarchical dictionary structure.
- `Finder`: A class for finding specific elements in the HTML code, using tags and classes (optional).

## Usage

To get started with PrettyHTML, install the library using the following command:

```shell
pip install prettyhtml
```

Import the necessary components and work with the library effortlessly:

```python
from prettyhtml import HandlerBlock

# Read the HTML code from a file
block_html = ""
with open("test.html", "r") as file:
    block_html = file.read()

# Instantiate the HandlerBlock class
HB = HandlerBlock(block_code=block_html)

# Convert the HTML code to a hierarchical dictionary format
out = HB.Handler()

# Access the extracted elements
print(list(out.keys()))
```

By using PrettyHTML, you can easily refactor HTML code into a more manageable dictionary format, making it simpler to interact with and manipulate the elements in your web development projects.
# HTML Handler Documentation

This documentation describes the purpose and usage of the HTML Handler, located at `C:/Users/sinic/Python_Project/handler_html/PrettyHTML/html_handler.py`.

## Usage

The HTML Handler is designed to parse HTML code blocks, find HTML elements without a specific class, and return a dictionary containing the elements organized by their paths within the HTML structure.

## Classes and Methods

### HandlerBlock

The `HandlerBlock` class is the main class of the HTML Handler, responsible for handling the main logic of parsing and organizing elements.

#### `__init__(self, block_code: str) -> None`

The constructor of the `HandlerBlock` class, which initializes the block with the given HTML code (`block_code`).

#### `Handler(self) -> dict`

The main method of the `HandlerBlock` class, which takes the HTML code block and returns a dictionary containing the organized elements without a specific class.

### utillites.Finder

This class is not documented in this file, but is a helper class used for finding and navigating elements within the given HTML block. It assists in locating parent elements and determining their paths.

#### `__handler_element(self) -> dict`

This private method is used internally by the `Handler` method. It takes the HTML code block and finds elements without a specific class, organizing them into a dictionary with the elements grouped by their paths.

#### `__get_item_path(self, finder: utillites.Finder, item) -> str`

This private method retrieves the path of a given HTML element within the parsed HTML structure. It traverses the parent elements of a node item, keeping track of their names to construct the element's path.

## Main

The file's main section demonstrates how to use the HTML Handler in practice:

1. Import the HTML code block from a file named "test.txt".
2. Create an instance of the `HandlerBlock` class with the HTML code block.
3. Call the `Handler` method to get the organized dictionary of elements.
4. Print the keys of the dictionary, which represent the paths of the elements without a specific class.
# utilities.py

This module contains the `Finder` class, which helps to easily search and extract elements from HTML code using BeautifulSoup.

## Usage

First, make sure you have installed BeautifulSoup4:

```bash
pip install beautifulsoup4
```

Usage Example:

```python
from bs4 import BeautifulSoup
from utilities import Finder

html_code = '''
<html>
    <head>
        <title>Example</title>
    </head>
    <body>
        <div>
            <p class="example-text">This is an example paragraph.</p>
            <p>Another paragraph.</p>
        </div>
    </body>
</html>
'''

finder = Finder(html_code)

# Searching by class name.
class_p paragraphs = finder.find_classes('p', 'example-text')
print(class_p)  # Output: [<p class="example-text">This is an example paragraph.</p>]

# Searching all elements with class
class_all paragraphs = finder.find_classes('p', None)
print(class_all)  # Output: [<p class="example-text">This is an example paragraph.</p>, <p>Another paragraph.</p>]

# Searching without class name
without_class_paragraphs = finder.find_without_class()
print(without_class_paragraphs)  # Output: [<p class="example-text">This is an example paragraph.</p>, <p>Another paragraph.</p>]
```

## Methods

### `Finder`

__Args:__
- `html_code`: str, the input HTML code to be parsed and searched from.

### `find_classes(self, type_item, class_name)`

__Args:__
- `type_item`: str, the type of the element to search for (e.g. "div", "p").
- `class_name`: str, the class name of the elements to search for.

__Returns:__
- list, a list of matching elements with the specified type and class name.

### `find_without_class(self)`

__Returns:__
- list, all elements in the HTML code.
