# import datasheets
# import openpyxl
import pyexcel_ods
# import pyexcel as pe
from pprint import pprint
import json

if __name__ == "__main__":
    file_name = 'C:\\Users\\Francesco\\Documents\\tests\\siren-tests\\siren-train-logs\\hyper-params-test.ods'
    data = pyexcel_ods.get_data(file_name)
    # print(json.dumps(data))
    pprint(data['Foglio1'])
    print(type(data['Foglio1']))

    print(data['Foglio1'][-2])

    pass