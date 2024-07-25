import requests 
import os
API_URL = "http://localhost:8050/"
from dotenv import load_dotenv
APP_SECRET_API_KEY = os.environ.get("APP_SECRET_API_KEY")

def get_execution_session_by_date(date):
    response = requests.get(f"{API_URL}/execution_session_by_date/", params={"date": date}, headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get execution session for the given date.", headers={"X-API-KEY": APP_SECRET_API_KEY})

def list_available_index_days():
    response = requests.get(f"{API_URL}/execution_session/available", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to list available index days.")

def get_last_execution_session(session_id):
    response = requests.get(f"{API_URL}/execution_session/", params={"session_id": session_id}, headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to display last execution session.")


def fetch_recent_exec_logs(limit=3):
    response = requests.get(f"{API_URL}/content_logs/?limit={limit}", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to load execution logs.")
    

def check_global_limit():
    response = requests.get(f"{API_URL}/check_global_limit/", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()["allowed"]
    else:
        raise Exception("Failed to check global query limit.")

def increment_global_query_count():
    response = requests.post(f"{API_URL}/increment_global_query_count/", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        return response.json()["success"]
    else:
        raise Exception("Failed to increment global query count.")

import streamlit as st

@st.experimental_fragment()
def authenticate():
    st.title("Twitter OAuth Authentication")
    st.write("Click the button below to authenticate the bot account.")
    
    if st.button("Authenticate with Twitter"):
        response = requests.get(f"{API_URL}/twitter/login", headers={"X-API-KEY": APP_SECRET_API_KEY})
        if response.status_code == 200 or response.status_code == 400:
            auth_url = response.url
            st.write(f"[Authenticate with Twitter]({auth_url})")
        else:
            st.error("Error! Failed to get authorization URL.")

@st.experimental_fragment()
def post_tweet_form():
    st.title("Post a Tweet")
    tweet_text = st.text_area("Enter your tweet:")
    
    if st.button("Post Tweet"):
        response = requests.post(
            f"{API_URL}/twitter/tweet",
            params={
                "tweet_text": tweet_text,
            }
        )
        if response.status_code == 200:
            st.success("Tweet posted successfully!")
        else:
            st.error("Error posting tweet: " + response.json().get("detail", "Unknown error"))


def get_gacetas(endpoint, params=None):
    response = requests.get(f"{API_URL}{endpoint}", params=params, headers={"X-API-KEY": APP_SECRET_API_KEY})
    return response


def list_gacetas():
    st.title("Gacetas List")
    response = get_gacetas("/gacetas", params={'order': 'desc'})
    
    # response = requests.get(f"{API_URL}/gacetas", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        gacetas = response.json().get("gacetas", [])
        for gacet in gacetas:
            gaceta          = gacet['gaceta']
            twitter_prompts = gacet['twitter_prompts']
            st.subheader(f"ID: {gaceta['id']}, Date: {gaceta['date']}, File Path: {gaceta['file_path']}")
            
            for sess in twitter_prompts:
                exec_session = sess['exec_session']
                st.subheader(f"Execution Session: {exec_session['id']}")
                st.write(f"Start Time: {exec_session['created_at']}")
                st.write(f"Status: {exec_session['status']}")
                st.write(f"Is Approved?: {exec_session['is_approved']}")
                
                logs = sess['logs']
                
                for content_log in logs:
                    st.subheader(f"Prompt: {content_log['name']}")
                    st.subheader(f"state: {content_log['state']}")
                    st.text_area("Prompt Text", value=content_log['prompt_text'], key=f"prompt_text_{content_log['execution_session_id']}", height=200)
                    st.text_area("Response", value=content_log['response'], key=f"response_{content_log['execution_session_id']}", height=200)
                    st.text_area("Sources", value=content_log['sources'], key=f"sources_{content_log['execution_session_id']}", height=100)
                    st.text_area("Raw Prompt", value=content_log['raw_prompt'], key=f"raw_prompt_{content_log['execution_session_id']}", height=100)
                    if st.button("Update Prompt Result", key=f"update_{content_log['execution_session_id']}"):
                        update_prompt_result(gaceta['id'], st.session_state[f"response_{content_log['execution_session_id']}"])
                    if st.button("Approve Tweet", key=f"approve_{content_log['execution_session_id']}"):
                        approve_tweet(gaceta['id'], content_log['id'], content_log['response'])
                        
        st.divider()
            #     generate_prompt(gaceta['id'])
            # if st.button("Approve Tweet", key=f"approve_{gaceta['id']}"):
            #     approve_tweet(gaceta['id'])
    else:
        st.error("Error fetching gacetas")

def approve_tweet(gaceta_id, content_exec_id, tweet_text):
    response = requests.post(
        f"{API_URL}/approve_tweet",
        headers={"X-API-KEY": APP_SECRET_API_KEY},
        json={"gaceta_id": gaceta_id, "content_exec_id": content_exec_id, "tweet_text": tweet_text}
    )
    if response.status_code == 200:
        st.success("Tweet posted successfully")
    else:
        st.error("Error posting tweet")
        
        

def get_me():
    response = requests.get(f"{API_URL}/twitter/me", headers={"X-API-KEY": APP_SECRET_API_KEY})
    if response.status_code == 200:
        user = response.json()
        st.write(f"User ID: {user['id']}")
        st.write(f"Name: {user['name']}")
        st.write(f"Username: {user['username']}")
    else:
        st.error("Error fetching user data")
        

def check_health():
    try:
        response = requests.get(f"{API_URL}/health_check", headers={"X-API-KEY": APP_SECRET_API_KEY})
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False