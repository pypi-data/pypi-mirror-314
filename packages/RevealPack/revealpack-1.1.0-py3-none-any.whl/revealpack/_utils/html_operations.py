import os
import logging
import sys

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
import sass


def beautify_html(html_str, indent_size=2):
    """
    Beautify an HTML string using BeautifulSoup's prettify method.

    Parameters:
        html_str (str): The HTML string to be beautified.
        indent_size (int): The number of spaces for indentation.

    Returns:
        str: The beautified HTML string.
    """
    # Remove existing indentation and extra spaces
    lines = html_str.split("\n")
    stripped_lines = [line.strip() for line in lines]
    cleaned_html = "\n".join(stripped_lines)

    # Beautify using BeautifulSoup
    formatter = HTMLFormatter(indent=indent_size)
    soup = BeautifulSoup(cleaned_html, "html.parser")
    return soup.prettify(formatter=formatter)


def compile_scss(input_file, output_file):
    """
    Compile an SCSS file to a CSS file using the `sass` Python package.

    Parameters:
        input_file (str): The path to the input SCSS file.
        output_file (str): The path to the output CSS file.
    """
    try:
        compiled_css = sass.compile(filename=input_file)
    except Exception as e:
        # os.chdir(current_directory)
        logging.error(f"Failed to compile {input_file}: {e}")
        sys.exit(1)
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(compiled_css)
    logging.info(f"Successfully compiled {input_file} to {output_file}")
