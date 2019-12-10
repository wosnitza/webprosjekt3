import simulator_common.simulator_constants as sc
import pandas as pd


# Below setting drives which header mapping is applied when
INPUT_TYPE = 'grouping'  # 'Loops Output', 'Norganics Output', ...

file_name = sc.PATH_TO_APPDATA + '\\' + sc.HEADER_MAPPING_FOLDER + '\\' + 'header-mapping.csv'
mapping_df = pd.read_csv(file_name)
mapping = dict(zip(mapping_df['norm_header'], mapping_df[INPUT_TYPE]))
mapping['Date_Columns'] = eval(mapping['Date_Columns'])
mapping['Amount_Columns'] = eval(mapping['Amount_Columns'])


def map(type:str, norm_header:str) -> str:
    map_df = mapping_df.dropna(subset=[type], inplace=False)
    map = dict(zip(map_df['norm_header'], map_df[type]))
    try:
        map['Date_Columns'] = eval(map['Date_Columns'])
    except:
        pass

    try:
        map['Amount_Columns'] = eval(map['Amount_Columns'])
    except:
        pass

    try:
        result = map[norm_header]
    except:
        result = ''

    return result


#
# # simulate_hedge
# if INPUT_TYPE == 'Loops Output':
#     AMOUNT = 'Invoice Amount'
#     INVOICE_DATE = 'Invoice Date'
#     DUE_DATE = 'Payment Date'
#     INVOICE_CURRENCY = 'Invoice Currency'
#     PAYMENT_CURRENCY = 'Payment Currency'
#     DATE_COLUMNS = ['Invoice Date', 'Payment Date']
# elif INPUT_TYPE == 'Other Output':
#     AMOUNT = 'Invoice Amount'
#     INVOICE_DATE = 'Invoice Date'
#     DUE_DATE = 'Payment Date'
#     INVOICE_CURRENCY = 'Invoice Currency'
#     PAYMENT_CURRENCY = 'Payment Currency'
#     DATE_COLUMNS = ['Invoice Date', 'Payment Date']
# elif INPUT_TYPE == 'Grouping Output':
#     AMOUNT = 'Amount'
#     INVOICE_DATE = 'Invoice_Date'
#     DUE_DATE = 'Due_Date'
#     INVOICE_CURRENCY = 'Currency'
#     PAYMENT_CURRENCY = 'Payment Currency'
#     DATE_COLUMNS = ['Invoice_Date', 'Due_Date']
#
# REQUIRED_COLUMNS = [AMOUNT, INVOICE_DATE, INVOICE_CURRENCY, DUE_DATE]
# OPTIONAL_COLUMNS = [PAYMENT_CURRENCY]
#
# #straight_convesrions
# INPUT_TYPE = 'Grouping Output'  # 'Loops Output', 'Norganics Output', ...
# if INPUT_TYPE == 'Loops Output':
#     AMOUNT = 'Invoice Amount'
#     INVOICE_DATE = 'Invoice Date'
#     INVOICE_CURRENCY = 'Invoice Currency'
#     CATEGORY = 'Category'
#     DATE_COLUMNS = [INVOICE_DATE]
# elif INPUT_TYPE == 'Norganics Output':
#     AMOUNT = 'ExchangeAmount'
#     INVOICE_DATE = 'DeliveryDate'
#     INVOICE_CURRENCY = 'Currency'
#     CATEGORY = 'Category'
#     DATE_COLUMNS = ['Due Date', INVOICE_DATE, 'OrderDate']
# elif INPUT_TYPE == 'Grouping Output':
#     AMOUNT = 'Amount'
#     INVOICE_DATE = 'Invoice_Date'
#     INVOICE_CURRENCY = 'Currency'
#     CATEGORY = 'Category'
#     DATE_COLUMNS = ['Due_Date', INVOICE_DATE]
# REQUIRED_COLUMNS = [INVOICE_DATE, AMOUNT, INVOICE_CURRENCY]
# OPTIONAL_COLUMNS = ['Category']
# DEFAULT_CATEGORY = 'COGS'
#
#
#
# # dataset_summarising
# DATES_COLUMNS = ['DeliveryDate', 'Due Date', 'OrderDate']
# EVENT_COLUMN = 'Aggregated_Event'
# HEADER_MAPPING = {'Supplier': 'Supplier_Name',  # Careful to ensure that all column headers are text in Excel!!
#                   'Country': 'Country',
#                   'OrderDate': 'Invoice_Date',
#                   'Amount': 'Amount [NOK]',
#                   'DeliveryDate': 'Due_Date',
#                   'Due Date': 'Due_Date_Plus_30',
#                   'ExchangeAmount_2': 'Amount',
#                   'ExchangeRate': 'Rate',
#                   'Currency': 'Currency',
#                   'GLAccountDescr': 'Cost_Center'}