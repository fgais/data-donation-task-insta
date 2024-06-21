import pandas as pd
import zipfile
import json
from bs4 import BeautifulSoup

def extract_followers_html(zip_file: str) -> pd.DataFrame:
    """
    extracts list of followers of the donor
    NOTE/TEST: for large followings, is there another file called e.g. followers_2.json?
    """
    try:
        df = pd.DataFrame()
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('connections/followers_and_following/followers_1.html') as f:
            soup = BeautifulSoup(f, 'html.parser')

            all_followers = soup.find_all("div", class_="_a706")
            single_followers = soup.find_all('a')

            for follower in single_followers:
                parent_div = follower.find_parent('div')
                date_div = parent_div.find_next_sibling('div')
                data.append(('follower', date_div.text, follower.text, follower['href']))

        df = pd.DataFrame(data, columns=["type","timestamp","user_name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_following_html(zip_file: str) -> pd.DataFrame:
    """
    extracts list of users that the donor follows
    NOTE: What about the keys?
    """
    try:
        df = pd.DataFrame()
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('connections/followers_and_following/following.html') as f:
            soup = BeautifulSoup(f, 'html.parser')

            all_following = soup.find_all("div", class_="_a706")
            single_following = soup.find_all('a')

            for following in single_following:
                parent_div = following.find_parent('div')
                date_div = parent_div.find_next_sibling('div')
                data.append(('following', date_div.text, following.text, following['href']))

        df = pd.DataFrame(data, columns=["type","timestamp","user_name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_saved_posts_html(zip_file: str) -> pd.DataFrame:
    """
    extracts list of saved posts of the donor
    """
    try:
        df = pd.DataFrame()
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('your_instagram_activity/saved/saved_posts.html') as f:
            soup = BeautifulSoup(f, 'html.parser')

            name_saved = soup.find_all("div", class_="_3-95 _2pim _a6-h _a6-i")
            date_saved = soup.find_all('td', class_ = "_2pin _2piu _a6_r")
            single_saved = soup.find_all('a')
            for idx, saved in enumerate(single_saved):
                data.append(('saved_post', date_saved[idx].text, name_saved[idx].text, saved.text))

        df = pd.DataFrame(data, columns=["type","timestamp","user_name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_your_topics_html(zip_file: str) -> pd.DataFrame:
    """
    extracts topics Instagram thinks the donor is interested in
    """
    try:
        df = pd.DataFrame()
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('preferences/your_topics/your_topics.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            topics = soup.find_all('div', class_="_a6-p")
            for topic in topics:
                data.append(('assigned_topic', topic.find('div').text))

            df = pd.DataFrame(data, columns = ['type', 'name'])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_likes_html(zip_file: str) -> pd.DataFrame:
    """
    extracts user's liked comments and posts
    NOTE/TEST: Are liked posts and comments all you can like?
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('your_instagram_activity/likes/liked_posts.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            liked_posts = soup.find_all('div', class_="_a6-p")
            liked_user_names = soup.find_all('div', class_="_3-95 _2pim _a6-h _a6-i")
            for idx, liked_post in enumerate(liked_posts):
                data.append(('liked_post', liked_post.find_all('div')[2].text.replace('\u202f',''), liked_user_names[idx].text, liked_post.find('a')['href']))

    except Exception as e:
        print(f"Something went wrong: {e}")

    try:
        file = zipfile.ZipFile(zip_file)
        with file.open('your_instagram_activity/likes/liked_comments.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            liked_comments = soup.find_all('div', class_="_a6-p")
            liked_comment_user_names = soup.find_all('div', class_="_3-95 _2pim _a6-h _a6-i")
            for idx, liked_comment in enumerate(liked_comments):
                data.append(('liked_comment', liked_comment.find_all('div')[2].text.replace('\u202f',''), liked_comment_user_names[idx].text, liked_comment.find('a')['href']))

    except Exception as e:
        print(f"Something went wrong: {e}")            

    df = pd.DataFrame(data, columns=["type","timestamp","user_name","link"])
    
    return df

def extract_account_setting_html(zip_file: str) -> pd.DataFrame:
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('personal_information/personal_information/personal_information.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            infos = soup.find_all('td', class_="_2pin _a6_q")
            for info in infos:
                if info.contents[0] == 'Private Account':
                    private_settings = info.find('div').text
                    data.append(('account_private', private_settings))
            infos = []
            df = pd.DataFrame(data, columns = ['type', 'value'])
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_account_location_html(zip_file: str) -> pd.DataFrame:
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('personal_information/information_about_you/account_based_in.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            infos = soup.find_all('td', class_="_2pin _a6_q")
            location = infos[0].find('div').text
            data.append(('account_based_in', location))
            df = pd.DataFrame(data, columns = ['type', 'value'])
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_posts_seen_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts posts seen by donor (data only covers last 2 weeks?)
    '''
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('ads_information/ads_and_topics/posts_viewed.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                time = post.find('td', class_='_2pin _2piu _a6_r').text.replace('\u202f','')
                user_name = post.find_all('div')[1].text
                data.append(('post_seen',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

    