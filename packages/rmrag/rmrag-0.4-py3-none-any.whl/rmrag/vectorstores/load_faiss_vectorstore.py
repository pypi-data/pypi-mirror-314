from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def load_faiss_vectorstore(vectorstore_folder:str='./vectorstore/', embedding_provider: str = 'HuggingFaceEmbeddings', specific_model:str='intfloat/multilingual-e5-large') -> FAISS:
    """  
    Description:
    Loads a local FAISS vectorstore

    Remember to have a .env file in the working directory with API keys for HuggingFace and OpenAI.

    Args: 
        vectorstore_folder: folder where the 'index.faiss' file is located. Defaults to './vectorstore/'.
        embedding_provider: Must be HuggingFaceEmbeddings or OpenAIEmbeddings. Defaults to HuggingFaceEmbeddings.
        specific_model: For example 'sentence-transformers/all-MiniLM-L6-v2' or 'text-embedding-3-small'. Defaults to 'intfloat/multilingual-e5-large'.

    Returns:
        A FAISS vectorstore object.
    """
   
    # List of supported embedding providers
    embedding_providers = {
        'HuggingFaceEmbeddings': HuggingFaceEmbeddings,
        'OpenAIEmbeddings': OpenAIEmbeddings
    }

    # Validate that the embedding_provider is supported
    if embedding_provider not in embedding_providers:
        raise ValueError("embedding_provider must be either 'HuggingFaceEmbeddings' or 'OpenAIEmbeddings'")
    
    # Map string input to the actual class
    embedding_class = embedding_providers[embedding_provider]

    try:
        # Create embeddings based on the provider and model
        if embedding_class == HuggingFaceEmbeddings:
            embeddings = embedding_class(model_name=specific_model, show_progress=True)
        elif embedding_class == OpenAIEmbeddings:
            embeddings = embedding_class(model=specific_model, show_progress_bar=True)

        print("Embeddings defined successfully.")
    except Exception as e:
        print("Error defining embeddings:", e)
        return # Stop execution if embeddings cannot be created

    try: 
        # Load the local FAISS vectorstore
        vectorstore = FAISS.load_local(vectorstore_folder, embeddings, allow_dangerous_deserialization=True)
        print("Vectorstore loaded successfully.")
        return vectorstore
    except Exception as e:
        print("Error loading vectorstore index: ", e)
        return