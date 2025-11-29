def fibb_seq(n):
    last = 0
    cur = 1
    for i in range(n):
        temp = last
        last = cur
        cur = cur + temp
    return cur

print(fibb_seq(5))