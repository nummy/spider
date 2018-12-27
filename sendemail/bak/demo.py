fp = open("todo4.txt")
output = open("todo4_1.txt", "w")
for line in fp:
    line = line.replace(",", ";")
    output.write(line)
output.close()