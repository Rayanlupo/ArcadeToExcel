#required libraries
import requests
import gspread
from google.oauth2.service_account import Credentials
import time
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]


credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(credentials)
token = "YOUR_TOKEN"
header = {'Authorization': f'Bearer {token}'}
response = requests.get("https://hackhour.hackclub.com/api/history/USER_ID", headers=header)
json_response = response.json()
data_list = json_response.get("data", [])
i = len(data_list) - 1  
row = 1
sheet_id = "SHEET_ID(you find it in the URL)"
sheet = client.open_by_key(sheet_id)
worksheet= sheet.sheet1
values_list = sheet.sheet1.row_values(1)



while i > 0:
    #if the response is successful
    if response.status_code == 200: 
        #print session number
        print("SESSION: ", i)
        
        #name
        if "work" in data_list[i]:
            #get name
            name = data_list[i].get("work")
            print(name)
            worksheet.update_acell(f"A{row}",name)
            time.sleep(1) # 1 second pause to prevent API rate limit
      
        #date
        if "createdAt" in data_list[i]:
            date = data_list[i].get("createdAt")
        #format date
            date = date[:10]
            date = date.split("-")
            date = f"{date[1]}/{date[2]}/{date[0]}"
            print(date)
        #update date in the sheet
            worksheet.update_acell(f"B{row}",date)
            time.sleep(1)

        #finished or not
        if "ended" in data_list[i]:
            #get status
            end = data_list[i].get("ended")
            end = str(end)
            #check if it's finished or now 
            if end:
                end = "Finished"
            else:
                end = "Not Finished"
            #update date in the sheet
            worksheet.update_acell(f'D{row}', end)
            
            time.sleep(1)
            print(end)
        #goal
        if "goal" in data_list[i]:
            #get goal
            goal = data_list[i].get("goal")
            print(goal)
            #check if there is a goal
            if goal == "No Goal":
                goal = "/"
            else: 
                goal = goal
            #update goal in the sheet
            worksheet.update_acell(f"C{row}",goal)
            time.sleep(1)
        #increment row and  decrese i
        row = row + 1
        i = i - 1
    else: 
        print("Error ", response.status_code)