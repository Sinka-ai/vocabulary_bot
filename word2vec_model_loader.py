import gensim.downloader as api

# Загрузим модель с интернета
model_word2vec = api.load('glove-wiki-gigaword-100')

# Сохраним модель на диск
model_word2vec.save('glove-wiki-gigaword-100.model')
