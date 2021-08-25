import os

BROKER_URL = os.environ.get('CLOUDAMQP_URL')
MONGODB_URI = os.environ.get('MONGODB_URI')
BACKEND_URI = os.environ.get('BACKEND_URI')
DB_NAME = os.environ.get('DB_NAME')

IG_PROFILE_COLL = 'instagram-profile'
IG_PROFILE_POST_COLL = 'instagram-post'
IG_HASHTAG_POST_COLL = 'instagram-hashtag-post'

FB_PROFILE_COLL = 'facebook-profile'
FB_PAGE_POST_COLL = 'facebook-page-post'
FB_GROUP_POST_COLL = 'facebook-group-post'

IG_USERNAME = os.environ.get("IG_USER")
IG_PASS = os.environ.get('IG_PASS')
FB_EMAIL = os.environ.get('FB_EMAIL')
FB_PASS = os.environ.get('FB_PASS')