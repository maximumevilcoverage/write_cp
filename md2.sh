#/bin/sh

if [ $# -ne 1 ]; then
    echo $0: usage: md2.sh filename
    exit 1
fi
python ./gentable.py "$1" > temp.md
echo "<head>" > output.html
echo "<style>" >> output.html
cat styles.css >> output.html
echo "</style>" >> output.html
echo "<script>" >> output.html
cat tablefilter.js >> output.html
echo "</script>" >> output.html
echo "</head>" >> output.html
python ./markdown2.py --extras header-ids,fenced-code-blocks,break-on-newline temp.md >> output.html
