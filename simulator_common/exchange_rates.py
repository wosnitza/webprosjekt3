<<<<<<< HEAD
"""This module takes some statistics around revenue and cost, and currency distribution in, and generates
a table for the exposure charts and matrix.
Other statistics can be extracted (manually?) from the accounts payable and receivable invoice files."""
=======
<<<<<<< HEAD
# This module contains the main exchange rates loading and returning functions. To be imported into
# every other module that needs exchange rates to run.
>>>>>>> master

import numpy as np
import pandas as pd
import simulator_common.simulator_constants as sc
import simulator_common.general_functions as gf
import simulator_common.exchange_rates as er
import simulator_utils.create_company as cc
import simulator_utils.interpret_pnl_from_clipboard as ipc
import simulator_utils.interpret_currency_distribution as icd
import main_workflows.straight_conversion as conv
import json
from datetime import timedelta, date
import pprint

# MAKE SURE TO FILL IN THE RIGHT COMPANY DETAILS IN sc.simulator_constants....

# 'Scale' or 'Fill with Accounting Currency': how to close gap between cost data and P&L

FILL_COST_GAPS = {'2014': 'Fill',
                  '2015': 'Fill',
                  '2016': 'Scale',
                  '2017': 'Scale',
                  '2018': 'Scale'}


def account_available(currency: str) -> int:
    """Generates a 'sign' for how to deal with the amount later in the exposure calculation."""
    if currency in sc.AVAILABLE_CURRENCY_ACCOUNTS:
        return -1
    else:
        return 1


def generate_mock_company(company, sales, procurement, net_income):
    # Set up a fictional company with a list of invoices according to certain statistics
    # company, sales, procurement, net_income = cc.set_up_company(cc.EXAMPLE_COMPANY)

    # Concatenate all sales and procurement datasets across all years
    proc_dataset = [v for k, v in procurement.items()]
    sales_dataset = [v for k, v in sales.items()]
    print("start")
    print(proc_dataset)
    print(sales_dataset)
    print("end")
    # Merge all lists of datasets into one set
    combined_set = pd.concat([pd.concat(proc_dataset, ignore_index=True), pd.concat(sales_dataset, ignore_index=True)],
                             ignore_index=True)

    # Add a few rows of net income to the procurement dataset so it it taken in as well
    for year in sc.YEARS:
        netinc_row = [net_income[int(year)],
                      sc.ACCOUNTING_CURRENCY,
                      date(int(year), 1, 1),
                      date(int(year), 1, 30),
                      sc.PNL_CATEGORIES[-1],
                      sc.ACCOUNTING_CURRENCY,
                      net_income[int(year)],
                      net_income[int(year)],
                      1.0]
        combined_set.loc[len(combined_set.index)] = netinc_row

    # Convert the dates columns to be datetime
    combined_set['Invoice_Date'] = pd.to_datetime(combined_set['Invoice_Date'])
    combined_set['Due_Date'] = pd.to_datetime(combined_set['Due_Date'])

    print("start")
    print(combined_set)
    print("end")

    # Now summarise this large dataframe into the format that we would have pasted from proff.no
    summary = ipc.pnl_from_generator(combined_set)
    summary_df = pd.DataFrame.from_dict(summary, orient='columns')

    # And convert to the pnl_distribution and yoy_growth like normal
    pnl_distribution, yoy_growth_dict = ipc.render_pnl_distribution(summary_df)

    # Store a two-column map of the results into a dataframe and export it to clipboard
    currencies, percentages, totals = icd.summarize_currency_distribution(conv.perform_conversion(combined_set))

    # Normalise and import the items into a dictionary of dictionaries
    distribution_dict = icd.convert_to_matrices(currencies, percentages, totals)

    return pnl_distribution, yoy_growth_dict, distribution_dict


def load_pnl_and_currency_data(pnl_distribution, yoy_growth_dict, distribution_dict) -> 'Some Dataframes':
    """Reads the saved dictionaries we need for this module: P&L distribution and currency distributions."""
    # if not use_example:
    #     try:
    #         file_name = gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-pnl-distribution.json')
    #         with open(sc.PATH_TO_CUSTOMER_DATA + '/' + sc.CUSTOMER_FOLDER_NAME + '/' + file_name, 'r') as fd:
    #             pnl_distribution, yoy_growth_dict = json.load(fd)
    #
    #         file_name = gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-currency-distribution.json')
    #         with open(sc.PATH_TO_CUSTOMER_DATA + '\\' + sc.CUSTOMER_FOLDER_NAME + '\\' + file_name, 'r') as fd:
    #             distribution_dict = json.load(fd)
    #
    #     except:  # Manually create distributions if a file is not found
    #         print('Could not find a .json file with pnl- and/or currencies distributions.')
    #         return
    # else:
    #     pnl_distribution, yoy_growth_dict, distribution_dict = generate_mock_company()

    # Load the 'problem space' with applied currencies and P&L stats
    currencies = distribution_dict['Revenue']['Columns'][1:]
    currency_risks = [er.retrieve_limit(x, sc.ACCOUNTING_CURRENCY, sc.RISK_WINDOW) for x in currencies]
    account_factor_vector = [account_available(x) for x in currencies]
    # pprint.pprint(distribution_dict)

    # If we 'scale' to the P&L, we can leave the distribution ratios as they are. But if we want to compensate in
    # a difference between the invoices data and the P&L data by adding more accounting currency for a category in a
    # year, we need to rework the ratios.
    for year in sc.YEARS:
        if FILL_COST_GAPS[year] != 'Scale':
            for cat in sc.PNL_CATEGORIES:
                index = [i for i, x in enumerate(pnl_distribution['Headers']) if x == cat][0]
                pnl_total_for_cat = pnl_distribution[year][index] * pnl_distribution[year][0]
                currency_vector = []
                curr_total_for_cat = distribution_dict[cat][year][0]

                for curr_ratio in distribution_dict[cat][year][1:]:
                    currency_vector.append(curr_ratio * curr_total_for_cat)

                currency_vector[0] += (pnl_total_for_cat - curr_total_for_cat)
                for i, curr_amount in enumerate(currency_vector):
                    distribution_dict[cat][year][i + 1] = curr_amount / pnl_total_for_cat

    # pprint.pprint(distribution_dict)

    return pnl_distribution, yoy_growth_dict, distribution_dict, currencies, currency_risks, account_factor_vector


