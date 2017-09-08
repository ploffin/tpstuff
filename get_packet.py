# -*- encoding: UTF-8 -*-

from __future__ import print_function
import os
import httplib2
import json

# pip install --upgrade google-api-python-client

from oauth2client.file import Storage
from oauth2client import client
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

SCOPES = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
OUT_PATH = '.'
CLIENT_SECRET_FILE = 'client_secret.json'

home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

storage = Storage(credential_path)
credentials = storage.get()

if not credentials or credentials.invalid:
    # Run through the OAuth flow and retrieve credentials
    json_data=open(CLIENT_SECRET_FILE).read()
    data = json.loads(json_data)
    CLIENT_ID = data['installed']['client_id']
    CLIENT_SECRET = data['installed']['client_secret']
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPES, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print('Go to the following link in your browser: ' + authorize_url)
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    storage.put(credentials)


# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)
drive_service = build('drive', 'v2', http=http)

def list_files(service):
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        for item in files['items']:
            yield item
        page_token = files.get('nextPageToken')
        if not page_token:
            break


for item in list_files(drive_service):
    if item.get('title')=='ELTP Season 10: Draft Packet':
        outfile = os.path.join(OUT_PATH, '%s' % 'dptable.csv')
        download_url = None
        if 'exportLinks' in item and 'text/csv' in item['exportLinks']:
            download_url = item['exportLinks']['text/csv']
        else:
            print('ERROR getting %s' % item.get('title'))
            print(item)
            print(dir(item))
        if download_url:
            print("downloading %s" % item.get('title'))
            resp, content = drive_service._http.request(download_url)
            if resp.status == 200:
                if os.path.isfile(outfile):
                    print("ERROR, %s already exist" % outfile)
                else:
                    with open(outfile, 'wb') as f:
                        f.write(content)
                    print("OK")
            else:
                print('ERROR downloading %s' % item.get('title'))
