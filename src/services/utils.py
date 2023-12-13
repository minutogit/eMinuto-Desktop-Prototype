# utils.py
import inspect
from datetime import datetime
import os

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

def file_exists(folder, filename):
    file_path = os.path.join(folder, filename)
    return os.path.exists(file_path)


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
        print("Relevante Daten für from_dict:", relevant_data)
        return cls(**relevant_data)


def dprint(*args, sep=' ', end='\n'):
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the outer frame (where dprint is called)
    outer_frame = inspect.getouterframes(current_frame, 2)
    # Get the frame information
    frame_info = outer_frame[1]

    # Extracting file name and line number
    file_name = frame_info.filename.split('/')[-1]
    line_number = frame_info.lineno

    # Constructing the debug information
    debug_info = f"{file_name}:{line_number} :"

    # Printing the debug information followed by the original print content
    print(debug_info, *args, sep=sep, end=end)
