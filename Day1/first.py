depth = 7
last = 0
first = True
tally = 0

while (True):
    try:
        depth = int(input())
    except ValueError:
        break
    if (first):
        last = depth
        first = False
        continue
    if depth == "done":
        break
    if depth > last:
        tally+=1
    last = depth

print(tally)



