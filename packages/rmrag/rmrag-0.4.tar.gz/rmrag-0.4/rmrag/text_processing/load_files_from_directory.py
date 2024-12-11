from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
import tqdm

def load_files_from_directory(directory_path:str='./data', source_column:str=None) -> list:
    """
    Description: 
    Reads .txt, .pdf, .csv and .docx files in a directory/folder and turns them into a list of langchain 'Documents' objects, which contains page_content, metadata(source), page/row. 

    Args:
    directory_path: The path to the folder containing the files. 
    source_column: Name of the column in the CSV files that will be quoted as the source. Defaults to file location if set to none. 

    Returns:
    A list with langchain 'Document' objects
    """

    documents = []
    try: 
        txt_loader = DirectoryLoader(
            directory_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True
        )
        documents.extend(txt_loader.load())

        pdf_loader = DirectoryLoader(
            directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True
        )
        documents.extend(pdf_loader.load())

        csv_loader = DirectoryLoader(
            directory_path, glob="**/*.csv", loader_cls=CSVLoader, show_progress=True,
            loader_kwargs={"encoding":"utf8", "source_column":source_column}
        )
        documents.extend(csv_loader.load())

        doc_loader = DirectoryLoader(
            directory_path, glob="**/*.docx", loader_cls=Docx2txtLoader, show_progress=True,
        )
        
        documents.extend(doc_loader.load())
        return documents
    
    except Exception as e:
        print("Error loading files from directory:", e)
        raise e