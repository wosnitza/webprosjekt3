import pandas as pd
# import xlrd
import os
import time
from datetime import timedelta, datetime
import math
import re
import json
import simulator_common.simulator_constants as sc


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


def average(x):
    """User defined averaging function used in the Pearson correlation. Returns the average across
    a list of items."""
    assert len(x) > 0
    return float(sum(x)) / len(x)


def pearson_def(x, y) -> float:
    """Pearson correlation between 2 series that need to be of equal size and date-synchronised items."""
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


def read_from_clipboard(date_columns='nan') -> 'DataFrame':
    """Using the Pandas framework, copy the table that is in the clipboard, into a data frame, and
    return that data frame. If the user provides a list of date column headers, Python will
    automatically (try to) interpret the dates in that column into datetime format."""

    # try:
    if date_columns == 'nan' or date_columns == '':
        clipboard_table = pd.read_clipboard()
    else:
        try:
            clipboard_table = pd.read_clipboard(parse_dates=date_columns, dayfirst=True)
        except:
            clipboard_table = pd.read_clipboard()
            print('Tried to parse dates, but the date_columns given may not exist.')

    if clipboard_table.size == 0 or clipboard_table.empty:
        clipboard_table = 'Clipboard is empty. Select an Excel table and try again.'
    else:
        print(clipboard_table.size, 'items imported from clipboard...')
    # except:
    #    clipboard_table = 'No clipboard contents found. Select an Excel table and try again.'

    return clipboard_table


def read_from_excel_file(file_name: str, worksheet_name: str, folder='downloads') -> 'DataFrame':
    """Reads the most recently changed excel file from selected folder with selected word in filename."""

    t = timing()
    # Set the folder. Allow user to specify 'Downloads' or 'Master'
    if folder.lower() == 'downloads':
        search_dir = r'C:\Users\Derek\Downloads'
    elif folder.lower() == 'master':
        search_dir = r'G:\My Drive\2. Development\Master Loops Files'
    else:
        search_dir = folder

    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files if
             ('.xlsx' in f or '.xlsm' in f) and file_name in f and not '~$' in f]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    dfs = pd.read_excel(files[0], sheet_name=worksheet_name)
    t('Worksheet ' + worksheet_name + ' imported from ' + files[0])

    return dfs

    # dfs = pd.DataFrame()
    # for i in range(1):
    #     dfs.append(pd.read_csv(files[i].split('\\')[-1], delimiter=','))


def normalise(payment_term: int) -> int:
    if payment_term < 11:
        result = 7
    elif payment_term < 18:
        result = 14
    elif payment_term < 26:
        result = 21
    elif payment_term < 38:
        result = 30
    elif payment_term < 53:
        result = 45
    elif payment_term < 75:
        result = 60
    elif payment_term < 95:
        result = 90
    elif payment_term < 140:
        result = 100
    elif payment_term < 225:
        result = 180
    elif payment_term < 318:
        result = 270
    else:
        result = 365

    return result


def normalise_terms(start_date: 'date', end_date: 'date', as_string=False) -> 'Various':
    if as_string:
        return str(normalise((end_date - start_date).days)).zfill(3)
    else:
        return normalise((end_date - start_date).days)


def convert_excel_amount(amount: 'Any', factor=1.0, keep_strings=False) -> float:
    """Converts number formats, also if a negative number is shown in parentheses ()."""

    if keep_strings:
        try:
            if amount.replace('-', '').split()[0].isalpha():
                return amount
        except:
            pass

    if '(' in str(amount):
        amount = float(str(amount).replace(',', '').replace('(', '').replace(')', '').replace(' ', '')) * -1
    else:
        try:
            amount = float(str(amount).replace(',', '').replace(' ', ''))
        except:
            amount = 0.0

    return amount * factor


def convert_excel_date(date: 'Any') -> 'datetime.date':
    """Checks whether date is a string or a date. If string, parse using %Y-%m-%d."""

    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    else:
        date = date

    return date


def fibonacci(n: int) -> int:
    return ((1 + math.sqrt(5)) ** n - (1 - math.sqrt(5)) ** n) / (2 ** n * math.sqrt(5))


def to_filename(name: str, extension='.txt') -> str:
    company_name = re.sub(r'[^\sa-zA-Z0-9]', '', name.replace('&', ' ')).lower().strip().replace(' ', '_')
    return company_name + extension


def load_from_clipboard_or_file(date_columns: 'List', amount_columns: 'List', required_columns: 'List',
                                optional_columns=None) -> 'Source: str, Dataframe':
    # Load either clipboard contents or file contents into a DataFrame. Uses global constants for now.
    # To be expanded with a reference to a customer name.

    t = timing()
    status = 'OK'

    try:
        input_table = read_from_clipboard(date_columns)
        loaded_from_clipboard = True
    except:
        loaded_from_clipboard = False

    if loaded_from_clipboard:
        try:
            try:
                try_columns = set.intersection(set(input_table.columns.values.tolist()), set(optional_columns))
                input_table = input_table[required_columns + list(try_columns)]
            except:
                input_table = input_table[required_columns]
        except:
            loaded_from_clipboard = False

    if not loaded_from_clipboard:
        try:
            input_table = read_from_excel_file(sc.ACCOUNTS_PAYABLE_SOURCE_DATA_WORKBOOK_WORDS,
                                               sc.ACCOUNTS_PAYABLE_SOURCE_DATA_WORKSHEET_WORDS,
                                               sc.PATH_TO_CUSTOMER_DATA + sc.CUSTOMER_FOLDER_NAME)
            try:
                try_columns = set.intersection(set(input_table.columns.values.tolist()), set(optional_columns))
                input_table = input_table[required_columns + list(try_columns)]
            except:
                input_table = input_table[required_columns]
        except:
            status = 'Neither the clipboard nor the customer data file and worksheet contain the data needed.'
            return None, None, status

    for amount_column in amount_columns:
        try:
            input_table[amount_column] = input_table[amount_column].apply(lambda x: convert_excel_amount(x, 1.0))
        except:
            continue

    source = 'clipboard' if loaded_from_clipboard else 'file'
    t('Data loaded from ' + source)

    return source, input_table, status


def generate_date_dimension(start='2010-01-01', end='2025-12-31') -> 'Dataframe to Clipboard':
    """Generates a dates dimension table that can be copied into a PowerBI file."""
    df = pd.DataFrame({'Date': pd.date_range(start, end)})
    df['Date_ID'] = df.Date.dt.strftime('%Y-%m-%d')
    df['Day'] = df.Date.dt.weekday_name
    df['Week'] = df.Date.dt.weekofyear
    df['Month'] = df.Date.dt.month
    df['Month_Short'] = df.Date.dt.strftime('%b')
    df['Month_Long'] = df.Date.dt.strftime('%B')
    df['Quarter'] = df.Date.dt.quarter
    df['Year'] = df.Date.dt.year
    df['Year_Half'] = (df.Quarter + 1) // 2
    df['Year_Month'] = df.Date.dt.strftime('%Y-%m')
    df['Year_Quarter'] = df.Date.dt.year.astype(str) + '-Q' + df.Date.dt.quarter.astype(str)

    return df


def pretty_write_json(path: str) -> 'Updated JSON File':
    """Rewrites an existing JSON file into a more readable format."""

    # company_name = gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-pnl_summary.json')

    with open(path, 'r+') as f:
        data = json.load(f)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    return

