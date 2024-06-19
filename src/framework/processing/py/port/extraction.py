import pandas as pd
import zipfile
import json


def extract_favorites(zip_file: str) -> pd.DataFrame:
    """
    extract favorite effects, hashtags, sounds and videos and puts them into one table.
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        # videos
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                fav_video_history = json_file["Activity"]["Favorite Videos"]["FavoriteVideoList"]
                fav_effects_history = json_file["Activity"]["Favorite Effects"]["FavoriteEffectsList"]
                fav_hts_history = json_file["Activity"]["Favorite Hashtags"]["FavoriteHashtagList"]
                fav_sound_history = json_file["Activity"]["Favorite Sounds"]["FavoriteSoundList"]

                for entry in fav_video_history:
                    data.append(("favorite video",entry["Date"],entry["Link"]))
                for entry in fav_effects_history:
                    data.append(("favorite effect",entry["Date"],entry["EffectLink"]))
                for entry in fav_hts_history:
                    data.append(("favorite hashtag",entry["Date"],entry["Link"]))
                for entry in fav_sound_history:
                    data.append(("favorite sound",entry["Date"],entry["Link"]))

        df = pd.DataFrame(data, columns=["type","timestamp","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_follower(zip_file: str) -> pd.DataFrame:
    """
    extracts the list of users that follow the doner
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                follower_list = json_file["Activity"]["Follower List"]["FansList"]

                for entry in follower_list:
                    data.append(("followedby",entry["Date"], entry["UserName"]))

        df = pd.DataFrame(data, columns=["type","timestamp","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_following(zip_file: str) -> pd.DataFrame:
    """
    extracts the list of users that the doner is following
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                follower_list = json_file["Activity"]["Following List"]["Following"]

                for entry in follower_list:
                    data.append(("follow",entry["Date"], entry["UserName"]))

        df = pd.DataFrame(data, columns=["type","timestamp","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_used_hashtags(zip_file: str) -> pd.DataFrame:
    """
    extracts the list of users that the doner is following
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                ht_list = json_file["Activity"]["Hashtag"]["HashtagList"]

                for entry in ht_list:
                    data.append(("hashtag use",entry["HashtagName"], entry["HashtagLink"]))

        df = pd.DataFrame(data, columns=["type","hashtag","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_login_history(zip_file: str) -> pd.DataFrame:
    """
    extracts the list of users that the doner is following
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                ht_list = json_file["Activity"]["Login History"]["LoginHistoryList"]

                for entry in ht_list:
                    data.append(("login",entry["Date"], entry["DeviceModel"],entry["DeviceSystem"], entry["NetworkType"]))

        df = pd.DataFrame(data, columns=["type","timestamp","model","system","networktype"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_recent_location(zip_file: str) -> pd.DataFrame:
    """
    extracts the list of users that the doner is following
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                entry = json_file["Activity"]["Most Recent Location Data"]["LocationData"]
                data.append(("location",entry["Date"], entry["GpsData"],entry["LastRegion"]))

        df = pd.DataFrame(data, columns=["type","timestamp","gps","region"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_blocklist(zip_file: str) -> pd.DataFrame:
    """
    accounts that have been blocked
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                # watch history
                watch_history = json_file["App Settings"]["Block"]["BlockList"]

                for entry in watch_history:
                    data.append(("watch",entry["Date"], entry["UserName"]))

        df = pd.DataFrame(data, columns=["type","timestamp","username"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_app_settings(zip_file: str) -> pd.DataFrame:
    """
    accounts that have been blocked
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                # settings
                entry = json_file["App Settings"]["Settings"]["SettingsMap"]
                data.append(("personalized ads",entry["Personalized Ads"]))
                data.append(("app language",entry["App Language"]))
                data.append(("interests",entry["Interests"]))

        df = pd.DataFrame(data, columns=["type","value"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_posted_videos(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                # video history
                video_history = json_file["Video"]["Videos"]["VideoList"]

                for entry in video_history:
                    data.append(("watch",entry["Date"], entry["WhoCanView"],entry["Likes"]))

        df = pd.DataFrame(data, columns=["type","timestamp","view_settings","likes"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df



def extract_watchlist(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    df = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        data = []
        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                # watch history
                watch_history = json_file["Activity"]["Video Browsing History"]["VideoList"]

                for entry in watch_history:
                    data.append(("watch",entry["Date"], entry["Link"]))

        df = pd.DataFrame(data, columns=["type","timestamp","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_likes(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """

    try:
        file = zipfile.ZipFile(zip_file)
        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)

                # like history
                like_history = json_file["Activity"]["Like List"]["ItemFavoriteList"]

                if like_history != None:

                    for entry in like_history:
                        data.append(("like",entry["Date"],entry["Link"]))
        
        df = pd.DataFrame(data, columns=["type","timestamp","link"])

        print(df)
    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_shares(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # share history
                share_history = json_file["Activity"]["Share History"]["ShareHistoryList"]

                for entry in share_history:
                    data.append(("share",entry["Date"],entry["Link"],entry["SharedContent"], entry["Method"]))

        df = pd.DataFrame(data, columns=["type","timestamp","link","shared_content","method"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df




def extract_search(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # search_history
                search_history = json_file["Activity"]["Search History"]["SearchList"]

                for entry in search_history:
                    data.append(("search",entry["Date"],entry["SearchTerm"]))

        df = pd.DataFrame(data, columns=["type","timestamp","search_term"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_ads_info(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # ad_interests

                ad_interests = json_file["Ads and data"]["Ad Interests"]["AdInterestCategories"]
                if ad_interests != None:
                    data.append(["ads_interests", "-","-",ad_interests])

                off_tt_ad_activities = json_file["Ads and data"]["Off TikTok Activity"]["OffTikTokActivityDataList"]
                if off_tt_ad_activities != None:
                    for entry in off_tt_ad_activities:
                        data.append(("off_tt_ad_activitiy",entry["TimeStamp"],entry["Source"], entry["Event"]))

        df = pd.DataFrame(data, columns=["type","timestamp","source", "event"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_comments(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # comment_history
                comment_history = json_file["Comment"]["Comments"]["CommentsList"]

                for entry in comment_history:
                    data.append(("comment",entry["Date"],entry["Comment"], entry["Photo"],entry["Url"]))

        df = pd.DataFrame(data, columns=["type","timestamp","comment", "photo","url"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df


def extract_watch_live(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # watch_live_history
                watch_live_history = json_file["Tiktok Live"]["Watch Live History"]["WatchLiveMap"]


                for entry in watch_live_history:

                    watch_live_instance = watch_live_history[entry]

                    data.append(("watch_live",entry,watch_live_instance["WatchTime"],watch_live_instance["Link"], watch_live_instance["Questions"]))

        df = pd.DataFrame(data, columns=["type","id","timestamp","link", "questions"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df

def extract_watch_live_comments(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    try:
        file = zipfile.ZipFile(zip_file)

        data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
        
                # watch_live_history
                watch_live_history = json_file["Tiktok Live"]["Watch Live History"]["WatchLiveMap"]


                for entry in watch_live_history:

                    watch_live_instance = watch_live_history[entry]["Comments"]
                    for comment in watch_live_instance:

                        data.append(("watch_live_comment",entry,comment["CommentTime"],comment["CommentContent"], comment["RawTime"]))

        df = pd.DataFrame(data, columns=["type","id","timestamp","content", "rawtime"])


    except Exception as e:
        print(f"Something went wrong: {e}")

    return df