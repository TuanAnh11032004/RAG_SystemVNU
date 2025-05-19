from langchain.chains import RetrievalQA
from embedder import create_vectorstore
from retriever import get_retriever
from reader import initialize_reader
import os
import sys

# Bắt buộc thêm dòng này nếu chạy trong VS Code để tránh lỗi UTF-8 khi in tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

def run_rag_system():
    vectorstore = create_vectorstore()
    retriever = get_retriever(vectorstore)
    llm = initialize_reader()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


    # Đọc câu hỏi
    with open("data/test/questions.txt", 'r', encoding='utf-8') as f:
        questions = f.readlines()

    answers = []
    for i, question in enumerate(questions, 1):
        print(f"\n🟡 Câu hỏi {i}: {question.strip()}", flush=True)
        answer = qa_chain.run(question.strip())
        print(f"✅ Trả lời: {answer}\n", flush=True)
        answers.append(answer)

    # Ghi kết quả
    with open("results/system_output_1.txt", 'w', encoding='utf-8') as f:
        f.write("\n".join(answers))

    print("🎉 Đã tạo kết quả đầu ra.", flush=True)

if __name__ == "__main__":
    run_rag_system()

    
