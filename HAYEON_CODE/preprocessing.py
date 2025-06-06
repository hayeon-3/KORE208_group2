import re
import unicodedata
from OldHangeul import OldTexts


def process_old_hangeul_text(filepath, encoding='utf-8', save_units_path=None):
    with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
        content = file.read()

    try:
        original_text = OldTexts(content)
    except Exception as e:
        print("OldTexts 처리 중 오류:", e)
        return
    
    ### 전처리
    # <body> ~ </body> 추출 (없으면 전체 사용)
    body_match = re.search(r"<body>(.*?)</body>", content, re.DOTALL)
    body_text = body_match.group(1) if body_match else content
    #태그 제거 
    no_tags = re.sub(r"<[^>]+>", "", str(body_text))
    #남은 한자 제거
    cleaned_text= re.sub(r"[\u4E00-\u9FFF]", "", no_tags)
    #정규화 추가
    cleaned_text = unicodedata.normalize("NFD", str(cleaned_text))


    # #어절단위 분리
    # units = re.split(r'[ ]+', cleaned_text)
    # units = [u for u in units if u]

    # print(f"어절 수: {len(units)}개 (앞 30개 출력)")
    # for unit in units[:30]:
    #     print(unit)

    # # OldTexts 객체로 다시 구성
    # cleaned_text_obj = OldTexts(cleaned_text)
    # print("최종 OldTexts 객체 생성 완료")
    # print(str(cleaned_text_obj)[:300], "...")

    # ⚠️ 여기서 바로 OldTexts 적용
    try:
        old_obj = OldTexts(cleaned_text)
    except Exception as e:
        print("OldTexts 오류:", e)
        return

    # 출력용 문자열
    output_str = str(old_obj)
    print("최종 OldTexts 객체 생성 완료")
    print(output_str[:300], "...")

    # 어절 분리 (OldTexts 처리된 텍스트에서 split)
    units = re.split(r'\s+', output_str)
    units = [u for u in units if u]
    print(f"어절 수: {len(units)}개 (앞 30개 출력)")
    for unit in units[:30]:
        print(unit)

    # 어절 리스트 저장
    if save_units_path:
        with open(save_units_path, 'w', encoding=encoding) as f:
            for unit in units:
                f.write(unit + '\n')
    return {
        "final_obj": old_obj,
        "cleaned_str": output_str,
        "units": units,
    }

result = process_old_hangeul_text(
    '/Users/hayeon/KORE208/finalproject/15-16세기/16/A6CF0004(1517)-1.txt',
    encoding='utf-8',
    save_units_path='/Users/hayeon/KORE208/finalproject/15-16세기/16/cleaned_A6CF0004(1517)-1.txt'
)