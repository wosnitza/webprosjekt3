# This module contains the main exchange rates loading and returning functions. To be imported into
# every other module that needs exchange rates to run.

import simulator_common.general_functions as gf
import simulator_common.simulator_constants as sc
import glob
import os
import csv
import math
import pandas as pd
import datetime


def load_rates() -> 'DataFrame, Array, Dictionary':
    """Load all exchange rate .csv files from Path into an exchange rates DataFrame, array, and dictionary."""

    # Read data from all available .csv files
    t = gf.timing()
    try:
        # Windows path
        path = r'C:\Apps\Currency Extractor\rates-files-for-python'
        # Mac path:
        # path = r'/Users/bjorngyles/Desktop/Currency Extractor/rates-files-for-python'
        all_files = glob.glob(os.path.join(sc.PATH_TO_RATES_DATA, "*.csv"))
        rates_from_files = pd.concat(
            pd.read_csv(f, thousands=',', decimal='.', quoting=csv.QUOTE_MINIMAL) for f in
            all_files)  # rates now contains all rates tables in the csv files
        note = str(len(rates_from_files)) + ' historic exchange rates loaded from available .csv files...'
    except:
        note = 'Rates loading from available .csv files failed.'
        rates_from_files = 0

    # Filter data frame to only contain keys that look like EURNOK_2019-05-19
    rates_from_files = rates_from_files.set_index('ID').filter(regex='^[A-Z]{6}[_][0-9]{4}[-][0-9]{2}[-][0-9]{2}$',
                                                               axis=0).reset_index()

    # Convert data frame also into a dictionary as it is MUCH faster to access later on
    rates_dictionary = {str(k): float(str(v).replace(',', '')) for k, v in
                        zip(rates_from_files['ID'], rates_from_files['Price'])}

    # Update user
    t(note)

    return rates_from_files.CROSS.unique(), rates_dictionary


def load_limits() -> 'Dict':
    """Loads a pre-made limits file from the hard drive. To be used in the hedging simulation."""

    t = gf.timing()
    try:
        # Windows open path
        with open(sc.PATH_TO_LIMITS_DATA + r'\Limits.csv', mode='r') as limits_file:
        # Mac open path
        # with open(sc.PATH_TO_LIMITS_DATA + r'/Limits.csv', mode='r') as limits_file:
            reader = csv.reader(limits_file)
            limits = {rows[0]: rows[1] for rows in reader}
        t(str(len(limits)) + ' limits loaded from Limits.csv.')
    except:
        print('Limits loading from Limits.csv failed.')
        limits = 0

    return limits


def load_correlations() -> 'Dict':
    """Loads a pre-made correlations file from the hard drive. To be used in the hedging simulation."""

    t = gf.timing()
    try:
        path = r'C:\Apps\Currency Extractor\limit-files-for-python\Correlations.csv'
        # Mac path:
        # path = r'/Users/bjorngyles/Desktop/Currency Extractor/limit-files-for-python/Correlations.csv'
        with open(path, mode='r') as correlations_file:
            reader = csv.reader(correlations_file)
            correlations = {rows[0]: rows[1] for rows in reader}
        t(str(len(correlations)) + ' correlations loaded from Correlations.csv.')
    except:
        print('Correlations loading from Correlations.csv failed.')
        correlations = 0

    return correlations


# def exchange_rate_df(rates_df: 'DataFrame', cross: str, ref_date: 'date') -> 'Float':
#     """When given a DataFrame of all exchange rates, finds the rate we need. Includes building crosses via
#     a common leg."""
#
#     t = gf.timing()
#
#     # Trap when the cross is equal, hence result = 1
#     if cross[:3] == cross[-3:]:
#         return 1
#
#     # Set variables
#     one_day = datetime.timedelta(days=1)
#     available_crosses = rates_df.CROSS.unique()
#
#     # Check where and how I might find my cross in the rates table
#     if cross in available_crosses:
#         test_string_1 = cross + '_' + ref_date.strftime("%Y-%m-%d")
#         test_string_2 = False
#     elif cross[-3:] + cross[:3] in available_crosses:
#         test_string_1 = cross[-3:] + cross[:3] + '_' + ref_date.strftime("%Y-%m-%d")
#         test_string_2 = False
#     elif (sc.CROSS_BASE_LEG + cross[-3:] in available_crosses) and (
#             sc.CROSS_BASE_LEG + cross[:3] in available_crosses):
#         test_string_1 = sc.CROSS_BASE_LEG + cross[-3:] + '_' + ref_date.strftime("%Y-%m-%d")
#         test_string_2 = sc.CROSS_BASE_LEG + cross[:3] + '_' + ref_date.strftime("%Y-%m-%d")
#     else:
#         return 'Could not find exchange rate in internal database'
#
#     # Try a few times going back in case the date is on a Sun or Sat or rate entry is missing
#     attempts = 0
#
#     t('Before try')
#     while attempts < 10:
#         try:
#             test_string_1 = test_string_1[:7] + ref_date.strftime("%Y-%m-%d")
#             result = float(rates_df.loc[rates_df.loc[:, 'ID'] == test_string_1, 'Price'].head(1))
#             if test_string_2:
#                 test_string_2 = test_string_2[:7] + ref_date.strftime("%Y-%m-%d")
#                 result /= float(rates_df.loc[rates_df.loc[:, 'ID'] == test_string_2, 'Price'].head(1))
#             break
#         except:
#             ref_date -= one_day
#             attempts += 1
#             result = 'Could not find exchange rate in internal database for cross ' + cross
#
#     t('Exchange rate returned')
#     return result


