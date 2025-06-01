print("hi")
import re
from OldHangeul import OldTexts

def process_old_hangeul_text(filepath, encoding='utf-8', save_units_path=None):
    with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
        content = file.read()

    try:
        original_text = OldTexts(content)
    except Exception as e:
        print("OldTexts 처리 중 오류:", e)
        return
    
    # <body> ~ </body> 추출 (없으면 전체 사용)
    body_match = re.search(r"<body>(.*?)</body>", content, re.DOTALL)
    body_text = body_match.group(1) if body_match else content

    #태그 제거 
    no_tags = re.sub(r"<[^>]+>", "", str(body_text))
    #남은 한자 제거
    cleaned_text= re.sub(r"[\u4E00-\u9FFF]", "", no_tags)
    #어절단위 분리
    units = re.split(r'[ ]+', cleaned_text)
    units = [u for u in units if u]

    print(f"어절 수: {len(units)}개 (앞 30개 출력)")
    for unit in units[:30]:
        print(unit)

    # OldTexts 객체로 다시 구성
    cleaned_text_obj = OldTexts(cleaned_text)
    print("최종 OldTexts 객체 생성 완료")
    print(str(cleaned_text_obj)[:300], "...")

    # 어절 리스트 저장
    if save_units_path:
        with open(save_units_path, 'w', encoding=encoding) as f:
            for unit in units:
                f.write(unit + '\n')
    return {
        "original": original_text,
        "cleaned_str": cleaned_text,
        "units": units,
        "final_obj": cleaned_text_obj
    }


result = process_old_hangeul_text(
    '/Users/hayeon/KORE208/finalproject/19-20세기/A0BB0111.txt',
    encoding='utf-16-le',
    save_units_path='/Users/hayeon/KORE208/finalproject/19-20세기/cleaned_A0BB0111.txt'
)

with open('/Users/hayeon/KORE208/finalproject/19-20세기/A0BB0111.txt', 'r', encoding='utf-16-le', errors='ignore') as file:
    content = file.read()
print(content)

import chardet

with open("/Users/hayeon/KORE208/finalproject/19-20세기/A0BB0111.txt", "rb") as f:
    result = chardet.detect(f.read())

print(result)
