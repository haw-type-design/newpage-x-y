for i in *.jpeg; do echo "<img src="/img/$i" width="100%">" >> "temp.html"; done
cat temp.html | sort -R > images.html
rm temp.html