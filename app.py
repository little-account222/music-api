import requests
import execjs
import time
import json
import re
from flask import Flask, request

app = Flask(__name__)

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "referer": "https://www.kugou.com/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
cookies = {
    "kg_mid": "beb914c0fee230cb657f8a93ae0f14f8",
    "kg_dfid": "08whHi3FG5w21X1UXf4HPPw6",
    "kg_dfid_collect": "d41d8cd98f00b204e9800998ecf8427e",
    "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": "1751767894,1752570803",
    "HMACCOUNT": "F7E84FB1113B3C28",
    "kg_mid_temp": "beb914c0fee230cb657f8a93ae0f14f8",
    "KuGoo": "KugooID=2375921465&KugooPwd=8F6D834CFA274993099198FC9069D3CB&NickName=%u0066%u006f%u0075%u006e%u0074%u0061%u0069%u006e&Pic=http://imge.kugou.com/kugouicon/165/20100101/20100101192931478054.jpg&RegState=1&RegFrom=&t=576fd9903d86ac5b74ac90525e74d24604feb6adc05f2bb8a612c51e4bbd40fd&a_id=1014&ct=1752572690&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0032%u0033%u0037%u0035%u0039%u0032%u0031%u0034%u0036%u0035&t1=",
    "KugooID": "2375921465",
    "t": "576fd9903d86ac5b74ac90525e74d24604feb6adc05f2bb8a612c51e4bbd40fd",
    "a_id": "1014",
    "UserName": "kgopen2375921465",
    "mid": "beb914c0fee230cb657f8a93ae0f14f8",
    "dfid": "08whHi3FG5w21X1UXf4HPPw6",
    "Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d": "1752572983"
}
url = "https://complexsearch.kugou.com/v2/search/song"
music_info_url = "https://wwwapi.kugou.com/play/songinfo"

with open("main.js",encoding="utf-8") as f:
    JS = execjs.compile(f.read())
pattern = r'callback123\((.*?)\)'


def search_music(keyword,pagesize,pagenumber):
  timestrap = str(int(time.time() * 1000))
  data = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
 "appid=1014",
 "bitrate=0",
 "callback=callback123",
 "clienttime=" + timestrap,
 "clientver=1000",
 "dfid=" + cookies["dfid"],
 "filter=10",
 "inputtype=0"
  ,"iscorrection=1",
 "isfuzzy=0",
 "keyword=" + keyword,
 "mid=" + cookies["mid"],
  "page=" + str(pagenumber)
  ,"pagesize=" + str(pagesize),
 "platform=WebFilter"
  ,"privilege_filter=0"
  ,"srcappid=2919"
  ,"token=" + cookies["t"],
 "userid="+ cookies["KugooID"],
 "uuid=" + cookies["kg_mid"],
 "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
  sign = JS.call("window.signer", "".join(data))
  params = {
      "callback": "callback123",
      "srcappid": "2919",
      "clientver": "1000",
      "clienttime": timestrap,
      "mid": cookies["mid"],
      "uuid": cookies["kg_mid"],
      "dfid": cookies["dfid"],
      "keyword": keyword,
      "page": str(pagenumber),
      "pagesize": str(pagesize),
      "bitrate": "0",
      "isfuzzy": "0",
      "inputtype": "0",
      "platform": "WebFilter",
      "userid": cookies["KugooID"],
      "iscorrection": "1",
      "privilege_filter": "0",
      "filter": "10",
      "token": cookies["t"],
      "appid": "1014",
      "signature": sign
  }
  response = requests.get(url, headers=headers, cookies=cookies, params=params)
  # print(response.text[11:-1])
  # print(re.search(pattern, response.text, re.DOTALL).group(1))
  match = json.loads(re.search(pattern, response.text, re.DOTALL).group(1))
  result_list = []
  for song in match["data"]["lists"]:
      result_list.append(
          {
              "song_id":song["EMixSongID"],
              "complete_song_name":song["FileName"],
              "singer_name":song["Singers"][0]["name"],
              "song_name":song["SongName"],
              "album_name":song["AlbumName"],
              "song_language":song["trans_param"]["language"],
          }
      )
  return result_list
