import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

st.title(" Text File Q&A Chatbot")

# Upload a .txt file
uploaded_file = st.file_uploader(" Upload a.txt file", type=["txt","ppt","pdf","word"])

if uploaded_file:
    # Read file text
    text = uploaded_file.read().decode("latin-1")
    st.success("File uploaded successfully!")

    # Embed full text
    doc_embedding = model.encode([text])
    

    # Get user question
    user_question = st.text_input(" Ask a question based on the file:")

    if user_question:
        # Embed question
        question_embedding = model.encode([user_question])

        # Calculate similarity
        score = cosine_similarity(question_embedding, doc_embedding)[0][0]

        st.write(f"Similarity Score: `{score:.2f}`")

        # Show answer if similar enough
        if score > 0.4:
            st.subheader("Answer (from the file):")
            st.write(text)
        else:
            st.warning("Sorry, I couldn't find a relevant answer.")
