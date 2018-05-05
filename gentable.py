#!/usr/bin/env python3
import re, sys
filename = sys.argv[1]
db = {}
db2 = {}
with open(filename) as f:
 c = f.read()
l = re.split("^# ", c,0, re.MULTILINE)
l = [x for x in l if x]
html = "<table id=\"problems\"><thead><tr><th>Title</th><th>Difficulty</th><th>Tags</th><th>Source</th><th>URL</th><th>Added</th></tr></thead><tbody>"
num = 0
difficulties = set() 
tagset = set()
sources = set()
for block in l:
    line = block.split('\n')
    line = list(filter(None, line))
    if not (line[1].startswith("D:") and line[2].startswith("U:") and line[3].startswith("S:") and line[4].startswith("T:") and line[5].startswith("A:")):
        print("Error: Incorrect format. Expected DUSTA. URLs must be unique.")
    oldtitle = line[0].strip()
    title = "<a href=\"#"+str(num)+"\">" + oldtitle + "</a>"
    db2["["+oldtitle+"]"] = title
    d = line[1].split('D:', 1)[1].strip().lower()
    difficulties.add(d)
    u = line[2].split('U:', 1)[1].strip()
    s = line[3].split('S:', 1)[1].strip().lower()
    sources.add(s)
    t = line[4].split('T:', 1)[1].strip().lower()
    a = line[5].split('A:', 1)[1].strip()
    tags = [x.strip() for x in t.split(",") if x]
    tags = sorted(tags)
    tagset.update(tags)
    db[num] = (title,d,', '.join(tags),s,u,a)
    num+=1
rows = []
for i in range(num):
    row = ["<tr>"]
    for elem in db[i]:
        row.append("<td>"+elem+"</td>")
    row.append("</tr>")
    rows.append(''.join(row))
html += "<p>Difficulties: "+', '.join(sorted(list(difficulties)))+"<br/>"
html += "Sources: "+', '.join(sorted(list(sources)))+"<br/>"
html += "Tags: "+', '.join(sorted(list(tagset)))+"</p>"
html += ''.join(rows)
html += """</tbody></table><script data-config>var tf = new TableFilter('problems');tf.init();</script>"""
num = 0
blocks = []
for block in l:
    line = block.split('\n')
    line[0] = "<h1 id=\""+str(num)+"\">" + line[0] + "</h1>"
    line[1] = "Difficulty: " + db[num][1];
    line[2] = "URL: " + db[num][2];
    line[3] = "Source: " + db[num][3];
    line[4] = "Tags: " + db[num][4];
    line[5] = "Date Added: " + db[num][5];
    num += 1
    blocks.append('\n'.join(line))
html += ''.join(blocks)
pattern = re.compile('|'.join(re.escape(key) for key in db2.keys()))
result = pattern.sub(lambda x: db2[x.group()], html)
print(result)