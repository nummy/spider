fp = open("result2.txt")
output = open("todo2.txt", "w")
counter = 0
emails = [] 
for line in fp:
    line = line.strip()
    email = "%s@qq.com" % line
    emails.append(email)
    if len(emails) == 40:
        output.write(",".join(emails) + "\n")
        emails = []
output.write(",".join(emails) + "\n")
emails = []
output.close()