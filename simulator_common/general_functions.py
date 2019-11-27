import pandas as pd
# import xlrd
import os
import time
from datetime import timedelta, datetime
import math
import re
import json
import simulator_common.simulator_constants as sc
import simulator_common.general_functions as gf


def timing():
    """Use to show how long operations take, and provide status updates to user in the console."""
    start_time = time.time()
    return lambda x: print("[{:.2f}s] {}".format(time.time() - start_time, x))


def date_range(start_date, end_date):
    """Generator function that yields one day at a time in a date range"""
    if end_date < start_date:
        start_date, end_date = end_date, start_date

    for n in range(int((end_date - start_date).days) + 1):
        yield_date = start_date + timedelta(n)
        if yield_date.strftime('%a') == 'Sat' or yield_date.strftime('%a') == 'Sun':
            continue
        yield yield_date
