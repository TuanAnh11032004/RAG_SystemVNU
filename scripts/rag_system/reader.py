from langchain.llms import LlamaCpp

def initialize_reader():
    # Đường dẫn tới mô hình GGUF LLaMA 3 đã tải
    model_path = "D:/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

    llm = LlamaCpp(
        model_path=model_path,
        n_ctx=4096,        # Context window
        n_threads=4,       # Số luồng CPU
        temperature=0.7,
        top_p=0.9,
        verbose=True
    )
    return llm

if __name__ == "__main__":
    reader = initialize_reader()
    print("✅ Reader (LLaMA 3) đã sẵn sàng.")

