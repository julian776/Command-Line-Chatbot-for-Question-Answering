from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import TextLoader
from dotenv import dotenv_values
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# In case you need it
config = dotenv_values(".env")

# Update to use your Pdf
loader = PyPDFLoader("07-patrutiu-baltes.pdf")
pages = loader.load_and_split()

text_splitter = CharacterTextSplitter(        
    separator = "\n\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    is_separator_regex = False,
)
docs = text_splitter.split_documents(pages)

model_name = "hkunlp/instructor-large"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True, 'show_progress_bar': True}
embeddings = HuggingFaceInstructEmbeddings(
    query_instruction="Represent the query for retrieval: ",
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

db = FAISS.from_documents(docs, embeddings)

while True:
    query = input("Ask something: ")
    if query.lower() == "exit":
        exit() 
    embedding_vector = embeddings.embed_query(query)
    docs = db.similarity_search_by_vector(embedding_vector)
    print(docs[0].page_content)