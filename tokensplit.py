import streamlit as st
import re

# Tokenize function
def tokenize(text):
    tokens = re.split(r'([,.:;?_!"()\']|--|\s)', text)
    return [t.strip() for t in tokens if t.strip()]

# SimpleTokenizer class
class SimpleTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab
        self.rev_vocab = {v: k for k, v in vocab.items()}

    def encode(self, text):
        tokens = tokenize(text)
        return [self.vocab.get(t, -1) for t in tokens]  # -1 for unknown tokens

    def decode(self, ids):
        tokens = [self.rev_vocab.get(i, "<UNK>") for i in ids]
        return " ".join(tokens)

# Streamlit UI
st.title("Simple Tokenizer with Vocabulary")

# Input texts
text = st.text_input("Known Text (used to create vocabulary):", "hi how are you")
unknown_text = st.text_input("Unknown Text (to encode/decode):", "hi where are you now")

# Tokenize known text and build vocab
tokens = tokenize(text)
vocab = {token: idx for idx, token in enumerate(sorted(set(tokens)))}

st.subheader("Step 1: Tokenization of Known Text")
st.write(tokens)

st.subheader("Step 2: Vocabulary")
st.write(vocab)

# Initialize tokenizer
tokenizer = SimpleTokenizer(vocab)

st.subheader("Step 3: Encoding and Decoding")

# Encode and decode known text
encoded = tokenizer.encode(text)
decoded = tokenizer.decode(encoded)
st.markdown("**Known Text**")
st.write("Encoded:", encoded)
st.write("Decoded:", decoded)

# Encode and decode unknown text
encoded_unknown = tokenizer.encode(unknown_text)
decoded_unknown = tokenizer.decode(encoded_unknown)
st.markdown("**Unknown Text**")
st.write("Encoded:", encoded_unknown)
st.write("Decoded:", decoded_unknown)
