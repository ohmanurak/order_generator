import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import re
import function_order

detailed_df = function_order.detailed_orderdata("https://docs.google.com/spreadsheets/d/17l5TKof_ZlDisjIW7ZxN6no24UHKSDvL4EmhDjqyeMI/edit?usp=sharing")

detailed_df['postal_code'] = detailed_df['Address'].apply(function_order.clean_address)
detailed_df['Address'] = detailed_df.apply(lambda row: row['Address'].replace(row['postal_code'], '').strip() if row['postal_code'] != "00000" else row['Address'], axis=1)

folder = "Week_" + str(detailed_df.iloc[0]['Weeknum'])

if not os.path.isdir(folder):
        os.mkdir(folder)
# print(detailed_df)
for index, row in detailed_df.iterrows():
    function_order.create_image(row['Address'], row['postal_code'], row['Name'],row['Tel'],folder,row)



function_order.create_pdf_from_images(folder, "misc/sender.png",folder+"_temp", f'{folder}/Parcel_print')