def pnl_factor(year: int, item: str, currency_item: int, mode: str, pnl_distribution, account_factor_vector) -> float:
    """Read the P&L distribution dictionary and retrieve the %-of-revenue factor.
    Adjust the sign of this factor based on whether there is a currency account for that
    curreny or not. If there is one, the treatment for netting in the calculations is different."""
    index = [i for i, x in enumerate(pnl_distribution['Headers']) if x == item][0]
    if mode == 'Netting':
        factor = account_factor_vector[currency_item]
    else:
        factor = abs(account_factor_vector[currency_item])

    if item == sc.PNL_CATEGORIES[0]:  # 'Revenue'
        factor = abs(factor)

    if item == sc.PNL_CATEGORIES[-1]:  # 'NetInc'
        factor = -1.0 * factor

    return float(pnl_distribution[year][index] * factor)


def construct_exposure_matrix(pnl_distribution, yoy_growth_dict, distribution_dict, currencies, currency_risks, account_factor_vector) -> 'Dataframe':
    """Constructs the exposure matrix. Results depends on whether we are netting or not. When netting, currencies
    for which a currency account exists (sc.AVAILABLE_CURRENCY_ACCOUNTS) are not converted back to ACCOUNTING_CURRENCY
    each time. When no currency account exists for that currency, amounts will be treated as though no netting
    is applied."""

    pnl_distribution, yoy_growth_dict, distribution_dict, currencies, currency_risks, account_factor_vector = \
        load_pnl_and_currency_data(pnl_distribution, yoy_growth_dict, distribution_dict)

    # Set up an empty dataframe with the columns as I want to export them to my dashboard
    dataframe_columns = ['Year', 'Currency', 'Type_of_Exposure', 'Exposed_Amount_[Acct_Curr]',
                         'Exposed_Amount_(Risked)', 'Volatility']
    results = pd.DataFrame(columns=dataframe_columns)

    # Perform 2 runs: one with a netting effect, and one without
    for mode in ['Netting', 'No Netting']:

        # Run an exposure simulation for each year of which we know the revenue
        for year, revenue in {x: y[0] for x, y in pnl_distribution.items() if str(x).isnumeric()}.items():
            exp = []
            for cat in sc.PNL_CATEGORIES:
                exp.append(
                    [pnl_factor(year, cat, i, mode, pnl_distribution, account_factor_vector) * v * revenue for i, v in
                     enumerate(distribution_dict[cat][year][1:])])
                exposure = np.asarray(exp)

            # Do a sum for each column (= currency)
            exposure_per_currency = [exposure[:, i].sum() for i in range(0, exposure.shape[1])]

            # The first entry (in ACCT_CURR) exposure = Net Income. The rest is abs() as exposure is the same in either direction.
            exposure_per_currency[0] = abs(
                pnl_factor(year, sc.PNL_CATEGORIES[-1], 0, mode, pnl_distribution, account_factor_vector) * revenue)
            exposure_per_currency[1:] = [abs(x) for x in exposure_per_currency[1:]]

            # Construct the table to be used by PowerBI
            for item in range(0, len(currencies)):
                line_item = [year, currencies[item], mode, exposure_per_currency[item],
                             exposure_per_currency[item] * currency_risks[item],
                             round(float(currency_risks[item] - 1), 3)]
                results.loc[len(results.index)] = line_item

    return results


def fibonacci_or_zero(counter, amount):
    if amount == 0.0:
        return 0.0
    else:
        return gf.fibonacci(counter + 1)


def clean_up_and_sort_results(results: 'Dataframe') -> 'Dataframe':
    """Clean up and sort the results table by risked exposure, so we can add a Fibonacci element to keep the
    charts readable."""

    results_sorted = results.assign(sortkey=results.groupby(
        ['Year', 'Type_of_Exposure'])['Exposed_Amount_(Risked)'].transform('mean')) \
        .sort_values(['sortkey', 'Exposed_Amount_(Risked)'], ascending=[True, True]) \
        .set_index(['Year', 'Type_of_Exposure']) \
        .drop('sortkey', axis=1)
    results_sorted['Counter'] = results_sorted.groupby(['Year', 'Type_of_Exposure']).cumcount() + 1
    results_sorted['Amount'] = results_sorted['Exposed_Amount_[Acct_Curr]']
    results_sorted['Fibonacci'] = results_sorted.apply(lambda row: fibonacci_or_zero(row.Counter, row.Amount), axis=1)

    return results_sorted.reset_index()


def main():
    t = gf.timing()
    results = clean_up_and_sort_results(construct_exposure_matrix())
    t('Exposure determined.')
    return results


<<<<<<< HEAD
if __name__ == '__main__':
    main().to_clipboard(index=False)
=======
available_crosses, rates_dict = load_rates()
limits = load_limits()
correlations = load_correlations()
=======
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
>>>>>>> master
>>>>>>> master
