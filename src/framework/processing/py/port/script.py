import port.api.props as props
from port.api.commands import (CommandSystemDonate, CommandUIRender, CommandSystemExit)

import pandas as pd
import zipfile
import json

import port.extraction_insta_html_lxml as extraction_insta_html


def process(session_id: str):
    #platform = "TikTok"
    platform = "Instagram"

    # Start of the data donation flow
    while True:
        # Ask the participant to submit a file
        file_prompt = generate_file_prompt(platform, "application/zip, text/plain")
        file_prompt_result = yield render_page(platform, file_prompt)

        # If the participant submitted a file: continue
        if file_prompt_result.__type__ == 'PayloadString':

            # Validate the file the participant submitted
            # In general this is wise to do 
            is_data_valid = validate_the_participants_input(file_prompt_result.value)

            # Happy flow:
            # The file the participant submitted is valid
            if is_data_valid == True:

                # Extract the data you as a researcher are interested in, and put it in a pandas DataFrame
                # Show this data to the participant in a table on screen
                # The participant can now decide to donate
                extracted_ads_viewed = extraction_insta_html.extract_ads_viewed_html(file_prompt_result.value)
                extracted_posts_viewed = extraction_insta_html.extract_posts_viewed_html(file_prompt_result.value)
                extracted_ads_clicked = extraction_insta_html.extract_ads_clicked_html(file_prompt_result.value)
                extracted_suggested_accs_viewed = extraction_insta_html.extract_suggested_acc_viewed_html(file_prompt_result.value)
                extracted_videos_watched = extraction_insta_html.extract_videos_watched_html(file_prompt_result.value)
                extracted_advertisers_using_info = extraction_insta_html.extract_advertisers_using_info_html(file_prompt_result.value)
                extracted_no_ads = extraction_insta_html.extract_ads_setting_html(file_prompt_result.value)
                extracted_off_meta_activity = extraction_insta_html.extract_off_meta_activity_html(file_prompt_result.value)
                extracted_followers = extraction_insta_html.extract_followers_html(file_prompt_result.value)
                extracted_following = extraction_insta_html.extract_following_html(file_prompt_result.value)
                extracted_acc_searches = extraction_insta_html.extract_account_searches_html(file_prompt_result.value)
                extracted_phrase_searches = extraction_insta_html.extract_word_or_phrase_searches_html(file_prompt_result.value)
                extracted_devices = extraction_insta_html.extract_used_devices_html(file_prompt_result.value)
                extracted_location = extraction_insta_html.extract_account_location_html(file_prompt_result.value)
                extracted_topics = extraction_insta_html.extract_your_topics_html(file_prompt_result.value)
                extracted_logins = extraction_insta_html.extract_login_activity_html(file_prompt_result.value)
                extracted_post_comments = extraction_insta_html.extract_post_comments_html(file_prompt_result.value)
                extracted_reels_comments = extraction_insta_html.extract_reel_comments_html(file_prompt_result.value)
                #extracted_insta_live ??
                extracted_liked_posts = extraction_insta_html.extract_likes_html(file_prompt_result.value)
                extracted_acc_setting = extraction_insta_html.extract_account_setting_html(file_prompt_result.value)
                extracted_links_in_dms = extraction_insta_html.extract_links_shared_in_dms_html(file_prompt_result.value)
                extracted_saved_posts = extraction_insta_html.extract_saved_posts_html(file_prompt_result.value)



                # extracted_favorites = extraction.extract_favorites(file_prompt_result.value)
                # extracted_follower = extraction.extract_follower(file_prompt_result.value)
                # extracted_following = extraction.extract_following(file_prompt_result.value)
                # hashtags_used = extraction.extract_used_hashtags(file_prompt_result.value)
                # login_history = extraction.extract_login_history(file_prompt_result.value)
                # recent_location = extraction.extract_recent_location(file_prompt_result.value)
                # extracted_blocks = extraction.extract_blocklist(file_prompt_result.value)
                # extracted_app_settings = extraction.extract_app_settings(file_prompt_result.value)
                # extracted_videos_posted = extraction.extract_posted_videos(file_prompt_result.value)
                # extracted_views = extraction.extract_watchlist(file_prompt_result.value)
                # extracted_shares = extraction.extract_shares(file_prompt_result.value)
                # extracted_likes = extraction.extract_likes(file_prompt_result.value)
                # extracted_search = extraction.extract_search(file_prompt_result.value)
                # extracted_adinfo = extraction.extract_ads_info(file_prompt_result.value)

                # extracted_watch_live = extraction.extract_watch_live(file_prompt_result.value)
                # extracted_comments = extraction.extract_comments(file_prompt_result.value)
                # extracted_wl_comments = extraction.extract_watch_live_comments(file_prompt_result.value)

                consent_prompt = generate_consent_prompt(extracted_ads_viewed,
                                                        extracted_posts_viewed,
                                                        extracted_ads_clicked,
                                                        extracted_suggested_accs_viewed,
                                                        extracted_videos_watched,
                                                        extracted_advertisers_using_info,
                                                        extracted_no_ads,
                                                        extracted_off_meta_activity,
                                                        extracted_followers,
                                                        extracted_following,
                                                        extracted_acc_searches,
                                                        extracted_phrase_searches,
                                                        extracted_devices,
                                                        extracted_location,
                                                        extracted_topics,
                                                        extracted_logins,
                                                        extracted_post_comments,
                                                        extracted_reels_comments,
                                                        extracted_liked_posts,
                                                        extracted_acc_setting,
                                                        extracted_links_in_dms,
                                                        extracted_saved_posts)
                
                consent_prompt_result = yield render_page(platform, consent_prompt)

                # If the participant wants to donate the data gets donated
                if consent_prompt_result.__type__ == "PayloadJSON":
                    yield donate(f"{session_id}-{platform}", consent_prompt_result.value)

                break

            # Sad flow:
            # The data was not valid, ask the participant to retry
            if is_data_valid == False:
                retry_prompt = generate_retry_prompt(platform)
                retry_prompt_result = yield render_page(platform, retry_prompt)

                # The participant wants to retry: start from the beginning
                if retry_prompt_result.__type__ == 'PayloadTrue':
                    continue
                # The participant does not want to retry or pressed skip
                else:
                    break

        # The participant did not submit a file and pressed skip
        else:
            break

    yield exit_port(0, "Success")
    yield render_end_page()


