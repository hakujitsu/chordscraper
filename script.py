import requests
from bs4 import BeautifulSoup as bs4

# Testcases
# Future improvement: add a txt file of links to parse and generate .cho file

# シャルル
# url = 'https://ja.chordwiki.org/wiki/%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%AB'

# 誰でもいいから付き合いたい
# url = 'https://ja.chordwiki.org/wiki/%E8%AA%B0%E3%81%A7%E3%82%82%E3%81%84%E3%81%84%E3%81%8B%E3%82%89%E4%BB%98%E3%81%8D%E5%90%88%E3%81%84%E3%81%9F%E3%81%84'

# ヒッチコック
# url = 'https://ja.chordwiki.org/wiki/%E3%83%92%E3%83%83%E3%83%81%E3%82%B3%E3%83%83%E3%82%AF'

# 高音厨音域テスト
# url = 'https://ja.chordwiki.org/wiki/%E9%AB%98%E9%9F%B3%E5%8E%A8%E9%9F%B3%E5%9F%9F%E3%83%86%E3%82%B9%E3%83%88'

# Flyers
# url = 'https://ja.chordwiki.org/wiki/Flyers'

# 366日
url = 'https://ja.chordwiki.org/wiki/366%E6%97%A5'

# 心做し
# url = 'https://ja.chordwiki.org/wiki/%E5%BF%83%E5%81%9A%E3%81%97';


# Automated file input
# urls = []
# with open("input/input.txt") as ip:
#     line = ip.readline()
#     if "http" in line:
#         urls.append(line)


# Retrieves html from url and parses it
r = requests.get(url)
soup = bs4(r.content, 'html.parser')

# Strings to write to chordfile
chordbody = []

# Parse title
title = soup.select_one('.title').contents[1]
chordbody.append("{title: " + title + "}")

# Parse artist
artist = soup.select_one('.subtitle').contents[1]
chordbody.append("{artist: " + artist + "}")
# Potential further parsing: distinguish between 
# 歌(sung by) / 作詞(lyricist) / 作曲(composer) / 編曲 (arrangement)


# Parse other details (if present)
# Tempo (BPM), time (time signature), capo/key, 簡単コード (easier chords)
deets = []
for item in soup.body:
    if(item.name == 'div' and item.has_attr("class") and "main" in item['class']):
        main = item.h2
        while main.name != 'div':
            main = main.next_sibling
        for x in main:
            if(x.name == 'p' and x.has_attr("class")) :
                if not ("comment" in x['class']):
                    break
                deets.append(x.string)
        break

for line in deets:
    if "BPM" in line:
        bpm = ""
        for c in line.partition('BPM=')[2]:
            if c.isdigit():
                bpm +=c
            else : break
        chordbody.append("{tempo: " + bpm + "}")
    if "拍子" in line:
        time = ""
        arr = []
        s = list(line.partition('拍子')[0])
        s.reverse()
        for c in s:
            if c.isdigit() or c == "/":
                arr.append(c)
            else : break   
        arr.reverse() 
        for c in arr:
            time += c
        chordbody.append("{time: " + time + "}")

# for line in deets:
#     print(line)

# Parse chords
chordbody.append("\n")
body = soup.select('p[class="line"]')

for line in body:
    l = line.contents[1:(len(line) - 1)]
    chordstring = ""
    for p in l:
        try:
            if(p =='\xa0'): 
                i = 0
            elif p['class'][0] == "chord" :
                chordstring += "[" + p.contents[0] + "]"
            else :
                chordstring += p.contents[0]
        except TypeError as e:
            print(e)
            print(p)
            print(l)
            print("error end")

    # print(chordstring)
    chordbody.append(chordstring)


# Writing to file
chordFile = open("output/" + title + ".cho", "w") 
for line in chordbody: 
    chordFile.write(line) 
    chordFile.write("\n") 

chordFile.close()


# Save into file

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

# save_html(r.content, "output/" + title + '.html')