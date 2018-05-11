import requests
from subprocess import call
headers = {
    "Origin": "http://www.full.co.kr",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "http://m.full.co.kr/",
    "Cookie": "userLoginSaveYN=Y; PPAP=MQ%3D%3D; userLoginSaveID=YVhKdmJuQmhjbXM9; _ga=GA1.3.667265205.1518902810; sessKey=8bfe91ada069b1893be0c2f4a38fb4ae1cb3581f68974913237b3c369c229ff5; partner=full; userLoginIdx=3018201; userLoginYN=Y; userReferer=http%3A%2F%2Fwww.full.co.kr%2F;"
}

data = {
    "kzF*A*d6ZHs!": "117",
    "k!L!n*5Y6tsHa": "78",
    "K2zi0VyorAUH!*9UArgz": "150",
    "GvzF_5*o6Q6g!yO3uh2Jz": "0",
    "K2zi0Vyli1YFPbzbGgzFJazg2j6nvz": "desc",
    "wvJU0v*HEDv!": "webMobile",
    "Z2er0YyevFK6lmz": "1.0.0",
}
link = "http://api.full.co.kr/live/"
adult_list = []
lists = requests.post(link, data=data, headers=headers).json()
print(lists['page'])
count = 0
for item in lists["list"]:
    if item['isAdult']:
        if item["isLive"]:
            if item['type'] == 'fan' or item['type'] == 'charge' or item['type'] == 'free':
                adult_list.append(item)
                count += 1
adult_list = sorted(adult_list, key=lambda x: x['user'], reverse=True)
count = 0
for item in adult_list:
    print("[{0:2}] code:{1:35} isAdult:{3:4} pw:{4:5} type:{5:6} users:{6:4} title:{2:30}".format(
        count, item['code'], item['title'],
        item['isAdult'],
        item['isPw'], item['type'], item['user']))
    count += 1


def get_stream(item):
    storage = item['storage']
    code = item['code']
    nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    alp = ['h', 'n']
    print(item)
    for num in nums:
        for a in alp:
            url = "http://streaming.neofuture.kr:1935/neofuture_live{}{}/_definst_/mp4:{}/{}/playist.m3u8?authkey=r".format(
                num, a, storage, code)
            print("try...", url)
            try:
                result = requests.get(url, headers=headers, timeout=1)
                if result.ok:
                    return url
            except:
                continue


index = int(input("번호를 입력하세요 : "))
link = get_stream(adult_list[index])
print(link)
# ffmpeg -live_start_index -99999 -i 'http://streaming.neofuture.kr:1935/neofuture_live08h/_definst_/mp4:storage39/ssckmy99_2805166_20180221010305/playist.m3u8?authkey=r' -c copy gold_something.ts
# call(["ffmpeg", "-live_start_index", "-99999", "-i", link, '-c', 'copy', "{}.ts".format(adult_list[index]['code'])])