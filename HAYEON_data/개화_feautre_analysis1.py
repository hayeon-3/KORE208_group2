#%%
import pandas as pd
from collections import Counter

# 파일 불러오기
df = pd.read_csv('/Users/hayeon/KORE208/finalproject/exercise_KORE208_group2/final_dataframe.csv')

# 문자 그룹 정의
b_chars = ['ᄈ', 'ᄣ', 'ᄤ', 'ᄥ', 'ᄦ', 'ᆲ', 'ᆹ']
s_chars = ['ᄊ', 'ᄧ', 'ᄨ', 'ᄩ', 'ᆪ', 'ᆳ', 'ᆹ', 'ᆻ']

# 문자 중복 포함 제거 (ᆹ 중복되므로 하나만 남기자)
s_chars = list(set(s_chars) - set(b_chars))  # ᆹ은 b계로만 포함

# 전체 대상 문자
target_chars = {char: f"U+{ord(char):04X}" for char in (b_chars + s_chars)}

# 결과 저장
rows = []

# timeline별 세기
for timeline, group in df.groupby('timeline'):
    text = ''.join(group['content'].astype(str).tolist())
    count = Counter(c for c in text if c in target_chars)

    row = {'timeline': timeline}

    # 문자별 개수
    for char in target_chars:
        row[char] = count.get(char, 0)

    # ✔️ 합계 계산
    row['ㅂ계_합계'] = sum(row[char] for char in b_chars)
    row['ㅅ계_합계'] = sum(row[char] for char in s_chars)

    rows.append(row)

#결과 DataFrame 생성 / 순서정렬 유지
result_df = pd.DataFrame(rows)
original_order = df['timeline'].drop_duplicates().tolist()
result_df['timeline'] = pd.Categorical(result_df['timeline'], categories=original_order, ordered=True)
result_df = result_df.sort_values(by='timeline')

# 저장
result_df.to_csv("char_count_17.csv", index=False, encoding='utf-8-sig')

# 확인
print(result_df.head())

# %%
