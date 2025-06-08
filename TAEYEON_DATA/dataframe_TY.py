#%%
import os
import pandas as pd
import numpy as np
os.getcwd()
#%%
os.chdir("./25-1/KORE208_group2")
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
g = open("./19-20세기/cleaned_A0BB0111.txt", 'r', encoding = 'utf-16').read()
h = open("./19-20세기/cleaned_A8CB0029.txt", 'r', encoding = 'utf-16').read()
i = open("./19-20세기/cleaned_P0BB0034.txt", 'r', encoding = 'utf-16').read()
# %%
old_kor = pd.DataFrame({'content':[a, b, c, d, e, f, g, h, i], 'timeline':['15-16C', '15-16C', '15-16C', '17-18C', '17-18C', '17-18C', '19-20C', '19-20C', '19-20C']})
# %%
old_kor.to_csv('old_kor.csv')
# %%
df = pd.read_csv('old_kor_example.csv')

#%%
import pandas as pd
import os

# 텍스트 파일들이 있는 폴더 경로
folder_path = r'C:\Users\bbbbb\Desktop\25-1\KORE208\output_txt'

# 해당 폴더 내의 모든 cleaned*.txt 파일 불러오기
file_list = [f for f in os.listdir(folder_path) if f.startswith('cleaned') and f.endswith('.txt')]

# 파일 내용과 빈 타임라인을 담을 리스트
data = []

for filename in sorted(file_list):  # 정렬하면 순서대로 정리돼서 보기 좋아
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
        data.append({'content': text, 'timeline': ''})  # 라벨은 나중에 수동으로 추가

# 데이터프레임 생성
df = pd.DataFrame(data)

# 확인용 출력 (앞부분만)
print(df.head())

#%%
# 저장 (엑셀/CSV)
df.to_csv('labeled_data_placeholder.csv', index=False, encoding='utf-8-sig')

#%%
pd.read_csv(r'C:\Users\bbbbb\Desktop\25-1\KORE208\output_txt\labeled_data_placeholder.csv', encoding = 'utf-8-sig')
# %%
add_samples = pd.DataFrame([
    {'content': '글 예시 샘플입니다', 'timeline': '15-16세기'},
    {'content': '이것은 또 다른 예시이다', 'timeline': '17-18세기'},
    {'content': '근대국어의 특징이 나타난다', 'timeline': '19-20세기'}])