import glob
from bs4 import BeautifulSoup

filenames = glob.glob("*.html")
output = open("result.txt", "w")
for filename in filenames:
    fp = open(filename, "r", encoding="utf-8")
    soup = BeautifulSoup(fp, "lxml")
    trs = soup.find_all("tr")
    print(len(trs))
    for tr in trs[1:]:
        nickname = tr.find(class_="td-user-nick").text.strip()
        qq = tr.select("td")[4].text.strip()
        year = tr.select("td")[6].text.strip("年")
        output.write(qq + "\n")
output.close()
        