with open("test.txt", encoding="utf-8") as f1, \
     open("copy_test.txt", encoding="utf-8") as f2:
    for n, (l1, l2) in enumerate(zip(f1, f2), 1):
        if l1 != l2:
            print(f"第{n}行不同")