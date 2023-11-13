import pickle
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
import pinecone
from htmlTemplates import css, bot_template, user_template


# two types we can create embeddings 
#1. OpenAIEmbeddings
#2. InstrctorsEmbeddings (Free but slow)
#3. I am using InstrctorsEmbeddings

def get_pdf_text(pdf_docs):
    text= ""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter= CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks= text_splitter.split_text(raw_text)
    return chunks
def get_vector_store(text_chunks):
    embeddings=OpenAIEmbeddings()
    # embeddings=HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore=FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

# def get_vector_store(text_chunks):
#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

#     # Connect to Pinecone
#     pinecone.init(api_key="PINECONE_API_KEY", environment="YOUR_ENVIRONMENT")

#     # Create or retrieve the Pinecone index
#     index_name = "your_index_name"
#     if index_name not in pinecone.list_indexes():
#         pinecone.create_index(index_name)
#     index = pinecone.Index(index_name)

#     # Upsert the vector store into Pinecone
#     index.upsert(ids=range(len(text_chunks)), vectors=vectorstore.vectors)

#     # Close the connection to Pinecone
#     pinecone.deinit()

#     return vectorstore


def get_conversation_chain(vectorstore):
    llm=ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    conversation_chain= ConversationalRetrievalChain.from_llm(llm=llm,
                                                            retriever=vectorstore.as_retriever(),
                                                            memory=memory
                                                            )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
   load_dotenv()

   st.set_page_config(page_title="Chat with multiple pdfs",page_icon=":books:")

   st.write(css, unsafe_allow_html=True) # it is supposed to show the html with streamlit

   if "conversation" not in st.session_state:
        st.session_state.conversation = None

   if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
   

   st.header("Chat with multiple pdfs:books:")

   user_question = st.text_input("Ask a question about your document")

   if user_question:
       print("user_question",user_question)
       handle_userinput(user_question)

   with st.sidebar:
       
       st.subheader("Your documents")

       pdf_docs= st.file_uploader("Upload your documents and click on process",accept_multiple_files=True)

       if st.button("process"):
           
           with st.spinner("processing"):
                #get pdf text
                raw_text= get_pdf_text(pdf_docs)
                # st.write(raw_text)

                #get the text chunks
                text_chunks=get_text_chunks(raw_text)
                # st.write(text_chunks)

                #create vector store
                vectorstore = get_vector_store(text_chunks)

                #create conversation chain

                # st.session_state.conversation = get_conversation_chain(vectorstore)  # for streamlit to know that it will not initialize again
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)



if __name__ =="__main__":
    main()