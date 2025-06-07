import olefile
import pandas as pd
from subprocess import Popen, PIPE
from OldHangeul import OldTexts

file = 'A6CG0021(1518).hwp'
process = Popen(['hwp5txt', file], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
data = stdout.decode('utf-8')
text=OldTexts(data)
print(text)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(str(text))

# text=OldTexts('스님이 免帖 나 주시고') #완성형이 포함된 텍스트입니다
# print(text)

# f = olefile.OleFileIO("ttt.hwp")
# encoded_text = f.openstream("PrvText").read()
# decoded_text = encoded_text.decode("UTF-16")
# # print(decoded_text) 
# decoded_text = decoded_text.split('\n')
# for dt in decoded_text:
#     print(dt)
# # for i in decoded_text:
# #     print(i)

# df = pd.DataFrame(decoded_text)

# with open("A5CA0001.txt", "r") as f:
#     for line in f:
#         print(line)