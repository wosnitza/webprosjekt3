"""Uses a dictionary of terms to generate correlating lists of invoices that together make up the
'company's' revenue, cost, and net profit.

This 'company' is for instance used in strategy simulations.
"""

import simulator_utils.invoice_generator as ig
import simulator_common.general_functions as gf
import main_workflows.straight_conversion as conv
import simulator_common.simulator_constants as sc

EXAMPLE_COMPANY = {'2014': {'Total_Revenue': 51911000,
                            'Net_Income': 1072000,
                            'Amount_of_Invoices': 100,
                            'Proc_Currency_Distribution': {'NOK': 28,
                                                           'EUR': 43,
                                                           'USD': 20,
                                                           'SEK': 4,
                                                           'DKK': 3,
                                                           'GBP': 2},
                            'Sales_Currency_Distribution': {'NOK': 90,
                                                            'EUR': 10}},
                   '2015': {'Total_Revenue': 69897000,
                            'Net_Income': 810000,
                            'Amount_of_Invoices': 100,
                            'Proc_Currency_Distribution': {'NOK': 28,
                                                           'EUR': 43,
                                                           'USD': 20,
                                                           'SEK': 4,
                                                           'DKK': 3,
                                                           'GBP': 2},
                            'Sales_Currency_Distribution': {'NOK': 90,
                                                            'EUR': 10}},
                   '2016': {'Total_Revenue': 101642000,
                            'Net_Income': 3278000,
                            'Amount_of_Invoices': 100,
                            'Proc_Currency_Distribution': {'NOK': 28,
                                                           'EUR': 43,
                                                           'USD': 20,
                                                           'SEK': 4,
                                                           'DKK': 3,
                                                           'GBP': 2},
                            'Sales_Currency_Distribution': {'NOK': 90,
                                                            'EUR': 10}},
                   '2017': {'Total_Revenue': 111681000,
                            'Net_Income': 1470000,
                            'Amount_of_Invoices': 100,
                            'Proc_Currency_Distribution': {'NOK': 28,
                                                           'EUR': 43,
                                                           'USD': 20,
                                                           'SEK': 4,
                                                           'DKK': 3,
                                                           'GBP': 2},
                            'Sales_Currency_Distribution': {'NOK': 90,
                                                            'EUR': 10}},
                   '2018': {'Total_Revenue': 112914000,
                            'Net_Income': 1140000,
                            'Amount_of_Invoices': 100,
                            'Proc_Currency_Distribution': {'NOK': 28,
                                                           'EUR': 43,
                                                           'USD': 20,
                                                           'SEK': 4,
                                                           'DKK': 3,
                                                           'GBP': 2},
                            'Sales_Currency_Distribution': {'NOK': 90,
                                                            'EUR': 10}},
                   }


def set_up_company(company: 'Dict') -> 'List of dicts':
    """'Crank up' a company with sales- and procurement invoices. The hardcoded set as per below
    is a simplified reflection of Norganic in 2017. But with less invoices, so faster to simulate.

    sales = ig.generate_list_of_invoices(2018, 60, 111681000, {'NOK': 100})
    procurement = ig.generate_list_of_invoices(2018, 100, 110211000, {'NOK': 28,
                                                                      'EUR': 43,
                                                                      'USD': 20,
                                                                      'SEK': 4,
                                                                      'DKK': 3,
                                                                      'GBP': 2})
    """

    # Create the mock-up company
    t = gf.timing()

    # Preload lists of invoices
    sales = {}
    procurement = {}
    net_income = {}

    years_in_company = [int(key) for key in company]

    for year in range(years_in_company[0], years_in_company[-1]+1):
        # Generate sales and procurement invoices with these values
        sales[year] = ig.generate_list_of_invoices(year,
                                                   company[str(year)]['Amount_of_Invoices'],
                                                   company[str(year)]['Total_Revenue'],
                                                   company[str(year)]['Sales_Currency_Distribution'],
                                                   'Revenue')
        procurement[year] = ig.generate_list_of_invoices(year,
                                                         company[str(year)]['Amount_of_Invoices'],
                                                         company[str(year)]['Total_Revenue'] -
                                                         company[str(year)]['Net_Income'],
                                                         company[str(year)]['Proc_Currency_Distribution'],
                                                         sc.DEFAULT_COSTS_CATEGORY)

        # Add a column for the NOK equivalent of the invoices on invoice date
        procurement[year] = conv.perform_conversion(procurement[year], True)
        sales[year] = conv.perform_conversion(sales[year], True)
        net_income[year] = company[str(year)]['Net_Income']

    t('Invoices and limits loaded.')

    return company, sales, procurement, net_income
