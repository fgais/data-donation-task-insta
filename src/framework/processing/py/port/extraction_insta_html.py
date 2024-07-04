import pandas as pd
import zipfile
import json
from bs4 import BeautifulSoup
from port.helper import read_file_from_zip

def extract_followers_html(zip_file: str) -> pd.DataFrame:
    """
    extracts list of followers of the donor
    NOTE/TEST: for large followings, is there another file called e.g. followers_2.json?
    """
    df = pd.DataFrame()
    try:
        
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'connections/followers_and_following/followers_1.html')

        with file.open(path) as f:
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
    df = pd.DataFrame()
    try:
        
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'connections/followers_and_following/following.html')
        with file.open(path) as f:
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
    df = pd.DataFrame()
    try:
        
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/saved/saved_posts.html')

        with file.open(path) as f:
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
    df = pd.DataFrame()
    try:
        
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'preferences/your_topics/your_topics.html')
        with file.open(path) as f:
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
    data = []
    try:
        file = zipfile.ZipFile(zip_file)
        
        path = read_file_from_zip(file, 'your_instagram_activity/likes/liked_posts.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            liked_posts = soup.find_all('div', class_="_a6-p")
            liked_user_names = soup.find_all('div', class_="_3-95 _2pim _a6-h _a6-i")
            for idx, liked_post in enumerate(liked_posts):
                data.append(('liked_post', liked_post.find_all('div')[2].text.replace('\u202f',''), liked_user_names[idx].text, liked_post.find('a')['href']))

    except Exception as e:
        print(f"Something went wrong: {e}")

    try:
        file = zipfile.ZipFile(zip_file)
        path = read_file_from_zip(file, 'your_instagram_activity/likes/liked_comments.html')
        with file.open(path) as f:
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
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'personal_information/personal_information/personal_information.html')
        with file.open(path) as f:
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
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'personal_information/information_about_you/account_based_in.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            infos = soup.find_all('td', class_="_2pin _a6_q")
            location = infos[0].find('div').text
            data.append(('account_based_in', location))
            df = pd.DataFrame(data, columns = ['type', 'value'])
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_posts_viewed_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts posts seen by donor (data only covers last 2 weeks?)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/posts_viewed.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                try:
                    time = post.find('td', class_='_2pin _2piu _a6_r').text.replace('\u202f','')
                except:
                    time = None
                try:
                    user_name = post.find_all('div')[1].text
                except: 
                    user_name = None
                data.append(('post_seen',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_ads_viewed_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts ads viewed by donor (data only covers last 2 weeks?)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/ads_viewed.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                try:
                    time = post.find('td', class_='_2pin _2piu _a6_r').text.replace('\u202f','')
                except:
                    time = None
                try:
                    user_name = post.find_all('div')[1].text
                except: 
                    user_name = None
                    
                data.append(('ad_seen',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_ads_clicked_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts ads clicked by donor (data only covers last 2 weeks?)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/ads_clicked.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                try:
                    time = post.find_all('div')[1].text
                except:
                    time = None
                try:
                    user_name = post.find_all('div')[0].text
                except: 
                    user_name = None
                    
                data.append(('ad_clicked',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df


def extract_videos_watched_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts videos watched by donor (data only covers last 2 weeks?)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/videos_watched.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                try:
                    time = post.find('td', class_='_2pin _2piu _a6_r').text.replace('\u202f','')
                except:
                    time = None
                try:
                    user_name = post.find_all('div')[1].text
                except: 
                    user_name = None
                    
                data.append(('video_watched',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_suggested_acc_viewed_html(zip_file: str) -> pd.DataFrame:
    '''
    extracts suggested accounts viewed by donor (data only covers last 2 weeks?)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/suggested_accounts_viewed.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            posts = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
            for post in posts:
                try:
                    time = post.find('td', class_='_2pin _2piu _a6_r').text.replace('\u202f','')
                except:
                    time = None
                try:
                    user_name = post.find_all('div')[1].text
                except: 
                    user_name = None
                    
                data.append(('suggested_acc_viewed',time,user_name))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'from_user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_advertisers_using_info_html(zip_file: str) -> pd.DataFrame:
    '''
    extract advertisers using users' info in some way
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            advertisers = soup.find_all('tr', class_="_1isx")
            for adv in advertisers:
                user_name = adv.find('td').text
                data.append(('advertiser_using_info',user_name))
        df = pd.DataFrame(data, columns = ['type', 'user'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
    return df

def extract_ads_setting_html(zip_file: str) -> pd.DataFrame:
    '''
    extract whether (personalized?) ads are disabled
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/instagram_ads_and_businesses/subscription_for_no_ads.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            setting = soup.find('td', class_="_2piu _a6_r")
            status = setting.text
            data.append(('subscription_no_ads',status))
        df = pd.DataFrame(data, columns = ['type', 'status'])
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_account_searches_html(zip_file: str) -> pd.DataFrame:
    '''
    extract account searches (of last 2 weeks)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'logged_information/recent_searches/account_searches.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            accounts = soup.find_all('div', class_="_a6-p")
            for subset in accounts:
                x = subset.find('td', class_="_2pin _a6_q")
                acc = x.find('div').text
                time = subset.find('td', class_="_2pin _2piu _a6_r").text.replace('\u202f','')
                data.append(('account_searched',time,acc))
                
        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'user_name'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_word_or_phrase_searches_html(zip_file: str) -> pd.DataFrame:
    '''
    extract phrase searches (of last 2 weeks)
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'logged_information/recent_searches/word_or_phrase_searches.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            accounts = soup.find_all('div', class_="_a6-p")
            for subset in accounts:
                x = subset.find('td', class_="_2pin _a6_q")
                phrase = x.find('div').text
                time = subset.find('td', class_="_2pin _2piu _a6_r").text.replace('\u202f','')
                data.append(('phrase_searched',time,phrase))
                
        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'phrase'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_off_meta_activity_html(zip_file: str) -> pd.DataFrame:
    '''
    extract off-meta activity
    This is still untested
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'apps_and_websites_off_of_instagram/apps_and_websites/your_activity_off_meta_technologies.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            pages = soup.find_all('div', class_="_4-u2 _3-8x _4-u8")
            for page in pages:
                off_meta = page.text
                data.append(('off_meta_activity', off_meta))
        
        df = pd.DataFrame(data, columns = ['type', 'platform'])

    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_used_devices_html(zip_file: str) -> pd.DataFrame:
    '''
    extract used devices and last login with them
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'personal_information/device_information/devices.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            devices = soup.find_all('div', class_="_a6-p")
            for device in devices:
                last_login = device.find('td', class_="_2pin _2piu _a6_r").text.replace('\u202f','')
                dev = device.find_all('td', class_="_2pin _a6_q")[1].find('div').text
                data.append(('device_detected', last_login, dev))
                
        df = pd.DataFrame(data, columns = ['type', 'last_login', 'device'])

    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_login_activity_html(zip_file: str) -> pd.DataFrame:
    '''
    extract login activity
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'security_and_login_information/login_and_account_creation/login_activity.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            logins = soup.find_all('div', class_="_a6-p")
            for login in logins:
                time = login.find('td', class_="_2pin _2piu _a6_r").text
                via = login.find_all('td', class_="_2pin _a6_q")[4].find('div').text
                data.append(('login', time, via))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'via'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_post_comments_html(zip_file: str) -> pd.DataFrame:
    '''
    extract donor's comments on posts
    NOTE: untested
    '''    
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/comments/post_comments_1.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            comments = soup.find_all('div', class_="_a6-p")
            for comment in comments:
                try:
                    text = comment.find_all('td', class_="_2pin _a6_q")[0].find('div').text
                except:
                    text = None
                try:
                    media_owner = comment.find_all('td', class_="_2pin _a6_q")[1].find('div').text
                except:
                    media_owner = None
                try:
                    time = comment.find('td', class_="_2pin _2piu _a6_r").text
                except:
                    time = None
                data.append(('post_comment', time, text, media_owner))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'text', 'media_owner'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_reel_comments_html(zip_file: str) -> pd.DataFrame:
    '''
    extract donor's comments on reels
    NOTE: untested
    '''    
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/comments/reels_comments.html')
        with file.open(path) as f:
            soup = BeautifulSoup(f, 'html.parser')
            comments = soup.find_all('div', class_="_a6-p")
            for comment in comments:
                try:
                    text = comment.find_all('td', class_="_2pin _a6_q")[0].find('div').text
                except:
                    text = None
                try:
                    media_owner = comment.find_all('td', class_="_2pin _a6_q")[1].find('div').text
                except:
                    media_owner = None
                try:
                    time = comment.find('td', class_="_2pin _2piu _a6_r").text
                except:
                    time = None
                data.append(('reel_comment', time, text, media_owner))

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'text', 'media_owner'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df

def extract_links_shared_in_dms_html(zip_file: str) -> pd.DataFrame:
    '''
    extract links from dms
    '''
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/messages/inbox/')
        
        folders = file.namelist()
        subfolders = [file for file in folders if 'your_instagram_activity/messages/inbox/' in file]
        message_files = [file for file in subfolders if '.html' in file]
        for chat in message_files:
            with file.open(chat) as f:
                soup = BeautifulSoup(f, 'html.parser')
                messages = soup.find_all('div', class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
                conv_partner = chat.replace(path, '')
                conv_partner = conv_partner.replace('/message_1.html','')
                partner_name = soup.find('div', class_="_a705").find('div', class_="_a70e").text
                for message in messages:
                    try:
                        sender = message.find('div', class_="_3-95 _2pim _a6-h _a6-i").text
                        if sender == partner_name:
                            sender = 'other'
                        else:
                            sender = 'self'

                        links = message.find_all('a')
                        time = message.find('div', class_="_3-94 _a6-o").text.replace('\u202f', '')
                        for link in links:
                            data.append(('link_shared_in_dm', time, link.attrs['href'], sender, conv_partner))
                    except:
                        pass

        df = pd.DataFrame(data, columns = ['type', 'timestamp', 'link', 'sender', 'conversation_partner'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df