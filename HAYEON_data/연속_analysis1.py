import pandas as pd


# 1. 파일 읽기
df = pd.read_csv("TAEYEON_DATA/final_dataframe.csv", encoding='utf-8-sig')

# 2. 분석 대상 문자 리스트 정의
patterns = {
    'ᆯᄋ': '종성ㄹ + 초성ㅇ',
    'ᆯᄂ': '종성ㄹ + 초성ㄴ',
    'ᆯᄅ': '종성ㄹ + 초성ㄹ',
}

# 3. 결과 저장 리스트
rows = []

# 4. timeline 별로 처리
for timeline, group in df.groupby('timeline'):
    text = ''.join(group['content'].astype(str).tolist())
    
    row = {'timeline': timeline}
    for pair in patterns:
        row[pair] = text.count(pair)
    rows.append(row)

# 5. 결과 DataFrame 생성
result_df = pd.DataFrame(rows).sort_values(by='timeline')

# 6. 저장
result_df.to_csv("HAYEON_data/char_count_ㄹ연속.csv", index=False, encoding='utf-8-sig')

# 7. 확인
print(result_df.head())
