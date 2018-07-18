fp = open("result.csv", "r", encoding="utf-8")
ids = set()
for line in fp:
    tid = line.split(",")[0]
    ids.add(tid)
print(len(ids))