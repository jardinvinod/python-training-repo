# Import LangChain document loader for .docx files
from langchain_community.document_loaders import Docx2txtLoader

# Import text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import Ollama embeddings
from langchain_community.embeddings import OllamaEmbeddings

# Import FAISS vector database
from langchain_community.vectorstores import FAISS

# Import os to check if file exists
import os


# Function to search the document and return top 3 matches
def search_document(file_path, user_query):

    # Check if the file exists
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return []

    try:
        # Load the .docx document
        loader = Docx2txtLoader(file_path)

        # Read document content
        documents = loader.load()

        print("Document loaded successfully.")

        # Split document into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = text_splitter.split_documents(documents)

        print("Number of chunks:", len(chunks))

        # Create embeddings using Ollama
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        # Store chunks in FAISS vector database
        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

        print("Document stored successfully in vector database.")

        # Retrieve the top 3 most similar chunks
        results = vector_store.similarity_search(
            user_query,
            k=3
        )

        # Return results
        return results

    except Exception as error:
        print("Error:", error)
        return []


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

# Name of the Word document
file_path = "my_document.docx"

# Get search input from the user
user_query = input("Enter your search question: ")

# Search the document
results = search_document(
    file_path,
    user_query
)


# Display top 3 matching results
if len(results) == 0:

    print("No matching results found.")

else:

    print("\nTOP 3 MATCHING RESULTS")
    print("=" * 60)

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("-" * 60)

        print(result.page_content)

        print("-" * 60)