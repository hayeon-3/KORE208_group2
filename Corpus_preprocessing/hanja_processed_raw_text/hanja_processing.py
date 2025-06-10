# %%
import os
import hanja
from hanja import hangul

def process_hanja_files(input_folder_path, output_folder_path):
    
    # 출력 폴더 생성성
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"출력 폴더 '{output_folder_path}'를 생성했습니다.")

    # 입력 폴더의 모든 파일 목록을 가져옵니다.
    for filename in os.listdir(input_folder_path):
        # 텍스트 파일(.txt)만 선택하여 처리합니다. 필요에 따라 다른 확장자도 추가할 수 있습니다.
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_folder_path, filename)
            output_filepath = os.path.join(output_folder_path, f"processed_{filename}") 

            print(f"'{filename}' 파일을 처리 중...")

            try:
                with open(input_filepath, 'r', encoding='utf-16') as infile:
                    content = infile.read()

                # --- 한자 처리 ---
                processed_content = hanja.translate(content, 'substitution') # 한자를 한글로 변환
               
                with open(output_filepath, 'w', encoding='utf-16') as outfile:
                    outfile.write(processed_content)

                print(f"'{filename}' 처리가 완료되어 '{os.path.basename(output_filepath)}'로 저장했습니다.")

            except Exception as e:
                print(f"오류 발생 - '{filename}' 처리 중 오류: {e}")
        else:
            print(f"'{filename}'은(는) 텍스트 파일이 아니므로 건너뜁니다.")

# --- 실제 사용 ---
if __name__ == "__main__":
    # !!! 중요: 아래 폴더 경로를 실제 사용하실 경로로 수정해주세요 !!!
    # 원본 파일들이 있는 폴더
    source_folder = "C:\\Users\\bbbbb\\Desktop\\25-1\\KORE208_group2\\raw_추가\\개화기_raw" 

    # 처리된 파일을 저장할 폴더
    destination_folder = "C:\\Users\\bbbbb\\Desktop\\25-1\\processed_enlightenment" # 예시 경로

    process_hanja_files(source_folder, destination_folder)
    print("\n모든 파일 처리가 완료되었습니다.")
# %%
