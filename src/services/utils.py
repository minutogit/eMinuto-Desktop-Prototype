# utils.py
import inspect
import json
import re
from datetime import datetime
import os, random, string

def get_version():
    """
    Reads the project version from the VERSION file.

    Returns:
        str: The version number or an error message if the file is not found.
    """
    try:
        # Determine the absolute path to the VERSION file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        version_file_path = os.path.join(base_dir, "../../VERSION")

        with open(version_file_path) as version_file:
            return version_file.read().strip()
    except FileNotFoundError:
        return "" # empty if Version file not found

def read_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string, or an empty string if the content
             cannot be read as text.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        # Logging the exception can be helpful for debugging
        print(f"Error reading file: {e}")
        return ""

def convert_json_string_to_dict(json_string):
    """
    Converts a JSON string to a Python dictionary.

    Args:
        json_string (str): The JSON string to convert.

    Returns:
        dict: The converted dictionary, or None if the conversion fails.
    """
    try:
        return json.loads(json_string)
    except ValueError as e:
        print(f"Error converting JSON string to dict: {e}")
        return None

def is_valid_object(obj):
    """
    Checks if the given object is a dictionary, a list, or a valid JSON string
    that represents a dictionary or a list. Needed for checking file content.

    Args:
        obj: The object to check. Can be a dict, a list, or a string.

    Returns:
        bool: True if the object is a dict, a list, or a valid JSON string representing a dict or a list,
              False otherwise.
    """
    # If obj is already a dict or list, return True
    if isinstance(obj, (dict, list)):
        return True

    # If obj is a string, try to parse it as JSON
    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
            return isinstance(parsed, (dict, list))
        except ValueError:
            return False

    # If obj is neither a dict, list, nor a string, return False
    return False

def random_string(length):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def get_timestamp(years_to_add=0, end_of_year=False):
    """
    Returns the current timestamp in ISO 8601 format in UTC.
    Optionally adds a number of years to the current timestamp.
    If end_of_year is True, sets the time to the end of that year.

    :param years_to_add: Optional number of years to add to the current date. Defaults to 0.
    :param end_of_year: If True, return the last moment of the current or future year. Defaults to False.
    :return: A string representing the timestamp in ISO 8601 format.
    """
    # Current time in UTC
    current_time = datetime.utcnow()

    # Add the specified number of years
    future_time = current_time.replace(year=current_time.year + years_to_add)

    # Set to the last moment of that year if end_of_year is True
    if end_of_year:
        future_time = future_time.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    return future_time.isoformat() + "Z"

def is_iso8601_datetime(string):
    """
    Checks if a string matches the ISO 8601 datetime format.
    :param string: The string to check.
    :return: True if the string is a valid ISO 8601 datetime, False otherwise.
    """
    iso8601_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$'
    return bool(re.match(iso8601_regex, string))

def get_years_valid(timestamp):
    """
    Calculates the number of years from the current time to the given timestamp.
    The result can be negative if the timestamp is in the past.

    Args:
        timestamp (str): The timestamp in ISO 8601 format in UTC.

    Returns:
        float: The number of years from now to the timestamp. Negative if the timestamp is in the past.
    """
    current_time = datetime.utcnow()
    timestamp_time = datetime.fromisoformat(timestamp.rstrip("Z"))

    # todo should be more accurate
    difference_in_years = (timestamp_time - current_time).total_seconds() / (365.25 * 24 * 60 * 60)
    return difference_in_years

def file_exists(folder, filename):
    file_path = os.path.join(folder, filename)
    return os.path.exists(file_path)

def join_path(*args):
    """
    Joins multiple directory components into a single path.

    Args:
        *args: A variable number of strings representing parts of the path.

    Returns:
        str: The full path created by joining all the given path components.
    """
    return os.path.join(*args)



def is_password_valid(password):
    """
    Check if the provided password meets the specified criteria.

    A valid password must meet the following conditions:
    - It must be at least 8 characters long.

    Args:
    password (str): The password string to be validated.

    Returns:
    bool: True if the password meets the criteria, False otherwise.
    """
    if len(password) < 8:
        return False
    return True

