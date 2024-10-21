import sys
import httplib2
from modules.core.singleton import Singleton
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class YoutubeService(metaclass=Singleton):
    def authenticate_youtube(self):
        flow = flow_from_clientsecrets(
            CLIENT_SECRETS_FILE,
            scope=YOUTUBE_UPLOAD_SCOPE,
        )

        storage = Storage("oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()),
        )
