import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import re

price_dict = {
    "Small set": 425,
    "Big set": 1236,
    "1cha pint": 309,
    "2cha pint": 309,
    "3cha pint": 309,
    "4cha pint": 309,
    "5cha pint": 469,
    "delivery": 150
}

def overall_orderdata(url_origi):
    url = url_origi[0:url_origi.find('edit')]+'export?format=xlsx'
    df = pd.read_excel(url,sheet_name = 0)
    return df

def detailed_orderdata(url_origi):
    url = url_origi[0:url_origi.find('edit')]+'export?format=xlsx'
    df = pd.read_excel(url,sheet_name = 1)
    df = df.dropna(subset=['Name'])
    df["Total Price"] = df["Order"].apply(lambda x: price_dict[x] if x == "Big set" else price_dict[x] + price_dict["delivery"])
    return df

def clean_address(address):
    if isinstance(address, str):
        # Find the last 5 characters that are digits
        match = re.search(r'(\d{1,5})\D*$', address)
        if match:
            return match.group(1).zfill(5)
    return "00000"

def format_address(address, max_line_length=34):
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

def create_image(address, postal_code, name, tel,folder):
    # Create a blank white image
    img = Image.open("ผู้รับ.png")
    
    # Initialize ImageDraw
    d = ImageDraw.Draw(img)
    # print(img.size)
    print(name)
    line_spacing = 15
    # Add text to the image
    d.text((1750,850), f"{name}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    d.text((1750,350), f"{format_tel_number(str(tel))}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    # d.text((800,1270), f"{format_address(address)}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 220), fill=(0, 0, 0))
    y = 1290
    for line in format_address(address).split('\n'):
        d.text((800, y), line, font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 200), fill=(0, 0, 0))
        y += 230 + line_spacing
    d.text((2150,2440), f"{str(postal_code)[0]}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    d.text((2650,2440), f"{str(postal_code)[1]}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    d.text((3150,2440), f"{str(postal_code)[2]}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    d.text((3650,2440), f"{str(postal_code)[3]}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    d.text((4150,2440), f"{str(postal_code)[4]}", font=ImageFont.truetype('EkkamaiNew-Regular.ttf', 250), fill=(0, 0, 0))
    
    # Save the image
    img.save(f"{folder}/{name}_address.png")