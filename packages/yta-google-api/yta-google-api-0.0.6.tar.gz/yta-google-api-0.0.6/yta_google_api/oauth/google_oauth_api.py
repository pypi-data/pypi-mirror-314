"""
TODO: Translate this and explain better

GOOGLE SLIDES PYTHON API
1. Te vas aquí (https://developers.google.com/slides/api/quickstart/python?hl=es-419) y pulsas en Habilitar API.
2. Seleccionas el proyecto y habilitas la API.
3. Nos vamos al listado, abrimos la de Google Slides y le damos a Crear credencial con ID de Oauth. Elegimos app de escritorio, le damos un nombre y aceptamos. Puede que ya tengamos una anteriormente creada (como es mi caso).
4. Abrimos los credenciales y encontraremos el secreto de cliente. Le damos a descargar y obtendremos un fichero, más o menos así:
{
    "web": {
    "client_id": "XXXXXXX.apps.googleusercontent.com",
    "client_secret": "XXXXXX",
    "redirect_uris": [],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
Este fichero lo necesitaremos poner en nuestro ordenador y apuntar a él desde la aplicación para que lo utilice para la verificación. Este servirá para identificarnos de cara a la autorización de uso de la aplicación, con los credenciales que hemos creado.
"""
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.remover import FileRemover
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.path import is_abspath, create_file_abspath
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


