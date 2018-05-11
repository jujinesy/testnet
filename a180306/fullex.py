from a180306.fulltv import FullTV
from subprocess import call

while True:
    lists = FullTV().list()
    count = 0
    print(len(lists))
    for x in lists:
        print(count+1, x.is_charge(), x.is_fan(), x.users, x.nick, x.type, x.title, x.category)
        print(lists[count].stream())
        count += 1
    index = int(input("번호를 입력하세요(새로고침은 -1) :"))
    if index < 0:
        continue
    link = lists[index].stream()
    print("[================================================]")
    print(lists[index].title)
    print(link)
    if str(input("녹화 y/n:")) == 'y':
        call(["ffmpeg", "-live_start_index", "-99999", "-i", link, '-c', 'copy', "{}.ts".format(lists[index].code)])

# http://cantv.streaming.cdn.broadbandidc.com:1935/wow3_hls/_definst_/sto4/livesound_1863269_20180301205733_H264/playlist.m3u8?key=r5z
