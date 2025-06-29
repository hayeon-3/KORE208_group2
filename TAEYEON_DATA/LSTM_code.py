# %%
#필요한 패키지 import > pip install tensorflow, pandas, numpy, scikit-learn, matplotlib(시각화)
#CSV 파일은 현재 github 내 final_dataframe.csv 불러오시면 됩니다. (15C, 16C, mordern, enlightenment 시기구분)
#현재 LSTM 모델이 어떻게 돌아가는지 시험적으로 코드를 써본 것이기 때문에, 데이터 추가 구축 후 코드 수정하겠습니다.
#데이터셋 분류 양 및 하이퍼파라미터 조정, 모델 성능평가 지표, 주석 역시 이후에 수정하겠습니다.
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np 
#%%
#(선택사항) 현재 작업경로 확인
import os

os.getcwd()

#%%
# 1. CSV 파일 로드 
df = pd.read_csv('../final_dataframe.csv')

#%%
# 2. 'content' 열 토큰화 (공백 기반 어절 split)
# Tokenizer는 내부적으로 텍스트를 공백 기준으로 분리하므로, 이 단계에서 직접 split()을 하지 않고
# Tokenizer에 리스트 형태가 아닌 문자열 리스트를 바로 전달하는 것이 더 효율적입니다.
# df['tokenized_content'] = df['content'].apply(lambda x: x.split(' ')) 

#%%
# 3. 어휘 집합 구축 및 정수 인코딩 (keras Tokenizer 활용)
# num_words: 가장 빈도가 높은 단어들만 사용할지 여부 (여기서는 모든 단어 사용)
# oov_token: Out-Of-Vocabulary 단어를 처리할 토큰 (훈련 데이터에 없는 단어)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['content']) # 텍스트를 학습하여 어휘 집합 구축

word_index = tokenizer.word_index # 단어-정수 매핑 딕셔너리
vocab_size = len(word_index) + 1 # 어휘 집합 크기 (+1은 0번 패딩 토큰 때문)

print(f"\n어휘 집합 크기 (vocab_size): {vocab_size}")
print("\n단어-정수 매핑 예시 (상위 10개):")
# sorted(word_index.items(), key=lambda item: item[1])은 값(정수 인덱스) 기준으로 정렬
for word, index in list(word_index.items())[:10]:
    print(f"'{word}': {index}")

# 텍스트 시퀀스를 정수 시퀀스로 변환
encoded_sequences = tokenizer.texts_to_sequences(df['content'])

print("\n정수 인코딩된 시퀀스 예시 (첫 2개):")
for i, seq in enumerate(encoded_sequences[:2]):
    print(f"Original: '{df['content'].iloc[i]}'")
    print(f"Encoded: {seq}\n")

#%%
# 4. 패딩 (Padding)
# 모든 시퀀스의 길이를 동일하게 맞춤
max_sequence_length = max(len(s) for s in encoded_sequences)
print(f"\n최대 시퀀스 길이: {max_sequence_length}")

padded_sequences = pad_sequences(encoded_sequences, maxlen=max_sequence_length, padding='post') # 뒤에 0으로 채움

print("\n패딩된 시퀀스 예시 (첫 2개):")
print(padded_sequences[:2])

#%%
# 5. 타임라인 레이블 정수 인코딩
# 현재 4개의 레이블: '15C', '16C', 'modern', 'enlightenmen'
# 딥러닝 분류 모델의 출력 레이어에 One-Hot Encoding을 사용하므로,
# 여기서는 라벨을 정수로 인코딩하고, 모델 구성 시 `to_categorical`을 사용할 수 있습니다.
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
df['timeline_encoded'] = label_encoder.fit_transform(df['timeline'])
num_classes = len(label_encoder.classes_) # 분류할 클래스 개수

print(f"\n타임라인 레이블 및 인코딩:")
for i, label in enumerate(label_encoder.classes_):
    print(f"'{label}' -> {i}")
print(f"총 분류 클래스 수: {num_classes}")
print("\n인코딩된 타임라인 레이블 예시:")
print(df[['timeline', 'timeline_encoded']].head())

# 모델 입력 준비 완료:
# X: padded_sequences (numpy 배열)
# y: df['timeline_encoded'].values (numpy 배열)
# %%

# 6. 타임라인 레이블 원-핫 인코딩
# 딥러닝 분류 모델의 출력 레이어에 사용될 원-핫 인코딩
# 예: 0 -> [1, 0, 0], 1 -> [0, 1, 0], 2 -> [0, 0, 1]
from tensorflow.keras.utils import to_categorical # to_categorical 임포트

labels_one_hot = to_categorical(df['timeline_encoded'], num_classes=num_classes)

print(f"\n원-핫 인코딩된 타임라인 레이블 예시:")
print(labels_one_hot[:5])

#%%
# 7. 데이터 분할 (훈련, 테스트 세트)
# 모델 훈련을 위한 입력(X)과 정답(y) 데이터 준비
X = padded_sequences # 패딩된 정수 시퀀스 (모델 입력)
y = labels_one_hot # 원-핫 인코딩된 타임라인 레이블 (모델 정답)

# sklearn.model_selection.train_test_split 임포트
from sklearn.model_selection import train_test_split

