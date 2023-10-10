#----------------------------------------- import modules -----------------------------------------#

from setup import*
import instaloader

#----------------------------------------- scrapping functions -----------------------------------------#

# get info function: get how many post does an instagram account made
def get_info(username):
  bot = instaloader.Instaloader()
  profile = instaloader.Profile.from_username(bot.context, username)
  posts = profile.mediacount
  return posts

# get info function: get how many post does an instagram account made
def get_post(username):
  bot = instaloader.Instaloader()
  posts = instaloader.Profile.from_username(bot.context, username).get_posts()
  for post in posts:
    return(f"https://www.instagram.com/p/{post.shortcode}")
