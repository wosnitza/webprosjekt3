"""Module to generate a set of dictionaries to be used in exposure simulation. Takes generic input
along with a copy-paste of proff.no P&L data from the clipboard, and generates a file with the
required dictionaries in the customer folder on the Drive. Also leaves a cleaned up copy of the P&L
statements in the clipboard, to be used for the P&L table in PowerBI.

Automatically checks for an existing file. If found, it will update the P&L distribution contents of this file."""

import simulator_common.general_functions as gf
import simulator_common.simulator_constants as sc
import json
import pprint
import simulator_utils.pretty_print_json as ppj
import pandas as pd

# MAKE SURE TO FILL IN THE RIGHT COMPANY DETAILS IN sc.simulator_constants....
# NR_OF_YRS_FOR_YOY_GROWTH_CALC = 2


def translate_pnl_item(original: str) -> str:
    """Straightforward translation of terms."""

    translation = {
        'Valutakode': 'N/A',
        'Sum salgsinntekter': '1. Revenue',
        'Annen driftsinntekt': '1. Revenue',
        'Sum driftsinntekter': 'N/A',
        'Varekostnad': '2. COGS (Neg)',
        'Beholdningsendringer': '4. SG&A (Neg)',
        'Lønnskostnader': '4. SG&A (Neg)',
        'Herav kun lønn': 'N/A',
        'Ordinære avskrivninger': '5. DA (Neg)',
        'Nedskrivning': '5. DA (Neg)',
        'Andre driftskostnader': '4. SG&A (Neg)',
        'Driftsresultat': 'N/A',
        'Inntekt på invest. annet foretak i sm konsern': 'N/A',
        'Inntekt på investering i datterselskap': 'N/A',
        'Sum annen renteinntekt': 'N/A',
        'Inntekt på invest. i tilknyttet selskap': 'N/A',
        'Sum annen finansinntekt': 'N/A',
        'Sum finansinntekter': '6. Interest and Tax',
        'Nedskrivning fin. anleggsmidler': 'N/A',
        'Sum annen rentekostnad': 'N/A',
        'Andre finanskostnader': 'N/A',
        'Sum annen finanskostnad': 'N/A',
        'Sum finanskostnader': '7. Interest and Tax (Neg)',
        'Resultat før skatt': 'N/A',
        'Sum skatt': '7. Interest and Tax (Neg)',
        'Ordinært resultat': 'N/A',
        'Ekstraordinære inntekter': '3. SG&A',
        'Ekstraordinære kostnader': '4. SG&A (Neg)',
        'Skatt ekstraordinært': '7. Interest and Tax (Neg)',
        'Årsresultat': '8. Net Income',
        'Utbytte': 'N/A',
        'Konsernbidrag': 'N/A',
    }
    return translation[original[0]]


def get_clean_pnl_data(pnl_data):
    """Translates the P&L categories and groups the totals per category."""

    # Translate and normalise the P&L (Norwegian) categories
    pnl_data['Category'] = pnl_data.apply(translate_pnl_item, axis=1)

    # Change the amount data found into actual numbers (leaving the occasional string in place)
    for year in sc.YEARS:
        pnl_data[year] = pnl_data[year].apply(lambda x: gf.convert_excel_amount(x, 1000, True))

    # Group by the new categories, and sum for each of the years
    return pnl_data.groupby(['Category'])[sc.YEARS].sum().reset_index()


