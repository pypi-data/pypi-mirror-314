from typing import Type
from rmrag.text_processing import load_files_from_directory, split_files
from rmrag.vectorstores import create_embeddings_and_faiss_vectorstore

def directory_into_faiss(directory_path:str, chunk_size:int, chunk_overlap:int, embedding_provider:Type, specific_model:str) -> None:
    """
    Full pipeline to load files in a specified folder, create chunks, and embed them into a FAISS vectorstore.

    # Example usage:
    directory_into_faiss(
    directory_path='./data', 
    chunk_size=1000,
    chunk_overlap=50, 
    embedding_provider=HuggingFaceEmbeddings, 
    specific_model='intfloat/multilingual-e5-large'
    )

    Args:
        directory_path (str): Path to directory/folder 
        chunk_size (int): Size of the chunks.
        chunk_overlap (int): Size of the chunk overlap.
        embedding_model (Type): The class of the embedding model to use.
        specific_model (str): Specific model name for the embeddings.

    Returns:
        None. It saves a FAISS vectorstore in a folder called 'vectorstore' in the current working directory.
    """
    print("Starting data loading...", directory_path)
    documents = load_files_from_directory(directory_path)
    if not documents:
        print("No documents loaded, stopping process.")
        return

    print("Splitting documents...")
    chunks = split_files(documents, chunk_size, chunk_overlap)
    if not chunks:
        print("No chunks created, stopping process.")
        return

    print("Embedding chunks and creating vector store...")
    create_embeddings_and_faiss_vectorstore(chunks, embedding_provider, specific_model)
    print("Vectorstore created successfully.")