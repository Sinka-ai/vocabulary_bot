from gensim.models import KeyedVectors

# Загружаем сохраненную модель с диска
model_word2vec = KeyedVectors.load('glove-wiki-gigaword-100.model', mmap='r')

print(model_word2vec)