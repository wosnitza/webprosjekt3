"""This module generates a matrixed currency distribution across years and P&L categories. Uses default
category if none given. Leaves a .json file in the customer folder that contains the full breakdown. This
breakdown is required for the exposure analysis."""

import simulator_common.general_functions as gf
import simulator_common.simulator_constants as sc
import simulator_common.header_mapping as hm
import main_workflows.straight_conversion as conv
import simulator_utils.pretty_print_json as ppj
import json

AMOUNT_COLUMN = 'Amount_[' + sc.ACCOUNTING_CURRENCY + ']'
EXPORT_COLUMNS = ['Category', 'Conversion_Date', 'Original_Currency', AMOUNT_COLUMN]


def generate_defaults():
    """I might get rid of this routine. We just have to generate P&L and currency distribution files."""

    # Three default currencies:
    CURRENCIES = [sc.ACCOUNTING_CURRENCY, 'EUR', 'USD']

    # region Estimate for each currency, which percentage of revenue etc. is in this currency
    revenue_dist = [0.8, 0.15, 0.5]  # If 3 currencies are given, these lists need to reflect 3 percentages
    cogs_dist = [0.25, 0.6, 0.15]
    sga_dist = [1.0, 0.0, 0.0]
    da_dist = [1.0, 0.0, 0.0]
    inttax_dist = [1.0, 0.0, 0.0]
    netinc_dist = [1.0, 0.0, 0.0]
    # endregion

    # Extract company file name from company folder name
    file_name = gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-pnl_summary.json')

    # region Initialise some temporary distribution dictionaries for saving to file
    yearly_revenue = {'Dictionary_Type': 'Yearly Revenue', 'Currency': sc.ACCOUNTING_CURRENCY}
    yoy_growth_dict = {}
    revenue_distribution = {'Dictionary_Type': 'Revenue Distribution', 'Currencies': CURRENCIES}
    cogs_distribution = {'Dictionary_Type': 'COGS Distribution', 'Currencies': CURRENCIES}
    sga_distribution = {'Dictionary_Type': 'SGA Distribution', 'Currencies': CURRENCIES}
    da_distribution = {'Dictionary_Type': 'DA Distribution', 'Currencies': CURRENCIES}
    interesttax_distribution = {'Dictionary_Type': 'Interest and Tax Distribution', 'Currencies': CURRENCIES}
    netincome_distribution = {'Dictionary_Type': 'Net Income Distribution', 'Currencies': CURRENCIES}
    # endregion

    # region Read contents from existing json file, if it exists
    try:
        create_new = False
        with open(sc.PATH_TO_CUSTOMER_DATA + '\\' + sc.CUSTOMER_FOLDER_NAME + '\\' + file_name, 'r') as fd:
            pnl_distribution, yearly_revenue, yoy_growth_dict, revenue_distribution, cogs_distribution, \
            sga_distribution, da_distribution, interesttax_distribution, netincome_distribution = json.load(fd)
    except:
        create_new = True

    return


def summarize_currency_distribution(dataset: 'Dataframe'):
    """Input is a dataframe with the required invoice data. Output is are a list and two dictionaries:
    1. A list of currencies in descending order of exposure
    2. A dict of percentages per currency per year per group
    3. A dict of total amount per group per year

    We use this data to calculate exposure further on in the tool."""

    # Group the dataframe to category, year, and currency
    dataset['Conversion_Date'] = dataset['Conversion_Date'].apply(lambda x: x.year)
    if hm.map(conv.INPUT_TYPE, 'Category') not in dataset.columns.values.tolist():
        dataset['Category'] = sc.DEFAULT_COSTS_CATEGORY

    # List of total per category per year
    totals_list = dataset.groupby(['Category', 'Conversion_Date']).sum().reset_index()
    totals_list['ID'] = totals_list.apply(lambda row: str(row.Category) + str(row.Conversion_Date), axis=1)
    totals = dict(zip(totals_list['ID'], totals_list[AMOUNT_COLUMN]))

    # Generate list of percentage per currency per year per category
    distribution = dataset.groupby(['Category', 'Conversion_Date', 'Original_Currency']).sum()
    percentage_list = distribution.groupby(['Category', 'Conversion_Date']).apply(lambda x: x / x.sum()).reset_index()
    percentage_list['ID'] = percentage_list.apply(
        lambda row: str(row.Category) + str(row.Conversion_Date) + str(row.Original_Currency), axis=1)
    percentages = dict(zip(percentage_list['ID'], percentage_list[AMOUNT_COLUMN]))

    # Generate list of the present currencies and their totals across years
    currency_list = dataset.groupby(['Original_Currency'], sort=False).agg(['sum']).sort_values((AMOUNT_COLUMN, 'sum'),
                                                                                                ascending=False).reset_index()
    currencies = [sc.ACCOUNTING_CURRENCY]
    for item in zip(currency_list['Original_Currency']):
        if item[0] != sc.ACCOUNTING_CURRENCY and item[0] != '':
            currencies.append(item[0])

    return currencies, percentages, totals


def convert_to_matrices(currencies: 'List', percentages: 'Dict', totals: 'Dict') -> 'Dict':
    distribution_dict = {}

    for category in sc.PNL_CATEGORIES:
        distribution_dict[category] = {'Columns': ['Total [' + currencies[0] + ']'] + currencies}
        for year in sc.YEARS:
            try:
                currency_items = [totals[category + str(year)]]
            except:
                currency_items = [0.0]

            for currency in currencies:
                try:
                    currency_items.append(percentages[category + str(year) + currency])
                except:
                    currency_items.append(0.0)

            currency_items[1] = 1 - sum(currency_items[2:])
            distribution_dict[category][year] = currency_items

    return distribution_dict


if __name__ == "__main__":
    # Load either clipboard contents or file contents into a DataFrame.
    source, input_table, status = gf.load_from_clipboard_or_file(conv.DATE_COLUMNS, conv.AMOUNT_COLUMNS,
                                                                 conv.REQUIRED_COLUMNS,
                                                                 conv.OPTIONAL_COLUMNS)

    if status == 'OK':
        # Store a two-column map of the results into a dataframe and export it to clipboard
        currencies, percentages, totals = summarize_currency_distribution(conv.perform_conversion(input_table))

        # Normalise and import the items into a dictionary of dictionaries
        distribution_dict = convert_to_matrices(currencies, percentages, totals)

        # Write this dictionary into a JSON file
        file_name = sc.PATH_TO_CUSTOMER_DATA + sc.CUSTOMER_FOLDER_NAME + '\\' + \
                    gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-currency-distribution.json')

        with open(file_name, 'w') as fd:
            fd.write(json.dumps(distribution_dict))

        # Export to screen
        print(ppj.prettyjson(distribution_dict, 4, 300))

    else:
        print('Seems like some data is missing from the clipboard or file import')
