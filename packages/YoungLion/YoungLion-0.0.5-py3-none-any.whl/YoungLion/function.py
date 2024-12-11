import os
import json
import csv
import yaml
import subprocess
import webbrowser
import sqlite3
import zipfile
import configparser
from configparser import ConfigParser
from collections import defaultdict
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any, List
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

class File:
    """
    A comprehensive file processing class that supports various operations on 
    JSON, TXT, CSV, LOG, INI, YML and other files with advanced error handling,
    directory management and flexible path processing features based on file-folder configuration.
    """

    SUPPORTED_FORMATS = ['.json', '.txt', '.log', '.pdf', '.xml', '.csv', '.yml', '.yaml', '.ini', '.properties', '.md', '.rtf', '.html', '.css', '.js']  # Supported file formats

    def __init__(self, filefolder: Optional[str] = None):
        """
        Initializes the File object with an optional filefolder for default file path handling.

        :param filefolder: Optional root directory for file operations, if specified.
        """
        self.filefolder = filefolder

    def _default_dict(self):
        """
        Generates a nested defaultdict structure to allow safe access to deeply nested keys without risk of KeyError.
        """
        return defaultdict(self._default_dict)

    def _recursive_update(self, target, default):
        """
        Recursively updates a target dictionary by filling in missing keys from a default dictionary.

        :param target: The dictionary to be updated.
        :param default: The dictionary containing default keys and values.
        :return: The updated target dictionary with all keys from the default dictionary.
        """
        for key, value in default.items():
            if isinstance(value, dict):
                target[key] = self._recursive_update(target.get(key, {}), value)
            else:
                target.setdefault(key, value)
        return target

    def _validate_and_prepare_path(self, path: str):
        """
        Converts a file path to an absolute path, optionally prepends filefolder, and ensures directory existence.

        :param path: The file path to validate and prepare.
        :return: An absolute file path, creating any required directories.
        """
        # If the path is relative and filefolder is provided, prepend filefolder to the path
        if not os.path.isabs(path) and self.filefolder and not (path.startswith("./") or path.startswith("../")):
            path = os.path.join(self.filefolder, path)
        
        absolute_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)  # Create required directories if missing
        return absolute_path

    # JSON File Operations

    def json_read(self, path: str, default: Optional[dict] = None) -> dict:
        """
        Reads data from a JSON file and returns it as a dictionary. If the file does not exist,
        creates an empty JSON file and returns the default dictionary if provided.

        :param path: Path to the JSON file.
        :param default: Optional default dictionary structure.
        :return: A dictionary containing JSON data or default values if the file is missing.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            data = default or {}
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f, object_hook=lambda d: defaultdict(self._default_dict, d))
            except json.JSONDecodeError as e:
                print(f"JSON decoding error while reading {path}: {e}")
                data = default or {}

        if default:
            data = self._recursive_update(data, default)
        
        return data

    def json_write(self, path: str, data: dict):
        """
        Writes a dictionary to a JSON file, ensuring directory structure exists.

        :param path: Path to the JSON file.
        :param data: A dictionary containing data to write.
        :raises TypeError: If data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("Data to be written must be a dictionary.")
        
        file_path = self._validate_and_prepare_path(path)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"An error occurred while writing to JSON file {path}: {e}")

    # TXT File Operations

    def txt_read_str(self, path: str) -> str:
        """
        Reads a text file and returns its entire content as a single string.

        :param path: Path to the text file.
        :return: A string containing the file's content.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # Create an empty file if it does not exist
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content

    def txt_read_linear(self, path: str) -> Dict[str, str]:
        """
        Reads a text file line by line, returning a dictionary with line numbers as keys.

        :param path: Path to the text file.
        :return: A dictionary where each line is mapped by line numbers.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # Create an empty file if it does not exist
            
        lines = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, 1):
                lines[str(idx)] = line.strip()
        
        return lines

    def txt_write_str(self, path: str, content: str):
        """
        Writes a single string content to a text file, overwriting any existing data.

        :param path: Path to the text file.
        :param content: The content to be written to the file.
        """
        file_path = self._validate_and_prepare_path(path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def txt_write_linear(self, path: str, data: Dict[int, str]):
        """
        Writes dictionary entries to a text file where keys are line numbers and values are line content.

        :param path: Path to the text file.
        :param data: Dictionary where each key represents a line number and value represents content.
        """
        file_path = self._validate_and_prepare_path(path)
        max_line = max(data.keys())
        
        with open(file_path, 'w', encoding='utf-8') as file:
            for line_num in range(1, max_line + 1):
                line_content = data.get(line_num, "")
                file.write(line_content + '\n')

    # LOG File Operations

    def log_read(self, path: str) -> Dict[str, str]:
        """
        Reads a log file line by line, returning each line as an entry in a dictionary with line numbers as keys.

        :param path: Path to the log file.
        :return: Dictionary where each key is a line number and value is the line content.
        """
        return self.txt_read_linear(path)

    def log_write(self, path: str, content: str):
        """
        Writes a single log entry to a log file, appending it to the end of the file.

        :param path: Path to the log file.
        :param content: Log entry to append to the file.
        """
        file_path = self._validate_and_prepare_path(path)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content + '\n')

    def log_write_entry(self, path: str, entry: str):
        """
        Writes a log entry with a timestamp to the log file, appending it to the end of the file.

        :param path: Path to the log file.
        :param entry: The log entry text.
        """
        from datetime import datetime

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {entry}"
        
        self.log_write(path, log_entry)

    # PDF File Operations

    def pdf_read(self, path: str) -> str:
        """
        Reads a PDF file and returns its text content as a single string.

        :param path: Path to the PDF file.
        :return: A string containing the text content of the PDF.
        :raises FileNotFoundError: If the PDF file does not exist.
        """
        file_path = self._validate_and_prepare_path(path)
        content = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        reader = PdfReader(file_path)
        for page in reader.pages:
            content.append(page.extract_text())
        
        return "\n".join(content)

    def pdf_write(self, path: str, content: str):
        """
        Writes text content to a PDF file, creating a new file or overwriting an existing one.

        :param path: Path to the PDF file.
        :param content: The text content to write to the PDF.
        """
        file_path = self._validate_and_prepare_path(path)
        
        # Set up a canvas to write text content to a new PDF
        c = canvas.Canvas(file_path)
        text_obj = c.beginText(40, 800)  # Position the text object at an initial Y-position
        
        # Write each line of content to the PDF
        for line in content.splitlines():
            text_obj.textLine(line)
        
        c.drawText(text_obj)
        c.save()
    def xml_read(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Reads an XML file and parses it into a Python dictionary.

        :param path: Path to the XML file.
        :return: A dictionary representing the XML structure, or None if the file doesn't exist or is invalid.
        :raises FileNotFoundError: If the XML file does not exist.
        :raises ET.ParseError: If there is an error parsing the XML file.
        """
        file_path = self._validate_and_prepare_path(path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Convert XML tree to a nested dictionary
            return self._xml_to_dict(root)
        except ET.ParseError as e:
            print(f"Error parsing the XML file {path}: {e}")
            return None

    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Converts an XML Element to a dictionary. Recursively processes child elements.

        :param element: The XML Element to convert.
        :return: A dictionary representation of the XML element.
        """
        parsed_data = {}
        
        for child in element:
            child_dict = self._xml_to_dict(child)
            # If the tag already exists in the dictionary, append to a list
            if child.tag in parsed_data:
                if isinstance(parsed_data[child.tag], list):
                    parsed_data[child.tag].append(child_dict)
                else:
                    parsed_data[child.tag] = [parsed_data[child.tag], child_dict]
            else:
                parsed_data[child.tag] = child_dict
        
        # Add attributes of the element as well
        if element.attrib:
            parsed_data['@attributes'] = element.attrib
        
        if element.text and element.text.strip():
            parsed_data['#text'] = element.text.strip()
        
        return parsed_data

    def xml_write(self, path: str, data: Dict[str, Any], root_element: Optional[str] = 'root'):
        """
        Writes a dictionary to an XML file.

        :param path: Path to the XML file.
        :param data: The data to be written as an XML structure.
        :param root_element: The name of the root element for the XML structure.
        :raises ValueError: If data is not a dictionary or cannot be converted to XML.
        """
        if not isinstance(data, dict):
            raise ValueError("Data to be written must be a dictionary.")

        file_path = self._validate_and_prepare_path(path)
        
        # Convert the dictionary to an XML tree
        root = self._dict_to_xml(data, root_element)
        tree = ET.ElementTree(root)
        
        # Write the tree to the file
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    def _dict_to_xml(self, data: Dict[str, Any], root_element: str) -> ET.Element:
        """
        Converts a dictionary to an XML Element, recursively processing nested structures.

        :param data: The dictionary containing data to convert.
        :param root_element: The name of the root element.
        :return: The corresponding XML Element object.
        """
        # Create the root element
        root = ET.Element(root_element)
        
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively create sub-elements for nested dictionaries
                sub_elem = self._dict_to_xml(value, key)
                root.append(sub_elem)
            elif isinstance(value, list):
                # Handle lists by creating a sub-element for each item in the list
                for item in value:
                    sub_elem = self._dict_to_xml(item, key)
                    root.append(sub_elem)
            else:
                # If the value is a simple type, set it as the text of the element
                sub_elem = ET.Element(key)
                sub_elem.text = str(value)
                root.append(sub_elem)
        
        return root

    def xml_append(self, path: str, data: Dict[str, Any], root_element: Optional[str] = 'root'):
        """
        Appends data to an existing XML file.

        :param path: Path to the XML file.
        :param data: Data to append to the XML file.
        :param root_element: The root element to use for appending.
        :raises ValueError: If data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Data to be appended must be a dictionary.")

        file_path = self._validate_and_prepare_path(path)

        # Check if the file exists and read the existing data
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()
        else:
            root = ET.Element(root_element)
        
        # Convert the dictionary to XML and append it to the root element
        new_elements = self._dict_to_xml(data, root_element)
        root.append(new_elements)

        # Write the updated XML tree back to the file
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    def xml_find(self, path: str, query: str) -> Optional[Dict[str, Any]]:
        """
        Finds and returns the first matching element based on the provided query.

        :param path: Path to the XML file.
        :param query: Query string to find the element (XPath).
        :return: A dictionary representing the matching XML element, or None if not found.
        :raises FileNotFoundError: If the XML file does not exist.
        :raises ET.ParseError: If there is an error parsing the XML file.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Find the element using XPath query
            element = root.find(query)
            if element is not None:
                return self._xml_to_dict(element)
            else:
                return None
        except ET.ParseError as e:
            print(f"Error parsing the XML file {path}: {e}")
            return None
    def csv_read(self, path: str, delimiter: str = ',', quotechar: str = '"') -> List[Dict[str, str]]:
        """
        Reads a CSV file and returns its contents as a list of dictionaries.
        Each row is represented as a dictionary where the keys are column headers.
        
        If the file does not exist, it creates an empty CSV file with headers.
        
        Parameters:
            path (str): Path to the CSV file.
            delimiter (str): Character used to separate values. Defaults to ','.
            quotechar (str): Character used to quote fields. Defaults to '"'.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries where each dictionary corresponds to a row.
        """
        file_path = self._validate_and_prepare_path(path)
        
        # If the file doesn't exist, create an empty CSV with headers
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=[], delimiter=delimiter, quotechar=quotechar)
                writer.writeheader()  # Write an empty header
            return []

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter, quotechar=quotechar)
            return [row for row in reader]

    def csv_write(self, path: str, data: List[Dict[str, str]], fieldnames: Optional[List[str]] = None, delimiter: str = ',', quotechar: str = '"'):
        """
        Writes a list of dictionaries to a CSV file. The keys of the dictionary represent the column headers.
        
        Parameters:
            path (str): Path to the CSV file.
            data (List[Dict[str, str]]): List of dictionaries to be written to the CSV.
            fieldnames (List[str], optional): List of fieldnames (headers) for the CSV file. Defaults to None, which uses the keys of the first dictionary.
            delimiter (str): Character used to separate values. Defaults to ','.
            quotechar (str): Character used to quote fields. Defaults to '"'.
        """
        if not data:
            raise ValueError("Data cannot be empty.")
        
        # If fieldnames are not provided, use the keys from the first dictionary
        if not fieldnames:
            fieldnames = data[0].keys()

        file_path = self._validate_and_prepare_path(path)
        
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter, quotechar=quotechar)
            writer.writeheader()
            writer.writerows(data)

    def csv_append(self, path: str, data: List[Dict[str, str]], fieldnames: Optional[List[str]] = None, delimiter: str = ',', quotechar: str = '"'):
        """
        Appends a list of dictionaries to an existing CSV file. The keys of the dictionary represent the column headers.
        
        Parameters:
            path (str): Path to the CSV file.
            data (List[Dict[str, str]]): List of dictionaries to be appended to the CSV.
            fieldnames (List[str], optional): List of fieldnames (headers) for the CSV file. Defaults to None, which uses the keys of the first dictionary.
            delimiter (str): Character used to separate values. Defaults to ','.
            quotechar (str): Character used to quote fields. Defaults to '"'.
        """
        if not data:
            raise ValueError("Data cannot be empty.")
        
        # If fieldnames are not provided, use the keys from the first dictionary
        if not fieldnames:
            fieldnames = data[0].keys()

        file_path = self._validate_and_prepare_path(path)
        
        # Append to the file, if it exists; otherwise, create a new file with headers
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter, quotechar=quotechar)
            if file.tell() == 0:  # If file is empty, write header first
                writer.writeheader()
            writer.writerows(data)

    def csv_update(self, path: str, data: List[Dict[str, str]], identifier: str, delimiter: str = ',', quotechar: str = '"'):
        """
        Updates specific rows in a CSV file. Identifies rows using a unique identifier (fieldname).
        
        Parameters:
            path (str): Path to the CSV file.
            data (List[Dict[str, str]]): List of dictionaries to update.
            identifier (str): The column name used to identify rows that need to be updated.
            delimiter (str): Character used to separate values. Defaults to ','.
            quotechar (str): Character used to quote fields. Defaults to '"'.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        # Read the existing content from the CSV file
        existing_data = self.csv_read(path, delimiter, quotechar)
        
        # Update the data
        updated_data = []
        for row in existing_data:
            for new_row in data:
                if row[identifier] == new_row[identifier]:
                    row.update(new_row)
            updated_data.append(row)
        
        # Write the updated data back to the CSV file
        self.csv_write(path, updated_data, fieldnames=existing_data[0].keys(), delimiter=delimiter, quotechar=quotechar)
    def yaml_read(self, path: str, default: Optional[dict] = None) -> dict:
        """
        Reads a YAML file and returns its contents as a dictionary. 
        If the file does not exist, it creates an empty YAML file with the default content.

        :param path: Path to the YAML file.
        :param default: Optional dictionary to provide default values if the file is missing.
        :return: A dictionary representing the YAML data.
        """
        file_path = self._validate_and_prepare_path(path)

        # If file does not exist, create an empty YAML file
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(default or {}, file, default_flow_style=False)
            return default or {}

        # Read existing YAML file
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(f"Error reading YAML file {path}: {e}")
                data = default or {}

        return data

    def yaml_write(self, path: str, data: dict):
        """
        Writes a dictionary to a YAML file. If the file exists, it will be overwritten.
        
        :param path: Path to the YAML file.
        :param data: A dictionary representing the data to be written.
        """
        file_path = self._validate_and_prepare_path(path)

        # Write to the YAML file
        with open(file_path, 'w', encoding='utf-8') as file:
            try:
                yaml.dump(data, file, default_flow_style=False)
            except yaml.YAMLError as e:
                print(f"Error writing to YAML file {path}: {e}")
    
    def ini_read(self, path: str, default: Optional[Dict[str, Dict[str, str]]] = None) -> Dict[str, Dict[str, str]]:
        """
        Reads an INI file and returns its contents as a dictionary.
        If the file does not exist, it creates an empty INI file with the default content.

        :param path: Path to the INI file.
        :param default: Optional dictionary to provide default values if the file is missing.
        :return: A dictionary representing the INI data.
        """
        file_path = self._validate_and_prepare_path(path)

        # If file does not exist, create an empty INI file with default content
        if not os.path.exists(file_path):
            config = configparser.ConfigParser()
            if default:
                for section, values in default.items():
                    config[section] = values
            with open(file_path, 'w', encoding='utf-8') as file:
                config.write(file)
            return default or {}

        # Read the existing INI file
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')

        # Convert to a dictionary
        data = {section: dict(config.items(section)) for section in config.sections()}

        return data

    def ini_write(self, path: str, data: Dict[str, Dict[str, str]], append: bool = False):
        """
        Writes a dictionary to an INI file. If the file exists, it can be either overwritten or appended.
        
        :param path: Path to the INI file.
        :param data: A dictionary representing the data to be written to the INI file.
        :param append: If True, the data will be appended to the file; if False, the file will be overwritten.
        """
        file_path = self._validate_and_prepare_path(path)

        config = configparser.ConfigParser()

        # If appending, read the existing file and add new sections/values
        if append:
            config.read(file_path, encoding='utf-8')

        for section, values in data.items():
            if not config.has_section(section):
                config.add_section(section)
            for key, value in values.items():
                config.set(section, key, value)

        with open(file_path, 'w', encoding='utf-8') as file:
            config.write(file)
    def properties_read(self, path: str) -> Dict[str, str]:
        """
        Reads a .properties file and returns the data as a dictionary.
        
        Each line in the .properties file should follow the format `key=value`.
        Lines that start with `#` or `!` are considered comments and ignored.

        :param path: Path to the .properties file.
        :return: A dictionary of key-value pairs read from the file.
        """
        file_path = self._validate_and_prepare_path(path)
        properties = {}

        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # Create empty file if not exists

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(('#', '!')) and '=' in line:
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()

        return properties

    def properties_write(self, path: str, data: Dict[str, str], append: bool = False):
        """
        Writes a dictionary to a .properties file. Supports appending or overwriting.

        :param path: Path to the .properties file.
        :param data: A dictionary where each key-value pair is written as `key=value`.
        :param append: If True, appends data to the file. If False, overwrites the file.
        """
        file_path = self._validate_and_prepare_path(path)
        mode = 'a' if append else 'w'

        with open(file_path, mode, encoding='utf-8') as f:
            for key, value in data.items():
                f.write(f"{key} = {value}\n")

    def md_read(self, path: str) -> str:
        """
        Reads a .md file and returns its content as a string.

        :param path: Path to the .md file.
        :return: A string containing the Markdown content.
        """
        file_path = self._validate_and_prepare_path(path)

        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # Create empty file if not exists

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content

    def md_write(self, path: str, content: str, append: bool = False):
        """
        Writes a string to a .md file. Supports appending or overwriting.

        :param path: Path to the .md file.
        :param content: Markdown content to write.
        :param append: If True, appends content to the file. If False, overwrites the file.
        """
        file_path = self._validate_and_prepare_path(path)
        mode = 'a' if append else 'w'

        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)

    def rtf_read(self, path: str) -> str:
        """
        Reads an RTF (.rtf) file and returns its content as a string.

        :param path: Path to the .rtf file.
        :return: A string containing the RTF content.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if not os.path.exists(file_path):
            open(file_path, 'w').close()  # Create empty file if not exists

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content

    def rtf_write(self, path: str, content: str, append: bool = False):
        """
        Writes a string to an RTF (.rtf) file. Supports appending or overwriting.

        :param path: Path to the .rtf file.
        :param content: Text content to write to the RTF file.
        :param append: If True, appends content to the file. If False, overwrites the file.
        """
        file_path = self._validate_and_prepare_path(path)
        mode = 'a' if append else 'w'

        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)

    def html_read(self, path: str) -> str:
        """
        Reads an HTML (.html, .htm) file and returns its content as a string.

        :param path: Path to the .html or .htm file.
        :return: A string containing the HTML content.
        """
        return self.rtf_read(path)

    def html_write(self, path: str, content: str, append: bool = False):
        """
        Writes a string to an HTML (.html, .htm) file. Supports appending or overwriting.

        :param path: Path to the .html or .htm file.
        :param content: HTML content to write to the file.
        :param append: If True, appends content to the file. If False, overwrites the file.
        """
        self.rtf_write(path, content, append)

    def css_read(self, path: str) -> str:
        """
        Reads a CSS (.css) file and returns its content as a string.

        :param path: Path to the .css file.
        :return: A string containing the CSS rules.
        """
        return self.rtf_read(path)

    def css_write(self, path: str, content: str, append: bool = False):
        """
        Writes a string to a CSS (.css) file. Supports appending or overwriting.

        :param path: Path to the .css file.
        :param content: CSS rules to write to the file.
        :param append: If True, appends content to the file. If False, overwrites the file.
        """
        self.rtf_write(path, content, append)

    def js_read(self, path: str) -> str:
        """
        Reads a JavaScript (.js) file and returns its content as a string.

        :param path: Path to the .js file.
        :return: A string containing the JavaScript code.
        """
        return self.rtf_read(path)

    def js_write(self, path: str, content: str, append: bool = False):
        """
        Writes a string to a JavaScript (.js) file. Supports appending or overwriting.

        :param path: Path to the .js file.
        :param content: JavaScript code to write to the file.
        :param append: If True, appends content to the file. If False, overwrites the file.
        """
        self.rtf_write(path, content, append)

    def js_run(self, path: str) -> str:
        """
        Executes a JavaScript (.js) file using Node.js and returns the output.

        :param path: Path to the .js file to execute.
        :return: The output of the executed JavaScript code.
        :raises RuntimeError: If the file does not exist or Node.js is not installed.
        """
        file_path = self._validate_and_prepare_path(path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        try:
            result = subprocess.run(['node', file_path], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error running JavaScript file {path}: {e.stderr}")

    def open_html(self, path: str, browser_name: Optional[str] = None):
        """
        Opens an HTML file in a specified or default web browser.
        
        :param path: Path to the HTML file.
        :param browser_name: Name of the web browser to use (e.g., 'chrome', 'firefox').
                            If None, opens in the default browser.
        """
        # Ensure the file exists
        file_path = self._validate_and_prepare_path(path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        # Convert path to URL format
        file_url = f"file://{file_path}"

        # Open in specified browser, or fallback to default if not available
        try:
            if browser_name:
                browser = webbrowser.get(browser_name)
                browser.open(file_url)
            else:
                webbrowser.open(file_url)
        except webbrowser.Error:
            print(f"Could not open the browser '{browser_name}'. Opening with the default browser instead.")
            webbrowser.open(file_url)

    def sql_execute(self, path: str, query: str, params: tuple = ()):
        """
        Executes an SQL query on a database file.
        
        :param path: Path to the .sql database file.
        :param query: SQL query to execute.
        :param params: Tuple of parameters for the query.
        :return: Query result for SELECT queries or confirmation of execution for other queries.
        """
        file_path = self._validate_and_prepare_path(path)
        
        with sqlite3.connect(file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                return f"Query executed successfully: {query}"

    def sql_create_table(self, path: str, table_name: str, columns: Dict[str, str]):
        """
        Creates a table in an SQL database.
        
        :param path: Path to the .sql database file.
        :param table_name: Name of the table to create.
        :param columns: Dictionary of column names and types.
        """
        cols = ", ".join([f"{col} {type_}" for col, type_ in columns.items()])
        self.sql_execute(path, f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")

    def sql_insert(self, path: str, table_name: str, data: Dict[str, Any]):
        """
        Inserts data into an SQL table.
        
        :param path: Path to the .sql database file.
        :param table_name: Name of the table to insert data into.
        :param data: Dictionary where keys are column names and values are data.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        self.sql_execute(path, f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

    def sql_query(self, path: str, query: str, params: tuple = ()):
        """
        Executes an SQL SELECT query and returns the results.
        
        :param path: Path to the .sql database file.
        :param query: SQL SELECT query to execute.
        :param params: Tuple of parameters for the query.
        :return: Results of the SELECT query.
        """
        return self.sql_execute(path, query, params)

    def handle_compressed(self, path: str, action: str, target: Optional[str] = None):
        """
        Handles compression and extraction of files in .zip, .rar, and similar formats.
        
        :param path: Path to the compressed file or directory.
        :param action: Either 'compress' to create an archive or 'extract' to extract files.
        :param target: Directory to extract files into, or name of the new archive.
        """
        file_path = self._validate_and_prepare_path(path)
        
        if action == 'compress':
            if not os.path.isdir(file_path):
                raise ValueError(f"The path {path} is not a directory.")
            archive_path = target if target else f"{file_path}.zip"
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        archive.write(full_path, arcname=os.path.relpath(full_path, file_path))
            print(f"Compressed to {archive_path}")

        elif action == 'extract':
            if not zipfile.is_zipfile(file_path):
                raise ValueError(f"The file {path} is not a valid compressed file.")
            target_dir = target if target else os.path.splitext(file_path)[0]
            with zipfile.ZipFile(file_path, 'r') as archive:
                archive.extractall(target_dir)
            print(f"Extracted to {target_dir}")
        else:
            raise ValueError("Invalid action. Choose either 'compress' or 'extract'.")