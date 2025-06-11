#%%
import pandas as pd
from collections import Counter

# 1. 파일 읽기
df = pd.read_csv('/Users/hayeon/KORE208/finalproject/exercise_KORE208_group2/final_dataframe.csv')

# 2. 분석 대상 문자 리스트 정의
target_chars = {
    'ᄞ': 'U+111E',  # ㄹ + ㅅ 병서 (합용)
    'ᄢ': 'U+1122',  # ㅁ + ㅅ 병서 (합용)
}

# 3. 결과 저장 리스트
rows = []

# 4. timeline 별로 처리
for timeline, group in df.groupby('timeline'):
    text = ''.join(group['content'].astype(str).tolist())
    count = Counter(c for c in text if c in target_chars)
    row = {'timeline': timeline}
    for char in target_chars:
        row[char] = count.get(char, 0)
    rows.append(row)

# 5. 결과 DataFrame 생성 / 순서정렬 유지
result_df = pd.DataFrame(rows)
original_order = df['timeline'].drop_duplicates().tolist()
result_df['timeline'] = pd.Categorical(result_df['timeline'], categories=original_order, ordered=True)
result_df = result_df.sort_values(by='timeline')

# 6. 저장
result_df.to_csv("char_count_16.csv", index=False, encoding='utf-8-sig')

# 7. 확인
print(result_df.head())

# %%
