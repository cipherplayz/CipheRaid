import json
import os
import requests
import time
import threading
from threading import Thread


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

auth_url = config['auth_url']



count = 0 


def get_headers(token):
    headers = {
                "accept": "*/*",
                # "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "authorization": token,
                "referer": "https://discord.com/channels/@me",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9007 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDA3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTYxODQyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    return headers


def authorize(token):
  global count
  while True:
    try:
      headers = get_headers(token)
      r = requests.post(auth_url, headers=headers, json={"authorize": "true"})
      # print(r.text)
      if r.status_code in (200, 201, 204):
        if 'location' in r.text:
          location = r.json()['location']
          requests.get(location)
          print(count, "[INFO]: Successfully Authorized:", token)
          count += 1
          break
        else:
          print("[ERROR]: Failed to Authorize:", token, r.text)
          break
      else:
        print("[ERROR]: Failed to Authorize:", token, r.text)
        break
    except Exception as e:
      print("[ERROR]: Failed to Authorize:", token, e)
      if "connection" in str(e):
        time.sleep(0.5)
        continue
      else:
        break
      # return


def send_messages(token, urll, channel_id, msg):
    url = f'{urll}/channels/{channel_id}/messages'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    data = {
        'content':f"{msg}"
    }
    requests.post(url,json=data, headers=headers)

def type_tokens(token, urll, channel_id):
    url = f'{urll}/channels/{channel_id}/typing'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    requests.post(url,headers=headers)


def convert_token_to_auth():
  _f = open("tokens.txt", "r").readlines()
  for _tk in _f:
    _tk = _tk.strip()
  # _tk = _tk.split(":")[2]
    time.sleep(0.1)
    threading.Thread(target=authorize, args=(_tk,)).start()

