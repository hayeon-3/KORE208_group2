#%%
import os
import pandas as pd
import numpy as np
os.getcwd()
# %%
#15-16세기 전처리 텍스트 불러오기기
a = open("./15-16세기/cleaned_A5CA0001-1.txt", 'r', encoding = 'utf-8').read()
b = open("./15-16세기/cleaned_A5CD0019-1.txt", 'r', encoding = 'utf-8').read()
c = open("./15-16세기/cleaned_A6CG0003-1.txt", 'r', encoding = 'utf-8').read()
# %%
#17-18세기 전처리 텍스트 불러오기기
d = open("./17-18세기/cleaned_A7BA0028-1.txt", 'r', encoding = 'utf-8').read()
e = open("./17-18세기/cleaned_A7CE0002-1.txt", 'r', encoding = 'utf-8').read()
f = open("./17-18세기/cleaned_A7CG0008-1.txt", 'r', encoding = 'utf-8').read()
# %%
#19-20세기 전처리 텍스트 불러오기기 (error!!)
g = open("./19-20세기/cleaned_A0BB0111.txt", 'r', encoding = 'utf-8').read()
h = open("./19-20세기/cleaned_A8CB0029.txt", 'r', encoding = 'utf-8').read()
i = open("./19-20세기/cleaned_P0BB0034.txt", 'r', encoding = 'utf-8').read()
# %%
old_kor = pd.DataFrame({'content':[a, b, c, d, e, f, 'g', 'h', 'i'], 'timeline':['15-16C', '15-16C', '15-16C', '17-18C', '17-18C', '17-18C', '19-20C', '19-20C', '19-20C']})
# %%
old_kor.to_csv('old_kor.csv')
# %%
