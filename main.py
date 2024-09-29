import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import function_order
import helpers.helpers as helpers
import os
from dotenv import load_dotenv
def main():
    # Load environment variables from .env file
    load_dotenv()

    sheet_url = helpers.verify_url(os.getenv("SHEET_URL"))

    detailed_df = function_order.detailed_orderdata(sheet_url)

    detailed_df['postal_code'] = detailed_df['Address'].apply(function_order.helpers.clean_address)
    detailed_df['Address'] = detailed_df.apply(lambda row: row['Address'].replace(row['postal_code'], '').strip() if row['postal_code'] != "00000" else row['Address'], axis=1)

    folder = "Week_" + str(detailed_df.iloc[0]['Weeknum'])

    if not os.path.isdir(folder):
            os.mkdir(folder)
    # print(detailed_df)
    for index, row in detailed_df.iterrows():
        function_order.create_image(row['Address'], row['postal_code'], row['Name'],row['Tel'],folder,row)


    function_order.create_pdf_from_images(folder, "misc/sender.png",folder+"_temp", f'{folder}/Parcel_print')
        

if __name__ == "__main__":
    main()

