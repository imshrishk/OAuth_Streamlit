# OAuth_Streamlit

This project demonstrates how to integrate Google authentication within a Streamlit web application. Users can log in using their Google accounts to securely access features or data.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation and Setup

### 1. Clone the Repository

```sh
git clone https://github.com/imshrishk/OAuth_Streamlit.git
cd OAuth_Streamlit
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure Google OAuth 2.0

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in and create or select an existing project.
3. Navigate to **API & Services** > **Enabled APIs & Services** and enable the **People API**.
4. Go to **OAuth consent screen** and choose **External**.
5. Fill out the **App information** and **Developer contact information**, then click **Save and Continue**.
6. Under **Scopes**, add the following:
   - `https://www.googleapis.com/auth/userinfo.email`
   - `https://www.googleapis.com/auth/userinfo.profile`
   
   Then click **Save and Continue**.
7. Add **Test users** and proceed.
8. Go to **Credentials**, click **Create Credentials**, and select **OAuth 2.0 Client IDs**.
9. Choose **Web application** as the application type, specify the **Name**, and add the **Authorized redirect URIs** (e.g., `http://localhost:5000` for local development).
10. Download the JSON file containing your credentials (Client ID and Client Secret).

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project with the following content, replacing the placeholders with your actual values:

```plaintext
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:5000
```

### 5. Run the Application

Start the Streamlit application using the following command:

```sh
streamlit run main.py
```

## How It Works

1. **Authorization URL**: The app generates a Google OAuth authorization URL that users can click to initiate the login process.
2. **Token Exchange**: After successful authentication, Google redirects back with an authorization code, which is exchanged for an access token.
3. **User Information**: The application retrieves and displays basic user information such as email upon successful login.

## Troubleshooting

- **Invalid Credentials**: Ensure your `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` are correctly configured in the `.env` file and match those specified in the Google Cloud Console.
- **API Errors**: Verify that the People API is enabled and correctly configured in your Google Cloud project.

For any issues, please refer to the [issues page](https://github.com/quarkum-0/OAuth_Streamlit/issues) or contact the maintainers.

---

