# Webprosjekt3 - FX-Lab

Requirements:
* Python 3 (We used version 3.8)
* Package manager system (We used PIP)

Prerequisites:
1. Install python packages via pip.
Copy paste the following line to install all the required python packages for this project.
		     
	     pip install dash dash_bootstrap_components dash_table pandas plotly 

2. Move or copy the **Apps** folder in the project root to the C:\ root. Should look like this **C:\Apps**

3. Run main.py from your IDE or via terminal using "python main.py"

Heading

## App functionality
Inside the web application you will be met by several inputs.

 1. Upload the file called **norganic-pnl-distribution.json**. This is located in: 
		`C:\Apps\Currency Extractor\Projects and customer Data\Norganic\`

 2. With the year slider on the bottom of the company section select year **2018**, due to some hardcoding this isnt dynamic yet, so only 2018 will work as of now. This will fill out Total Procurement, Net Income, Total Revenue and select year in all columns.
 3. In the supplier section input yearly invoices (for example: 50).
 4. For both supplier side and customer side fill out currency distribution. (For example: **Supplier**: USD: 40%, NOK: 50%, EUR: 10% and **Customer**: USD: 50%, NOK: 50%)
 5. Click generate.
 6. This will populate the Accounting tab and Exposure tab with charts and data.


## MAC.
For MAC you have to comment out the paths for windows and comment in the paths for MAC in simulator_constants.py and simulator_common\exchange_rates.py, and reformat the paths to your APPS folder location
