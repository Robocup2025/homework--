#回文数
num=int(input())
s=str(num)
if s==s[::-1]:
    print("yes")
else:
    print("no")