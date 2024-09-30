import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
import constants.constants as constants
import helpers.helpers as helpers
import logging

def calculate_order_price(row, price_dict):
    total_price = 0
    total_items = 0
    
    for item, price in price_dict.items():
        if item != "delivery":
            total_price += row[item] * price
            total_items += row[item]

    # Apply delivery fee rules
    if row["Big set"] > 0 or row["Small set"] >= 4:
        delivery_fee = 0
    else:
        delivery_fee = price_dict["delivery"]

    total_price += delivery_fee

    return total_price


def detailed_orderdata(url):
    # Load the content into a pandas DataFrame
    try:
        # Try to load the content into a pandas DataFrame
        df = pd.read_excel(BytesIO(url.content), sheet_name=1)
    except ValueError as e:
        logging.error(f"Error loading Excel file: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
    
    # Drop rows where 'Name' is missing
    df = df.dropna(subset=['Name'])
    
    # Apply your order price calculation
    df["Total Price"] = df.apply(calculate_order_price, axis=1, price_dict=constants.PRICE_DICT)
    
    # Filter by the current week and pickup status
    df = df[(df['Weeknum'] == helpers.current_weeknum()) & (df['pickup'] == False)]

    
    return df



def order(order_list):
    text = ""
    
    try:
        if int(order_list.get('Small set', 0)) > 0:
            text += "Small set: " + str(int(order_list['Small set'])) + "\n"
        if int(order_list.get('Big set', 0)) > 0:
            text += "Big set: " + str(int(order_list['Big set'])) + "\n"
        if int(order_list.get('1cha pint', 0)) > 0:
            text += "1cha pint: " + str(int(order_list['1cha pint'])) + "\n"
        if int(order_list.get('2cha pint', 0)) > 0:
            text += "2cha pint: " + str(int(order_list['2cha pint'])) + "\n"
        if int(order_list.get('3cha pint', 0)) > 0:
            text += "3cha pint: " + str(int(order_list['3cha pint'])) + "\n"
        if int(order_list.get('4cha pint', 0)) > 0:
            text += "4cha pint: " + str(int(order_list['4cha pint'])) + "\n"
        if int(order_list.get('5cha pint', 0)) > 0:
            text += "5cha pint: " + str(int(order_list['5cha pint'])) + "\n"
        if int(order_list.get('1cha 4oz', 0)) > 0:
            text += "1cha 4oz: " + str(int(order_list['1cha 4oz'])) + "\n"
        if int(order_list.get('2cha 4oz', 0)) > 0:
            text += "2cha 4oz: " + str(int(order_list['2cha 4oz'])) + "\n"
        if int(order_list.get('3cha 4oz', 0)) > 0:
            text += "3cha 4oz: " + str(int(order_list['3cha 4oz'])) + "\n"
        if int(order_list.get('4cha 4oz', 0)) > 0:
            text += "4cha 4oz: " + str(int(order_list['4cha 4oz'])) + "\n"
        if int(order_list.get('5cha 4oz', 0)) > 0:
            text += "5cha 4oz: " + str(int(order_list['5cha 4oz'])) + "\n"

    except KeyError as e:
        logging.error(f"Key error: {e} not found in order_list")
    
    return text

from PIL import Image, ImageDraw, ImageFont

def create_image(address, postal_code, name, tel, folder, row, app_path):
    try:
        # Load the base image
        img = Image.open(f"{app_path}/misc/chachacha_mail-05.png")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
        return

    text = order(row)
    print(f"{text} \n {name} \n")
 


    # Initialize ImageDraw
    d = ImageDraw.Draw(img)
    
    # Define constants for text positions and font size
    FONT_SIZE = 50
    LINE_SPACING = 33
    Y_START = 380

    try:
        # Add contact details to the image
        d.text((550, 158), helpers.format_tel_number(str(tel)), 
                font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), FONT_SIZE), fill=(0, 0, 0))
        d.text((400, 285), name, 
                font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), FONT_SIZE), fill=(0, 0, 0))

        # Add address to the image
        y = Y_START
        for liner, line in enumerate(helpers.format_address(address).split('\n')):
            x_position = (230, y) if liner == 0 else (150, y)
            d.text(x_position, line, 
                    font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), FONT_SIZE), fill=(0, 0, 0))
            y += 50 + LINE_SPACING

        # Add postal code
        for i, digit in enumerate(str(postal_code)):
            d.text((420 + i * 90, 710), digit, 
                    font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), FONT_SIZE), fill=(0, 0, 0))

        # Add order details
        d.text((400, 900), text, 
                font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), FONT_SIZE), fill=(0, 0, 0))

        # Save the image
        img.save(f"{folder}/{name}_address.png")
    except Exception as e:
        logging.error(f"Error while creating the image: {e}")






def create_pdf_from_images(image_directory, extra_image_path, temp_folder, output_pdf_path):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Get all image files from the directory
    try:
        image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
        image_files.sort()
    except Exception as e:
        logging.error(f"Error reading image directory '{image_directory}': {e}")
        return

    # Define page size and layout
    page_width, page_height = A4  # A4 size in points (1 point = 1/72 inch)
    image_width = page_width / 2   # Width of each image (2 images per row)
    image_height = page_height / 4  # Height of each image (4 rows)

    # Create a PDF canvas
    output_pdf_name = f"{output_pdf_path}_{str(helpers.current_weeknum())}.pdf"
    try:
        c = canvas.Canvas(output_pdf_name, pagesize=A4)
    except Exception as e:
        logging.error(f"Error creating PDF canvas: {e}")
        return

    # Ensure the temporary folder exists
    try:
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
    except Exception as e:
        logging.error(f"Error creating temporary folder '{temp_folder}': {e}")
        return

    # Initialize counters
    x = 0
    y = page_height - image_height
    count = 0

    for image_file in image_files:
        try:
            # Open the main image
            image_path = os.path.join(image_directory, image_file)
            with Image.open(image_path) as img:
                img = img.resize((int(image_width), int(image_height)), Image.LANCZOS)
                main_image_path = os.path.join(temp_folder, f"main_image_{count}.jpg")
                img.save(main_image_path, quality=99, subsampling=0)

            # Open and process the extra image
            with Image.open(extra_image_path) as extra_img:
                extra_img = extra_img.resize((int(image_width), int(image_height)), Image.LANCZOS)
                extra_image_path_temp = os.path.join(temp_folder, f"extra_image_{count}.jpg")
                extra_img.save(extra_image_path_temp, quality=95, subsampling=0)

            # Draw the main image and the extra image on the PDF
            # Position the images
            c.drawImage(extra_image_path_temp, x, y, width=image_width, height=image_height)
            c.drawImage(main_image_path, x, y - image_height, width=image_width, height=image_height)

            count += 1
            if count % 4 == 0:
                c.showPage()
                x = 0
                y = page_height - image_height
            else:
                x += image_width
                if count % 2 == 0:
                    x = 0
                    y -= 2 * image_height

            # Remove temporary image files after use
            os.remove(main_image_path)
            os.remove(extra_image_path_temp)

        except Exception as e:
            logging.error(f"Error processing image '{image_file}': {e}")
            continue  # Skip to the next image

    # Save the PDF
    try:
        c.save()
        logging.info(f"PDF saved successfully at: {output_pdf_name}")
    except Exception as e:
        logging.error(f"Error saving PDF: {e}")

    # Remove the temporary folder after all images are processed
    try:
        if os.path.isdir(temp_folder):
            os.rmdir(temp_folder)
    except Exception as e:
        logging.error(f"Error removing temporary folder '{temp_folder}': {e}")
