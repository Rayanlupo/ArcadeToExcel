import requests

token = "213edb5c-0a84-49f6-be66-f18d31e22400"
header = {'Authorization': f'Bearer {token}'}
response = requests.get("https://hackhour.hackclub.com/api/history/U074C9BE604", headers=header)
json_response = response.json()
data_list = json_response.get("data", [])
i = 0
sheet_id = "145fClGtHKTutKw0MtmuzNLdNBBoGQcgutOUJK9ry3JE"

while i < len(data_list):
    if response.status_code == 200:
        print("SESSION: ", i)
        #name
        if "work" in data_list[i]:
            name = data_list[i].get("work")
            print(name)

      
        #date
        if "createdAt" in data_list[i]:
            date = data_list[i].get("createdAt")
        
            date = date[:10]
            date = date.split("-")
            date = f"{date[1]}/{date[2]}/{date[0]}"
            print(date)
        i = i + 1
        if "ended" in data_list[i]:
            valiation = data_list[i].get("ended")
            
            print(valiation)
            
    else: 
        print("Error ", response.status_code)
 