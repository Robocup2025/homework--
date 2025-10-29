#找bug
if __name__=="__main__":
    #语法错误
    list=list(range(1000))
    for idx in range(len(list)-1,-1,-1):
        if list[idx]%2==1:
          list.pop(idx)      #删了前面的影响后面的计数，导致混乱。不如从后遍历
print(list)