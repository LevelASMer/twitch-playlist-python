import json
import requests

_CLIENT_ID_ = "kimne78kx3ncx6brgo4mv6wki5h1ko"

def GetToken(id: str, isVod: bool):
    _HEADERS = {
      'Client-id': _CLIENT_ID_,
    }
  
    _DATA = json.dumps([{
      "operationName": "PlaybackAccessToken",
      "extensions": {
        "persistedQuery": {
          "version": 1,
          "sha256Hash":         "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
        }
      },
      "variables": {
        "isLive": True if isVod == False else False,
        "login": '' if isVod == True else id,
        "isVod": True if isVod == True else False,
        "vodID": id if isVod == True else '',
        "playerType": "embed"
      }
    }])
  
    _RESPONSE = requests.post(
        'https://gql.twitch.tv/gql',
        headers=_HEADERS,
        data=_DATA)
    if isVod == True:
        return _RESPONSE.json()[0]['data']['videoPlaybackAccessToken']
    else:
        return _RESPONSE.json()[0]['data']['streamPlaybackAccessToken']

def ParsePlaylist(data: str):
    _PLAYLISTS = []
    _DATA = data.split('\n')
  
    count = 0
  
    for i in _DATA[2:]:
        count += 1
        if count % 3 == 0:
            _PLAYLISTS.append({
                "quality": _DATA[count - 1].split('NAME="')[1].split('"')[0],
                "url": _DATA[count + 1],
            })
                              
    return _PLAYLISTS;

def GetPlaylist(id: str, isVod: bool):
    _VALUE = GetToken(id, isVod)
    _URL = 'https://usher.ttvnw.net/{}/{}.m3u8?client_id={}&token={}&sig={}&allow_source=true&allow_audio_only=true'.format(
        'vod' if isVod == True else 'api/channel/hls',
        id,
        _CLIENT_ID_,
        _VALUE['value'],
        _VALUE['signature']
    )
  
    _RESPONSE = requests.get(_URL)
  
    if _RESPONSE.status_code == 200:
        return ParsePlaylist(_RESPONSE.text)
    else:
        return 'Sorry, something wrong!'
