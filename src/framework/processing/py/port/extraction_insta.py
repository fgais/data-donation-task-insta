import pandas as pd
import zipfile
import json

def extract_account_setting(zip_file: str) -> pd.DataFrame:
    """
    extracts whether account is set to private
    NOTE: There's a German and English version depending on the download language...
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('personal_information/personal_information/personal_information.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            if 'Privates Konto' in json_file['profile_user'][0]['string_map_data']:
                data.append(("account_private",json_file['profile_user'][0]['string_map_data']['Privates Konto']['value']))
            elif 'Private account' in json_file['profile_user'][0]['string_map_data']:
                data.append(("account_private",json_file['profile_user'][0]['string_map_data']['Privates Konto']['value']))
            
            df = pd.DataFrame(data, columns=["type","setting"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df
def extract_likes(zip_file: str) -> pd.DataFrame:
    """
    extracts user's liked comments and posts
    NOTE/TEST: Are liked posts and comments all you can like?
    NOTE: What about the keys?
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('your_instagram_activity/likes/liked_posts.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for key in json_file.keys():
                for entry in json_file[key]:
                    data.append((key,entry['string_list_data'][0]['timestamp'], 
                        entry['title'],entry['string_list_data'][0]['href']))


    except Exception as e:
        print(f"Something went wrong: {e}")
        
    try:
        file = zipfile.ZipFile(zip_file)
        with file.open('your_instagram_activity/likes/liked_comments.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for key in json_file.keys():
                for entry in json_file[key]:
                    data.append((key,entry['string_list_data'][0]['timestamp'], entry['title'],
                                 entry['string_list_data'][0]['href']))
    except Exception as e:
        print(f"Something went wrong: {e}")
        
    df = pd.DataFrame(data, columns=["type","timestamp","user_name","link"])

    return df

def extract_following(zip_file: str) -> pd.DataFrame:
    """
    extracts list of users that the donor follows
    NOTE: What about the keys?
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('connections/followers_and_following/following.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for key in json_file.keys():
                for entry in json_file[key]:
                    data.append((key,entry['string_list_data'][0]['timestamp'], 
                        entry['string_list_data'][0]['value'],entry['string_list_data'][0]['href']))

            df = pd.DataFrame(data, columns=["type","timestamp","name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_followers(zip_file: str) -> pd.DataFrame:
    """
    extracts list of followers of the donor
    NOTE/TEST: for large followings, is there another file called e.g. followers_2.json?
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('connections/followers_and_following/followers_1.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for entry in json_file:
                data.append(("follower",entry['string_list_data'][0]['timestamp'], 
                    entry['string_list_data'][0]['value'],entry['string_list_data'][0]['href']))

            df = pd.DataFrame(data, columns=["type","timestamp","name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_your_topics(zip_file: str) -> pd.DataFrame:
    """
    extracts topics Instagram thinks the user is interested in
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('preferences/your_topics/your_topics.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for key in json_file.keys():
                for entry in json_file[key]:
                    data.append((key,entry['string_map_data']['Name']['value']))

            df = pd.DataFrame(data, columns=["type","topic"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_saved_posts(zip_file: str) -> pd.DataFrame:
    """
    extracts list of saved posts of the donor
    NOTE: What about the keys?
    """
    df = pd.DataFrame()
    try:
        file = zipfile.ZipFile(zip_file)
        data = []
        with file.open('your_instagram_activity/saved/saved_posts.json') as f:
            temp_file = f.read()
            json_file = json.loads(temp_file)
            for key in json_file.keys():
                for entry in json_file[key]:
                    data.append((key,entry['string_map_data']['Saved on']['timestamp'],entry['title'],
                        entry['string_map_data']['Saved on']['href']))

        df = pd.DataFrame(data, columns=["type","timestamp","name","link"])
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

