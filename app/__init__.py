from flask import Flask, request, render_template
from app.tasks.instagram_scraper import ig_profile, ig_user_post, ig_hashtag_post
from app.tasks.facebook_scraper import fb_profile, fb_page_post, fb_group_post
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# index
@app.route('/')
def index():
    return render_template('index.html')


# # get instagram profile
@app.route('/instagram/profile/<username>',methods=['GET'])
def profileIG(username):
    if request.method == 'GET':
        ig_profile.delay(username)
        return 'scraping instagram profile {} is in progress'.format(username)


# get instagram profile post
@app.route('/instagram/post/<username>', methods=['GET'])
def profilePostIG(username):
    if request.method == 'GET':
        ig_user_post.delay(username)
        return 'scraping instagram posts of {} is in progress.'.format(username)


# get instagram hashtag post
@app.route('/instagram/post/hashtag/<hashtag_name>', methods=['GET'])
def hashtagPostIG(hashtag_name):
    if request.method == 'GET':
        ig_hashtag_post.delay(hashtag_name)
        return 'scraping instagram posts of hashtag {} is in progress.'.format(hashtag_name)


# get facebook profile info
@app.route('/facebook/profile/<username>', methods=['GET'])
def profileFB(username):
    if request.method == 'GET':
        fb_profile.delay(username)
        return 'scraping facebook profile of {} is in progress.'.format(username)


# get page post
@app.route('/facebook/page/<page_name>', methods=['GET'])
def pageFB(page_name):
    if request.method == 'GET':
        fb_page_post.delay(page_name)
        return 'scraping facebook page posts of {} is in progress.'.format(page_name)


# get group post
@app.route('/facebook/group/<group_name>', methods=['GET'])
def groupFB(group_name):
    if request.method == 'GET':
        fb_group_post.delay(group_name)
        return 'scraping facebook group posts of {} is in progress.'.format(group_name)
