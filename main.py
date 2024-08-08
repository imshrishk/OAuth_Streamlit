import os
import asyncio
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

st.set_page_config(page_title="SignUp", page_icon="✍️", layout="centered")

# Initialize session state
def initialize_session_state():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    if "stay_logged_in" not in st.session_state:
        st.session_state["stay_logged_in"] = True  # Turned on by default
    if "user_picture" not in st.session_state:
        st.session_state["user_picture"] = ""
    if "last_login_time" not in st.session_state:
        st.session_state["last_login_time"] = None
    if "display_user_id" not in st.session_state:
        st.session_state["display_user_id"] = True  # Toggle for displaying user ID
    if "display_user_email" not in st.session_state:
        st.session_state["display_user_email"] = True  # Toggle for displaying user email
    if "display_user_picture" not in st.session_state:
        st.session_state["display_user_picture"] = True  # Toggle for displaying user picture
    if "display_login_time" not in st.session_state:
        st.session_state["display_login_time"] = True  # Toggle for displaying login time

initialize_session_state()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

client = GoogleOAuth2(client_id, client_secret) if client_id and client_secret else None

# Asynchronous functions for OAuth
async def get_authorization_url(client, redirect_uri):
    return await client.get_authorization_url(redirect_uri, scope=["profile", "email"])

async def get_access_token(client, redirect_uri, code):
    return await client.get_access_token(code, redirect_uri)

async def get_user_info(client, token):
    user_info = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", token)
    return user_info

# Main application logic
def main():
    st.markdown(
        """
        <style>
            .main-header {
                text-align: center;
                font-size: 2.5em;
                color: #4A90E2;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            .login-btn {
                text-align: center;
                font-size: 1.5em;
                margin-top: 20px;
            }
            .logout-btn {
                text-align: center;
                margin-top: 20px;
            }
            .welcome-message {
                font-size: 1.2em;
                color: #333;
            }
            .last-login {
                font-size: 0.9em;
                color: #666;
            }
            .profile-pic {
                border-radius: 50%;
                margin-right: 10px;
            }
            .checkbox {
                margin-top: 10px;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="main-header">Welcome to the SignUp Page</div>', unsafe_allow_html=True)

    if client and not st.session_state["authenticated"]:
        authorization_url = asyncio.run(get_authorization_url(client, redirect_uri))
        query_params = st.experimental_get_query_params()

        if "code" in query_params:
            code = query_params["code"][0]
            try:
                token = asyncio.run(get_access_token(client, redirect_uri, code))
                user_info = asyncio.run(get_user_info(client, token["access_token"]))
                st.session_state["user_id"] = user_info["id"]
                st.session_state["user_email"] = user_info["email"]
                st.session_state["user_picture"] = user_info["picture"]
                st.session_state["authenticated"] = True
                st.session_state["last_login_time"] = datetime.now()
            except Exception as e:
                st.error(f"Error during authentication: {e}")
        else:
            st.markdown(f'<div class="login-btn"><a target="_self" href="{authorization_url}">Login with Google</a></div>', unsafe_allow_html=True)

    if st.session_state["authenticated"]:
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.session_state["display_user_picture"]:
                st.image(st.session_state["user_picture"], width=50, class_='profile-pic')
        with col2:
            if st.session_state["display_user_email"]:
                st.markdown(f'<div class="welcome-message">Welcome {st.session_state["user_email"]}</div>', unsafe_allow_html=True)
            if st.session_state["display_login_time"]:
                last_login = st.session_state["last_login_time"].strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(f'<div class="last-login">Last login: {last_login}</div>', unsafe_allow_html=True)
            if st.session_state["display_user_id"]:
                st.markdown(f'<div class="welcome-message">User ID: {st.session_state["user_id"]}</div>', unsafe_allow_html=True)

        if st.button("LogOut", key="logout-btn"):
            st.session_state["user_id"] = ""
            st.session_state["authenticated"] = False
            st.session_state["user_email"] = ""
            st.session_state["user_picture"] = ""
            st.session_state["last_login_time"] = None

        st.checkbox("Stay logged in", value=st.session_state["stay_logged_in"], key="stay_logged_in", class_="checkbox")

        # Auto logout after a certain time of inactivity
        logout_duration = timedelta(minutes=30)
        if st.session_state["last_login_time"] and datetime.now() - st.session_state["last_login_time"] > logout_duration:
            st.session_state["user_id"] = ""
            st.session_state["authenticated"] = False
            st.session_state["user_email"] = ""
            st.session_state["user_picture"] = ""
            st.session_state["last_login_time"] = None
            st.warning("You have been logged out due to inactivity.")

        with st.sidebar:
            st.markdown("### Display Preferences")
            st.session_state["display_user_id"] = st.checkbox("Display User ID", value=st.session_state["display_user_id"])
            st.session_state["display_user_email"] = st.checkbox("Display User Email", value=st.session_state["display_user_email"])
            st.session_state["display_user_picture"] = st.checkbox("Display User Picture", value=st.session_state["display_user_picture"])
            st.session_state["display_login_time"] = st.checkbox("Display Login Time", value=st.session_state["display_login_time"])
    else:
        st.write("Please log in to access your account.")

if __name__ == "__main__":
    main()
