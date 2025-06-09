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


# timeline 컬럼을 제외한 나머지 열들 중에서
# 값의 합(sum)이 0인 열 제거
non_timeline_cols = timeline_jongseong_df.columns.difference(['timeline'])

# 열들 중 합계가 0이 아닌 것만 선택
non_zero_cols = [col for col in non_timeline_cols if timeline_jongseong_df[col].sum() != 0]

# timeline 컬럼 포함해서 다시 구성
filtered_df = timeline_jongseong_df[['timeline'] + non_zero_cols]

# 결과 확인
print(filtered_df.head())



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# macOS용 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False 

def plot_top_jongseong_per_timeline(df, timeline_col='timeline', top_n=10):
    """
    각 timeline별로 가장 많이 등장한 종성 top-N을 막대그래프로 시각화합니다.
    
    Parameters:
        df (pd.DataFrame): 종성 수가 정리된 데이터프레임
        timeline_col (str): timeline 구분 열 이름
        top_n (int): 시각화할 상위 종성 개수
    """
    jongseong_cols = [col for col in df.columns if col != timeline_col]

    for _, row in df.iterrows():
        timeline = row[timeline_col]
        counts = row[jongseong_cols]
        top_counts = counts.sort_values(ascending=False).head(top_n)

        plt.figure(figsize=(8, 5))
        plt.bar(top_counts.index, top_counts.values)
        plt.title(f"Top {top_n} 종성 - {timeline}")
        plt.xlabel("종성 문자")
        plt.ylabel("빈도 수")
        plt.grid(True, axis='y')
        plt.tight_layout()
        plt.show()

df = pd.read_csv("HAYEON_data/timeline_jongseong_count.csv", encoding='utf-8-sig')
plot_top_jongseong_per_timeline(df)





