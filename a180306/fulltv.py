import grequests as grequests
import requests


class BroadCast:
    def __init__(self, title, thumb, nick, id, code, pw, type, storage, users, category):
        self.title = title
        self.thumb = thumb
        self.nick = nick
        self.id = id
        self.code = code
        self.pw = pw
        self.type = type
        self.storage = storage
        self.users = users
        self.category = category

    def stream(self):
        storage = self.storage
        code = self.code
        urls = []
        for num in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']:
            for a in ['h', 'n']:
                url = "http://streaming.neofuture.kr:1935/neofuture_live{}{}/_definst_/mp4:{}/{}/playist.m3u8?authkey=".format(
                    num, a, storage, code)
                urls.append(url)
        rs = (grequests.get(u, timeout=1) for u in urls)
        for r in grequests.map(rs):
            if r is not None:
                if 200 == r.status_code:
                    return r.url

    def users(self):
        return self.users

    def title(self):
        return self.title

    def thumb(self):
        return self.thumb

    def is_locked(self):
        return self.pw

    def is_fan(self):
        return self.type == 'fan'

    def is_charge(self):
        return self.type == 'charge'


class FullTV:
    def __init__(self):
        self.result = 0
        self.header = {
            "Origin": "http://www.full.co.kr",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "http://m.full.co.kr/",
            "Cookie": "userLoginSaveYN=Y; PPAP=MQ%3D%3D; userLoginSaveID=aa; sessKey=aa; partner=jjoowonna; userLoginIdx=0; userLoginYN=Y; userReferer=http%3A%2F%2Fwww.full.co.kr%2F;"
        }

    def list(self):
        data = {
            "kzF*A*d6ZHs!": "117",
            "k!L!n*5Y6tsHa": "78",
            "K2zi0VyorAUH!*9UArgz": "200",
            "GvzF_5*o6Q6g!yO3uh2Jz": "0",
            "K2zi0Vyli1YFPbzbGgzFJazg2j6nvz": "desc",
            "wvJU0v*HEDv!": "webPc",
            "Z2er0YyevFK6lmz": "1.0.0",
        }
        lists = requests.post("http://api.full.co.kr/live/", data=data, headers=self.header).json()

        broadcases = []
        for item in lists['list']:
            userId = item['userId']
            userNick = item['userNick']
            category = item['category']
            isAdult = item['isAdult']
            isPw = item['isPw']
            bType = item['type']
            isLive = item['isLive']
            liveType = item['liveType']
            storage = item['storage']
            thumbUrl = item['thumbUrl']
            code = item['code']
            title = item['title']
            user = item['user']

            if isAdult is False:
                continue
            if isLive is not True:
                continue
            if liveType == 'rec':
                continue
            if category in ['mov', 'game','music']:
                continue
            # if bType == 'fan':

            broadcases.append(BroadCast(title, thumbUrl, userNick, userId, code, isPw, bType, storage, user, category))
        broadcases = sorted(broadcases, key=lambda x: x.users, reverse=True)
        return broadcases
