def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})

if __name__ == "__main__":
    print("Retriever đã sẵn sàng.")
