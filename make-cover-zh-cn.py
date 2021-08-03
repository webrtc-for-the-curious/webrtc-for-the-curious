#!/usr/bin/python3

import subprocess

def contributions(folder = "content/"):
    proc = subprocess.Popen(['git','log', '--shortstat', '--pretty="%aN"', folder],stdout=subprocess.PIPE)

    contributions=dict()

    author=""
    for i, linecrlf in enumerate(proc.stdout):
        line = linecrlf.rstrip()
        if i % 3 == 0:
            author=line.decode("utf-8").replace('"', '')
            if not author in contributions:
                contributions[author] = 0
        if i % 3 == 2:
            tokens = line.decode("utf-8").split(" ")
            if len(tokens) > 6:
                contributions[author] += int(tokens[4]) + int(tokens[6])
            else:
                contributions[author] += int(tokens[4])

    return contributions

def sort_by_contrib(contrib: dict):
    authors_by_contrib=list(contrib.items())
    authors_by_contrib.sort(reverse=True, key=lambda x: x[1])
    return authors_by_contrib


authors_by_contrib=sort_by_contrib(contributions("content/"))

best = authors_by_contrib[0]

convert_command="""convert -font WenQuanYi-Zen-Hei -fill black \
    -pointsize 160 -draw "text 480,340 'WebRTC'" \
    -pointsize 90 -draw "text 660,550 '适合好奇的人'" \
"""

convert_command+=f" -pointsize 60 -draw \"text 120,1780 '{best[0]}'\""
ypos=1800
for i in range(1,min(3, len(authors_by_contrib))):
    ypos = ypos + i*24
    convert_command+=f" -pointsize 40 -draw \"text 120,{ypos} '{authors_by_contrib[i][0]}'\""

ypos = ypos + i*24
convert_command+=f" -pointsize 30 -draw \"text 120,{ypos} '和 webrtcforthecurious.com 团队'\""

translators = contributions("content.zh-cn/")
best_translator=sort_by_contrib(translators)[0]

ypos = ypos + i*24
convert_command+=f" -pointsize 30 -draw \"text 120,{ypos} '{best_translator[0]} 翻译'\"" # i just used google translate to get this

convert_command+=" \"content/images/epub-cover notitle.png\" \"content.zh-cn/images/epub-cover.png\""
print(convert_command)
subprocess.check_output(convert_command, shell=True, text=True)
