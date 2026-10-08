from collections import Counter
text="never gonna give you up never gonna let you down"
words=text.lower().split()
vocab={"<UNK>":0}
for word in sorted(set(words)):
    vocab[word]=len(vocab)

encoded=[vocab.get(word, vocab["<UNK>"]) for word in words]
print("Vocab:", vocab)
print("Encoded:", encoded)
print("Decoded:", [next(k for k,v in vocab.items() if v==i) for i in encoded])
