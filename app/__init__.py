from flask import Flask, jsonify, request
from flask_cors import CORS
from app.models.instagram import InstagramScraper
from app.models.dbmodel import MongoDBModel
from app.models.facebook import FacebookScraper
from app.models import config


app = Flask(__name__)
CORS(app)


db_name = 'kecilin-intern'
ig_profile = 'instagram-profile'
ig_post = 'instagram-post'
hashtag_post = 'hashtag-post'
fb_profile = 'facebook-profile'
group_post = 'facebook-group-post'
page_post = 'facebook-page-post'

mongo = MongoDBModel(db_name, URI=config.URI)
ig = InstagramScraper()
fb = FacebookScraper()

# index
@app.route('/')
def index():
    return "test scraping facebook dan instagram"


# get instagram profile
@app.route('/instagram/profile/<username>',methods=['GET'])
def profileIG(username):
    if request.method == 'GET':
        profile = ig.getProfileInfo(username)
        mongo.insertByOne(ig_profile, profile)

        return jsonify({'status': 'OK!'})


# get instagram profile post
@app.route('/instagram/post/<username>', methods=['GET'])
def profilePostIG(username):
    if request.method == 'GET':
        posts = ig.getProfilePost(username, limit=20)
        for post in posts:
            mongo.insertByOne(ig_post, post)

        return jsonify({'status': 'OK!'})


# get instagram hashtag post
@app.route('/instagram/post/hashtag/<hashtag_name>', method=['GET'])
def hashtagPostIG(hashtag_name):
    if request.method == 'GET':
        posts = ig.getHashtagPost(hashtag_name)
        for post in posts:
            comments = ig.getPostComments(post['shortcode'])
            post['comments'] = comments
            mongo.insertByOne(hashtag_post, post)
        
        return jsonify({'status': 'OK!'})


# get facebook profile info
@app.route('/facebook/profile/<username>', methods=['GET'])
def profileFB(username):
    if request.method == 'GET':
        profile = fb.scrape_profile(username)
        mongo.insertByOne(fb_profile, profile)
        
        return jsonify({'status': 'OK!'})


# get page post
@app.route('/facebook/page/<page_name>', methods=['GET'])
def pageFB(page_name):
    if request.method == 'GET':
        posts = fb.scrape_page(page_name, posts_per_page=5)
        for post in posts:
            mongo.insertByOne(page_post, post)

        return jsonify({'status': 'OK!'})


# get group post
@app.route('/facebook/group/<group_name>', methods=['GET'])
def pageFB(group_name):
    if request.method == 'GET':
        posts = fb.scrape_group(group_name, posts_per_page=5)
        for post in posts:
            mongo.insertByOne(page_post, post)

        return jsonify({'status': 'OK!'})
