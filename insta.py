#----------------------------------------- import modules -----------------------------------------#

from setup import*
from selenium import webdriver
import requests, asyncio, nest_asyncio, pyppeteer
nest_asyncio.apply()

#----------------------------------------- scrapping functions -----------------------------------------#

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
    

# get post function: get the las post of any account      
async def get_post(user):
    pageurl = f"https://www.instagram.com/{username}"
    result = ""
    browser = await pyppeteer.launch({"headless": True}, executablePath= chrome_path)
    page = await browser.newPage()
    await page.goto(pageurl)
    await asyncio.sleep(2)
    cont = await page.content()
    await browser.close()
    if "/p/" not in cont:
        return ("An error has occured, please retry in a few minutes.")
    else:
        location = cont.index("/p/")
        for i in range(14):
            result = result + cont[location+i]
        return(f'https://www.instagram.com{result}/')
username = ""