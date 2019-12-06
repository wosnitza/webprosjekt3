"""This module contains code to generate a list of invoices for a full year given certain parameters:

year: The year for which we want to generate the invoice list (invoice date will be in this year)
amount_of_invoices: The amount of invoices we want in the list
total_cost: The total cost (in the accounting currency) that the invoices add up to
currency_distribution: A dictionary of how the invoices and invoice totals are to be divided between different
    currencies. Allows the user to specify which percentage of the total_cost is allocated to which currency.

    So the other way around: the invoices in the list will have amounts in their original currency. When converted
    on their due date to the accounting currency, their total will add up to be the total_cost specified.

The result is copied to the clipboard for pasting into for instance Excel.

"""

import pandas as pd
import random
from datetime import timedelta, date
import simulator_common.general_functions as gf
import simulator_common.exchange_rates as er
import simulator_common.simulator_constants as sc


def generate_currency(currency_distribution: 'Dict') -> 'List':
    """Randomiser function to generate x times a currency according to the distribution given in INCOME_DISTRIBUTION."""

    currency_list = []
    for k, v in currency_distribution.items():
        currency_list.append([k for _ in range(v)])
    currency_list = [item for sublist in currency_list for item in sublist]

    return currency_list


def generate_list_of_invoices(year: int, amount_of_invoices: int, total_cost: float,
                              currency_distribution, category: str) -> 'Dataframe':
    """This function does the bulk of the work, as specified in the header of this module."""

    # Set up the end results dataframe
    invoices = pd.DataFrame()

    # Set boundaries for the generating
    start_date = date(year, 1, 1)
    lower_invoice_bound = 0.004 * total_cost * 100
    upper_invoice_bound = 0.05 * total_cost * 100

    # Generate the list of currencies for my invoices
    currency_list = generate_currency(currency_distribution)

    # Generate a list of viable payment terms and their frequency
    payment_terms = []
    for i in range(len(sc.EXPOSURE_WINDOWS)):
        payment_terms.extend(sc.EXPOSURE_WINDOWS[i] for x in range(sc.EXPOSURE_WINDOWS_DISTRIBUTION[i]))

    # Generate end result columns
    invoice_date = [start_date + timedelta(days=random.randint(0, 364)) for x in range(amount_of_invoices)]
    due_date = [invoice_date[x] + timedelta(days=payment_terms[random.randint(0, len(payment_terms) - 1)]) for x in
                range(amount_of_invoices)]
    amount = [float(random.randint(lower_invoice_bound, upper_invoice_bound) / 100) for _ in range(amount_of_invoices)]
    currencies = [currency_list[random.randint(0, len(currency_list) - 1)] + '-' + str(i) for i in
                  range(amount_of_invoices)]

    # Decide on a scaling factor for each currency, so their totals add up to the division
    pair_dict = dict(zip(currencies, amount))
    currencies = [x[:3] for x in currencies]  # Restore the currencies list to the currency codes
    factor_dict = {}
    for currency in currency_distribution.keys():
        factor_dict[currency] = sum(v for k, v in pair_dict.items() if currency in k)
        factor_dict[currency + '_tot'] = (total_cost * (currency_distribution[currency]) / 100) / factor_dict[
            currency] if factor_dict[currency] != 0.0 else 0.0
    amount = [v * factor_dict[k[:3] + '_tot'] for k, v in pair_dict.items()]

    # Now we convert the invoice amounts back to their original currency
    amount_conv = [amount[i] * er.exchange_rate(sc.ACCOUNTING_CURRENCY + currencies[i], v) for i, v in
                   enumerate(due_date)]

    # Round the amounts to 2 digits
    amount = [round(x, 2) for x in amount]
    amount_conv = [round(x, 2) for x in amount_conv]

    # Load results into the invoices dataframe
    invoices['Amount'] = amount_conv
    invoices['Currency'] = currencies
    invoices['Invoice_Date'] = invoice_date
    invoices['Due_Date'] = due_date
    invoices['Category'] = category
    invoices['Payment_Currency'] = sc.ACCOUNTING_CURRENCY
    invoices['Amount_On_Due_Date_[' + sc.ACCOUNTING_CURRENCY + ']'] = amount

    return invoices


def normalise_terms_vector():
    """Use this to quickly copy a list of payment terms from Excel, and get a vector of normalised terms
    in return. Use to verify """
    dataset = pd.DataFrame()
    terms_df = pd.read_clipboard()
    terms = terms_df['0'].values.tolist()
    result = [gf.normalise(int(x)) for x in terms]
    dataset['Result'] = result
    dataset.to_clipboard(index=False)
    return


def main():
    invoice_list = generate_list_of_invoices(2018, 100, 10000000, {'NOK': 80, 'EUR': 15, 'USD': 5}, "COGS")
    invoice_list.to_clipboard(index=False)
    print(invoice_list)
    print(invoice_list['Amount'].sum())

    return


if __name__ == '__main__':
    main()
