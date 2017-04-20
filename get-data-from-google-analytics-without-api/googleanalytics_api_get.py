# importing the requests library
# you can install any library with pip package using "pip install requests"
import requests
import json
import csv

# obtain "Access token:" in second step at https://developers.google.com/oauthplayground/
TOKEN = "ACCESS TOKEN HASH"
GA_ID = "ga:12345678"


# api-endpoint
URL = "https://www.googleapis.com/analytics/v3/data/mcf"

# defining a params dict for the parameters to be sent to the API
# https://developers.google.com/analytics/devguides/reporting/mcf/v3/reference
PARAMS = {     
    'ids': GA_ID,
    'metrics': 'mcf:totalConversions,mcf:totalConversionValue',
    'dimensions': 'mcf:sourceMediumPath',
    'start-date': '2017-04-01',
    'end-date': '2017-05-01',
    'max-results': 100 # maximal value is 10000
    }
headers = {'Authorization': 'Bearer ' + TOKEN}

# sending GET request and saving the response as response object
r = requests.get(url=URL, params=PARAMS, headers=headers)

# response status
print("Response status code: %s\n" % (r.status_code))

if (r.status_code == 200):

    # extracting data in json format
    data = r.json()

    # extracting parameters
    itemsPerPage = data['itemsPerPage']
    totalResults = data['totalResults']

    # printing the output
    print("Items per page: %s\nTotal results: %s\n" % (itemsPerPage, totalResults))

    employee_parsed = json.loads(r.text)
    rows = employee_parsed['rows']

    #emp_data = employee_parsed['employee_details']

    # open a file for writing
    file_data = open('output.csv', 'w', newline='')
    # create the csv writer object
    csvwriter = csv.writer(file_data)

    count = 0
    # formatting data into CSV format
    for row in rows:
        line = []
        path = row[0]['conversionPathValue']
        totalConversions = row[1]['primitiveValue']
        totalConversionsValue = row[2]['primitiveValue']
        if count == 0:
            headers = []
            headers.append('totalConversions')
            headers.append('totalConversionsValue')
            headers.append('conversionPathValue')
            csvwriter.writerow(headers)

        line.append(totalConversions)
        line.append(totalConversionsValue)
        for item in path:
            line.append(item['nodeValue'])

#        print("%s\t%s\t%s" % (path, totalConversions, totalConversionsValue))
        csvwriter.writerow(line)

        count += 1

    file_data.close()

