import requests
import sys
import os
import json
import webbrowser

if len(sys.argv) < 2:
    sys.exit('Usage: %s client_id' % sys.argv[0])

client_id = sys.argv[1]
print("https://login.live.com/oauth20_authorize.srf?response_type=code&client_id=" + client_id + "&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=office.onenote wl.offline_access")


initialAuth = requests.get("https://login.live.com/oauth20_authorize.srf?response_type=code&client_id=" + client_id + "&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=office.onenote wl.offline_access")
webbrowser.open(url=initialAuth.url)

code = input('Input Code from URL: ')

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type': 'authorization_code', 'client_id': client_id, 'code': code, 'redirect_uri': 'https://login.live.com/oauth20_desktop.srf'}

auth = requests.post("https://login.live.com/oauth20_token.srf", headers=headers, data=payload)
config = json.loads(auth.text)

atoken = config[u'access_token']
rtoken = config[u'refresh_token']

data = {'app_id': client_id, 'access_token': atoken, 'refresh_token': rtoken}
print("save the following to ~/.onenote_export.json")
print(json.dumps(data))
