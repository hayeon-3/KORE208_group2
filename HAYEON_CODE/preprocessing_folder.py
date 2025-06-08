import os
import re
import unicodedata
from OldHangeul import OldTexts

def read_file_with_fallback(filepath):
    # utf-8로 먼저 시도
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # utf-16으로 재시도
        try:
            with open(filepath, 'r', encoding='utf-16') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 인코딩 실패: {filepath} → {e}")
            return None

def process_old_hangeul_text(filepath):
    content = read_file_with_fallback(filepath)
    if content is None:
        return None

    try:
        original_text = OldTexts(content)
    except Exception as e:
        print(f"OldTexts 처리 중 오류 ({filepath}):", e)
        return None

    body_match = re.search(r"<body>(.*?)</body>", content, re.DOTALL)
    body_text = body_match.group(1) if body_match else content
    no_tags = re.sub(r"<[^>]+>", "", str(body_text))
    cleaned_text = re.sub(r"[\u4E00-\u9FFF]", "", no_tags)
    cleaned_text = unicodedata.normalize("NFD", str(cleaned_text))

    try:
        old_obj = OldTexts(cleaned_text)
    except Exception as e:
        print(f"OldTexts 오류 ({filepath}):", e)
        return None

    output_str = str(old_obj)
    units = re.split(r'\s+', output_str)
    units = [u for u in units if u]

    return units

def process_all_txt_files_to_cleaned_folder(input_folder):
    output_folder = os.path.join(input_folder, "cleaned_output")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            units = process_old_hangeul_text(input_path)  # 변수명 통일

            if units:
                output_filename = f"cleaned_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                with open(output_path, 'w', encoding='utf-16') as f:
                    for unit in units:
                        f.write(unit + '\n')
                print(f"저장 완료: {output_filename} ({len(units)}개 어절)")
            else:
                print(f"처리 실패: {filename}")



folder_path = "/Users/hayeon/Downloads/19"
process_all_txt_files_to_cleaned_folder(folder_path)
