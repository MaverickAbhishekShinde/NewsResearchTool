The News Research Tool is a Streamlit-based web application designed to help users load, process, and query news articles from various URLs. The application features user authentication with signup and login capabilities, ensuring secure access to the tool. It uses LangChain for document processing, OpenAI for generating responses, and FAISS for efficient querying of document embeddings.

Data Loading:
Load news articles from provided URLs.

Text Processing:
Split large texts into manageable chunks.

Embedding and Indexing:
Create and store document embeddings using FAISS.

Querying:
Query the processed documents and retrieve relevant answers with sources.

Technologies Used
Streamlit: For building the web interface.
LangChain: For document loading, text splitting, and embeddings.
OpenAI API: For generating answers to user queries.
FAISS: For storing and querying document embeddings.
bcrypt: For secure password hashing.
MySQL: For user data storage and management.
Pickle: For saving and loading the FAISS index.
dotenv: For managing environment variables.
