from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_files(documents:list, chunk_size:int=500, chunk_overlap:int=50)->list:
    """
    Description: 
    Splits loaded Document into chunks of text. 
    You can experiment with chunk_size and chunk_overlap size for your specific case. 

    Args:
    documents: The loaded documents to split
    chunk_size: The size of the chunks. Defaults to 500. 
    chunk_overlap: siz of chunk_overlap. Defaults to 50. 

    Returns:
    A list of text chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators = ["\n\n", "\n", " ", ""])
        chunks = text_splitter.split_documents(documents)
        print('Chunks created: ', len(chunks))
    
        for doc in chunks:
            tekst = doc.page_content
            kilde = doc.metadata.items()
            final_content = f"Tekst: {tekst}\n\nKilde: {kilde}"
            doc.page_content = final_content

        return chunks

    except Exception as e:
        print("Error splitting files: ", e)
        raise e