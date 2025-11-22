import os, random, string, shutil
def rand_line(l=30):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=l))
file_cnt = int(input("文件？"))
line_cnt = int(input("随机字符？")) 
test_dir = "test"
os.makedirs(test_dir, exist_ok=True) 
for i in range(file_cnt):
      path = os.path.join(test_dir, f"file_{i+1}.txt")  
      with open(path, "w", encoding="utf-8") as f:
              for _ in range(line_cnt):
                      f.write(rand_line() + "\n")
for fname in os.listdir(test_dir):
       old_path = os.path.join(test_dir, fname) 
       new_path = os.path.join(test_dir, fname.replace(".txt", "-python.txt"))
       with open(old_path, encoding="utf-8") as f:
         lines = [l.rstrip("\n") + "-python\n" for l in f]
       with open(new_path, "w", encoding="utf-8") as f:
              f.writelines(lines)
              os.remove(old_path)       