def render_pnl_distribution(clean_pnl_data):
    """Generate relative distributions in preparation for saving the JSON."""

    # Initiate the pnl_distribution dictionary with a header line
    pnl_distribution = {
        'Headers': ['Total Revenue [' + sc.ACCOUNTING_CURRENCY + ']'] + [cat for cat in sc.PNL_CATEGORIES]}
    yoy_growth = []

    # Loop the years and make the calculations for each year
    for year in sc.YEARS:
        # 'Manually' calculate the big-ticket items from the dataset
        revenue = clean_pnl_data.loc[0, year]
        cogs = abs(clean_pnl_data.loc[1, year]) / revenue
        sga = abs(clean_pnl_data.loc[3, year] - clean_pnl_data.loc[2, year]) / revenue
        da = abs(clean_pnl_data.loc[4, year]) / revenue
        inttax = abs(clean_pnl_data.loc[6, year] - clean_pnl_data.loc[5, year]) / revenue
        netinc = clean_pnl_data.loc[7, year] / revenue
        netinc_checksum = revenue - clean_pnl_data.loc[1, year] - (
                clean_pnl_data.loc[3, year] - clean_pnl_data.loc[2, year]) - \
                          clean_pnl_data.loc[4, year] - (clean_pnl_data.loc[6, year] - clean_pnl_data.loc[5, year])

        # Print small check for consistency
        print('Year:', 'Calculated:', 'From proff.no:', 'Difference:')
        print(year, netinc_checksum, clean_pnl_data.loc[7, year], netinc_checksum - clean_pnl_data.loc[7, year])

        # Always generate a new P&L distribution and yearly revenue distribution
        pnl_distribution[year] = [float(round(revenue, 0)), 1.0, cogs, sga, da, inttax, netinc]
        # yearly_revenue[year] = float(round(revenue, 0))

        # Add a year-on-year growth percentage
        # if int(year) >= int(sc.YEARS[-NR_OF_YRS_FOR_YOY_GROWTH_CALC]):
        #     yoy_growth.append(
        #         ((pnl_distribution[year][0] - pnl_distribution[str(int(year) - 1)][0]) /
        #          pnl_distribution[str(int(year) - 1)][0]))

    return pnl_distribution, yoy_growth


def running_average():
    sum = 0.0
    count = 0
    value = yield (float('nan'))
    while True:
        sum += value
        count += 1
        value = yield (sum / count)


def render_yoy_growth_dict(yoy_growth_list: 'List') -> 'Dict':
    """Figure out the year-on-year growth using a running average of x years"""
    ravg = running_average()
    next(ravg)  # advance the coroutine to the first yield
    yoy_growth_ravg = [round(ravg.send(x), 4) for x in yoy_growth_list]
    return dict(zip(['Growth year ' + str(x + 1) for x in range(NR_OF_YRS_FOR_YOY_GROWTH_CALC)], yoy_growth_ravg))


def pnl_conversion():
    # Read the P&L copy-paste from the proff.no website
    clean_data = get_clean_pnl_data(gf.read_from_clipboard())
    clean_data.dropna().to_clipboard(index=False)  # Leave a P&L table in the clipboard as a bonus...
    pnl_distribution, yoy_growth = render_pnl_distribution(clean_data)

    # Write the dictionaries as a list to a JSON file
    file_name = gf.to_filename(sc.CUSTOMER_FOLDER_NAME, '-pnl-distribution.json')
    with open(sc.PATH_TO_CUSTOMER_DATA + '\\' + sc.CUSTOMER_FOLDER_NAME + '\\' + file_name, 'w') as fd:
        fd.write(json.dumps([pnl_distribution, render_yoy_growth_dict(yoy_growth)]))

        # gf.pretty_write_json(sc.PATH_TO_CUSTOMER_DATA + '\\' + sc.CUSTOMER_FOLDER_NAME + '\\' + file_name)

    # Export to screen
    pprint.pprint(pnl_distribution)
    pprint.pprint(render_yoy_growth_dict(yoy_growth))
    print(ppj.prettyjson(pnl_distribution, 4, 300))


def pnl_from_generator(invoices: 'Dataframe'):
    """Use pd.concat([df1, df2], ignore_index=True) to merge the sales and procurement invoice lists
    as well as all the lists across all years prior to running this"""
    
    NORM_AMOUNT_COL = 'Amount_On_Due_Date_[' + sc.ACCOUNTING_CURRENCY + ']'
    # yearly_totals = invoices.set_index('Invoice_Date').groupby(pd.Grouper(freq='Y'))[NORM_AMOUNT_COL].sum().reset_index()
    results = {'Category': [],
               '2018': []}

    for pnl_descriptor in sc.PNL_DESCRIPTORS:
        pnl_category = [k for k, v in sc.PNL_MAPPING.items() if v == pnl_descriptor]
        results['Category'].append(pnl_descriptor)
        for year in sc.YEARS:
            if len(pnl_category) > 0:
                scope = invoices[invoices.Category == pnl_category[0]][invoices.Invoice_Date.dt.year == int(year)]
                results[str(year)].append(scope[NORM_AMOUNT_COL].sum())
            else:
                results[str(year)].append(0.0)

    return results


if __name__ == "__main__":
    pnl_conversion()
