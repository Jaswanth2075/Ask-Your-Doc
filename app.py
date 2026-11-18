import streamlit as st

from document_processing.document_processor import extracted_doc

from rag.chunking import split_text
from rag.embeddings import generate_embeddings
from rag.vector_store import create_vector_store

st.title("📚 Ask Your Doc")

st.write(
    "Upload your documents and ask questions "
    "based on their contents."
)

uploaded_files = st.file_uploader(
    "Upload your documents",
    type=["pdf", "txt", "xlsx", "xls"],
    accept_multiple_files=True
)


# --------------------------------
# 6. Process Button
# --------------------------------

def process_documents(files):
    all_docs = []

    for file in files :
        doc = extracted_doc(file)
        all_docs.extend(doc)

    if not all_docs:
        raise ValueError("No Content Uploaded")
    
    #chunking
    all_chunks = []
    for doc in all_docs:
        text = doc["text"]
        metadata = doc["metadata"]
        chunks = split_text(text)

        for chunk_id, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "text" : chunk,
                    "metadata" : {
                        **metadata,
                        "chunk_id": chunk_id
                    }
                }
            )
    if not all_chunks:
        raise ValueError("Chunking Error")


    #embedding
    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    #Create FAISS vector store
    vector_index = create_vector_store(
        all_chunks,
        embeddings
    )

    return vector_index, all_chunks




if st.button(
    "Process Documents",
    disabled=not uploaded_files,
    use_container_width=True
):

    with st.spinner("Processing your documents..."):

        try:

            index, chunks = process_documents(
                uploaded_files
            )

            



            st.session_state.vector_index = index
            st.session_state.chunks = chunks
            st.session_state.ready = True
            st.session_state.chat_history = []

            st.success(
                f"Successfully processed {len(uploaded_files)} document(s)!"
            )

        except Exception as e:

            st.error(f"Processing failed: {e}")


# --------------------------------
# 7. Chat Interface
# --------------------------------

if st.session_state.ready:

    st.divider()

    st.subheader("💬 Chat with your documents")

    # Display previous conversation
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View sources"):
                    for source in message["sources"]:
                        st.write(source)

    # User text input
    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question:

        # Display user question
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve relevant chunks and generate answer
        with st.chat_message("assistant"):

            with st.spinner("Finding your answer..."):

                try:

                    retrieved_chunks = retrieve_chunks(
                        question,
                        st.session_state.vector_index,
                        st.session_state.chunks,
                        top_k=TOP_K,
                        model_name=EMBEDDING_MODEL
                    )

                    answer = generate_answer(
                        question,
                        retrieved_chunks,
                        GEMINI_API_KEY
                    )

                    st.markdown(answer)

                    sources = []

                    for item in retrieved_chunks:

                        metadata = item.get("metadata", {})

                        source = metadata.get(
                            "source",
                            "Unknown"
                        )

                        location = ""

                        if "page" in metadata:
                            location = f" | Page {metadata['page']}"

                        elif "sheet" in metadata:
                            location = f" | Sheet {metadata['sheet']}"

                        sources.append(
                            f"{source}{location}"
                        )

                    with st.expander("View sources"):
                        for source in dict.fromkeys(sources):
                            st.write(f"- {source}")

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": list(dict.fromkeys(sources))
                    })

                except Exception as e:

                    st.error(f"Error generating answer: {e}")


# --------------------------------
# 8. Reset Chat
# --------------------------------

if st.session_state.ready:

    if st.button("Clear Chat"):

        st.session_state.chat_history = []
        st.rerun()








