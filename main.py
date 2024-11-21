
import os
import function_order
import helpers.helpers as helpers
import os
from dotenv import load_dotenv
import sys
import constants.constants as constants

import os
import logging
import pandas as pd  # Assuming pandas is used for DataFrame operations

def main(app_path):
    # Ensure logging is set up
    logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
    try:
        # URL verification
        try:
            sheet_response = helpers.verify_url(constants.SHEET_URL)
            sheet_url = sheet_response.url  # Assuming you need the URL; adjust as necessary
            if not sheet_url:
                raise ValueError("Invalid or empty sheet URL")
        except Exception as e:
            logging.error(f"Error verifying URL: {e}")
            return  # Exit the function if the URL is invalid
        
        # Fetch detailed order data
        try:
            detailed_df = function_order.detailed_orderdata(sheet_response)
            if detailed_df.empty:
                raise ValueError("Detailed order data is empty")
        except Exception as e:
            logging.error(f"Error fetching order data: {e}")
            return

        # Clean address and postal code
        try:
            detailed_df['postal_code'] = detailed_df['Address'].apply(function_order.helpers.clean_address)
        except Exception as e:
            logging.error(f"Error cleaning addresses: {e}")
            return

        try:
            detailed_df['Address'] = detailed_df.apply(
                lambda row: row['Address'].replace(row['postal_code'], '').strip() 
                if row['postal_code'] != "00000" else row['Address'], 
                axis=1
            )
        except Exception as e:
            logging.error(f"Error processing address: {e}")
            return

        # Validate 'Weeknum' column existence and type
        if 'Weeknum' not in detailed_df.columns:
            logging.error("Column 'Weeknum' is missing from the data")
            return

        try:
            week_num = int(detailed_df.iloc[0]['Weeknum'])
        except (ValueError, TypeError) as e:
            logging.error(f"Invalid Weeknum value: {e}")
            return

        folder = os.path.join(app_path, f'Week_{week_num}')

        # Create folder if it doesn't exist
        try:
            if not os.path.isdir(folder):
                os.makedirs(folder, exist_ok=True)  # Use makedirs to create intermediate directories if needed
        except OSError as e:
            logging.error(f"Error creating folder {folder}: {e}")
            return

        # Iterate through rows and create images
        for _, row in detailed_df.iterrows():
            try:
                function_order.create_image(
                    row['Address'], 
                    row['postal_code'], 
                    row['Name'], 
                    row['Tel'], 
                    folder, 
                    row, 
                    app_path
                )
            except Exception as e:
                logging.error(f"Error creating image for {row.get('Name', 'Unknown')} at {row.get('Address', 'Unknown')}: {e}")
                continue  # Continue to the next row even if one row fails

        # Create PDF from images
        try:
            sender_image_path = os.path.join(app_path, 'misc', 'sender.png')
            temp_folder = f"{folder}_temp"
            parcel_print_folder = os.path.join(folder, 'Parcel_print')
            function_order.create_pdf_from_images(folder, sender_image_path, temp_folder, parcel_print_folder)
        except Exception as e:
            logging.error(f"Error creating PDF from images: {e}")
            return

    except Exception as e:
        logging.error(f"An unexpected error occurred in main: {e}")
        

if __name__ == "__main__":
    # is run from exe
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    # is run from python main.py
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    main(application_path)