# 데이터를 훈련 세트와 테스트 세트로 분할
# test_size=0.2: 전체 데이터의 20%를 테스트 데이터로 사용
# random_state=42: 재현성을 위한 시드 (동일한 결과를 얻기 위해 고정)
# stratify=y: y(레이블)의 비율을 훈련/테스트 세트에서 동일하게 유지 (클래스 불균형 방지)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n훈련 데이터 X_train shape: {X_train.shape}")
print(f"훈련 데이터 y_train shape: {y_train.shape}")
print(f"테스트 데이터 X_test shape: {X_test.shape}")
print(f"테스트 데이터 y_test shape: {y_test.shape}")

#%%
# 8. LSTM 모델 정의 및 구축 
# 필요한 Keras 레이어 임포트
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

embedding_dim = 100 # 각 단어(어절)를 표현할 임베딩 벡터의 차원 (하이퍼파라미터, 50~300 사이에서 조절)

model = Sequential() # 순차적으로 레이어를 쌓아 올리는 Keras 모델
# Embedding Layer: 단어 인덱스를 저차원 밀집 벡터(임베딩)로 변환하는 역할
# input_dim: 어휘 집합의 크기 (총 단어 개수, vocab_size, 이전 코드에서 계산됨)
# output_dim: 임베딩 벡터의 차원 (embedding_dim)
# input_length: 입력 시퀀스의 길이 (패딩된 최대 길이, max_sequence_length, 이전 코드에서 계산됨)
model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length))

# LSTM Layer: 시퀀스 데이터를 처리하고 장기 의존성을 학습
# units: LSTM 셀의 출력 차원 (hidden state size), 모델의 '기억력'과 복잡도를 결정 (하이퍼파라미터, 64, 128, 256 등)
# return_sequences=False: 분류 작업이므로 마지막 타임 스텝의 출력만 Dense Layer로 전달
model.add(LSTM(units=128))

# Dropout Layer: 과적합(overfitting) 방지를 위해 무작위로 일부 뉴런을 비활성화
# 0.5: 50%의 뉴런을 비활성화 (하이퍼파라미터, 0.2~0.5 사이에서 조절)
model.add(Dropout(0.5))

# Dense Layer (출력 층): 최종 분류를 위한 완전 연결층
# units: 분류할 클래스의 개수 (num_classes, 이전 코드에서 계산됨)와 동일해야 함
# activation='softmax': 다중 클래스 분류 시 각 클래스에 속할 확률을 출력
model.add(Dense(units=num_classes, activation='softmax'))

# 모델의 구조 요약 정보 출력
model.summary()

#%%
# 9. 모델 컴파일 
# 모델 학습에 필요한 설정 (최적화 방법, 손실 함수, 평가 지표)
model.compile(
    optimizer='adam', # 최적화 도구: Adam (가장 널리 사용되고 효과적)
    loss='categorical_crossentropy', # 손실 함수: 다중 클래스 분류를 위한 교차 엔트로피 (원-핫 인코딩된 레이블 사용 시)
    metrics=['accuracy'] # 모델 성능 평가 지표: 정확도
)

#%%
# 10. 모델 학습 (훈련)
# X_train과 y_train 데이터를 사용하여 모델 학습
history = model.fit(
    X_train, y_train,
    epochs=10, # 전체 훈련 데이터를 반복할 횟수 (하이퍼파라미터, 데이터 양에 따라 조절)
    batch_size=32, # 한 번에 처리할 샘플의 개수 (하이퍼파라미터, GPU 메모리 및 학습 속도에 영향)
    validation_split=0.2, # 훈련 데이터 중 20%를 검증 데이터로 사용하여 학습 중 성능 모니터링
    verbose=1 # 학습 진행 상황을 자세히 출력 (0: 출력 없음, 1: 진행바, 2: 에포크마다 요약)
)

#%%
# 11. 모델 평가 (테스트 데이터)
# 훈련되지 않은 X_test와 y_test 데이터를 사용하여 최종 모델 성능 평가
loss, accuracy = model.evaluate(X_test, y_test, verbose=0) # verbose=0: 출력 없이 결과만 반환
print(f"\n테스트 데이터 손실(Loss): {loss:.4f}")
print(f"테스트 데이터 정확도(Accuracy): {accuracy:.4f}")

#%%
# 12. 추가: 학습 과정 시각화 (선택 사항)
import matplotlib.pyplot as plt # matplotlib 임포트

# 학습 히스토리에서 정확도와 손실 값 가져오기
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

#%%
# 13. 추가: 예측 및 분류 결과 확인 (선택 사항)
# 테스트 데이터의 일부 샘플에 대한 예측
predictions = model.predict(X_test)
# 각 예측은 클래스별 확률 분포이므로, 가장 높은 확률을 가진 클래스를 선택
predicted_classes = np.argmax(predictions, axis=1)

# 실제 클래스와 예측 클래스를 비교
true_classes = np.argmax(y_test, axis=1)

print("\n--- 테스트 데이터 예측 결과 예시 ---")
for i in range(min(5, len(X_test))): # 첫 5개 샘플만 확인
    print(f"샘플 {i+1}:")
    print(f"  실제 레이블 (인코딩): {true_classes[i]}")
    print(f"  예측 레이블 (인코딩): {predicted_classes[i]}")
    # 실제 레이블을 원래 문자열로 변환 (역변환)
    print(f"  실제 시대: {label_encoder.inverse_transform([true_classes[i]])[0]}")
    print(f"  예측 시대: {label_encoder.inverse_transform([predicted_classes[i]])[0]}")
    print("-" * 20)
# %%
