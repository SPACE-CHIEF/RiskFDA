import pandas as pd
import json
import requests
import numpy
import time

DATAPATH = 'C:/Users/Robert/Downloads/Citations_InspectionsDataMerged_v4.csv'


def load_data(path):
    df = pd.read_csv(path)
    return df


inspections_citations = load_data(DATAPATH)


list_urls = ['https://api.fda.gov/drug/ndc.json?count=openfda.manufacturer_name.exact', 'https://api.fda.gov/drug/label.json?search=effective_time:[20040101+20190705]&count=openfda.manufacturer_name.exact', 'https://api.fda.gov/drug/enforcement.json?count=recalling_firm.exact', 'https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20190705]&count=patient.drug.openfda.manufacturer_name.exact']
list_of_names = []
def get_facilities(urls):
    response1 = requests.get(urls[0])
    response2 = requests.get(urls[1])
    response3 = requests.get(urls[2])
    response4 = requests.get(urls[3])

    # Print the status of the response code
    print(response1.status_code)
    print(response2.status_code)
    print(response3.status_code)
    print(response4.status_code)
    # Match the API contents to the contents on the
    json_res1 = response1.json()
    json_res2 = response2.json()
    json_res3 = response3.json()
    json_res4 = response4.json()
    for result in range(len(json_res1['results'])):
        list_of_names.append(json_res1['results'][result]['term'])
    for result in range(len(json_res2['results'])):
        list_of_names.append(json_res2['results'][result]['term'])
    for result in range(len(json_res3['results'])):
        list_of_names.append(json_res3['results'][result]['term'])
    for result in range(len(json_res4['results'])):
        list_of_names.append(json_res4['results'][result]['term'])


get_facilities(list_urls)


inspections_citations_list = list(inspections_citations['Legal Name'])

nf = [x for x in inspections_citations_list if x in list_of_names]

print(len(nf))

final_df = inspections_citations[inspections_citations['Legal Name'].isin(nf)]
print(final_df)



"""Get the address of a facility """
base_point = 'https://api.fda.gov/drug/enforcement.json?search=recalling_firm.exact:'
end_point = '&count=address_1.exact'
def get_address(base, end):
    addresses = []
    for facility_name in nf:
        full_query = base + '"' + facility_name + '"' + end
        print(full_query)
        response = requests.get(full_query)
        json_res = response.json()
        print(json_res)
        for result in range(len(json_res['results'])):
            addresses.append(json_res['results'][result]['term'])
        time.sleep(60)
            
    return addresses

addresses = get_address(base_point, end_point)

print(addresses)


final_df.to_csv('C:/Users/Robert/Desktop/risk_model.csv', index=False)