import requests
import gspread
from google.oauth2.service_account import Credentials
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]


credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(credentials)
token = "213edb5c-0a84-49f6-be66-f18d31e22400"
header = {'Authorization': f'Bearer {token}'}
response = requests.get("https://hackhour.hackclub.com/api/history/U074C9BE604", headers=header)
json_response = response.json()
data_list = json_response.get("data", [])
i = len(data_list) - 1  
row = 1
sheet_id = "145fClGtHKTutKw0MtmuzNLdNBBoGQcgutOUJK9ry3JE"
sheet = client.open_by_key(sheet_id)
worksheet= sheet.sheet1
values_list = sheet.sheet1.row_values(1)



while i > 0:
    if response.status_code == 200:
        print("SESSION: ", i)
        #name
        if "work" in data_list[i]:
            name = data_list[i].get("work")
            print(name)
            worksheet.update_acell(f"A{row}",name)
      
        #date
        if "createdAt" in data_list[i]:
            date = data_list[i].get("createdAt")
        
            date = date[:10]
            date = date.split("-")
            date = f"{date[1]}/{date[2]}/{date[0]}"
            print(date)
       
        if "ended" in data_list[i]:
            valiation = data_list[i].get("ended")
            
            print(valiation)
        row = row + 1
        i = i - 1
    else: 
        print("Error ", response.status_code)