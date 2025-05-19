import pdfplumber
import os
import csv

# Đường dẫn tới file PDF
pdf_path = "D:/03.2025.-DAnh-sach-cac-nganh-tuyen-sinh-SDH-nam-2025-ULIS-V1.pdf"

# Thư mục để lưu kết quả
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# Mở PDF và trích xuất bảng từ từng trang
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()

        if not tables:
            continue  # Không có bảng trong trang này

        for table_index, table in enumerate(tables):
            output_filename = f"table_trang{page_num+1}_so{table_index+1}.csv"
            output_path = os.path.join(output_dir, output_filename)

            # Ghi bảng ra file CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in table:
                    writer.writerow(row)

            print(f"✅ Đã lưu bảng {table_index+1} từ trang {page_num+1} vào: {output_path}")
