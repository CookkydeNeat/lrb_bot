#----------------------------------------- import modules -----------------------------------------#

from setup import*
from selenium import webdriver
import requests, asyncio, nest_asyncio, time
nest_asyncio.apply()

#----------------------------------------- scrapping functions -----------------------------------------#

# INSTA_URL = 

# get info function: get how many post does an instagram account made
def get_info(username):
    account = requests.get(f'https://www.instagram.com/{username}')
    if "Posts" in account.text:
        location = account.text.index("Posts")-8
        result=""
        for i in range(10):
            if account.text[location+i].isdigit():
                result = result + account.text[location+i]
        return int(result)
    else:
        return float("inf")
    

# get post function: get the las post of any account      
async def get_post(user):
    url = f"https://www.instagram.com/{user}"
    result = ""
<<<<<<< HEAD
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    if "/p/" not in html:
=======
    browser = await pyppeteer.launch(headless=True)
    page = await browser.newPage()
    await page.goto(pageurl)
    await asyncio.sleep(1)
    cont = await page.content()
    await browser.close()
    if "/p/" not in cont:
        print(f"Unable to retrieve post count for {username}")
<<<<<<< HEAD
>>>>>>> 5fe87268faa8e50f64e6c82e2a704c0309993219
=======
>>>>>>> 5fe87268faa8e50f64e6c82e2a704c0309993219
        return ("An error has occured, please retry in a few minutes.")
    else:
        location = html.index("/p/")
        for i in range(14):
            result = result + html[location+i]
        return(f'https://www.instagram.com{result}/')
        
    




