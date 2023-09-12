import requests



def get_info(username):
    def wrapper():
        print(f"Checking user {username}...")
        account = requests.get(f"https://www.instagram.com/{username}")
        print("Posts" in account.text)
        if "Posts" in account.text:
            location = account.text.index("Posts") - 8
            result = ""
            for i in range(10):
                if account.text[location + i].isdigit():
                    result = result + account.text[location + i]
            print(f"{username} made {result} post(s) for now")
            return int(result)
    return wrapper

