import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader


def parse_document(file_path):
    """
    Parse a document based on its file type.
    
    Args:
    file_path (str): Path to the document file
    
    Returns:
    list: List of document pages
    
    Raises:
    ValueError: If the file type is not supported
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    if extension == '.pdf':
        loader = PyMuPDFLoader(file_path)
    elif extension == '.docx':
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
    try:
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading document: {str(e)}")
