fp  = open("own.txt", encoding="utf-8")
owns = {}
for line in fp:
    line = line.strip()
    arr = line.split(":")
    qq = arr[0]
    name = arr[1]
    owns[qq] = name


fp  = open("result.txt", encoding="utf-8")
other = {}
for line in fp:
    line = line.strip()
    arr = line.split(":")
    qq = arr[0]
    name = arr[1]
    other[qq] = name

keys1 = set(owns.keys())
keys2 = set(other.keys())
inter = keys1.intersection(keys2)
print(inter)

for qq in inter:
    print("%s:%s" % (qq, owns[qq]))