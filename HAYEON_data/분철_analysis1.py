#%%
import pandas as pd


# 1. 파일 읽기
df = pd.read_csv('/Users/hayeon/KORE208/finalproject/exercise_KORE208_group2/final_dataframe.csv')

# 2. 종성 자모 (U+11A8 ~ U+11FF)
jongseong_chars = [chr(code) for code in range(0x11A8, 0x1200)]
cho_ieung = 'ᄋ'  # 초성 이응 (U+110B)

# 3. 만들 조합: 종성 + 초성ᄋ
pair_patterns = {js: js + cho_ieung for js in jongseong_chars}


# 4. 결과 저장 리스트
rows = []

# 5. timeline 별로 처리
for timeline, group in df.groupby('timeline'):
    text = ''.join(group['content'].astype(str).tolist())
    
    row = {'timeline': timeline}
    for js, pair in pair_patterns.items():
        row[pair] = text.count(pair)
    rows.append(row)

# 5. 결과 DataFrame 생성 / 순서정렬 유지
result_df = pd.DataFrame(rows)
original_order = df['timeline'].drop_duplicates().tolist()
result_df['timeline'] = pd.Categorical(result_df['timeline'], categories=original_order, ordered=True)
result_df = result_df.sort_values(by='timeline')

# 6. 저장
result_df.to_csv("char_count_분철연철.csv", index=False, encoding='utf-8-sig')

# 7. 확인
print(result_df.head())


#아예 등장하지 않은 패턴 제거
# 'timeline' 열은 유지하고, 나머지 열 중 합이 0이 아닌 것만 필터링
non_timeline_cols = result_df.columns.difference(['timeline'])
non_zero_cols = [col for col in non_timeline_cols if result_df[col].sum() > 0]

# 새 DataFrame 구성 (timeline + 유효한 열만 유지)
filtered_df = result_df[['timeline'] + non_zero_cols]
filtered_df.to_csv("char_count_분철연철_cleaned.csv.csv", index=False, encoding='utf-8-sig')
filtered_df.head()

# %%
