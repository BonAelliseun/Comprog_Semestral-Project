def fibb_seq(n):
    last = 0
    cur = 1
    for i in range(n-1):
        temp = last
        last = cur
        cur = cur + temp
    return last

print(fibb_seq(10))