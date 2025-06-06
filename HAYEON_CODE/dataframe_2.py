import os
import pandas as pd
import numpy as np
import os

print(os.getcwd())  # 현재 작업 디렉토리 확인
#'/Users/hayeon/KORE208/finalproject'


#15세기 전처리 텍스트 불러오기기
a15 = open("15-16세기/15/cleaned_A5CA0001-1.txt", 'r', encoding = 'utf-8').read()
b15 = open("15-16세기/15/cleaned_A5CD0019-1.txt", 'r', encoding = 'utf-8').read()
c15 = open("15-16세기/15/cleaned_A5CD0006(1447)-1.txt", 'r', encoding = 'utf-8').read()
d15 = open("15-16세기/15/cleaned_A5CD0021(1459)-1.txt", 'r', encoding = 'utf-8').read()

#16세기 전처리 텍스트 불러오기
a16 = open("15-16세기/16/cleaned_A6CF0004(1517)-1.txt", 'r', encoding = 'utf-8').read()
b16 = open("15-16세기/16/cleaned_A6CG0003-1.txt", 'r', encoding = 'utf-8').read()
c16 = open("15-16세기/16/cleaned_A6CG0009.txt", 'r', encoding = 'utf-16').read()
d16 = open("15-16세기/16/cleaned_A6CG0021(1518)-1.txt", 'r', encoding = 'utf-8').read()

#근대(17-1833) 전처리 텍스트 불러오기
a17 = open("17-18세기/cleaned_A7BA0028-1.txt", 'r', encoding = 'utf-8').read()
b17 = open("17-18세기/cleaned_A7CE0002-1.txt", 'r', encoding = 'utf-8').read()
c17 = open("17-18세기/cleaned_A7CG0008-1.txt", 'r', encoding = 'utf-8').read()
d17 = open("19-20세기/cleaned_P8BB0001(1830).txt", 'r', encoding = 'utf-16').read()
e17 = open("19-20세기/cleaned_P9BB0016(1848).txt", 'r', encoding = 'utf-16').read()

#개화기 전처리 텍스트 불러오기
a18 = open("개화기/cleaned_A0BB0111(1915).txt", 'r', encoding = 'utf-16').read()
b18 = open("개화기/cleaned_A8CB0029(1884).txt", 'r', encoding = 'utf-16').read()
c18 = open("개화기/cleaned_P0BB0034(1890).txt", 'r', encoding = 'utf-16').read()
d18 = open("개화기/cleaned_P9BC0002(1896).txt", 'r', encoding = 'utf-8').read()
e18 = open("개화기/cleaned_PABB0003(1909).txt", 'r', encoding = 'utf-16').read()


old_kor = pd.DataFrame({
    'content': [
        a15, b15, c15, d15,
        a16, b16, c16, d16,
        a17, b17, c17, d17, e17,
        a18, b18, c18, d18, e18
    ],
    'timeline': [
        '15C', '15C', '15C', '15C',
        '16C', '16C', '16C', '16C',
        'modern', 'modern', 'modern', 'modern', 'modern',
        'enlightenment', 'enlightenment', 'enlightenment', 'enlightenment', 'enlightenment'
    ]
})


old_kor.to_csv('old_kor_2.csv')