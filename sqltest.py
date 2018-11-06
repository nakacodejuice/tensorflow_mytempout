import requests
import json
chat_id = 327717695
tokenTelegram = "491859422:AAF2jRsyvyjk3T7EucgsMOpAdlqshORHH2E"
hosttelegram ="https://api.telegram.org/bot"
Message = {'chat_id': chat_id, 'text': 'test'}
headers = {'content-type': 'application/json'}
proxies = dict(http='socks5://192.168.2.105:9050',
               https='socks5://192.168.2.105:9050')
requests.post(hosttelegram + tokenTelegram + '/sendMessage', data=json.dumps(Message), proxies=proxies, headers=headers)