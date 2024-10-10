# The load_pdfs_by_filename function iterates over all PDF files in a specified folder, loads the pages from each PDF using PyPDFLoader, and stores them in a dictionary with the filenames as keys.
import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs_by_filename(folder_path, verbose=False):
    pdf_pages_by_filename = {}
    # Iterate over all PDF files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            doc_path = os.path.join(folder_path, filename)
            if verbose:
                print(f"Loading PDF: {filename}")
            loader = PyPDFLoader(doc_path)
            pages = loader.load()
            if verbose:
                print(f"Number of pages loaded from {filename}: {len(pages)}")
            # Store pages in a dictionary with the filename as the key
            pdf_pages_by_filename[filename] = pages
    return pdf_pages_by_filename




# The split_pdf_pages_into_chunks function splits the pages of each PDF stored in the pdf_pages dictionary into smaller chunks using RecursiveCharacterTextSplitter, storing the resulting chunks in a new dictionary keyed by the PDF filenames.
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_pdf_pages_into_chunks(pdf_pages, chunk_size=500, chunk_overlap=50, verbose=False):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    pdf_chunks_by_filename = {}

    # Iterate over each PDF's pages stored in pdf_pages dictionary
    for filename, pages in pdf_pages.items():
        if verbose:
            print(f"Splitting pages from {filename} into chunks.")
        # Split the pages into chunks
        chunks = text_splitter.split_documents(pages)
        pdf_chunks_by_filename[filename] = chunks
        if verbose:
            print(f"Total chunks created from {filename}: {len(chunks)}")
    
    return pdf_chunks_by_filename




############################## Chroma approach
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os

def save_to_chrom(chunks: list[Document], CHROMA_PATH, openAI_key):
    # Check if the database already exists.
    if os.path.exists(CHROMA_PATH):
        # Load the existing database to append new data.
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings(api_key=openAI_key))
        # Add new chunks to the database.
        db.add_documents(chunks)
    else:
        # If it doesn't exist, create a new one.
        db = Chroma.from_documents(
            chunks, embedding=OpenAIEmbeddings(api_key=openAI_key), persist_directory=CHROMA_PATH
        )
    
    # Ensure changes are saved to the disk.
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    


import shutil
def remove_chrom(CHROMA_PATH):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("DB removed")
        



from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def inspect_chrom(CHROMA_PATH, openAI_key):
    # Load the existing database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings(api_key=openAI_key))
    data = db.get()
    # Retrieve and print data (for example, printing document IDs or contents)
    
    # Extract unique sources
    unique_sources = {item['source'] for item in data["metadatas"]}
    # Convert set back to a list
    unique_sources_list = list(unique_sources)
    return(unique_sources_list)