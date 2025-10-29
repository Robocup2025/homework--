#数字魏书
num=int(input())
a=num
b=0
while a>0:
    a//=10
    b+=1
print("weishu",b)
a=num
while a>0:
    number=a%10
    numberstr=str(number)
    print(numberstr,end="")
    a-=number
    a//=10