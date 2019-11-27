# webprosjekt3

[DHG] has proposed a few modules into the 'invoices' branch on 21.11.2019.

In the /data folder, there are .csv files with historic exchange rates.

Create a folder locally called 'C:\Apps\Currency Extractor\rates-files-for-python' and store the .csv files there.

Create a folder locally called 'C:\Apps\Currency Extractor\limit-files-for-python' and store the Correlations.csv and Limits.csv there.

There are 3 Python modules that are stored in a folder called 'simulator_common': exchange_rates.py, general_functions.py, and simulator_constants.py

There is 1 Python in a folder called 'simulator_utils': invoice_generator.py.

Once the Python is in your IDE, makes sure the import statements reference the right files. Run invoice_generator.py and copy the clipboard into an Excel file. You then see the lists you generated. Store this in a database if you can.

If we can get this to work, I can also add the code that will update the charts we have selected.

# This was changed to MAC folder locations. To change for windows comment out mac paths and uncomment windows paths in invoice-generator.py, exchange-rates.py and simulator-constants.py
