# utils.py
import copy
import random
import string
import json
from src.services.utils import dprint

def modify_char(char):
    """ Modifies a character to a different character of the same type (digit, letter, punctuation). """
    while True:
        if char.isdigit():
            new_char = random.choice(string.digits.replace(char, ''))
        elif char.isalpha():
            new_char = random.choice(string.ascii_letters.replace(char, ''))
        else:
            new_char = random.choice(string.punctuation.replace(char, ''))
        if new_char != char:
            break

    return new_char

def modify_value(value):
    """ Modifies a single character in a given value to ensure the modified value is different from the original. """
    value = str(value)
    if len(value) > 0:
        index_to_change = random.randint(0, len(value) - 1)
        char_to_replace = value[index_to_change]
        new_char = modify_char(char_to_replace)
        new_value = value[:index_to_change] + new_char + value[index_to_change + 1:]
        return new_value
    return value

def v_modify_voucher(input_dict):
    """ Modifies a randomly chosen item in the dictionary except for 'guarantor_signatures' and 'transactions' keys. """
    keys_to_modify = [key for key in input_dict if key not in ['guarantor_signatures', 'transactions']]
    if not keys_to_modify:
        return input_dict  # Return original dict if no keys to modify

    key_to_modify = random.choice(keys_to_modify)
    input_dict[key_to_modify] = modify_value(str(input_dict[key_to_modify]))

    return input_dict

def v_modify_guarantor(input_dict):
    """ Modifies a randomly chosen item within 'guarantor_signatures' key of the dictionary. """
    if 'guarantor_signatures' in input_dict and input_dict['guarantor_signatures']:
        rand_guarantor_index = random.randint(0, len(input_dict['guarantor_signatures']) - 1)
        guarantor_signature_pair = input_dict['guarantor_signatures'][rand_guarantor_index]

        rand_element_index = random.randint(0, len(guarantor_signature_pair) - 1)
        selected_element = guarantor_signature_pair[rand_element_index]

        if isinstance(selected_element, dict):
            rand_key = random.choice(list(selected_element.keys()))
            selected_element[rand_key] = modify_value(selected_element[rand_key])
        else:
            guarantor_signature_pair[rand_element_index] = modify_value(selected_element)

    return input_dict

def v_modify_transaction(input_dict):
    """ Modifies a randomly chosen item within 'transactions' key of the dictionary. """
    if 'transactions' in input_dict and input_dict['transactions']:
        rand_transaction_index = random.randint(0, len(input_dict['transactions']) - 1)
        transaction_keys = list(input_dict['transactions'][rand_transaction_index].keys())
        if transaction_keys:
            rand_key = random.choice(transaction_keys)
            input_dict['transactions'][rand_transaction_index][rand_key] = \
                modify_value(input_dict['transactions'][rand_transaction_index][rand_key])

    return input_dict

def v_modify_all(input_dict):
    """ Randomly modifies a character in the JSON representation of the dictionary. """
    original_dict_str = json.dumps(input_dict, indent=4)

    while True:
        lines = original_dict_str.split('\n')
        rand_line_index = random.randint(0, len(lines) - 1)
        line_to_modify = lines[rand_line_index]

        if line_to_modify:
            index_to_change = random.randint(0, len(line_to_modify) - 1)
            char_to_replace = line_to_modify[index_to_change]
            modified_char = modify_char(char_to_replace)

            modified_line = line_to_modify[:index_to_change] + modified_char + line_to_modify[index_to_change + 1:]
            lines[rand_line_index] = modified_line
            modified_str = '\n'.join(lines)

        try:
            modified_dict = json.loads(modified_str)
            if modified_dict != input_dict:
                break
        except json.JSONDecodeError:
            continue

    return modified_dict


def compare_and_highlight_differences(original_json, modified_json):
    """ Compares two JSON strings line by line, highlighting differences. """
    original_lines = original_json.splitlines()
    modified_lines = modified_json.splitlines()

    if modified_json == original_json:
        print("No differences found.")

    for orig_line, mod_line in zip(original_lines, modified_lines):
        if orig_line != mod_line:
            highlighted_changes = "".join(["#" if char != orig_char else "_"
                                           for char, orig_char in zip(mod_line, orig_line)])
            print("Original: ", orig_line)
            print("Diff    : ", highlighted_changes)
            print("Modified: ", mod_line)
            print()

def modify_voucher(input_dict, mode=None, print_info=False):
    """ Modifies the content of a voucher to test if the verification detects the modification or corrupted voucher.

    Available modes: 'voucher', 'guarantor', 'transactions', 'all'.
    """
    if isinstance(input_dict, str):
        try:
            input_dict = json.loads(input_dict)
        except json.JSONDecodeError:
            return input_dict

    modified_dict = copy.deepcopy(input_dict)

    if mode == "voucher":
        modified_dict = v_modify_voucher(modified_dict)
    elif mode == "guarantor":
        modified_dict = v_modify_guarantor(modified_dict)
    elif mode == "transactions":
        modified_dict = v_modify_transaction(modified_dict)
    elif mode == "all":
        modified_dict = v_modify_all(modified_dict)

    original_json = json.dumps(input_dict, indent=4)
    modified_json = json.dumps(modified_dict, indent=4)

    if print_info:
        print("Comparing and highlighting differences:")
        compare_and_highlight_differences(original_json, modified_json)

    return modified_json
