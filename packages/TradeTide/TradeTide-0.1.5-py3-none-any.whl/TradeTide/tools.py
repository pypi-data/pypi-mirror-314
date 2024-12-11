#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from datetime import timedelta
from dateutil.relativedelta import relativedelta
import re
import numbers


def percent_to_float(string_value: str | float) -> float:
    """
    Converts a percentage string to a float.

    If the input is already a number, it returns the input as-is. If the input is a string formatted as a percentage
    (e.g., "50.5%"), it converts this string to a float representing the decimal form of the percentage (e.g., 0.505).

    Parameters:
        string_value (str or numbers.Number): The percentage string or a numeric value.

    Returns:
        float: The input percentage as a decimal if the input is a string, or the original numeric value if the input is a number.
    """
    if 'pip' in string_value.lower():
        pip_number = string_value.split('pip')
        return float(pip_number[0])

    if isinstance(string_value, numbers.Number):
        return string_value

    if '%' not in string_value:
        return float(string_value)

    else:
        return float(string_value.replace(',', '.')[:-1]) / 100


def parse_time_string_to_delta(time_string: str):
    # Regular expression to extract the number and the unit (days, months, etc.)
    match = re.match(r"(\d+)\s*(days?|months?|years?|weeks?|hours?|minutes?|seconds?)", time_string, re.I)
    if not match:
        raise ValueError("Invalid time string format.")

    quantity, unit = match.groups()
    quantity = int(quantity)

    # Convert to lowercase to standardize the unit
    unit = unit.lower()

    # Map the unit to a timedelta or relativedelta
    if unit in ['day', 'days']:
        return timedelta(days=quantity)
    elif unit in ['week', 'weeks']:
        return timedelta(weeks=quantity)
    elif unit in ['hour', 'hours']:
        return timedelta(hours=quantity)
    elif unit in ['minute', 'minutes']:
        return timedelta(minutes=quantity)
    elif unit in ['second', 'seconds']:
        return timedelta(seconds=quantity)
    elif unit in ['month', 'months']:
        return relativedelta(months=quantity)
    elif unit in ['year', 'years']:
        return relativedelta(years=quantity)
    else:
        raise ValueError("Unsupported time unit.")




class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None



class LinkedList:
    def __init__(self):
        self.head = None
        self.current = None  # This will be used for iteration

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if self.current:
            data = self.current.data
            self.current = self.current.next
            return data
        else:
            raise StopIteration

    def delete(self, key):
        cur_node = self.head
        if cur_node and cur_node.data == key:
            self.head = cur_node.next
            cur_node = None
            return
        prev = None
        while cur_node and cur_node.data != key:
            prev = cur_node
            cur_node = cur_node.next
        if cur_node is None:
            return
        prev.next = cur_node.next
        cur_node = None

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next



# -
