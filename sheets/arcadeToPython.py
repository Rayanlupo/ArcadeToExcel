#libraries
import requests
import gspread
from google.oauth2.service_account import Credentials
import time
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]


credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(credentials)
token = "YOUR_TOKEN_HERE"
header = {'Authorization': f'Bearer {token}'}
response = requests.get("https://hackhour.hackclub.com/api/history/USER_ID", headers=header)
json_response = response.json()
data_list = json_response.get("data", [])
i = len(data_list) - 1  
row = 1
sheet_id = "SHEET_ID_HERE"
sheet = client.open_by_key(sheet_id)
worksheet= sheet.sheet1
values_list = sheet.sheet1.row_values(1)


worksheet.update_acell(f"A1","Name")
worksheet.update_acell(f"B1","Date")
worksheet.update_acell(f"C1","Goal")
worksheet.update_acell(f"D1","Finished?")
worksheet.update_acell(f"E1","Minutes")
worksheet.update_acell(f"F1","Completed")


while i > 0:
    if response.status_code == 200:
        print("SESSION: ", i)
        #name
        if "work" in data_list[i]:
            name = data_list[i].get("work")
            print(name)
            worksheet.update_acell(f"A{row}",name)
            time.sleep(1) # 1 second pause to prevent API rate limit
      
        #date
        if "createdAt" in data_list[i]:
            date = data_list[i].get("createdAt")
        
            date = date[:10]
            date = date.split("-")
            date = f"{date[1]}/{date[2]}/{date[0]}"
            print(date)
            worksheet.update_acell(f"B{row}",date)
            time.sleep(1)
            
        #goal
        if "goal" in data_list[i]:
            #get goal
            goal = data_list[i].get("goal")
        
            print(goal)
            #check if there is a goal or not 
            if goal == "No Goal":
                goal = "/"
            else: 
                goal = goal
            worksheet.update_acell(f"C{row}",goal)
            time.sleep(1)
        #minutes
        if  "elapsed" in data_list[i]:
            #get minutes
            minutes = data_list[i].get("elapsed")
            print(minutes)
            #update value
            worksheet.update_acell(f"E{row}",minutes)
            time.sleep(1)
       
        row = row + 1
        i = i - 1
    else: 
        print("Error ", response.status_code)