'''def extract_the_data_you_are_interested_in(zip_file: str) -> pd.DataFrame:
    """
    This function extracts the data the researcher is interested in

    In this case we extract from the zipfile:
    * The file names
    * The compressed file size
    * The file size

    You could extract anything here
    """
    out = pd.DataFrame()

    try:
        file = zipfile.ZipFile(zip_file)

        watch_data = []
        share_data = []
        like_data = []

        for name in file.namelist():
            with file.open(name) as f:
                temp_file = f.read()  
                json_file = json.loads(temp_file)
                
                # watch history
                watch_history = json_file["Activity"]["Video Browsing History"]["VideoList"]

                for entry in watch_history:
                    watch_data.append(("watch",entry["Date"], entry["Link"]))

                # share history
                share_history = json_file["Activity"]["Share History"]["ShareHistoryList"]

                for entry in share_history:
                    share_data.append(("share",entry["Date"],entry["Link"],entry["SharedContent"], entry["Method"]))

                # like history
                like_history = json_file["Activity"]["Like List"]["ItemFavoriteList"]

                for entry in like_history:
                    like_data.append(("like",entry["Date"],entry["Link"]))


        watch_df = pd.DataFrame(watch_data, columns=["type","timestamp","link"])
        share_df = pd.DataFrame(share_data, columns=["type","timestamp","link","shared_content","method"])
        like_df = pd.DataFrame(like_data, columns=["type","timestamp","link"])

    except Exception as e:
        print(f"Something went wrong: {e}")

    return watch_df'''


def validate_the_participants_input(zip_file: str) -> bool:
    """
    Check if the participant actually submitted a zipfile
    Returns True if participant submitted a zipfile, otherwise False

    In reality you need to do a lot more validation.
    Some things you could check:
    - Check if the the file(s) are the correct format (json, html, binary, etc.)
    - If the files are in the correct language
    """

    try:
        with zipfile.ZipFile(zip_file) as zf:
            return True
    except zipfile.BadZipFile:
        return False


