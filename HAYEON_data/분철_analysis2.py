import pandas as pd
from collections import Counter

# 1. 파일 읽기
df = pd.read_csv("TAEYEON_DATA/final_dataframe.csv", encoding='utf-8-sig')

# 2. 종성 문자 + 초성 ᄋ 조합 만들기
jongseong_chars = [chr(code) for code in range(0x11A8, 0x1200)]
cho_ieung = 'ᄋ'
patterns = {js: js + cho_ieung for js in jongseong_chars}

# 3. 결과 저장
rows = []

# 4. timeline별 처리
for timeline, group in df.groupby('timeline'):
    count_total = Counter()
    
    for content in group['content'].astype(str):
        # 텍스트를 음절 단위로 나눈다 (공백이나 줄바꿈 단위 기준)
        parts = content.replace('\n', ' ').split()
        
        for part in parts:
            if len(part) <= 2:  # ✅ 2음절 이하인 경우만
                for pair in patterns.values():
                    count_total[pair] += part.count(pair)

    # row 생성
    row = {'timeline': timeline}
    for js, pair in patterns.items():
        row[pair] = count_total.get(pair, 0)
    rows.append(row)

# 5. DataFrame 정리
result_df = pd.DataFrame(rows).sort_values(by='timeline')

# 6. 필요 시 저장
result_df.to_csv("HAYEON_data/분철_음절.csv", index=False, encoding='utf-8-sig')

# 7. 확인
print(result_df.head())
