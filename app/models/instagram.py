from datetime import datetime
from time import sleep
from app.models import config
import instaloader
from instaloader import Instaloader, Post, Profile

"""
This scripts is based on https://github.com/instaloader/instaloader.
"""

class InstagramScraper():
    loader = Instaloader()
    loader.login(config.IG_USERNAME, config.IG_PASS)
    # def loginInstaloader(username, password):
    #     return InstagramScraper.loader.login(username, password)

    def getProfileInfo(self, target_username):
        """
            - args:
                - target_username : username target untuk mengambil data profil. format str
            - output:
                - objek dictionary berisikan metadata profil target
        """
        profile = Profile.from_username(self.loader.context, target_username)
        sleep(10)
        data = {
            'userid': profile.userid, #str
            'username': profile.username, #str
            'biography' : profile.biography, #str
            'media_count' : profile.mediacount, #int
            'followers_count' : profile.followers, #int
            'following_count' : profile.followees, # int
            'profile_pic_url' : profile.profile_pic_url #str
        }
        return data

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
    

    def getProfilePost(self, target_username, limit=20):
        """
            - args:
                - target_username : username target untuk mengambil data postingan. format str
                - limit : batasan jumlah posting yang diambil dari akun target. default 20.
            - output:
                - objek list berisikan metadata postingan target
        """
        profile = Profile.from_username(self.loader.context, target_username)
        sleep(3)
        posts = profile.get_posts()
        posts_data = list()

        if len(posts_data) <= limit:
            for post in posts:
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
                sleep(3)

        return posts_data


    def getHashtagPost(self, hashtag_name, based_on='recent', post_limit=100):
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

        try:
            while hasNextPage and (len(hashtag_posts) <= post_limit):
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

                print('move to next page', datetime.now())
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
