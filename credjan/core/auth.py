from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd
from django.db import models
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Rtifl_TNKu92gfG2mUwNYUgzesDlSdKPmJtIeV6k8Rw'

creds = None
# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes #for the first time.

# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes #for the first time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()

df_dict = {}
properties = sheet_metadata.get('sheets')
for  item in properties:
    table = item.get('properties').get('title')
    df_dict[table] = pd.DataFrame()
    
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=table + '!A1:F').execute()
    header = result.get('values', [])[0]
    
    values = result.get('values', [])[1:] 
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                if col_id < len(row):
                    column_data.append(row[col_id])
                else:
                    column_data.append('')
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df_dict[table] = pd.concat(all_data, axis=1)

tables = {}
for table,df in df_dict.items():
    tables[table] = {}
    for i in range(0, df.shape[0]):
        attr = {}
        attr['default'] = 'None'
        if df['MAX LENGTH'][i] != '':
            attr['max_length'] = df['MAX LENGTH'][i]
        if df['KEY'][i] == 'primary key':
            attr['primary_key'] = 'True'
        tables[table][df['ATTRIBUTES'][i]] = [df['DATA TYPE'][i], attr]
print(tables)
def get_type(attr_type):
    if isinstance(attr_type, list):
        attr = attr_type[0] + 'Field('
        for k,v in attr_type[1].items():
            attr = attr + k + '=' + v + ','
        attr = attr[:-1]
        return(attr + (')\n'))
    else:
       return (attr_type + 'Field()\n')

get_type(attr_type=df)
script = 'from django.db import models\n'

for model,attributes in tables.items():
    script = script + "class " + model + "(models.Model):\n"
    for attr_name,attr_type in attributes.items():
        script = script + '\t' + attr_name + ' = models.' + get_type(attr_type)
               
root = 'E:/VS-CODE/Projects/credjan/core/'
file_name = root + 'models.py'
with open(file_name, "w") as py_file:
    print(py_file)
    py_file.write(script)

script = """from django.contrib import admin\n

from .models import *
"""


for model in tables.keys():
    script = script + "admin.site.register(" + model + ")\n"
script

file_name = root + 'admin.py'
with open(file_name, "w",encoding='utf-8') as py_file:
    py_file.write(script)