# 
import os
from langchain_community.document_loaders import PyPDFLoader
import warnings

def upload_PDFs(folder_path, supabase_DB, args_Search, verbose=False):
    # Check if 'topic' and 'subtopic' are provided in args_Search
    if not isinstance(args_Search, dict) or 'topic' not in args_Search or 'subtopic' not in args_Search:
        raise ValueError("Error: 'args_Search' must be a dictionary containing both 'topic' and 'subtopic' keys.")
    
    # Suppress specific PDF warnings
    warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")
    
    # Get the names of all files already in the DB
    res = supabase_DB.storage.from_('files').list()
    alreadyUploaded = [file['name'] for file in res]
    
    # Extract topic and subtopic from args_Search
    topic = args_Search.get('topic')
    subtopic = args_Search.get('subtopic')

    # Iterate over all PDF files in the specified folder
    counter = 0
    for filename in os.listdir(folder_path):
        # Check if the file is a PDF and is not in the excluded list
        if filename.endswith(".pdf") and filename not in alreadyUploaded:
            counter = counter + 1
            
            if verbose:
                print(f"Upload PDF: {filename}")
            
            # Upload PDFs:
            #> changing path argument to "path="AI/10.1002_sd.2048.pdf" would create a subfolder called "AI" in your storage
            with open(folder_path + filename, 'rb') as f:
                supabase_DB.storage.from_("files").upload(file=f,path=filename, file_options={"content-type": "pdf"})
                
            # Use PyPDFLoader to load PDF and get metadata
            pdf_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(pdf_path)
            doc = loader.load()
            num_pages = len(doc)  # This will give the number of pages in the PDF
            
            # Add entry to DB:  
                        # Add entry to DB with the number of pages
            entry_PDF = {
                'id': filename,
                'topic': topic,
                'subtopic': subtopic,
                'num_pages': num_pages
            }
            supabase_DB.table('documents').insert(entry_PDF).execute()

        else:
            print(f'The following file: "{filename}" is a) not a PDF or b) was already uploaded in the DB.')
    print(f"In total {counter} PDFs were sucessfully uploaded to your DB.")






def non_processed_PDFs(supabase_DB, verbose=False):
    
    # Get the names of all files already in the DB
    res = supabase_DB.storage.from_('files').list()
    alreadyUploaded = [file['name'] for file in res]
    
    res = supabase_DB.table("documents_chunks").select("id").execute()
    # Convert the list of tuples to a dictionary
    data_dict = dict(res)
    # Access the 'data' key directly
    data_items = data_dict.get('data', [])
    # Extract topics from the list of dictionaries within 'data'
    ids = [entry['id'] for entry in data_items]
    ids = set(ids)
    print("ids in your table documents_chunks:\n", ids)
    
    return alreadyUploaded




def download_PDF(folderpath, filename, supabase_DB):
    
    with open(folderpath + "/" + filename, 'wb+') as f:
        res = supabase_DB.storage.from_('files').download(filename)
        f.write(res)

  
  
def load_split_embed(supabase_DB, path_to_PDFs, args_Split, LMM):
    # Check if 'topic' and 'subtopic' are provided in args_Search
    if not isinstance(args_Split, dict) or 'chunk_size' not in args_Split or 'chunk_overlap' not in args_Split:
        raise ValueError("Error: 'args_Split' must be a dictionary containing both 'chunk_size' and 'chunk_overlap' keys.")
    
    # Extract topic and subtopic from args_Search
    chunk_size = args_Split.get('chunk_size')
    chunk_overlap = args_Split.get('chunk_overlap')
    
    arrayPDFs = non_processed_PDFs(supabase_DB=supabase_DB, verbose=False)
    arrayPDFs = arrayPDFs[:3] # !!!!
    # download all PDFs, which have not been processed
    for pdf in arrayPDFs:
        download_PDF(folderpath=path_to_PDFs, filename=pdf, supabase_DB=supabase_DB)
        
    # load all PDFs
    pdf_pages = load_pdfs_by_filename(path_to_PDFs, verbose=False)
    # split all PDFs into chunks
    pdf_chunks = split_pdf_pages_into_chunks(pdf_pages, chunk_size=chunk_size, chunk_overlap=chunk_overlap, verbose=False)

    arrayChunkedPDFs = list(pdf_chunks.keys())
    
    for pdf in arrayChunkedPDFs:
        print(pdf)
        # get chunks of PDF
        tmp_pdf_chunks = pdf_chunks[pdf]
        # create embeddings
        tmp_embeddings = create_embeddings(single_pdf_chunks=tmp_pdf_chunks, LMM=LMM, verbose=False)

        for index, _ in enumerate(tmp_pdf_chunks):
            # print(f"Chunk {index}:")
            
            entry_chunk = {
                'id': pdf,
                'order_chunks': index,
                'section': None,
                'content': tmp_pdf_chunks[index].page_content,
                'embedding': tmp_embeddings[index].tolist()
                }
            
            supabase_DB.table('documents_chunks').insert(entry_chunk).execute()
  
# The load_pdfs_by_filename function iterates over all PDF files in a specified folder, loads the pages from each PDF using PyPDFLoader, and stores them in a dictionary with the filenames as keys.
import os
from langchain_community.document_loaders import PyPDFLoader
def load_pdfs_by_filename(folder_path, verbose=False):
    
    # Suppress specific PDF warnings
    warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")
    
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




from sentence_transformers import SentenceTransformer
import pandas as pd

def create_embeddings(single_pdf_chunks, LMM, verbose=False):
    # single entries of "split_pdf_pages_into_chunks" are an array of text chunks
    tmp_chunks = []  # Initialize an empty array to store the extracted content

    # Iterate over each page or chunk in first_pdf_chunks
    for chunk in single_pdf_chunks:
        content = chunk.page_content
        tmp_chunks.append(content)

    # Load the pre-trained model
    model = SentenceTransformer(LMM)
    # Extract features
    features = model.encode(tmp_chunks)
    
    # Print the features as a pandas dataframe
    if verbose:
        print(pd.DataFrame(features))
        
    return features







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