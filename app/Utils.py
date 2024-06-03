import nepali_datetime, datetime
from dateutil.relativedelta import *
from Constants import *
from Utils import *
import os

# file_path_prefix = os.environ['USERPROFILE']
# email_list_filepath = rf"{file_path_prefix}/Documents/QuickFox/email_list.txt"


# def get_nepali_date_obj():
#     nepali_date = nepali_datetime.date.today().replace(day=1)
#     nepali_date = nepali_date-datetime.timedelta(days=1)
#     return nepali_date

# def get_english_date_obj():
#     english_date = datetime.date.today().replace(day=1)
#     english_date = english_date-datetime.timedelta(days=1)
#     return english_date

# def get_first_quarter():
#     english_date = datetime.date.today().replace(day=1)
#     english_date = english_date-datetime.timedelta(days=20)
#     return english_date

# def get_second_quarter():
#     english_date = datetime.date.today().replace(day=1)
#     english_date = english_date-datetime.timedelta(days=10)
#     return english_date


def input_text(text, desktop, enter=False):
    for x in text:
        if x in "!@#$%^&*()":
            desktop.type_text(x, enter=False)
        elif x == ' ':
            desktop.press_keys('space')
        else:
            desktop.press_keys(x)
            
    if enter:
        desktop.press_keys('enter')

