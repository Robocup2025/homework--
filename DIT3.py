#费勃拉起数列
a=0
b=1
n=int(input())
num=[0,1]
if n<=2:
    if n==1:
        print("0")
    else:
        print("0 1")
c=1   #全局变量？python里面有局部变量的概念否？
for i in range(1,n-1):
    c=a+b
    num.append(c)
    a=b
    b=c
print(num)
