import pandas as pd
import zipfile
import json
from lxml import etree
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
            tree = etree.parse(f, etree.HTMLParser())
            
            single_followers = tree.xpath("//a")
            for follower in single_followers:
                parent_div = follower.getparent()
                date_div = parent_div.getnext()
                if date_div is not None and date_div.tag == 'div':
                    data.append(('follower', date_div.text, follower.text, follower.get('href')))

        df = pd.DataFrame(data, columns=["type", "timestamp", "user_name", "link"])
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
            tree = etree.parse(f, etree.HTMLParser())
            
            single_following = tree.xpath("//a")
            for following in single_following:
                parent_div = following.getparent()
                date_div = parent_div.getnext()
                if date_div is not None and date_div.tag == 'div':
                    data.append(('following', date_div.text, following.text, following.get('href')))

        df = pd.DataFrame(data, columns=["type", "timestamp", "user_name", "link"])
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
            tree = etree.parse(f, etree.HTMLParser())  # Load the tree in one line
            
            name_saved = tree.xpath("//div[contains(@class, '_3-95 _2pim _a6-h _a6-i')]")
            date_saved = tree.xpath("//td[contains(@class, '_2pin _2piu _a6_r')]")
            single_saved = tree.xpath("//a")

            for idx, saved in enumerate(single_saved):
                data.append(('saved_post', date_saved[idx].text, name_saved[idx].text, saved.text))

        df = pd.DataFrame(data, columns=["type", "timestamp", "user_name", "link"])
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
            tree = etree.parse(f, etree.HTMLParser())  # Load the tree in one line
            
            topics = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")

            for topic in topics:
                topic_name = topic.xpath(".//div/text()")
                if topic_name:
                    data.append(('assigned_topic', topic_name[0]))

        df = pd.DataFrame(data, columns=['type', 'name'])
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
            tree = etree.parse(f, etree.HTMLParser())
            liked_posts = tree.xpath("//div[contains(@class, '_a6-p')]")
            liked_user_names = tree.xpath("//div[contains(@class, '_3-95 _2pim _a6-h _a6-i')]")
            
            for idx, liked_post in enumerate(liked_posts):
                post_text = liked_post.xpath(".//div[2]//text()")
                user_name = liked_user_names[idx].text if liked_user_names[idx] is not None else ''
                post_link = liked_post.xpath(".//a//@href")
                
                if post_text and post_link:
                    data.append(('liked_post', post_text[0].replace('\u202f',''), user_name, post_link[0]))

    except Exception as e:
        print(f"Something went wrong with liked posts: {e}")

    try:
        path = read_file_from_zip(file, 'your_instagram_activity/likes/liked_comments.html')
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            liked_comments = tree.xpath("//div[contains(@class, '_a6-p')]")
            liked_comment_user_names = tree.xpath("//div[contains(@class, '_3-95 _2pim _a6-h _a6-i')]")
            
            for idx, liked_comment in enumerate(liked_comments):
                comment_text = liked_comment.xpath(".//div[2]//text()")
                user_name = liked_comment_user_names[idx].text if liked_comment_user_names[idx] is not None else ''
                comment_link = liked_comment.xpath(".//a//@href")
                
                if comment_text and comment_link:
                    data.append(('liked_comment', comment_text[0].replace('\u202f',''), user_name, comment_link[0]))

    except Exception as e:
        print(f"Something went wrong with liked comments: {e}")            

    df = pd.DataFrame(data, columns=["type", "timestamp", "user_name", "link"])
    
    return df