def exchange_rate(cross: str, ref_date: 'date') -> 'Float':
    """When given a dictionary of all exchange rates, finds the rate we need. Includes building crosses via
    a common leg."""

    # Trap when the cross is equal, hence result = 1
    if cross[:3] == cross[-3:]:
        return 1

    # Set variables
    one_day = datetime.timedelta(days=1)

    # Check where and how I might find my cross in the rates table
    if cross in available_crosses:
        test_string_1 = cross + '_'
        test_string_2 = False
    elif cross[-3:] + cross[:3] in available_crosses:
        test_string_1 = cross[-3:] + cross[:3] + '_'
        test_string_2 = 'Invert'
    elif (sc.CROSS_BASE_LEG + cross[-3:] in available_crosses) and (
            sc.CROSS_BASE_LEG + cross[:3] in available_crosses):
        test_string_1 = sc.CROSS_BASE_LEG + cross[-3:] + '_'
        test_string_2 = sc.CROSS_BASE_LEG + cross[:3] + '_'
    else:
        return 'Could not find cross in internal database'

    # Try a few times going back in case the date is on a Sun or Sat or rate entry is missing
    attempts = 0

    while attempts < 10:
        try:
            test_string_1 = test_string_1[:7] + ref_date.strftime('%Y-%m-%d')
            result = rates_dict[test_string_1]
            if test_string_2 == 'Invert':
                result = 1 / rates_dict[test_string_1]
            elif test_string_2:
                test_string_2 = test_string_2[:7] + ref_date.strftime('%Y-%m-%d')
                result /= rates_dict[test_string_2]
            break
        except:
            ref_date -= one_day
            attempts += 1
            result = 0.0

    return result


def add_limits(limit_key: str) -> 'AddToDict':
    """When we find a cross in the input data for which we don't have protection limits available in the
    limits data, we 'infer' upper and lower limits by applying the cosine rule for volatility. We use limits
    across two known legs as input, and calculate the 3rd."""

    # Set variables to use in the formula
    correlation = float(correlations[sc.CROSS_BASE_LEG + limit_key[:3] + '-' + sc.CROSS_BASE_LEG + limit_key[3:6]])
    l1_up = float(limits[sc.CROSS_BASE_LEG + limit_key[:3] + limit_key[6:] + '-upper'])
    l2_up = float(limits[sc.CROSS_BASE_LEG + limit_key[3:6] + limit_key[6:] + '-upper'])
    l1_low = float(limits[sc.CROSS_BASE_LEG + limit_key[:3] + limit_key[6:] + '-lower'])
    l2_low = float(limits[sc.CROSS_BASE_LEG + limit_key[3:6] + limit_key[6:] + '-lower'])

    # Apply the formula to the variables
    la_up = math.sqrt(l1_up ** 2 + l2_up ** 2 - (2 * l1_up * l2_up * correlation))
    la_low = math.sqrt(l1_low ** 2 + l2_low ** 2 - (2 * l1_low * l2_low * correlation)) * -1

    # Add limits to the dataset
    limits[limit_key + '-upper'] = la_up
    limits[limit_key + '-lower'] = la_low

    return


def retrieve_limit(foreign_currency: str, accounting_currency: str, risk_window: int) -> float:
    if foreign_currency == accounting_currency:
        return 1
    limit_key = foreign_currency + accounting_currency + str(risk_window).zfill(3) + '-100'
    if limit_key + '-upper' not in limits:
        add_limits(limit_key)
    return 1 + max(abs(float(limits[limit_key + '-upper'])), abs(float(limits[limit_key + '-lower'])))


available_crosses, rates_dict = load_rates()
limits = load_limits()
correlations = load_correlations()
