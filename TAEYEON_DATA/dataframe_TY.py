#%%
import os
import pandas as pd

def create_labeled_dataframe_from_nested_folders(base_master_folder_path):
    
    data = [] # 텍스트 내용과 라벨을 저장할 리스트

    # --- 폴더 이름과 라벨 매핑 정의 ---
    # 이 딕셔너리를 필요에 따라 수정하여 원하는 폴더 이름과 라벨을 추가하세요.
    # 키는 'processed_XX' 형태의 폴더 이름이고, 값은 부여할 라벨입니다.
    folder_name_to_label_map = {
        "processed_15": "15C",
        "processed_16": "16C",
        "processed_modern": "modern",
        "processed_enlightenment": "enlightenment",
        # 필요한 다른 processed_X 폴더와 그에 해당하는 라벨을 여기에 추가하세요.
    }
    # -------------------------------

    if not os.path.isdir(base_master_folder_path):
        print(f"오류: 최상위 폴더 '{base_master_folder_path}'는 유효한 경로가 아닙니다.")
        return pd.DataFrame(columns=['content', 'timeline'])

    print(f"최상위 폴더: '{base_master_folder_path}'에서 파일 탐색 시작.")

    # 최상위 폴더 내의 모든 항목을 탐색합니다.
    for processed_folder_name in os.listdir(base_master_folder_path):
        # 현재 항목의 전체 경로를 만듭니다.
        current_processed_folder_path = os.path.join(base_master_folder_path, processed_folder_name)

        # 1. 항목이 폴더이고, 2. 미리 정의된 매핑에 해당하는 폴더 이름인지 확인합니다.
        if os.path.isdir(current_processed_folder_path) and \
           processed_folder_name in folder_name_to_label_map:

            # 해당 'processed_XX' 폴더 안에 있는 'cleaned_output' 폴더의 경로를 만듭니다.
            cleaned_output_folder_path = os.path.join(current_processed_folder_path, "cleaned_output")

            # 'cleaned_output' 폴더가 실제로 존재하는지 확인합니다.
            if not os.path.isdir(cleaned_output_folder_path):
                print(f"경고: '{cleaned_output_folder_path}' 폴더를 찾을 수 없습니다. 건너뜁니다.")
                continue

            # 이 폴더의 라벨을 가져옵니다.
            label = folder_name_to_label_map[processed_folder_name]

            print(f"'{processed_folder_name}' 폴더 ({cleaned_output_folder_path})의 파일을 처리 중... 라벨: {label}")

            # 'cleaned_output' 폴더 내의 모든 텍스트 파일을 읽습니다.
            for filename in os.listdir(cleaned_output_folder_path):
                if filename.endswith(".txt"):
                    filepath = os.path.join(cleaned_output_folder_path, filename)

                    try:
                        # 파일 인코딩 처리 (UTF-8 우선, 실패 시 UTF-16, Latin-1 대체)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        try:
                            with open(filepath, 'r', encoding='utf-16') as f:
                                content = f.read()
                        except UnicodeDecodeError:
                            # 최후의 수단: Latin-1 (모든 바이트를 오류 없이 디코드)
                            with open(filepath, 'r', encoding='latin-1', errors='replace') as f:
                                content = f.read()
                                print(f"경고: '{filename}' 파일을 Latin-1로 읽었으며, 일부 문자가 대체되었을 수 있습니다.")
                        except Exception as e:
                            print(f"오류: '{filename}' 파일을 UTF-16으로도 읽을 수 없습니다. {e}")
                            continue
                    except Exception as e:
                        print(f"오류: '{filename}' 파일을 읽는 중 예상치 못한 오류 발생: {e}")
                        continue

                    data.append({'content': content, 'timeline': label})
                    # print(f" - '{filename}' 추가됨") # 디버깅용: 파일이 제대로 추가되는지 확인

        elif os.path.isdir(current_processed_folder_path):
            print(f"경고: '{processed_folder_name}' 폴더는 미리 정의된 라벨 매핑에 없어 건너뜜니다.")
        # else: 파일은 무시 (폴더만 처리)

    df = pd.DataFrame(data)
    print(f"\n총 {len(df)}개의 데이터 포인트를 가진 데이터 프레임이 생성되었습니다.")
    return df

# --- 사용 예시 (경로 및 파일이름 확인 필수) ---
if __name__ == "__main__":
    # !!! 중요: 이 경로를 정확하게 수정하세요 !!!
    # 'processed_15', 'processed_16' 등이 들어있는 'hanja_processed_raw_text' 폴더의 경로
    base_data_folder = r"C:\Users\bbbbb\Desktop\25-1\KORE208_group2\hanja_processed_raw_text"

    # 데이터 프레임 생성 함수 호출
    machine_learning_df = create_labeled_dataframe_from_nested_folders(base_data_folder)

    # 생성된 데이터 프레임의 상위 5행을 출력하여 확인
    print("\n생성된 데이터 프레임 미리보기:")
    print(machine_learning_df.head())

    # 데이터 프레임 정보 확인
    print("\n데이터 프레임 정보:")
    machine_learning_df.info()

    # 각 라벨별 데이터 개수 확인
    print("\n라벨별 데이터 개수:")
    print(machine_learning_df['timeline'].value_counts())

    # 데이터 프레임을 CSV 파일로 저장(본인의 경로로 수정필요)
    output_base_dir = r"C:\Users\bbbbb\Desktop\25-1\KORE208_group2"
    
    output_file_name = 'final_dataframe.csv'

    output_csv_path = os.path.join(output_base_dir, output_file_name)

    machine_learning_df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"\n데이터 프레임이 '{output_csv_path}'에 CSV 파일로 저장되었습니다.")
