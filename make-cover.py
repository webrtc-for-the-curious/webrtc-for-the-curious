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

convert_command="""convert -font FreeSans-Bold -fill black \
    -pointsize 160 -draw "text 480,340 'WebRTC'" \
    -pointsize 80 -draw "text 720,460 'for the'" \
    -pointsize 120 -draw "text 660,550 'Curious'" \
"""

convert_command+=f" -pointsize 60 -draw \"text 120,1780 '{best[0]}'\""
ypos=1800
for i in range(1,min(3, len(authors_by_contrib))):
    ypos = ypos + i*24
    convert_command+=f" -pointsize 40 -draw \"text 120,{ypos} '{authors_by_contrib[i][0]}'\""

ypos = ypos + i*24
convert_command+=f" -pointsize 30 -draw \"text 120,{ypos} 'and the webrtcforthecurious.com team'\""


convert_command+=" \"content/images/epub-cover notitle.png\" \"content/images/epub-cover.png\""
print(convert_command)
subprocess.check_output(convert_command, shell=True, text=True)
