# Import Streamlit for the chat UI
import streamlit as st

# Import LangChain components for RAG
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Import built-in modules for Ollama API
import json
import urllib.request
import os


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

DOCUMENT_FILE = "my_document.docx"
OLLAMA_MODEL = "qwen2.5:0.5b"


# --------------------------------------------------
# FUNCTION TO CREATE THE RAG VECTOR DATABASE
# --------------------------------------------------

@st.cache_resource
def create_vector_store():

    # Check if the document exists
    if not os.path.exists(DOCUMENT_FILE):
        return None

    # Load the .docx document
    loader = Docx2txtLoader(DOCUMENT_FILE)

    documents = loader.load()

    # Split the document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    # Create embeddings using Ollama
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # Store the chunks in FAISS
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store


# --------------------------------------------------
# FUNCTION TO RETRIEVE TOP 3 DOCUMENT CHUNKS
# --------------------------------------------------

def retrieve_top_3(vector_store, question):

    # Search for the 3 most relevant document chunks
    results = vector_store.similarity_search(
        question,
        k=3
    )

    return results


# --------------------------------------------------
# FUNCTION TO CALL OLLAMA
# --------------------------------------------------

def ask_ollama(messages):

    # Ollama chat API
    url = "http://localhost:11434/api/chat"

    # Data sent to Ollama
    data = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    # Convert data to JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create HTTP request
    request = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        # Send the request
        with urllib.request.urlopen(request) as response:

            response_data = response.read().decode("utf-8")

            result = json.loads(response_data)

            return result["message"]["content"]

    except Exception as error:

        return f"Error: {error}"


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.title("Chat RAG")

st.write(
    "Ask questions about the information stored in my Word document."
)


# --------------------------------------------------
# CREATE / LOAD VECTOR DATABASE
# --------------------------------------------------

vector_store = create_vector_store()

if vector_store is None:

    st.error(
        f"Document '{DOCUMENT_FILE}' was not found."
    )

    st.stop()


# --------------------------------------------------
# CREATE CHAT MEMORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# DISPLAY PREVIOUS CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# --------------------------------------------------
# GET QUESTION FROM USER
# --------------------------------------------------

user_question = st.chat_input(
    "Ask a question about the document"
)


if user_question:

    # Save user question in chat memory
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Display user question
    with st.chat_message("user"):

        st.write(user_question)


    # --------------------------------------------------
    # RETRIEVE TOP 3 RESULTS
    # --------------------------------------------------

    top_results = retrieve_top_3(
        vector_store,
        user_question
    )


    # Combine the top 3 chunks into one context
    document_context = ""

    for index, result in enumerate(top_results, start=1):

        document_context += (
            f"\nDocument Result {index}:\n"
            f"{result.page_content}\n"
        )


    # --------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------

    system_prompt = """
You are a helpful document assistant.

Answer the user's question using the document context provided.

If the answer cannot be found in the document context,
say: "I could not find this information in the document."

Do not invent information.
"""


    # --------------------------------------------------
    # CREATE MESSAGES FOR LLM
    # --------------------------------------------------

    llm_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # Add previous chat history
    llm_messages.extend(
        st.session_state.messages[:-1]
    )


    # Add current question together with RAG context
    llm_messages.append(
        {
            "role": "user",
            "content": (
                f"Document context:\n"
                f"{document_context}\n\n"
                f"Question:\n"
                f"{user_question}"
            )
        }
    )


    # --------------------------------------------------
    # ASK OLLAMA
    # --------------------------------------------------

    with st.spinner("Searching document and generating answer..."):

        answer = ask_ollama(
            llm_messages
        )


    # Save assistant answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # Display answer
    with st.chat_message("assistant"):

        st.write(answer)


    # --------------------------------------------------
    # SHOW TOP 3 RETRIEVED RESULTS
    # --------------------------------------------------

    with st.expander("View Top 3 Retrieved Results"):

        for index, result in enumerate(
            top_results,
            start=1
        ):

            st.write(f"### Result {index}")

            st.write(
                result.page_content
            )