def render_end_page():
    """
    Renders a thank you page
    """
    page = props.PropsUIPageEnd()
    return CommandUIRender(page)


def render_page(platform: str, body):
    """
    Renders the UI components
    """
    header = props.PropsUIHeader(props.Translatable({"en": platform, "nl": platform }))
    footer = props.PropsUIFooter()
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def generate_retry_prompt(platform: str) -> props.PropsUIPromptConfirm:
    text = props.Translatable({
        "en": f"Unfortunately, we cannot process your {platform} file. Continue, if you are sure that you selected the right file. Try again to select a different file.",
        "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen."
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "Continue",
        "nl": "Verder"
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def generate_file_prompt(platform, extensions) -> props.PropsUIPromptFileInput:
    description = props.Translatable({
        "en": f"Please follow the download instructions and choose the file that you stored on your device. Click “Skip” at the right bottom, if you do not have a {platform} file. ",
        "nl": f"Volg de download instructies en kies het bestand dat u opgeslagen heeft op uw apparaat. Als u geen {platform} bestand heeft klik dan op “Overslaan” rechts onder."
    })
    return props.PropsUIPromptFileInput(description, extensions)




def generate_consent_prompt(*args: pd.DataFrame) -> props.PropsUIPromptConsentForm:
    description = props.Translatable({
       "en": "Below you will find meta data about the contents of the zip file you submitted. Please review the data carefully and remove any information you do not wish to share. If you would like to share this data, click on the 'Yes, share for research' button at the bottom of this page. By sharing this data, you contribute to research <insert short explanation about your research here>.",
       "nl": "Hieronder ziet u gegevens over de zip die u heeft ingediend. Bekijk de gegevens zorgvuldig, en verwijder de gegevens die u niet wilt delen. Als u deze gegevens wilt delen, klik dan op de knop 'Ja, deel voor onderzoek' onderaan deze pagina. Door deze gegevens te delen draagt u bij aan onderzoek over <korte zin over het onderzoek>."
    })

    donate_question = props.Translatable({
       "en": "Do you want to share this data for research?",
       "nl": "Wilt u deze gegevens delen voor onderzoek?"
    })

    donate_button = props.Translatable({
       "en": "Yes, share for research",
       "nl": "Ja, deel voor onderzoek"
    })

    tables = [] 
    outputnames = ["Your viewed ads",
                    "Your viewed posts",
                    "Your clicked ads",
                    "Your viewed suggested accounts",
                    "Your watched videos",
                    "Advertisers using your info",
                    "Your ad setting",
                    "Your off-Meta activity",
                    "Your followers",
                    "Accounts you follow",
                    "Your account searches",
                    "Your phrase searches",
                    "Your devices",
                    "Your location",
                    "Your Instagram topics",
                    "Your logins",
                    "Your post comments",
                    "Your reel comments",
                    "Your liked posts",
                    "Your account settings",
                    "Your links sent via DM",
                    "Your saved posts"]
    for index, df in enumerate(args):
        print("Test Print ------------")
        print(index)
        print(outputnames, outputnames[index])
        table_title = props.Translatable({
            "en": f"{outputnames[index]}",
            #"en": f"Your Data Donations content (Table {index + 1}/{len(args)})",
            "nl": "De inhoud van uw zip bestand"
        })
        tables.append(props.PropsUIPromptConsentFormTable(f"zip_contents_{index}", table_title, df))

    return props.PropsUIPromptConsentForm(
       tables,
       [],
       description = description,
       donate_question = donate_question,
       donate_button = donate_button
    )


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)


def exit_port(code, info):
    return CommandSystemExit(code, info)


##################################################################################
# Exercise for the reader

# Add an extra table to the output
# This table should calculate 2 aggegrate statistics about your the files in your zipfile

# 1. it should give the total number of files in the zipfile
# 2. it should give the total number of bytes of all files in the zipfile
# 3. As a bonus: count the number of times the letter a occurs in all text files in the zipfile. By all means use AI to find out how to do this

# Depending on your data the table could look like this:
# | Statistic | Value |
# -----------------------------
# | Total number of files | 12 | 
# | Total number of bytes | 762376 | 
# | Total occurrences of 'a' in text files | 2378 | 


##################################################################################
# Hints

# Hint 1: Write a function that extracts the statistics and put them in a dataframe. 
#  In order to do that you can copy extract_the_data_you_are_interested_in() and then modify it so it extracts the total number of files and bytes

# Hint 2: If you wrote that function, then
# Changes these lines:
# extracted_data = extract_the_data_you_are_interested_in(file_prompt_result.value)
# consent_prompt = generate_consent_prompt(extracted_data)

# to:
# extracted_data = extract_the_data_you_are_interested_in(file_prompt_result.value)
# extracted_data_statistics = extract_statistics_you_are_interested_in(file_prompt_result.value)
# consent_prompt = generate_consent_prompt(extracted_data, extracted_data_statistics)

##################################################################################
# Answer:

# Uncomment all these lines to see the answer in action

#def extract_statistics_you_are_interested_in(zip_file: str) -> pd.DataFrame:
#    """
#    Function that extracts the desired statistics
#    """
#    out = pd.DataFrame()
#    count = 0 
#    total_number_of_bytes = 0
#    total_a_count = 0
#
#    try:
#        file = zipfile.ZipFile(zip_file)
#        for name in file.namelist():
#            info = file.getinfo(name)
#            count += 1
#            total_number_of_bytes += info.file_size
#
#            # Check if the file is a text file
#            # if so, open it and count the letter a
#            if name.endswith('.txt'):
#                with file.open(name) as txt_file:
#                    content = txt_file.read().decode('utf-8')
#                    total_a_count += content.count('a')
#
#        data = [
#            ("Total number of files", count),
#            ("Total number of bytes", total_number_of_bytes),
#            ("Total occurrences of 'a' in text files", total_a_count),
#        ]
#
#        out = pd.DataFrame(data, columns=["Statistic", "Value"])
#
#    except Exception as e:
#        print(f"Something went wrong: {e}")
#
#    return out
#
#
#def process(session_id: str):
#    platform = "Platform of interest"
#
#    # Start of the data donation flow
#    while True:
#        # Ask the participant to submit a file
#        file_prompt = generate_file_prompt(platform, "application/zip, text/plain")
#        file_prompt_result = yield render_page(platform, file_prompt)
#
#        # If the participant submitted a file: continue
#        if file_prompt_result.__type__ == 'PayloadString':
#
#            # Validate the file the participant submitted
#            # In general this is wise to do 
#            is_data_valid = validate_the_participants_input(file_prompt_result.value)
#
#            # Happy flow:
#            # The file the participant submitted is valid
#            if is_data_valid == True:
#
#                # Extract the data you as a researcher are interested in, and put it in a pandas DataFrame
#                # Show this data to the participant in a table on screen
#                # The participant can now decide to donate
#                extracted_data = extract_the_data_you_are_interested_in(file_prompt_result.value)
#                extracted_data_statistics = extract_statistics_you_are_interested_in(file_prompt_result.value)
#                consent_prompt = generate_consent_prompt(extracted_data, extracted_data_statistics)
#                consent_prompt_result = yield render_page(platform, consent_prompt)
#
#                # If the participant wants to donate the data gets donated
#                if consent_prompt_result.__type__ == "PayloadJSON":
#                    yield donate(f"{session_id}-{platform}", consent_prompt_result.value)
#
#                break
#
#            # Sad flow:
#            # The data was not valid, ask the participant to retry
#            if is_data_valid == False:
#                retry_prompt = generate_retry_prompt(platform)
#                retry_prompt_result = yield render_page(platform, retry_prompt)
#
#                # The participant wants to retry: start from the beginning
#                if retry_prompt_result.__type__ == 'PayloadTrue':
#                    continue
#                # The participant does not want to retry or pressed skip
#                else:
#                    break
#
#        # The participant did not submit a file and pressed skip
#        else:
#            break
#
#    yield exit_port(0, "Success")
#    yield render_end_page()
#