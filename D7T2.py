import random,string,os
def rand_line(length=50):
    return ''.join(random.choices(string.printable[:-6], k=length))  
src = "test.txt"
dst = "copy_test.txt"
i = int(input("行数 i："))
with open(src, "w", encoding="utf-8") as f:
    for _ in range(i):
        f.write(rand_line() + '\n')
with open(src, encoding="utf-8") as f1, open(dst, "w", encoding="utf-8") as f2:
    f2.write(f1.read())
print(f"{src} → {dst} ")