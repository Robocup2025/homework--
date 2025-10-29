#最后剩下谁
num=list(range(1,234))
count=0
p=0
while len(num)>1:
    count+=1
    if count==3:
        num.pop(p)
        count=0
    else:
        p+=1
    p%=len(num)
print(num[0])