#创建顺序文件
import random,string
from pathlib import Path
now=Path(__file__).resolve().parent
new=now/'img'
new.mkdir(exist_ok=True,parents=True)
used=set()
while len(used)<100:
    name=''.join(random.choices(string.ascii_letters+string.digits,k=4))
    used.add(name)
for fname in used:
    (new/f"{fname}.png").touch()
    