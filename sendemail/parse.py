import glob
from bs4 import BeautifulSoup

def get_qq():
    fp = open("my_qq.txt")
    qq_lst = []
    for line in fp:
        line = line.strip()
        qq_lst.append(line)
    return qq_lst


qq_lst = get_qq()
filenames = glob.glob("IT技术编程群.html")
output = open("result.txt", "w", encoding="utf-8")
for filename in filenames:
    fp = open(filename, "r", encoding="utf-8")
    soup = BeautifulSoup(fp, "lxml")
    trs = soup.find_all("tr")
    print(len(trs))
    for tr in trs[1:]:
        nickname = tr.find(class_="td-user-nick").text.strip()
        qq = tr.select("td")[4].text.strip()
        year = tr.select("td")[6].text.strip("年")
        if qq not in qq_lst:
            output.write(qq + ":" + nickname + "\n")
output.close()
        