import os

raw_data_dir = "data/raw_data"
processed_data_dir = "data/processed_data"
if not os.path.exists(processed_data_dir):
    os.makedirs(processed_data_dir)

for filename in os.listdir(raw_data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(raw_data_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            # Loại bỏ ký tự thừa, khoảng trắng dư
            cleaned_text = " ".join(text.split())
        with open(os.path.join(processed_data_dir, filename), 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

print("Đã làm sạch dữ liệu và lưu vào thư mục processed_data.")

