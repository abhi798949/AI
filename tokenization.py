import re
import tiktoken

# Read the text file
with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Tokenize the text using regex
def tokenize_regex(text):
    preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
    return [item.strip() for item in preprocessed if item.strip()]

preprocessed = tokenize_regex(raw_text)

# Create vocabulary
all_words = sorted(set(preprocessed))
vocab = {token: integer for integer, token in enumerate(all_words)}

# Tokenizer V1: Basic tokenizer
class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        preprocessed = tokenize_regex(text)
        return [self.str_to_int[s] for s in preprocessed]

    def decode(self, ids):
        text = " ".join( [self.int_to_str[i] for i in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

# Tokenizer V2: Tokenizer with <|unk|> and <|endoftext|>
all_tokens = sorted(list(set(preprocessed)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
vocab_v2 = {token: integer for integer, token in enumerate(all_tokens)}

class SimpleTokenizerV2:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        preprocessed = tokenize_regex(text)
        preprocessed = [item if item in self.str_to_int else "<|unk|>" for item in preprocessed]
        return [self.str_to_int[s] for s in preprocessed]

    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        text = re.sub(r'\s+([,.?!\"()\'])', r'\1', text)
        return text

# Tiktoken example
def tiktoken_example():
    enc = tiktoken.get_encoding("gpt2")
    print("Tiktoken encode:", enc.encode("This is a test!"))
    print("Tiktoken decode:", enc.decode([835, 318, 257, 2202, 0]))

    text = "Hello, do you like tea? In the sunlit terraces of the palace."
    tokenizer_v1 = SimpleTokenizerV1(vocab)
    tokenizer_v2 = SimpleTokenizerV2(vocab_v2)

    ids_v1 = tokenizer_v1.encode(text)
    ids_v2 = tokenizer_v2.encode(text)
    ids_tiktoken = enc.encode(text)

    print("Our Tokenizer V1:", tokenizer_v1.decode(ids_v1))
    print("Our Tokenizer V2:", tokenizer_v2.decode(ids_v2))
    print("Tiktoken:", enc.decode(ids_tiktoken))

# Run examples
tokenizer_v1 = SimpleTokenizerV1(vocab)
text_v1 = """It's the last he painted, you know," 
           Mrs. Gisburn said with pardonable pride."""
print("Tokenizer V1 Encode:", tokenizer_v1.encode(text_v1))
print("Tokenizer V1 Decode:", tokenizer_v1.decode(tokenizer_v1.encode(text_v1)))

tokenizer_v2 = SimpleTokenizerV2(vocab_v2)
text_v2 = "Hello, do you like tea? <|endoftext|> In the sunlit terraces of the palace."
print("Tokenizer V2 Encode:", tokenizer_v2.encode(text_v2))
print("Tokenizer V2 Decode:", tokenizer_v2.decode(tokenizer_v2.encode(text_v2)))

tiktoken_example()