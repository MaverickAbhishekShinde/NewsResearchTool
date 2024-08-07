
import os
import streamlit as st
import pickle
import time
import requests
from requests.exceptions import Timeout
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env (especially openai api key)

st.title("News Research Tool")
st.sidebar.title("News Article URLs")

urls = []
for i in range(1):
    url = st.sidebar.text_input(f"URL {i + 1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

def load_data_from_url(urls, max_retries=3, timeout=60):
    attempt = 0
    while attempt < max_retries:
        try:
            loader = UnstructuredURLLoader(urls=urls)
            main_placeholder.text("Data Loading...Started...")
            # Assuming loader.load() accepts a timeout parameter or similar
            data = loader.load();
            return data
        except () as e:
            print(1)
            attempt += 1
            main_placeholder.text(f"Attempt {attempt} failed: {str(e)}")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(2)
            print(e)
            main_placeholder.text(f"An unexpected error occurred: {str(e)}")
            break
    main_placeholder.text("Data loading failed after several attempts.")
    return None


if process_url_clicked:
    # load data
    data = load_data_from_url(urls)
    if not data:
        st.error("No data loaded from URLs. Please check your input URLs.")
    else:
        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=10000
        )
        main_placeholder.text("Text Splitter...Started...")
        docs = text_splitter.split_documents(data)
        #print(docs)
        st.write(docs)

        if not docs:
            st.error("No documents split. Please check your input URLs and separators.")
        else:
            # create embeddings and save it to FAISS index
            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
            main_placeholder.text("Embedding Vector Started Building...")
            time.sleep(2)

            # Save the FAISS index to a pickle file
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_openai, f)

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)



