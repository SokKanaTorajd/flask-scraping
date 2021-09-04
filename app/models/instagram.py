from datetime import datetime
from time import sleep
from app.models import config
import instaloader
from instaloader import Instaloader, Post, Profile

"""
This scripts is based on https://github.com/instaloader/instaloader.
"""

class InstagramScraper():

    def __init__(self):
        self.loader = Instaloader()


    def loginInstaloader(self, username, password):
        
        if self.loader.test_login() == username:
            filename = './app/models/{}_session'.format(username)
            return self.loader.load_session_from_file(username=username, filename=filename)

        if self.loader.test_login() != username:
            # login to instagram account
            self.loader.login(username, password)
            # save logged in session into file. 
            # format in requests.Session object, so there is no file extension.
            filename = './app/models/{}_session'.format(username)
            return self.loader.save_session_to_file(filename=filename)


    def getPostComments(self, shortcode, limit=50):
        """
            - args:
                - shortcode : kode postingan ig.
                - limit : batasan jumlah komentar yang diambil dalam satu postingan. default = 50.
            - output: 
                - objek list berisi metadata komentar sebuah postingan.
            - catatan:
                - limit dibuat 50 agar tidak terlalu banyak request dan mencegah terkena ban IP atau akun.
        """
        post = Post.from_shortcode(self.loader.context, shortcode)
        sleep(5)
        comments = post.get_comments()
        scraped_comments = list()
        for field in comments:
            if len(scraped_comments) <= limit:
                data = {
                    'comment_id' : field.id, #int
                    'username': field.owner.username, #str
                    'text': field.text, #str
                    'timestamp' : field.created_at_utc, #datetime in utc
                    'likes_count': field.likes_count, #int
                }
                scraped_comments.append(data)
        
        return scraped_comments
    

    def getProfilePost(self, target_username, limit=24):
        """
            - args:
                - target_username : username target untuk mengambil data postingan. format str
                - limit : batasan jumlah posting yang diambil dari akun target. default 24.
            - output:
                - objek list berisikan metadata postingan target
        """
        profile = Profile.from_username(self.loader.context, target_username)
        sleep(3)
        posts = profile.get_posts()
        posts_data = list()
        n = len(posts_data)

        for post in posts:
            if n <= limit:
                comments = self.getPostComments(post.shortcode)
                post_data = {
                    'shortcode' : post.shortcode, #str
                    'mediaid' : post.mediaid, #int
                    'post_owner' : post.owner_profile.username, #str
                    'caption' : post.caption, #str
                    'date_utc' : post.date_utc, #datetime in utc
                    'like_count' : post.likes, #int
                    'comment_count' : post.comments, #int
                    'comments' : comments # list
                }
                posts_data.append(post_data)
                n = len(posts_data)
                sleep(3)

        return posts_data


    def getHashtagPost(self, hashtag_name, based_on='recent', post_limit=120):
        """
            - args:
                - hashtag_name : nama hashtag dalam format string. tidak perlu menyertakan simbol '#'.
                - based_on : ambil data posting berdasarkan recent_media.
                - post_limit : batas untuk mendapatkan jumlah data posting maksimal untuk menghindari ban terhadap IP atau akun ig yang digunakan untuk scraping. default adalah 100.

            - output:
                - mengembalikan objek berupa list posting instagram berdasarkan pencarian hashtag.
            
            - notes:
                - jika request gagal karen kesalahan KeyError tetap mengembalikan data yang sudah diambil.
                
        """
        path = 'explore/tags/{}/'.format(hashtag_name)
        jsonData = self.loader.context.get_json(path=path, params={'__a': 1})
        hasNextPage = True
        hashtag_posts = list()
        n = len(hashtag_posts)

        try:
            while hasNextPage and (n < post_limit):
                for section in jsonData['data'][based_on]['sections']:
                    for post in section['layout_content']['medias']:
                        data = {
                            'shortcode' : post['media']['code'], #str
                            'mediaid' : post['media']['pk'], #int
                            'post_owner' : post['media']['user']['username'], #str
                            'caption' : post['media']['caption']['text'], #str
                            'date_utc' : datetime.utcfromtimestamp(post['media']['taken_at']), #datetime in utc
                            'like_count' : post['media']['like_count'], #int
                            'comment_count' : post['media']['comment_count'] #int
                        }
                        hashtag_posts.append(data)

                hasNextPage = jsonData['data'][based_on]['more_available']
                if hasNextPage:
                    jsonData = self.loader.context.get_json(
                        path=path, params={
                            '__a':1, 
                            'max_id': jsonData['data'][based_on]['next_max_id']
                        })
                        
                n = len(hashtag_posts)
                sleep(5)

            return hashtag_posts
        
        except KeyError as e:
            print('error terdeteksi. panjang data = {}'.format(len(hashtag_posts)))
            print(e)
            return hashtag_posts
        
        except instaloader.exceptions.QueryReturnedNotFoundException as not_found:
            return {'error' : {'message': not_found}}
        
        except instaloader.exceptions.ConnectionException as conn:
            return {'error' : {'message': conn}}
