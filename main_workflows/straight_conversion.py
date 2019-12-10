"""The code in this module takes an Excel table that has been copied into the clipboard,
(needs to be able to) find the invoice amount, invoice date, and invoice currency, and converts
the invoice amount to the ACCOUNTING_CURRENCY. Results are passed back to the clipboard for
copying back into the Excel sheet - two columns: Amount and Rate."""

import simulator_common.exchange_rates as er
import simulator_common.general_functions as gf
import simulator_common.simulator_constants as sc
import simulator_common.header_mapping as hm
import pandas as pd
import numpy as np

# Set column header- and other  constants
INPUT_TYPE = 'grouping'  # 'loops', 'other', 'norganic', 'norganic_for_summarising', ...

# One-off loading into variable. Using hm.map is waaaay too slow. Keep this until rewritten.
AMOUNT = hm.map(INPUT_TYPE, 'Amount')
INVOICE_DATE = hm.map(INPUT_TYPE, 'Invoice_Date')
INVOICE_CURRENCY = hm.map(INPUT_TYPE, 'Invoice_Currency')
CATEGORY = hm.map(INPUT_TYPE, 'Category')

DATE_COLUMNS = hm.map(INPUT_TYPE, 'Date_Columns')
AMOUNT_COLUMNS = [AMOUNT]
REQUIRED_COLUMNS = [INVOICE_DATE, AMOUNT, INVOICE_CURRENCY]
OPTIONAL_COLUMNS = [CATEGORY]


def perform_conversion(input_table: 'Dataframe', add_to_original_set=False) -> 'SetOfConvertedData':
    """Takes an input dataframe, and generates a converted amount in the accounting currency for each row.
    Uses the invoice date as the reference date."""

    t = gf.timing()
    # Generate a column of answers back into the clipboard
    original_currency = []
    conversion_dates = []
    conversion_amounts = []
    conversion_rates = []
    original_category = []
    converted_data = pd.DataFrame()

    # Loop all the rows in the input_table (check https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas for how to improve this.
    for i, row in input_table.iterrows():
        amount = gf.convert_excel_amount(row[AMOUNT])
        date = gf.convert_excel_date(row[INVOICE_DATE])
        currency = row[INVOICE_CURRENCY]
        try:
            category = row[CATEGORY]
        except:
            category = sc.DEFAULT_COSTS_CATEGORY

        try:
            rate = er.exchange_rate(currency + sc.ACCOUNTING_CURRENCY, date.date())
        except:
            rate = er.exchange_rate(currency + sc.ACCOUNTING_CURRENCY, date)

        if not isinstance(rate, str):
            original_currency.append(currency)
            conversion_dates.append(date)
            conversion_rates.append(float(rate))
            conversion_amounts.append(amount * float(rate))
            original_category.append(category)
        else:
            original_currency.append(np.nan)
            conversion_dates.append(np.nan)
            conversion_rates.append(np.nan)
            conversion_amounts.append(np.nan)
            original_category.append(np.nan)

    # Add the results to the converted_data DataFrame
    converted_data['Original_Currency'] = original_currency
    converted_data['Conversion_Date'] = conversion_dates
    converted_data['Amount_[' + sc.ACCOUNTING_CURRENCY + ']'] = conversion_amounts
    converted_data['Rate'] = conversion_rates
    converted_data['Category'] = original_category

    if add_to_original_set:
        input_table['Amount_[' + sc.ACCOUNTING_CURRENCY + ']'] = conversion_amounts
        input_table['Rate'] = conversion_rates
        converted_data = input_table

    # Print message
    t(str(len(converted_data)) + ' rows of conversion results generated')

    # Return the converted data set. If run in this module, results will be copied to clipboard.
    # If called from another module, results will be further used.
    return converted_data


if __name__ == "__main__":
    # Load either clipboard contents or file contents into a DataFrame.
    source, input_table, status = gf.load_from_clipboard_or_file(DATE_COLUMNS, AMOUNT_COLUMNS, REQUIRED_COLUMNS,
                                                                 OPTIONAL_COLUMNS)

    # Store a two-column map of the results into a dataframe and export it to clipboard
    converted_dataset = perform_conversion(input_table)[['Amount_[' + sc.ACCOUNTING_CURRENCY + ']', 'Rate']]
    converted_dataset.to_clipboard(index=False)
