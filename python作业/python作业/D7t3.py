with open("test.txt", "r+", encoding="utf-8") as f:
    old = f.read()  
    f.seek(0)      
    f.write("python\n" + old + "\npython") 
    f.truncate()      
print("ok")