def extract_account_setting_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'personal_information/personal_information/personal_information.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            infos = tree.xpath("//td[contains(@class, '_2pin _a6_q')]")
            
            for info in infos:
                if info.text.strip() == 'Private Account':
                    private_settings = info.xpath(".//div//text()")
                    if private_settings:
                        data.append(('account_private', private_settings[0]))

        df = pd.DataFrame(data, columns=['type', 'value'])
    
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
            tree = etree.parse(f, etree.HTMLParser())
            infos = tree.xpath("//td[contains(@class, '_2pin _a6_q')]")
            
            if infos:
                location = infos[0].xpath(".//div//text()")
                if location:
                    data.append(('account_based_in', location[0]))

        df = pd.DataFrame(data, columns=['type', 'value'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_posts_viewed_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/posts_viewed.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            posts = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")
            
            for post in posts:
                try:
                    time = post.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                try:
                    user_name = post.xpath(".//div[1]//div//text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('post_seen', time, user_name))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'from_user'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_ads_viewed_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/ads_viewed.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            posts = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")
            
            for post in posts:
                try:
                    time = post.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                try:
                    user_name = post.xpath(".//div[1]//div//text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('ad_seen', time, user_name))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'from_user'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_ads_clicked_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/ads_clicked.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            posts = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")
            
            for post in posts:
                try:
                    time = post.xpath(".//div[1]//div//text()")
                    time = time[0] if time else None
                except:
                    time = None
                
                try:
                    user_name = post.xpath(".//div//text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('ad_clicked', time, user_name))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'from_user'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_videos_watched_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/videos_watched.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            posts = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")
            
            for post in posts:
                try:
                    time = post.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]/text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                try:
                    user_name = post.xpath(".//div[1]/div/text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('video_watched', time, user_name))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'from_user'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_suggested_acc_viewed_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/ads_and_topics/suggested_accounts_viewed.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            posts = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]")
            
            for post in posts:
                try:
                    time = post.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                try:
                    user_name = post.xpath(".//div[1]//div//text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('suggested_acc_viewed', time, user_name))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'user_name'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_advertisers_using_info_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            advertisers = tree.xpath("//tr[contains(@class, '_1isx')]")
            
            for adv in advertisers:
                try:
                    user_name = adv.xpath(".//td//text()")
                    user_name = user_name[0] if user_name else None
                except:
                    user_name = None
                
                data.append(('advertiser_using_info', user_name))

        df = pd.DataFrame(data, columns=['type', 'user'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_ads_setting_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'ads_information/instagram_ads_and_businesses/subscription_for_no_ads.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            setting = tree.xpath("//td[contains(@class, '_2piu _a6_r')]/text()")
            status = setting[0] if setting else None
            data.append(('subscription_no_ads', status))
        
        df = pd.DataFrame(data, columns=['type', 'status'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_account_searches_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'logged_information/recent_searches/account_searches.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            accounts = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for subset in accounts:
                try:
                    acc = subset.xpath(".//td[contains(@class, '_2pin _a6_q')]//div//text()")
                    acc = acc[0] if acc else None
                except:
                    acc = None
                
                try:
                    time = subset.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                data.append(('account_searched', time, acc))
        
        df = pd.DataFrame(data, columns=['type', 'timestamp', 'user_name'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_word_or_phrase_searches_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'logged_information/recent_searches/word_or_phrase_searches.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            searches = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for subset in searches:
                try:
                    phrase = subset.xpath(".//td[contains(@class, '_2pin _a6_q')]//div//text()")
                    phrase = phrase[0] if phrase else None
                except:
                    phrase = None
                
                try:
                    time = subset.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0].replace('\u202f', '') if time else None
                except:
                    time = None
                
                data.append(('phrase_searched', time, phrase))
        
        df = pd.DataFrame(data, columns=['type', 'timestamp', 'phrase'])
    
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_off_meta_activity_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'apps_and_websites_off_of_instagram/apps_and_websites/your_activity_off_meta_technologies.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            pages = tree.xpath("//div[contains(@class, '_4-u2 _3-8x _4-u8')]")
            
            for page in pages:
                off_meta = page.xpath(".//text()")
                off_meta = ''.join(off_meta).strip() if off_meta else None
                data.append(('off_meta_activity', off_meta))
        
        df = pd.DataFrame(data, columns=['type', 'platform'])

    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_used_devices_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'personal_information/device_information/devices.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            devices = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for device in devices:
                try:
                    last_login = device.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    last_login = last_login[0].replace('\u202f', '') if last_login else None
                except:
                    last_login = None
                
                try:
                    dev = device.xpath(".//td[contains(@class, '_2pin _a6_q')][1]//div//text()")
                    dev = dev[0] if dev else None
                except:
                    dev = None
                
                data.append(('device_detected', last_login, dev))
        
        df = pd.DataFrame(data, columns=['type', 'last_login', 'device'])

    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_login_activity_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'security_and_login_information/login_and_account_creation/login_activity.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            logins = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for login in logins:
                try:
                    time = login.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0] if time else None
                except:
                    time = None
                
                try:
                    via = login.xpath(".//td[contains(@class, '_2pin _a6_q')]//text()")[8]
                except:
                    via = None
                
                data.append(('login', time, via))
        
        df = pd.DataFrame(data, columns=['type', 'timestamp', 'via'])

    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_post_comments_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/comments/post_comments_1.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            comments = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for comment in comments:
                try:
                    text = comment.xpath(".//td[contains(@class, '_2pin _a6_q')][1]//div//text()")
                    text = text[0] if text else None
                except:
                    text = None
                
                try:
                    media_owner = comment.xpath(".//td[contains(@class, '_2pin _a6_q')][1]//div//text()")
                    media_owner = media_owner[1] if media_owner else None
                except:
                    media_owner = None
                
                try:
                    time = comment.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0] if time else None
                except:
                    time = None
                
                data.append(('post_comment', time, text, media_owner))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'text', 'media_owner'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")
    
    return df

def extract_reel_comments_html(zip_file: str) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        path = read_file_from_zip(file, 'your_instagram_activity/comments/reels_comments.html')
        
        with file.open(path) as f:
            tree = etree.parse(f, etree.HTMLParser())
            comments = tree.xpath("//div[contains(@class, '_a6-p')]")
            
            for comment in comments:
                try:
                    text = comment.xpath(".//td[contains(@class, '_2pin _a6_q')][1]//div//text()")
                    text = text[0] if text else None
                except:
                    text = None
                
                try:
                    media_owner = comment.xpath(".//td[contains(@class, '_2pin _a6_q')][1]//div//text()")
                    media_owner = media_owner[1] if media_owner else None
                except:
                    media_owner = None
                
                try:
                    time = comment.xpath(".//td[contains(@class, '_2pin _2piu _a6_r')]//text()")
                    time = time[0] if time else None
                except:
                    time = None
                
                data.append(('reel_comment', time, text, media_owner))

        df = pd.DataFrame(data, columns=['type', 'timestamp', 'text', 'media_owner'])
        
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
            try:
                chat_path = read_file_from_zip(file, chat)
                with file.open(chat_path) as f:
                    tree = etree.parse(f, etree.HTMLParser())

                    messages = tree.xpath("//div[contains(@class, 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder')]") 
                    conv_partner = chat.replace(path, '')
                    conv_partner = conv_partner.replace('/message_1.html','')
                    partner_name = tree.xpath("//div[contains(@class, '_a705')]//div[contains(@class, '_a70e')]//text()")[0]
                    for message in messages:
                        try:
                            sender = message.xpath(".//div[contains(@class, '_3-95 _2pim _a6-h _a6-i')]//text()")[0]
                            if sender == partner_name:
                                sender = 'other'
                            else:
                                sender = 'self'

                            links = message.xpath(".//a")
                            time = message.xpath(".//div[contains(@class, '_3-94 _a6-o')]//text()")[0].replace('\u202f', '')

                            for link in links:
                                data.append(('link_shared_in_dm', time, link.attrib['href'], sender, conv_partner))
                        except Exception as e:
                            print(e)
            except:
                pass

            df = pd.DataFrame(data, columns = ['type', 'timestamp', 'link', 'sender', 'conversation_partner'])
        
    except Exception as e:
        print(f"Something went wrong: {e}")   
        
    return df