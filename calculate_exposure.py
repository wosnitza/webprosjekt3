"""This module takes some statistics around revenue and cost, and currency distribution in, and generates
a table for the exposure charts and matrix.

Other statistics can be extracted (manually?) from the accounts payable and receivable invoice files."""

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

    invoice_df = combined_set

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
    currencies, percentages, totals = icd.summarize_currency_distribution(
        conv.perform_conversion(combined_set))

    # Normalise and import the items into a dictionary of dictionaries
    distribution_dict = icd.convert_to_matrices(
        currencies, percentages, totals)

    return pnl_distribution, yoy_growth_dict, distribution_dict, invoice_df


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
    currency_risks = [er.retrieve_limit(
        x, sc.ACCOUNTING_CURRENCY, sc.RISK_WINDOW) for x in currencies]
    account_factor_vector = [account_available(x) for x in currencies]
    # pprint.pprint(distribution_dict)

    # If we 'scale' to the P&L, we can leave the distribution ratios as they are. But if we want to compensate in
    # a difference between the invoices data and the P&L data by adding more accounting currency for a category in a
    # year, we need to rework the ratios.
    for year in sc.YEARS:
        if FILL_COST_GAPS[year] != 'Scale':
            for cat in sc.PNL_CATEGORIES:
                index = [i for i, x in enumerate(
                    pnl_distribution['Headers']) if x == cat][0]
                pnl_total_for_cat = pnl_distribution[year][index] * \
                    pnl_distribution[year][0]
                currency_vector = []
                curr_total_for_cat = distribution_dict[cat][year][0]

                for curr_ratio in distribution_dict[cat][year][1:]:
                    currency_vector.append(curr_ratio * curr_total_for_cat)

                currency_vector[0] += (pnl_total_for_cat - curr_total_for_cat)
                for i, curr_amount in enumerate(currency_vector):
                    distribution_dict[cat][year][i +
                                                 1] = curr_amount / pnl_total_for_cat

    # pprint.pprint(distribution_dict)

    return pnl_distribution, yoy_growth_dict, distribution_dict, currencies, currency_risks, account_factor_vector


def pnl_factor(year: int, item: str, currency_item: int, mode: str, pnl_distribution, account_factor_vector) -> float:
    """Read the P&L distribution dictionary and retrieve the %-of-revenue factor.
    Adjust the sign of this factor based on whether there is a currency account for that
    curreny or not. If there is one, the treatment for netting in the calculations is different."""
    index = [i for i, x in enumerate(
        pnl_distribution['Headers']) if x == item][0]
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
        load_pnl_and_currency_data(
            pnl_distribution, yoy_growth_dict, distribution_dict)

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
            exposure_per_currency = [exposure[:, i].sum()
                                     for i in range(0, exposure.shape[1])]

            # The first entry (in ACCT_CURR) exposure = Net Income. The rest is abs() as exposure is the same in either direction.
            exposure_per_currency[0] = abs(
                pnl_factor(year, sc.PNL_CATEGORIES[-1], 0, mode, pnl_distribution, account_factor_vector) * revenue)
            exposure_per_currency[1:] = [abs(x)
                                         for x in exposure_per_currency[1:]]

            # Construct the table to be used by PowerBI
            for item in range(0, len(currencies)):
                line_item = [year, currencies[item], mode, exposure_per_currency[item],
                             exposure_per_currency[item] *
                             currency_risks[item],
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
    results_sorted['Counter'] = results_sorted.groupby(
        ['Year', 'Type_of_Exposure']).cumcount() + 1
    results_sorted['Amount'] = results_sorted['Exposed_Amount_[Acct_Curr]']
    results_sorted['Fibonacci'] = results_sorted.apply(
        lambda row: fibonacci_or_zero(row.Counter, row.Amount), axis=1)

    return results_sorted.reset_index()


def main():
    t = gf.timing()
    results = clean_up_and_sort_results(construct_exposure_matrix())
    t('Exposure determined.')
    return results


if __name__ == '__main__':
    main().to_clipboard(index=False)