def get_music_info(music_id):
    timestrap = str(int(time.time() * 1000))
    data = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt","appid=1014","clienttime=" + timestrap,"clientver=20000","dfid=" + cookies["dfid"],"encode_album_audio_id=" + music_id,"mid=" + cookies["mid"],"platid=4","srcappid=2919","token=" + cookies["t"],"userid=" + cookies["KugooID"],"uuid=" + cookies["kg_mid"],"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
    sign = JS.call("window.signer", "".join(data))
    params = {
        "srcappid": "2919",
        "clientver": "20000",
        "clienttime": timestrap,
        "mid": cookies["mid"],
        "uuid": cookies["kg_mid"],
        "dfid": cookies["dfid"],
        "appid": "1014",
        "platid": "4",
        "encode_album_audio_id": music_id,
        "token": cookies["t"],
        "userid": cookies["KugooID"],
        "signature": sign
    }
    response = requests.get(music_info_url, headers=headers, params=params).json()
    response = response["data"]
    return {
        "album_name":response["album_name"],
        "song_cover":response["img"],
        "singer_avatar":response["authors"][0]["avatar"],
        "lyrics":response["lyrics"],
        "song_mp3_url":response["play_backup_url"]
    }



@app.route("/get/search")
def search_music():
    if request.args.get("keyword") and request.args.get("pagenumber"):
        return {
            "code":200,
            "data":search_music(request.args.get("keyword"), 10, request.args.get("pagenumber")),
            "warn":"不可用于非法用途，不得借此牟利，仅交流学习使用。"
        }
    else:
        return "参数不完全，请访问/目录查看使用说明"

def search_music(keyword,pagesize,pagenumber):
  timestrap = str(int(time.time() * 1000))
  data = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
 "appid=1014",
 "bitrate=0",
 "callback=callback123",
 "clienttime=" + timestrap,
 "clientver=1000",
 "dfid=" + cookies["dfid"],
 "filter=10",
 "inputtype=0"
  ,"iscorrection=1",
 "isfuzzy=0",
 "keyword=" + keyword,
 "mid=" + cookies["mid"],
  "page=" + str(pagenumber)
  ,"pagesize=" + str(pagesize),
 "platform=WebFilter"
  ,"privilege_filter=0"
  ,"srcappid=2919"
  ,"token=" + cookies["t"],
 "userid="+ cookies["KugooID"],
 "uuid=" + cookies["kg_mid"],
 "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
  sign = JS.call("window.signer", "".join(data))
  params = {
      "callback": "callback123",
      "srcappid": "2919",
      "clientver": "1000",
      "clienttime": timestrap,
      "mid": cookies["mid"],
      "uuid": cookies["kg_mid"],
      "dfid": cookies["dfid"],
      "keyword": keyword,
      "page": str(pagenumber),
      "pagesize": str(pagesize),
      "bitrate": "0",
      "isfuzzy": "0",
      "inputtype": "0",
      "platform": "WebFilter",
      "userid": cookies["KugooID"],
      "iscorrection": "1",
      "privilege_filter": "0",
      "filter": "10",
      "token": cookies["t"],
      "appid": "1014",
      "signature": sign
  }
  response = requests.get(url, headers=headers, cookies=cookies, params=params)
  match = json.loads(response.text[12:-2])
  result_list = []
  for song in match["data"]["lists"]:
      result_list.append(
          {
              "song_id":song["EMixSongID"],
              "complete_song_name":song["FileName"],
              "singer_name":song["Singers"][0]["name"],
              "song_name":song["SongName"],
              "album_name":song["AlbumName"],
              "song_language":song["trans_param"]["language"],
          }
      )
  return result_list
def get_music_info(music_id):
    timestrap = str(int(time.time() * 1000))
    data = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt","appid=1014","clienttime=" + timestrap,"clientver=20000","dfid=" + cookies["dfid"],"encode_album_audio_id=" + music_id,"mid=" + cookies["mid"],"platid=4","srcappid=2919","token=" + cookies["t"],"userid=" + cookies["KugooID"],"uuid=" + cookies["kg_mid"],"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
    sign = JS.call("window.signer", "".join(data))
    params = {
        "srcappid": "2919",
        "clientver": "20000",
        "clienttime": timestrap,
        "mid": cookies["mid"],
        "uuid": cookies["kg_mid"],
        "dfid": cookies["dfid"],
        "appid": "1014",
        "platid": "4",
        "encode_album_audio_id": music_id,
        "token": cookies["t"],
        "userid": cookies["KugooID"],
        "signature": sign
    }
    response = requests.get(music_info_url, headers=headers, params=params).json()
    response = response["data"]
    return {
        "album_name":response["album_name"],
        "song_cover":response["img"],
        "singer_avatar":response["authors"][0]["avatar"],
        "lyrics":response["lyrics"],
        "song_mp3_url":response["play_backup_url"]
    }



@app.route("/get/info")
def music_info():
    if request.args.get("music_id"):
        return {
            "code":200,
            "data":get_music_info(request.args.get("music_id")),
            "warn":"不可用于非法用途，不得借此牟利，仅交流学习使用。"
        }
    else:
        return "参数不完全，请访问/目录查看使用说明"


