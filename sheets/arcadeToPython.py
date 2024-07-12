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
token = "YOUR_API_TOKEN_HERE"
header = {'Authorization': f'Bearer {token}'}
response = requests.get("https://hackhour.hackclub.com/api/history/YOUR_SLACK_ID", headers=header)
json_response = response.json()
data_list = json_response.get("data", [])
i = len(data_list) - 1  
row = 2  #row 1 is for the headers

sheet_id = "YOUR_SHEET_ID_HERE( you find it in the URL)"
sheet = client.open_by_key(sheet_id)
worksheet= sheet.sheet1
values_list = sheet.sheet1.row_values(1)

#Headers
worksheet.update_acell(f"A1","Name")
worksheet.update_acell(f"B1","Date")
worksheet.update_acell(f"C1","Goal")
worksheet.update_acell(f"D1","Minutes")
worksheet.update_acell(f"E1","Progres Bar")



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
            #get date
            date = data_list[i].get("createdAt")
            #format date
            date = date[:10]
            date = date.split("-")
            date = f"{date[2]}/{date[1]}/{date[0]}"
            print(date)
            #update date in the sheet
            worksheet.update_acell(f"B{row}",date)
            time.sleep(1)
            
        #goal
        if "goal" in data_list[i]:
            #get goal
            goal = data_list[i].get("goal")
            print(goal)
            #check if goal is "No Goal"
            if goal == "No Goal":
                goal = "/"
            else: 
                goal = goal
            #update goal in the sheet
            worksheet.update_acell(f"C{row}",goal)
            time.sleep(1)
        #minutes
        if  "elapsed" in data_list[i]:
            #get minutes
            minutes = data_list[i].get("elapsed")
            print(minutes)
            #update minutes in the sheet
            worksheet.update_acell(f"D{row}",minutes)
            time.sleep(1)
            #progress bar
            formule = f'=SPARKLINE(D{row}; {{"charttype" \ "bar"; "max" \ 60}})'
            worksheet.update_acell(f"E{row}",formule)
        #increment row and decrease i
        row = row + 1
        i = i - 1
    #if the response is not successful
    else: 
        print("Error ", response.status_code)