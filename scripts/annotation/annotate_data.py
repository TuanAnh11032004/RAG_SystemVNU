import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Sử dụng mô hình T5 tiếng Việt từ VietAI
model_name = "VietAI/vit5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Đường dẫn tới thư mục chứa dữ liệu văn bản
processed_data_dir = "data/processed_data"
questions = []
answers = []

# Hàm sinh câu hỏi từ ngữ cảnh và câu trả lời
def generate_question(context, answer):
    input_text = f"viết câu hỏi: {context} trả lời là {answer}"
    inputs = tokenizer([input_text], return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=64,
            num_beams=4,
            early_stopping=True
        )

    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return question

# Duyệt qua các tệp văn bản trong thư mục
for filename in os.listdir(processed_data_dir):
    file_path = os.path.join(processed_data_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # Tách câu đơn giản bằng dấu chấm
        sentences = text.split(".")
        for sent in sentences:
            if "lấy tên là" in sent and "năm" in sent:
                sent = sent.strip()
                # Cố gắng trích ra năm
                try:
                    year_part = sent.split("năm")[-1].strip().split(" ")[0]
                    answer_text = f"năm {year_part}"
                except:
                    continue

                question = generate_question(sent, answer_text)
                questions.append(question)
                answers.append(answer_text + ".")

# Tạo thư mục nếu chưa tồn tại
os.makedirs("data/test", exist_ok=True)

# Ghi câu hỏi và câu trả lời ra file
with open("data/test/questions.txt", 'w', encoding='utf-8') as f:
    f.write("\n".join(questions))
with open("data/test/reference_answers.txt", 'w', encoding='utf-8') as f:
    f.write("\n".join(answers))

print("✅ Đã tạo tập dữ liệu test bằng mô hình VietAI/vit5-base.")


