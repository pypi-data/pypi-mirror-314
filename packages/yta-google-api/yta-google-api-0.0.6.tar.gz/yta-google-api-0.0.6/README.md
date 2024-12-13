# YTA Google Api

The simplest way to interact with the Google API services.

This library is intented to simplify the interaction with the Google API for using the Google services such as Youtube, Slides, etc.

# Instructions
- Go to Google Developers Console (https://console.cloud.google.com/), create an Oauth user and enable the service you need to use.
- Obtain your Oauth user secret, download it and place it in your project (calling it `client-secret.json` is ok).
- Create a folder called `token_files` in your project.
- Use this `from yta_google_api.oauth.google_oauth_api import GoogleOauthAPI` in your code to import the Oauth main class.
- Create a `CLIENT_SECRET_FILENAME = PROJECT_ABSPATH + 'client-secret.jon'` and a `TOKEN_FILES_ABSPATH' = PROJECT_ABSPATH + 'token_files/'`
- Instantiate it as `instance = GoogleOauthAPI(CLIENT_SECRET_FILENAME, TOKEN_FILES_ABSPATH)`
- And now you have to look for your service `API_NAME`, `API_VERSION` and `SCOPES` to be able to create a new service by `intance.create_service(API_NAME, API_VERSION, SCOPES)`.