from app.models.instagram import InstagramScraper
from app.models.dbmodel import MongoDBModel
from app.models import config
from app.tasks import worker
from time import sleep


mongo = MongoDBModel(config.DB_NAME, config.MONGODB_URI)
ig = InstagramScraper()

@worker.task(name='instagram_scraper.ig_profile')
def ig_profile(username):
    profile = ig.getProfileInfo(username)
    mongo.insertByOne(config.IG_PROFILE_COLL, profile)
    return 'scraping instagram profile: {}, succeeded.'.format(username)

@worker.task(name='instagram_scraper.ig_user_post')
def ig_user_post(username):
    posts = ig.getProfilePost(username)
    for post in posts:
        mongo.insertByOne(config.IG_PROFILE_POST_COLL, post)
    return 'scraping instagram user post: {}, succeeded.'.format(username)

@worker.task(name='instagram_scraper.ig_hashtag_post')
def ig_hashtag_post(hashtag):
    posts = ig.getHashtagPost(hashtag)
    sleep(10)
    for post in posts:
        comments = ig.getPostComments(post['shortcode'])
        post['comments'] = comments
        mongo.insertByOne(config.IG_HASHTAG_POST_COLL, post)

    return 'scraping instagram hashtag post: {}, succeeded.'.format(hashtag)

