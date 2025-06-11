#%%
import os
import pandas as pd

#%%
def create_labeled_dataframe_from_nested_folders(base_master_folder_path):
    
    data = []  # 텍스트 내용과 라벨을 저장할 리스트

    folder_name_to_label_map = {
        "processed_15": "15C",
        "processed_16": "16C",
        "processed_modern": "modern",
        "processed_enlightenment": "enlightenment",
    }

    if not os.path.isdir(base_master_folder_path):
        print(f"오류: 최상위 폴더 '{base_master_folder_path}'는 유효한 경로가 아닙니다.")
        return pd.DataFrame(columns=['content', 'timeline'])

    print(f"최상위 폴더: '{base_master_folder_path}'에서 파일 탐색 시작.")

    # ✅ 이 for문부터 전체가 함수 내부로 들어가야 함
    for processed_folder_name in folder_name_to_label_map.keys():
        current_processed_folder_path = os.path.join(base_master_folder_path, processed_folder_name)
        cleaned_output_folder_path = os.path.join(current_processed_folder_path, "cleaned_output")

        if not os.path.isdir(cleaned_output_folder_path):
            print(f"경고: '{cleaned_output_folder_path}' 폴더를 찾을 수 없습니다. 건너뜁니다.")
            continue

        label = folder_name_to_label_map[processed_folder_name]
        print(f"'{processed_folder_name}' 폴더 ({cleaned_output_folder_path})의 파일을 처리 중... 라벨: {label}")

        for filename in os.listdir(cleaned_output_folder_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(cleaned_output_folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(filepath, 'r', encoding='utf-16') as f:
                            content = f.read()
                    except UnicodeDecodeError:
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

    df = pd.DataFrame(data)
    print(f"\n총 {len(df)}개의 데이터 포인트를 가진 데이터 프레임이 생성되었습니다.")
    return df

# --- 사용 예시 (경로 및 파일이름 확인 필수) ---
if __name__ == "__main__":
    # !!! 중요: 이 경로를 정확하게 수정하세요 !!!
    # 'processed_15', 'processed_16' 등이 들어있는 'hanja_processed_raw_text' 폴더의 경로
    base_data_folder = r"/Users/hayeon/KORE208/finalproject/Corpus_preprocessing/hanja_processed_raw_text"

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
    output_base_dir = r"/Users/hayeon/KORE208/finalproject/exercise_KORE208_group2"
    
    output_file_name = 'final_final_dataframe.csv'

    output_csv_path = os.path.join(output_base_dir, output_file_name)

    machine_learning_df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"\n데이터 프레임이 '{output_csv_path}'에 CSV 파일로 저장되었습니다.")

# %%
