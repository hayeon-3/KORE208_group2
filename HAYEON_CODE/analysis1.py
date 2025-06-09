import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

# 1. CSV 파일 불러오기
old_kor = pd.read_csv('old_kor_2.csv', index_col=0)

# 2. 시기별 개수 세기 함수
def count_char_by_timeline(df, char_list):
    """
    df: old_kor 데이터프레임
    char_list: 세고 싶은 문자 리스트
    return: 시기별 각 문자 개수 DataFrame
    """
 
    count_data = []

    for timeline, group in df.groupby('timeline'):
        row = {'timeline': timeline}
        text_all = ''.join(group['content'].astype(str))  # 하나의 문자열로 합치기
        for ch in char_list:
            row[ch] = text_all.count(ch)
        count_data.append(row)

    return pd.DataFrame(count_data).set_index('timeline')

# 3. 시기별 개수세기 실행하기
# 세고 싶은 문자들 리스트
chars_to_count = [':', 'ᅙ', 'ᅀ', '', 'ᄞ', 'ᄢ']

# old_kor_2.csv 불러오기
old_kor = pd.read_csv('old_kor_2.csv', index_col=0)

# 문자 개수 분석 실행
char_counts = count_char_by_timeline(old_kor, chars_to_count)

# 결과 출력
print(char_counts)

#저장
char_counts.to_csv('char_counts_by_timeline.csv', encoding='utf-8-sig')


##3. 종성 세기
import pandas as pd
from collections import Counter

# 종성 유니코드 문자들
jongseong_chars = [chr(code) for code in range(0x11A8, 0x1200)]

# 결과를 저장할 리스트
rows = []

# 각 timeline 그룹별 처리
for timeline, group in df_sample.groupby('timeline'):
    text = ''.join(group['content'].astype(str).tolist())  # 그룹 내 content 모두 합치기
    count = Counter(c for c in text if c in jongseong_chars)
    row = {'timeline': timeline}
    for j in jongseong_chars:
        row[j] = count.get(j, 0)
    rows.append(row)

# 결과 DataFrame
timeline_jongseong_df = pd.DataFrame(rows)

# 보기 좋게 정렬 (timeline 기준)
timeline_jongseong_df = timeline_jongseong_df.sort_values(by='timeline')

# 결과 보기
timeline_jongseong_df.to_csv("timeline_jongseong_count.csv", index=False, encoding='utf-8-sig')

df_reload = pd.read_csv("timeline_jongseong_count.csv", encoding='utf-8-sig')

print(df_reload.head())