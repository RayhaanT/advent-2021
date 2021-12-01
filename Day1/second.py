index = 0
tally = 0

windows = []
current = []

while (True):
    try:
        depth = int(input())
    except ValueError:
        break

    current.append(depth)

    if(index < 2):
        index += 1
        continue
    if(index > 2):
        current.pop(0)
    index += 1
    windows.append(current[0] + current[1] + current[2])

first = True
for x in range(1, len(windows)):
    if windows[x] > windows[x-1]:
        tally+=1

print(tally)
