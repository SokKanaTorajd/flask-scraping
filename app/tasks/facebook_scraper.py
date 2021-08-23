from app.models.facebook import FacebookScraper
from app.models.dbmodel import MongoDBModel
from app.models import config
from app.tasks import worker


mongo = MongoDBModel(config.DB_NAME, config.MONGODB_URI)
fb = FacebookScraper()

@worker.task(name='facebook_scraper.fb_profile')
def fb_profile(username):
    profile = fb.scrape_profile(username)
    profile['username'] = username
    mongo.insertByOne(config.FB_PROFILE_COLL, profile)
    return 'scraping facebook profile: {}, succeeded.'.format(username)

@worker.task(name='facebook_scraper.fb_page_post')
def fb_page_post(page_name):
    posts = fb.scrape_page(page_name)
    for post in posts:
        mongo.insertByOne(config.FB_PAGE_POST_COLL, post)
    return 'scraping facebook page post: {}, succeeded.'.format(page_name)

@worker.task(name='facebook_scraper.fb_group_post')
def fb_group_post(group_name):
    posts = fb.scrape_group(group_name)
    for post in posts:
        mongo.insertByOne(config.FB_GROUP_POST_COLL, post)
    return 'scraping facebook group post: {}, succeeded.'.format(group_name)
    
