#----------------------------------------- import modules -----------------------------------------#

from setup import*
import requests, asyncio, nest_asyncio, pyppeteer
nest_asyncio.apply()

#----------------------------------------- scrapping functions -----------------------------------------#

# get info function: get how many post does an instagram account made
def get_info(username):
    result=""
    account = requests.get(f'https://www.instagram.com/{username}')
    if "Posts" in account.text:
        location = account.text.index("Posts")-8
        for i in range(20):
            if account.text[location+i].isdigit():
                result = result + account.text[location+i]
        result = int(result)
        return result
    else:
        return None

# get info function: get how many post does an instagram account made

async def get_post(username):
    pageurl = f"https://www.instagram.com/{username}"
    result = ""
    browser = await pyppeteer.launch({"headless": False})
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

async def debug_pyppeteer():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await browser.close()
    return("debug pyppeteer succefuly executed !")
