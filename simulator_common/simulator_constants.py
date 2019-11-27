
# Enter customer-specific data that will apply to / is relevant for all tools in this toolbox
# We will need to create a class that holds this customer specific information, loaded into a global dictionary
# and retrieved via calls to the class attributes or options. Then only put the company technical name / ID
# as a constants in this module.
CUSTOMER_ORG_ID = '984155913'
CUSTOMER_FULL_NAME = 'Norganic AS'
CUSTOMER_FOLDER_NAME = 'Norganic'

# Currency related constants
ACCOUNTING_CURRENCY = 'NOK'
AVAILABLE_CURRENCY_ACCOUNTS = ['NOK', 'EUR', 'USD']
CROSS_BASE_LEG = 'EUR'

# Constants for doing currency distribution and P&L distribution (needs to be the same...)
YEARS = ['2014', '2015', '2016', '2017', '2018']
PNL_CATEGORIES = ['Revenue', 'COGS', 'SG&A', 'DA', 'IntTax', 'NetInc']
DEFAULT_COSTS_CATEGORY = 'COGS'

# System variables for windows
# PATH_TO_CUSTOMER_DATA = r'G:\Shared drives\Monetor Shared Drive\09. Projects and Customer Data\\'
# PATH_TO_APPDATA = r'C:\Apps\Currency Extractor'
# PATH_TO_RATES_DATA = PATH_TO_APPDATA + r'\rates-files-for-python'
# PATH_TO_LIMITS_DATA = PATH_TO_APPDATA + r'\limit-files-for-python'
# HEADER_MAPPING_FOLDER = r'header-mapping-for-python'

# System variables for mac
PATH_TO_CUSTOMER_DATA = r'G:\Shared drives\Monetor Shared Drive\09. Projects and Customer Data\\'
PATH_TO_APPDATA = r'/Users/bjorngyles/Desktop/Currency Extractor'
PATH_TO_RATES_DATA = PATH_TO_APPDATA + r'/rates-files-for-python'
PATH_TO_LIMITS_DATA = PATH_TO_APPDATA + r'/limit-files-for-python'
HEADER_MAPPING_FOLDER = r'header-mapping-for-python'

# ACCOUNTS_PAYABLE_SOURCE_DATA_WORKBOOK_WORDS = 'Sample Data'
# ACCOUNTS_PAYABLE_SOURCE_DATA_WORKSHEET_WORDS = 'SupplierOrderLineAndCopyView'
ACCOUNTS_PAYABLE_SOURCE_DATA_WORKBOOK_WORDS = 'Data Tables, Summarised'
ACCOUNTS_PAYABLE_SOURCE_DATA_WORKSHEET_WORDS = 'Summarised (Month)'


# Payment constants
DEFAULT_PAYMENT_TERM = 30
RISK_WINDOW = 60  # Used in calculating exposure

# Risk and exposure constants
EXPOSURE_WINDOWS = [7, 14, 21, 30, 45, 60, 90, 100, 180, 270, 365]
RISK_LEVELS = [0, 20, 40, 60, 80, 100, 120]  # 120 is the 20/20 hindsight hedge
RISK_LEVELS_REV = [120, 100, 80, 60, 40, 20, 0]

