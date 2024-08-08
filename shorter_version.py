import os
import asyncio
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(page_title="Google OAuth Login", page_icon="🔒")

# Initialize OAuth client
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
client = GoogleOAuth2(client_id, client_secret) if client_id and client_secret else None

async def get_authorization_url(client, redirect_uri):
    return await client.get_authorization_url(redirect_uri, scope=["profile", "email"])

async def get_access_token(client, redirect_uri, code):
    return await client.get_access_token(code, redirect_uri)

async def get_user_info(client, token):
    response = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", token)
    return response.json()

def main():
    if client:
        authorization_url = asyncio.run(get_authorization_url(client, redirect_uri))
        query_params = st.experimental_get_query_params()
        
        if "code" in query_params:
            code = query_params["code"][0]
            try:
                token = asyncio.run(get_access_token(client, redirect_uri, code))
                user_info = asyncio.run(get_user_info(client, token["access_token"]))
                st.write(f"Authenticated as: {user_info['email']}")
            except Exception as e:
                st.error(f"Error during authentication: {e}")
        else:
            st.markdown(f'<a href="{authorization_url}" target="_self">Login with Google</a>', unsafe_allow_html=True)
    else:
        st.error("OAuth client not initialized. Check your CLIENT_ID and CLIENT_SECRET.")

if __name__ == "__main__":
    main()
