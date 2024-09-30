import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
import constants.constants as constants
import helpers.helpers as helpers

def overall_orderdata(url):
    df = pd.read_excel(url,sheet_name = 0)
    return df
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
    df = pd.read_excel(BytesIO(url.content), sheet_name=1)
    
    # Drop rows where 'Name' is missing
    df = df.dropna(subset=['Name'])
    
    # Apply your order price calculation
    df["Total Price"] = df.apply(calculate_order_price, axis=1, price_dict=constants.PRICE_DICT)
    
    # Filter by the current week and pickup status
    df = df[df['Weeknum'] == helpers.current_weeknum()] 
    df = df[df['pickup'] == False]
    
    return df



def order(order_list):
    text = ""
    if int(order_list['Small set'])>0:
        # print("Small set:",order_list['Small set'])
        text += "Small set: "+str(int(order_list['Small set']))+"\n"
    if int(order_list['Big set'])>0:
        # print("Big set:",order_list['Big set'])
        text += "Big set: "+str(int(order_list['Big set']))+"\n"
    if int(order_list['1cha pint'])>0:
        # print("1cha pint:",order_list['1cha pint'])
        text += "1cha pint: "+str(int(order_list['1cha pint']))+"\n"
    if int(order_list['2cha pint'])>0:
        # print("2cha pint:",order_list['2cha pint'])
        text += "2cha pint: "+str(int(order_list['2cha pint']))+"\n"
    if int(order_list['3cha pint'])>0:
        # print("3cha pint:",order_list['3cha pint'])
        text += "3cha pint: "+str(int(order_list['3cha pint']))+"\n"
    if int(order_list['4cha pint'])>0:
        # print("4cha pint:",order_list['4cha pint'])
        text += "4cha pint: "+str(int(order_list['4cha pint']))+"\n"
    if int(order_list['5cha pint'])>0:
        # print("5cha pint:",order_list['5cha pint'])
        text += "5cha pint: "+str(int(order_list['5cha pint']))+"\n"
    if int(order_list['1cha 4oz'])>0:
        # print("1cha 4oz:",order_list['1cha 4oz'])
        text += "1cha 4oz: "+str(int(order_list['1cha 4oz']))+"\n"
    if int(order_list['2cha 4oz'])>0:
        # print("2cha 4oz:",order_list['2cha 4oz'])
        text += "2cha 4oz: "+str(int(order_list['2cha 4oz']))+"\n"
    if int(order_list['3cha 4oz'])>0:
        # print("3cha 4oz:",order_list['3cha 4oz'])
        text += "3cha 4oz: "+str(int(order_list['3cha 4oz']))+"\n"
    if int(order_list['4cha 4oz'])>0:
        # print("4cha 4oz:",order_list['4cha 4oz'])
        text += "4cha 4oz: "+str(int(order_list['4cha 4oz']))+"\n"
    if int(order_list['5cha 4oz'])>0:
        # print("5cha 4oz:",order_list['5cha 4oz'])
        text += "5cha 4oz: "+str(int(order_list['5cha 4oz']))+"\n"
    return text
def create_image(address, postal_code, name, tel,folder,row,app_path):
    # Create a blank white image
    img = Image.open(f"{app_path}/misc/chachacha_mail-05.png")
    text = order(row)
    print(text)
    # Initialize ImageDraw
    d = ImageDraw.Draw(img)
    # print(img.size)
    print(name)
    line_spacing = 33
    # Add text to the image
    print(helpers.resource_path(constants.EKKAMAI_FONT_PATH))
    d.text((550,158), f"{helpers.format_tel_number(str(tel))}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((400,285), f"{name}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    
    # d.text((800,1270), f"{format_address(address)}", font=ImageFont.truetype(constants.EKKAMAI_FONT_PATH, 220), fill=(0, 0, 0))
    y = 380
    liner = 0
    for line in helpers.format_address(address).split('\n'):
        if liner==0:
            d.text((150, y), "      "+line, font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
            y += 50 + line_spacing
        else:
            d.text((150, y), line, font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
            y += 50 + line_spacing
        liner+=1
    d.text((420,710), f"{str(postal_code)[0]}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((510,710), f"{str(postal_code)[1]}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((600,710), f"{str(postal_code)[2]}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((690,710), f"{str(postal_code)[3]}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((780,710), f"{str(postal_code)[4]}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    d.text((400,900), f"{text}", font=ImageFont.truetype(helpers.resource_path(constants.EKKAMAI_FONT_PATH), 50), fill=(0, 0, 0))
    # Save the image
    img.save(f"../../{folder}/{name}_address.png")


def create_pdf_from_images(image_directory, extra_image_path, temp_folder, output_pdf_path):
    # Get all image files from the directory
    image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    
    # Sort the files to maintain a consistent order
    image_files.sort()

    # Define page size and layout
    page_width, page_height = A4
    image_width = page_width / 2
    image_height = page_height / 4
    extra_height = page_height / 4

    # Create a PDF canvas
    c = canvas.Canvas(output_pdf_path+"_"+str(helpers.current_weeknum())+".pdf", pagesize=A4)

    # Initialize counters
    x = 0
    y = page_height - image_height
    count = 0

    # Ensure the temporary folder exists
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    for image_file in image_files:
        # Open the main image
        image_path = os.path.join(image_directory, image_file)
        with Image.open(image_path) as img:
            # Rotate the image 90 degrees clockwise
            # img = img.rotate(-90, expand=True)
            
            # Resize image to fit within the specified dimensions with high-quality resampling
            img = img.resize((int(image_width), int(image_height)), Image.LANCZOS)
            
            # Save the resized image to a temporary file with a unique name
            main_image_path = os.path.join(temp_folder, f"main_image_{count}.jpg")
            img.save(main_image_path, quality=99, subsampling=0)  # Save with high quality

        # Open and process the extra image
        with Image.open(extra_image_path) as extra_img:
            # Rotate the extra image 90 degrees clockwise
            # extra_img = extra_img.rotate(-90, expand=True)
            
            # Resize the extra image to fit within the specified dimensions with high-quality resampling
            extra_img = extra_img.resize((int(image_width), int(image_height)), Image.LANCZOS)
            
            # Save the resized extra image to a temporary file with a unique name
            extra_image_path_temp = os.path.join(temp_folder, f"extra_image_{count}.jpg")
            extra_img.save(extra_image_path_temp, quality=95, subsampling=0)  # Save with high quality

        # Draw the main image and the extra image on the PDF
        c.drawImage(extra_image_path_temp, x , y, width=image_width, height=image_height)
        c.drawImage(main_image_path, x, y- image_height, width=image_width, height=extra_height)
        
        count +=1
        if count % 4 == 0:
            c.showPage()
            x = 0
            y = page_height - image_height
        else:
            x+= image_width
            if count % 2 == 0:
                x = 0
                y = y- 2*image_height
        # Update positions
        # count += 2
        # if count % 8 == 0:
        #     c.showPage()  # Add a new page after every 4 pairs of images (8 images)
        #     x = 0
        #     y = page_height - image_height
        # else:
        #     x +=  image_width  # Move to the next pair of images
        #     if count % 4 == 0:
        #         x = 0
        #         y -= image_height

        # Remove temporary image files after use
        os.remove(main_image_path)
        os.remove(extra_image_path_temp)

    # Save the PDF
    c.save()

    # Remove the temporary folder after all images are processed
    if os.path.isdir(temp_folder):
        os.rmdir(temp_folder)