class GoogleOauthAPI:
    """
    Class to open Google API Services connections with different
    platforms (Youtube, Slides, etc.) through the Google Oauth
    authentication system. You must instantiate one object for 
    each token credential you have. This means that if you have
    one token with access to all services, just instantiate this
    GoogleOauthAPI object using that unique 'token_filename'
    only.

    This class will store the token files Google will return when
    the authorization request is successfull. This token files 
    will be stored in the project root folder as 'token_files'
    folder.

    Your client secret information  must be a .json file that 
    includes your client id, your client secret and some other 
    fields. You can download this information from Google API
    web platform by creating your Oauth user. Here is an example:
    {
	  "web": {
		"client_id": "XXXXXXX.apps.googleusercontent.com",
		"client_secret": "XXXXXX",
		"redirect_uris": [],
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://accounts.google.com/o/oauth2/token"
	  }
	}
    """
    PROJECT_ABSOLUTE_PATH = get_project_abspath()
    CLIENT_SECRET_PATH = PROJECT_ABSOLUTE_PATH + 'client-secret.json'
    TOKEN_FILES_DIRNAME = 'token_files'

    def __init__(self, client_secret_filename: str, token_files_abspath: str):
        """
        The 'client_secret_filename' is the path to the file that contains
        the client secret credentials obtained from Google Developers API 
        Console. It must be a relative or an absolute path to a file.

        The 'token_files_abspath' is the absolute path of the folder that
        contains (or will contain) the tokens that Google returns us when
        the Oauth authentication is done. These tokens will be identified
        with the service we are using and have expiration time.
        """
        if not client_secret_filename or not FileValidator.is_file(client_secret_filename) or not FileValidator.file_exists(client_secret_filename):
            raise Exception('GoogleOauthAPI could not be instantiated due to the token was not found.')
        
        if not token_files_abspath or not is_abspath(token_files_abspath) or not FileValidator.is_folder(token_files_abspath):
            raise Exception('The provided token files abspath was not valid.')

        # Force the creation of the token files abspath
        self.token_files_abspath = token_files_abspath
        self.client_secret_filename = client_secret_filename
        create_file_abspath(self.token_files_abspath + '/force_creation')

    def __get_credentials(self, api_name: str, api_version: str, scopes: list):
        credentials = None
        token_filename = self.__get_token_filename(api_name, api_version)

        if FileValidator.file_exists(token_filename):
            credentials = Credentials.from_authorized_user_file(token_filename, scopes)

        return credentials
    
    def __get_token_filename(self, api_name: str, api_version: str):
        """
        Returns the token filename for the provided API.
        """
        # TODO: Sanitize this
        return self.token_files_abspath + f'/token_{api_name}_{api_version}.json'
    
    def __write_credentials_to_json(self, credentials: Credentials, api_name: str, api_version: str):
        # This below is a stringified json
        FileWriter.write_file(credentials.to_json(), self.__get_token_filename(api_name, api_version))

    def __refresh_oauth_token(self, api_name: str, api_version: str, scopes: list):
        """
        This method will refresh the Oauth token if needed and
        will write the updated one in the file. If the refresh
        token is valid, they will be refreshed with a request.
        If not, this method will open the Google Oauth flow 
        that involves the user by opening the web browser and
        letting them to access with a Google Account to grant
        the access.
        """
        creds = self.__get_credentials(api_name, api_version, scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Credentials .token and .expiry are updated
                self.__write_credentials_to_json(creds, api_name, api_version)
            else:
                self.start_google_auth_flow(api_name, api_version, scopes)

    def start_google_auth_flow(self, api_name: str, api_version: str, scopes: list):
        """
        Opens the user web browser to grant access to the Google
        API by login with a Google Account.
        """
        # We need to send scopes as a string separated with commas
        # ['scope','scope'] is not working, so try 'scope,scope2'
        scopes = ",".join(scopes)

        auth_flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_filename, scopes)

        creds = auth_flow.run_local_server(port = 0)
        self.__write_credentials_to_json(creds, api_name, api_version)

    def is_oauth_token_valid(self, api_name: str, api_version: str, scopes: list):
        """
        This method checks if the Oauth token is still valid and
        we are able to make requests, or if not.

        @param
            **scopes**
            Array of scopes to be aplied. Something like 
            ['https://www.googleapis.com/auth/presentations']
            is valid.
        """
        # Here 'scopes' is an array
        if not api_name:
            raise Exception('No valid API name provided.')
        
        if not api_version:
            raise Exception('No valid API version provided.')
        
        if not scopes or len(scopes) == 0:
            # TODO: Do more checkings
            raise Exception('No valid Scopes provided.')

        try:
            creds = self.__get_credentials(api_name, api_version, scopes)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Credentials are expired but we can refresh them
                    try:
                        creds.refresh(Request())
                        # Credentials .token and .expiry are updated
                        self.__write_credentials_to_json(creds, api_name, api_version)
                    except:
                        return False
                else:
                    # Expired credentials and/or not refresh token
                    return False
        except Exception as e:
            # Unable to obtain the credentials
            # TODO: Maybe raise the Exception (?)
            return False
        
        return True
    
    def create_service(self, api_name: str, api_version: str, scopes: list):
        """
        Creates an API service for the provided 'api_name', 'api_version'
        and scopes and returns it.

        @param
            **scopes**
            Array of scopes to be aplied. Something like 
            ['https://www.googleapis.com/auth/presentations']
            is valid.
        """
        if not api_name:
            raise Exception('No valid API name provided.')
        
        if not api_version:
            raise Exception('No valid API version provided.')
        
        if not scopes or len(scopes) == 0:
            # TODO: Do more checkings
            raise Exception('No valid Scopes provided.')
        
        # TODO: Maybe we can obtain here the credentials
        # directly and force, when creating the service,
        # to be sure that it is valid.
        if not self.is_oauth_token_valid(api_name, api_version, scopes):
            self.__refresh_oauth_token(api_name, api_version, scopes)

        try:
            service = build(api_name, api_version, credentials = self.__get_credentials(api_name, api_version, scopes), static_discovery = False)
            print(api_name, api_version, 'service created successfully')

            return service
        except Exception as e:
            print(f'Failed to create service instance for {api_name}')
            print(e)
            if e == '[Errno 11001] getaddrinfo failed':
                # I have no internet so do not remove it
                print('Check your internet connection, please.')
                return None
            # I saw t his message:
            # Removing "C:/Users/dania/Desktop/PROYECTOS/youtube-stuff/token_files//token_youtube_v3.json".
            token_file = self.__get_token_filename(api_name, api_version)
            print('Removing "' + token_file + '".')
            FileRemover.delete_file(token_file)

            return None
        

"""
The code is now like this because I don't know exactly
some of the situations for some of the 'return False'
in 'is_oauth_token_valid' method. We could force the
'get_credentials' method to do update the json file
start a Google Oauth process, but for not it is ok like
this.
"""