def amount_precision(amount, precision=2):
    """
    Determines the maximum precision (number of decimal places) of the specified amount.
    If the last two decimal places are zero, no decimal place is shown.

    :param amount: The floating-point number to be rounded.
    :param precision: The number of decimal places to round to. Default is 2.
    :return: The rounded number, formatted as a string.
    """
    rounded_amount = round(amount, precision)

    # Check if rounded amount is effectively an integer
    if rounded_amount == int(rounded_amount):
        return f"{int(rounded_amount)}"
    else:
        return f"{rounded_amount:.{precision}f}"


def display_balance(number):
    """
    Formats a float or integer number to a string with 2 decimal places, a comma as the decimal separator,
    and a space every three digits for better readability.

    Args:
        number (float or int): The number to be formatted.

    Returns:
        str: The formatted string.

    Raises:
        ValueError: If the input is not a float or integer.
    """
    if isinstance(number, (float, int)):
        # Round the number to 2 decimal places
        rounded_number = round(number, 2)

        # Convert the number to a string, replacing '.' with ','
        formatted_string = f"{rounded_number:.2f}".replace(".", ",")

        # Split the string into the integer and decimal parts
        integer_part, decimal_part = formatted_string.split(",")

        # Reverse the integer part to insert space every three digits
        reversed_integer = integer_part[::-1]
        spaced_integer = ' '.join(reversed_integer[i:i + 3] for i in range(0, len(reversed_integer), 3))

        # Reverse back and combine with the decimal part
        formatted_string = spaced_integer[::-1] + "," + decimal_part

        return formatted_string
    else:
        raise ValueError("The function accepts only float or int as input.")


def get_double_spending_vtransaction_ids(all_vouchers):
    """
    Extracts transaction IDs (t_id) from voucher transactions that have the same previous_hash and same sender_id
    across all provided vouchers, avoiding duplicates. If multiple t_ids have the same previous_hash and same sender_id
    it is evidence that double spending has occurred.

    Args:
    all_vouchers (list): A list of vouchers, each containing a list of transactions.

    Returns:
    list: A list of lists, where each inner list contains t_ids that share the same previous_hash.and the same sender_id
          Returns an empty list if no t_ids share the same previous_hash.
    """

    # Dictionary to group t_ids by previous_hash using sets to avoid duplicates
    hash_groups = {}

    # Iterate over each voucher and transaction
    for voucher in all_vouchers:
        for transaction in voucher.transactions:
            prev_hash = transaction['previous_hash']
            sender_id = transaction['sender_id']
            prev_hash_senders = prev_hash + sender_id
            t_id = transaction['t_id']
            hash_groups.setdefault(prev_hash_senders, set()).add(t_id)

    # Extract groups of t_ids with more than one element and convert each set to a list
    # This groups with 2 or more transactions are double spends!
    return [list(group) for group in hash_groups.values() if len(group) > 1]


class Serializable:
    """
    A base class that provides methods to convert an object to a dictionary and vice versa,
    facilitating JSON serialization and deserialization of objects derived from this class.

    The `to_dict` method converts the attributes of the class instance into a dictionary,
    excluding any private attributes (those starting with an underscore).
    This is useful for converting the object into a format that can be easily serialized into JSON.

    The `from_dict` class method creates a new instance of the class from a dictionary,
    typically used for deserializing a JSON object back into an instance of the class.
    It assumes that the dictionary keys correspond to the names of the arguments in the class constructor.
    """

    def to_dict(self):
        """
        Converts the attributes of the class into a dictionary.
        """
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    @classmethod
    def from_dict(cls, dict_):
        constructor_args = inspect.signature(cls.__init__).parameters
        relevant_data = {key: dict_[key] for key in dict_ if key in constructor_args}

        instance = cls(**relevant_data)
        for key, value in dict_.items():
            if key not in constructor_args:
                setattr(instance, key, value)

        return instance


def dprint(*args, sep=' ', end='\n'):
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the outer frame (where dprint is called)
    outer_frame = inspect.getouterframes(current_frame, 2)
    # Get the frame information
    frame_info = outer_frame[1]

    # Extracting file path and line number
    full_file_path = frame_info.filename
    line_number = frame_info.lineno

    # Get the current working directory (where the program was started)
    base_dir = os.getcwd()

    # Make the file path relative to the base directory
    # os.path.relpath() computes a relative filepath to the file from the current working directory.
    relative_file_path = os.path.relpath(full_file_path, base_dir)

    # Constructing the debug information with the relative file path
    debug_info = f"{relative_file_path}:{line_number}"
    print(debug_info) # Printing the debug information
    # followed by the original print content
    print(*args, sep=sep, end=end)
