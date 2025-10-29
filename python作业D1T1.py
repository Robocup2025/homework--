#三位数组合
num=[]
for baiwei in range(1,5):
    for shiwei in range(1,5):
        for gewei in range(1,5):
            if baiwei!=shiwei and shiwei!=gewei and baiwei!=gewei:
                number=baiwei*100+shiwei*10+gewei*1
                num.append(number)
print("manzudesanweishugeshu",len(num))
print(num)