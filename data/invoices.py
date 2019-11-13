import pandas as pd
import random
from datetime import timedelta, date
def generate_list_of_invoices(year: int, amount_of_invoices: int, total_cost: float, currencies: 'List') -> 'Dataframe':
    invoices = pd.DataFrame()
    start_date = date(year, 1, 1)
    lower_invoice_bound = 0.005 * total_cost
    upper_invoice_bound = 0.08 * total_cost
    # payment_terms = [0, 7, 14, 30, 45, 60, 100, 180, 270, 365]
    payment_terms = []
    payment_terms.extend(0 for x in range(4))
    payment_terms.extend(7 for x in range(8))
    payment_terms.extend(14 for x in range(8))
    payment_terms.extend(30 for x in range(16))
    payment_terms.extend(45 for x in range(12))
    payment_terms.extend(60 for x in range(6))
    payment_terms.extend(100 for x in range(2))
    payment_terms.extend(180 for x in range(1))
    payment_terms.extend(270 for x in range(1))
    payment_terms.extend(365 for x in range(1))
    invoice_date = [start_date + timedelta(days=random.randint(0, 365)) for x in range(amount_of_invoices)]
    due_date = [invoice_date[x] + timedelta(days=payment_terms[random.randint(0, len(payment_terms) - 1)]) for x in
                range(amount_of_invoices)]
    amount = [float(random.randint(lower_invoice_bound, upper_invoice_bound)) for x in range(amount_of_invoices)]
    factor = total_cost / sum(amount)
    amount = [x * factor for x in amount]
    currency = [currencies[0] for x in range(amount_of_invoices)]
    invoices['Amount'] = amount
    invoices['Currency'] = currency
    invoices['Invoice_Date'] = invoice_date
    invoices['Due_Date'] = due_date
    return invoices
invoice_list = generate_list_of_invoices(2018, 100, 10000000, ['NOK'])
print(invoice_list)
print(invoice_list['Amount'].sum())