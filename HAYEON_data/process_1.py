from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

tokenizer = Tokenizer()
tokenizer.fit_on_texts(text)
print(tokenizer.word_index)

with open('/Users/hayeon/KORE208/finalproject/15-16세기/cleaned_A5CA0001-1.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import sentencepiece as spm

# 텍스트 파일 기반 모델 학습
spm.SentencePieceTrainer.train(
    input= text,
    model_prefix='spm_model',
    vocab_size=800,
    character_coverage=1.0,
    model_type='bpe'  # unigram, bpe, char, word
)

sp = spm.SentencePieceProcessor()
sp.load("spm_model.model")

tokens = sp.encode("훈민정음", out_type=str)
print(tokens)  # 예: ['훈', '민', '정음']
