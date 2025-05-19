import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    processed_data_dir = "data/processed_data"
    documents = []

    # Đọc dữ liệu
    for filename in os.listdir(processed_data_dir):
        with open(os.path.join(processed_data_dir, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            documents.append(Document(page_content=content, metadata={"source": filename}))

    # ✅ Chia nhỏ trước khi embed
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)

    print(f"✅ Chia thành {len(split_docs)} đoạn từ {len(documents)} file.")

    # Tạo Chroma vectorstore
    vectorstore = Chroma.from_documents(split_docs, embedding=embeddings)

    return vectorstore

if __name__ == "__main__":
    vectorstore = create_vectorstore()
    print("✅ Đã tạo vectorstore từ tài liệu đã chia nhỏ.")

