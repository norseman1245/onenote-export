import requests
import json
import os
import sys
import shutil


conf = "/Users/jonas/.onenote_export.json"

if not os.path.exists(conf):
    sys.exit("Can't find config file.")

if len(sys.argv) < 2:
    sys.exit('Usage: %s dest' % sys.argv[0])

if sys.argv[1].endswith('/') is True:
    backup_dir = sys.argv[1]
else:
    backup_dir = sys.argv[1]+'/'

if os.path.exists(backup_dir):
    q = input('Destination dir exists already, shall we delete it? (y/n) ')
    if q == 'y':
        try:
            shutil.rmtree(backup_dir)
        except:
            sys.exit("Couldn't remove directory")
    else:
        sys.exit('Ok, bye.')

file_path = os.path.join(conf)
with open(file_path) as fi:
    data = json.load(fi)
    app_id = data['app_id']
    refresh_token = data['refresh_token']
    access_token = data['access_token']

headers = {'Authorization': 'Bearer '+access_token}

getNotebooks = requests.get("https://www.onenote.com/api/v1.0/me/notes/notebooks", headers=headers)

if getNotebooks.status_code == 401:
    reAuthHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
    reAuthData = {'grant_type': 'refresh_token', 'client_id': app_id, 'redirect_uri': 'https://login.live.com/oauth20_desktop.srf', 'refresh_token': refresh_token}
    reAuth = requests.post("https://login.live.com/oauth20_token.srf", headers=reAuthHeaders, data=reAuthData)
    new_token = json.loads(reAuth.text)['access_token']
    access_token = new_token
    headers = {'Authorization': 'Bearer '+new_token}

getNotebooks = requests.get("https://www.onenote.com/api/v1.0/me/notes/notebooks", headers=headers)

notebooks = {}

for nb in json.loads(getNotebooks.text)['value']:
    notebooks[nb['id']] = nb['name']

sections = {}

for k,v in notebooks.items():
    getSections = requests.get("https://www.onenote.com/api/v1.0/me/notes/notebooks/"+k+"/sections", headers=headers)
    if getSections.status_code != 200:
        sys.exit("Couldn't load sections.")

    for scts in json.loads(getSections.text)['value']:
        if scts['name'] in sections:
            sections.append(scts['name'])
        else:
            sections[scts['id']] = scts['name']

for a,b in sections.items():
    getS = requests.get("https://www.onenote.com/api/v1.0/me/notes/sections/"+a, headers=headers)
    if getS.status_code != 200:
        sys.exit("Couldn't load sections.")

    getPages = requests.get("https://www.onenote.com/api/v1.0/me/notes/sections/"+a+"/pages", headers=headers)
    if getPages.status_code != 200:
        sys.exit("Couldn't get pages.")

    for pages in json.loads(getPages.text)['value']:
        apath = backup_dir+json.loads(getS.text)['parentNotebook']['name'] + '/' + pages['parentSection']['name']

        try:
            os.makedirs(apath, exist_ok=True)
        except OSError as exception:
            sys.exit(exception)

        getContent = requests.get(pages['contentUrl'], headers=headers)
        filename = pages['title']+'.html'
        try:
            writefile = open(os.path.join(apath, filename), 'w')
            writefile.write(getContent.text)
            writefile.close()
            print('saved', filename)
        except:
            sys.exit("Couldn't write file.")
