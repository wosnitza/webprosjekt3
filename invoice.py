import json
import pandas as pd

distribution_data = """[{
        "Headers": [
            "Total Revenue [NOK]",
            "Revenue",
            "COGS",
            "SG&A",
            "DA",
            "IntTax",
            "NetInc"
        ],
        "2014": [
            51922000.0,
            1.0,
            0.7943453642001463,
            0.16767458880628636,
            0.002792650514232888,
            0.014541042332729863,
            0.020646354146604522
        ],
        "2015": [
            69914000.0,
            1.0,
            0.8065480447406814,
            0.17003747461166577,
            0.0039191006093200215,
            0.007909717653116686,
            0.011585662385216123
        ],
        "2016": [
            101717000.0,
            1.0,
            0.8005249859905423,
            0.14880501784362496,
            0.005210535112124817,
            0.013232792945132082,
            0.03222666810857575
        ],
        "2017": [
            111853000.0,
            1.0,
            0.8229551286062957,
            0.14478824886234612,
            0.00728634904741044,
            0.011828024281869954,
            0.013142249202077728
        ],
        "2018": [
            112958000.0,
            1.0,
            0.7861948688893217,
            0.2194266895660334,
            0.007755094814001664,
            0.0032932594415623507,
            -0.010092246675755591
        ]
    },
    {
        "Growth year 1": 0.0996,
        "Growth year 2": 0.0548
    }]"""

with open("distribution.json", "r") as fd:
    pnl_distribution, yoy_growth_dict = json.load(fd)

barName = pnl_distribution.pop("Headers")

df = pd.DataFrame(pnl_distribution)


for key, value in df.items():
    value[1:] = value[1:] * value[0]


df = df.T
df.columns = barName
df.reset_index(level=0, inplace=True, col_fill="Year")
df.rename(columns={"index": "Year"}, inplace=True)


