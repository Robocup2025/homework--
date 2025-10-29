import random, csv, statistics, os
FILE = "data_10x3.csv"
with open(FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["col1", "col2", "col3"])
    for _ in range(10):
        writer.writerow([random.randint(0, 100) for _ in range(3)])
with open(FILE, encoding="utf-8") as f:
    col2 = [int(row[1]) for row in csv.reader(f)][1:]  
print("第二列最大值:", max(col2))
print("第二列最小值:", min(col2))
print("第二列平均值:", statistics.mean(col2))
print("第二列中位数:", statistics.median(col2))