import pandas as pd
import requests
import io
import dash_table

url = "https://api.mockaroo.com/api/generate.csv"

querystring = {"key":"74cdb890","count":"4"}

payload = """[
    {
      "name": "Account",
      "null_percentage": 0,
      "type": "Currency Code",
      "formula": ""
    },
    {
      "name": "Balance",
      "null_percentage": 0,
      "type": "Money",
      "min": 10000,
      "max": 1000000,
      "symbol": "none",
      "formula": ""
    },
    {
      "name": "product_amount",
      "null_percentage": 0,
      "type": "Number",
      "min": 100,
      "max": 10000,
      "decimals": 0,
      "formula": ""
    }
    ]"""

headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "7452cb14-b0cc-4889-9097-6f15155ad0b9,8908d038-ab38-4158-8286-d682593e6a62",
    'Host': "api.mockaroo.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "694",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }




def fetchMockaroo():
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    data = pd.read_csv(io.StringIO(response.text))
    return data


def createTable(data):
    fetchMockaroo()
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
    )


print(fetchMockaroo())
