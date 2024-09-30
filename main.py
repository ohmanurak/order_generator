
import os
import function_order
import helpers.helpers as helpers
import os
from dotenv import load_dotenv
import sys
import logging
import constants.constants as constants
import time
def main(app_path):
    # # Load environment variables from .env file
    # extDataDir = os.getcwd()
    # if getattr(sys, 'frozen', False):
    #     extDataDir = sys._MEIPASS
    # load_dotenv(dotenv_path=os.path.join(app_path, '.env'))
    # sheet_url = helpers.verify_url(os.getenv("SHEET_URL"))
    sheet_url = helpers.verify_url(constants.SHEET_URL)


    detailed_df = function_order.detailed_orderdata(sheet_url)

    detailed_df['postal_code'] = detailed_df['Address'].apply(function_order.helpers.clean_address)
    detailed_df['Address'] = detailed_df.apply(lambda row: row['Address'].replace(row['postal_code'], '').strip() if row['postal_code'] != "00000" else row['Address'], axis=1)

    folder = f'{app_path}/Week_' + str(detailed_df.iloc[0]['Weeknum'])

    if not os.path.isdir(folder):
            os.mkdir(folder)
    # print(detailed_df)
    for index, row in detailed_df.iterrows():
        function_order.create_image(row['Address'], row['postal_code'], row['Name'],row['Tel'],folder,row,app_path)


    function_order.create_pdf_from_images(folder, f'{app_path}/misc/sender.png',folder+'_temp', f'{folder}/Parcel_print')
        

if __name__ == "__main__":

    if getattr(sys, 'frozen', False):
        print('EHH?')
        application_path = sys._MEIPASS
    else:
        print('AHH?')
        application_path = os.path.dirname(os.path.abspath(__file__))
    print("!@", application_path)
    logging.debug(application_path)	
    main(application_path)