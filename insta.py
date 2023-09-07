import requests, json
import time

def get_info(username):
    print(username)
    account = requests.get(f'https://www.instagram.com/{username}')
    print("Posts" in account.text)
    if "Posts" in account.text:
        location = account.text.index("Posts")-8
        result=""
        for i in range(10):
            if account.text[location+i].isdigit():
                result = result + account.text[location+i]
        print(f"{username} made {result} post(s) for now")
        return int(result)

# while True:
#     get_info("la_potato_squad")
#     time.sleep(60) 
    