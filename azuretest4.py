import requests
import json
from tabulate import tabulate 


def build_pricing_table(json_data, table_data):
    for item in json_data['Items']:
        meter = item['meterName']
        if 'Spot' in meter or 'Low Priority' in meter:
            continue
        table_data.append([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], meter, item['productName']])
        
def main():
    table_data = []
    table_data.append(['SKU', 'Retail Price', 'Unit of Measure', 'Region', 'Meter', 'Product Name'])
    
    #api_url = "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview"
    api_url="https://prices.azure.com/api/retail/prices"
    query = "armRegionName eq 'westus2' and armSkuName eq 'Standard_E2a_v4' and priceType eq 'Consumption'"
    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)
    
    build_pricing_table(json_data, table_data)
    nextPage = json_data['NextPageLink']
    
    while(nextPage):
        response = requests.get(nextPage)
        json_data = json.loads(response.text)
        nextPage = json_data['NextPageLink']
        build_pricing_table(json_data, table_data)

    print(tabulate(table_data, headers='firstrow', tablefmt='psql'))
    
if __name__ == "__main__":
    main()