import pdfplumber
import os

# Đường dẫn đến tệp PDF và thư mục lưu trữ
pdf_path = "D:/congtuyensinhVNU.pdf"
output_dir = "data/raw_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Trích xuất văn bản từ PDF
with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

# Lưu văn bản
with open(os.path.join(output_dir, "vnu_congthongtintuyensinhVNU.txt"), 'w', encoding='utf-8') as file:
    file.write(text)

print("Đã trích xuất văn bản từ tệp PDF.")