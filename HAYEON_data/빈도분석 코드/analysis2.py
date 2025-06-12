#%%
import pandas as pd
from collections import Counter

df = pd.read_csv('/Users/hayeon/KORE208/finalproject/exercise_KORE208_group2/final_dataframe.csv')



#%%
#1. 종성 개수 세기
def count_jongseong_by_timeline(df, content_col='content', timeline_col='timeline',
                                 output_csv_path=None, return_df=True):
    """
    주어진 DataFrame에서 timeline별 종성(U+11A8 ~ U+11FF) 등장 횟수를 세어 반환하거나 저장합니다.

    Parameters:
        df (pd.DataFrame): 분석할 데이터프레임
        content_col (str): 종성이 들어 있는 텍스트 열 이름
        timeline_col (str): 타임라인(구분자) 열 이름
        output_csv_path (str or None): 저장할 CSV 경로. None이면 저장하지 않음
        return_df (bool): 결과 DataFrame을 반환할지 여부

    Returns:
        pd.DataFrame or None: 결과 데이터프레임 또는 None
    """

    jongseong_chars = [chr(code) for code in range(0x11A8, 0x1200)]
    rows = []

    for timeline, group in df.groupby(timeline_col):
        text = ''.join(group[content_col].astype(str).tolist())
        count = Counter(c for c in text if c in jongseong_chars)
        row = {timeline_col: timeline}
        for j in jongseong_chars:
            row[j] = count.get(j, 0)
        rows.append(row)

    result_df = pd.DataFrame(rows)

    original_order = df[timeline_col].drop_duplicates().tolist()
    result_df[timeline_col] = pd.Categorical(result_df[timeline_col], categories=original_order, ordered=True)
    result_df = result_df.sort_values(by=timeline_col)

    if output_csv_path:
        result_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    return result_df if return_df else None

#%%
# 기존 df에 대해 실행
result = count_jongseong_by_timeline(
    df,
    content_col='content',
    timeline_col='timeline',
    output_csv_path='timeline_jongseong_count.csv',
    return_df=True
)


# %%
