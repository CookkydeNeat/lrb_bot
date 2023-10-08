#----------------------------------------- import modules -----------------------------------------#

from setup import*
import requests, asyncio, nest_asyncio, pyppeteer
nest_asyncio.apply()

#----------------------------------------- scrapping functions -----------------------------------------#

# get info function: get how many post does an instagram account made
def get_info(username):
  url = f"https://istoryv.com/v/{username}"
  result = ""
  account = requests.get(url)
  if account.status_code == 200:
    if "Posts" in account.text:
      location = account.text.index("Posts") - 8
      for i in range(10):
        if account.text[location + i].isdigit():
          result = result + account.text[location + i]
      result = int(result)
      return result
    else:
      return "failed"
  else:
    return "failed"

# get info function: get how many post does an instagram account made
async def get_post(username):
  url = f"https://storiesdown.com/?ig={username}"
  result = ""
  account = requests.get(url)
  if account.status_code == 200:
    if "/p/" in account.text:
      location = account.text.index("/p/")
      for i in range(14):
        result = result + account.text[location + i]
      return (f"https://www.instagram.com{result}")
    else:
      return "failed"
  else:
    return "failed"
username = ""

async def debug_pyppeteer():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await browser.close()
    return("debug pyppeteer succefuly executed !")

def debug_request():
    account = requests.get(f'https://www.instagram.com/{username}')
    print(account)
    return("debug request succefuly executed !") 
