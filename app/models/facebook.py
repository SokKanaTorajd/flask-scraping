from facebook_scraper import get_posts, get_profile

"""
This scripts is based on https://github.com/kevinzg/facebook-scraper
"""

class FacebookScraper():
    def scrape_profile(self, username):
        """
            Get facebook profile info. cannot get friend's count. 
            Arg: username. string format
            Returns facebook user's profile in dictionary format
        """
        profile = get_profile(username)
        return profile

    def scrape_page(self, page_name, timeout=30, with_comments=True, page=10, posts_per_page=10):
        """
            Desc: Get facebook page's post with its comments (if available).
            Args: 
                - page_name: the name or id of facebook page (Open Public). string format.
                - timeout: timeout count. default 30. don't make it too fast. integer format.
                - with_coments: default True. if True, it will also retrieve the post's comments. Boolean format.
                - page: set how many page we post we want to retrieve. default 10. Integer format.
                - posts_per_page: to request how many posts return in a single page. default 10 posts. Integer format.
            Returns page's post with limited amounts in Facebook_Scraper format.
        """
        posts = get_posts(page_name, page_limit=page, timeout=timeout, 
                            options={'comments': with_comments, 'posts_per_page':posts_per_page})
        return posts

    def scrape_group(self, group_name, timeout=30, with_comments=True, page=10, posts_per_page=10):
        """
            Desc: Get facebook group's post with its comments (if available).
            Args: 
                - group_name: the name or id of facebook group (Open Public). string format.
                - timeout: timeout count. default 30. don't make it too fast. integer format.
                - with_coments: default True. if True, it will also retrieve the post's comments. Boolean format.
                - page: set how many page we post we want to retrieve. default 10. Integer format.
                - posts_per_page: to request how many posts return in a single page. default 10 posts. Integer format.
            Returns page's post with limited amounts in Facebook_Scraper format.
        """
        posts = get_posts(group=group_name, page_limit=page, timeout=timeout, 
                            options={'comments': with_comments, 'posts_per_page':posts_per_page})
        return posts