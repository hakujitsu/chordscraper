import requests
from bs4 import BeautifulSoup as bs4

# Sharuru
# url = 'https://ja.chordwiki.org/wiki/%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%AB'

# Tsukiaitai
url = 'https://ja.chordwiki.org/wiki/%E8%AA%B0%E3%81%A7%E3%82%82%E3%81%84%E3%81%84%E3%81%8B%E3%82%89%E4%BB%98%E3%81%8D%E5%90%88%E3%81%84%E3%81%9F%E3%81%84'

# Hitchcock
# url = 'https://ja.chordwiki.org/wiki/%E3%83%92%E3%83%83%E3%83%81%E3%82%B3%E3%83%83%E3%82%AF'


r = requests.get(url)
soup = bs4(r.content, 'html.parser')

# Title
title = soup.select_one('.title').contents[1]


# Chords
# main = soup.select('.main')

body = soup.select('p[class="line"]')

chordbody = []

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
outF = open(title + ".txt", "w") 
for line in chordbody: 
    outF.write(line) 
    outF.write("\n") 

outF.close()


# Save into file

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

# save_html(r.content, title + '.html')