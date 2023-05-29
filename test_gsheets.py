import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_pandas import *

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("private/gs_cred.json", scope)
client = gspread.authorize(credentials)

#sheet = client.create("WorkHistory")

#sheet.share('natali.atamanova1@gmail.com', perm_type='user', role='writer')

# Open the spreadsheet
#sheet = client.open("NewDatabase").sheet1
# read csv with pandas
#df = pd.read_csv('football_news')
# export df to a sheet
#sheet.update([df.columns.values.tolist()] + df.values.tolist())

sheet = client.open("workworkwork").sheet1

print(pd.DataFrame(sheet.get_all_records()))