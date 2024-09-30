import re
from datetime import datetime,timedelta
import requests
import certifi
import sys, os
import logging

# formatters
def clean_address(address):
    if isinstance(address, str):
        # Find the last 5 characters that are digits
        match = re.search(r'(\d{1,5})\D*$', address)
        if match:
            return match.group(1).zfill(5)
    return "00000"

def format_address(address, max_line_length=38):
    address= str(address)
    words = address.split()
    formatted_address = ""
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_line_length:
            current_line += (" " if current_line else "") + word
        else:
            formatted_address += current_line + "\n"
            current_line = word

    formatted_address += current_line  # Add the last line
    return formatted_address

def format_tel_number(tel):
    # Extract all digits from the tel number
    digits = re.sub(r'\D', '', tel)
    
    # Ensure we have exactly 10 digits
    if len(digits) != 10:
        return "Invalid Number"
    
    # Format the digits into the desired pattern
    formatted_tel = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    return formatted_tel


def current_weeknum():
    # Get the current date
    current_date = datetime.now()
    
    # Adjust the date to make Tuesday the first day of the week
    adjusted_date = current_date - timedelta(days=(current_date.weekday() + 6) % 7)
    
    # Get the ISO calendar week number
    week_number = adjusted_date.isocalendar()[1]

    logging.info(week_number)
    
    return week_number
# connection tester

def verify_url(url_origi):
    try:
        url = url_origi.split('edit')[0] + 'export?format=xlsx'
        # Fetch the Excel file content over HTTPS using requests
        response = requests.get(url, verify=certifi.where())
        response.raise_for_status()  # Raise an exception for HTTP errors (like 404 or 500)
        
        return response
    except requests.exceptions.SSLError as e:
        raise ValueError(f"SSL error: {e}") from e
    except requests.exceptions.RequestException as e:
        raise ValueError(f"HTTP error: {e}") from e
    




    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)