from flask import Flask, request, render_template, jsonify
from app.tasks.instagram_scraper import ig_profile, ig_user_post, ig_hashtag_post
from app.tasks.facebook_scraper import fb_profile, fb_page_post, fb_group_post
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# index
@app.route('/')
def index():
    return render_template('index.html')


# scraping instagram profile
@app.route('/instagram/profile',methods=['GET'])
def profileIG():
    if request.method == 'GET':
        username = request.form['username']
        scraped = ig_profile.delay(username)
        feedback = {'target_profile': username, 
                    'sosmed': 'instagram',
                    'task_id': scraped.id, 
                    'status': scraped.status}

        return jsonify(feedback)

# scraping instagram profile post
@app.route('/instagram/post', methods=['GET'])
def profilePostIG():
    if request.method == 'GET':
        username = request.form['username']
        user_post = ig_user_post.delay(username)
        feedback = {'post_target': username,
                    'sosmed': 'instagram', 
                    'task_id': user_post.id, 
                    'status': user_post.status}
        return jsonify(feedback)


# scraping instagram hashtag post
@app.route('/instagram/hashtag', methods=['GET'])
def hashtagPostIG():
    if request.method == 'GET':
        hashtag_name = request.form['hashtag']
        hashtag_post = ig_hashtag_post.delay(hashtag_name)
        feedback = {'target_hashtag': hashtag_name, 
                    'sosmed': 'instagram',
                    'task_id': hashtag_post.id, 
                    'status': hashtag_post.status}

        return jsonify(feedback)


# scraping facebook profile info
@app.route('/facebook/profile', methods=['GET'])
def profileFB():
    if request.method == 'GET':
        fb_username = request.form['username']
        profile = fb_profile.delay(fb_username)
        feedback = {'target_profile': fb_username, 
                    'sosmed': 'facebook',
                    'task_id': profile.id, 
                    'status': profile.status}

        return jsonify(feedback)

# scraping page post
@app.route('/facebook/page', methods=['GET'])
def pageFB(page_name):
    if request.method == 'GET':
        page_name = request.form['page']
        fb_page = fb_page_post.delay(page_name)
        feedback = {'target_page': page_name, 
                    'sosmed': 'facebook',
                    'task_id': fb_page.id, 
                    'status': fb_page.status}

        return jsonify(feedback)

# get group post
@app.route('/facebook/group', methods=['GET'])
def groupFB(group_name):
    if request.method == 'GET':
        group_name = request['group']
        fb_group = fb_group_post.delay(group_name)
        feedback = {'target_group': group_name, 
                    'sosmed': 'facebook',
                    'task_id': fb_group.id, 
                    'status': fb_group.status}

        return jsonify(feedback)