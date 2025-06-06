# Simple word splitter
def split_text(text):
    return text.split()

# Original known sentence
sentence = "hi how are you"

# Unknown sentence to test
new_sentence = "hi where are you now"

# Step 1: Split sentence into words
words = split_text(sentence)
print("Words from sentence:", words)

# Step 2: Make vocabulary (each word gets a number)
vocab = {}
index = 0
for word in words:
    if word not in vocab:
        vocab[word] = index
        index += 1

print("Vocabulary:", vocab)

# Step 3: Make the reverse of vocab to decode numbers back to words
reverse_vocab = {}
for word, number in vocab.items():
    reverse_vocab[number] = word

# Step 4: Encoding = turn words into numbers
def encode(text):
    words = split_text(text)
    code = []
    for word in words:
        if word in vocab:
            code.append(vocab[word])
        else:
            code.append(-1)  # unknown word
    return code

# Step 5: Decoding = turn numbers back into words
def decode(numbers):
    result = []
    for num in numbers:
        if num in reverse_vocab:
            result.append(reverse_vocab[num])
        else:
            result.append("<UNK>")  # unknown word
    return " ".join(result)

# Try encoding and decoding
print("\nEncoding original sentence:")
encoded_original = encode(sentence)
print("Encoded:", encoded_original)
print("Decoded:", decode(encoded_original))

print("\nEncoding unknown sentence:")
encoded_new = encode(new_sentence)
print("Encoded:", encoded_new)
print("Decoded:", decode(encoded_new))
