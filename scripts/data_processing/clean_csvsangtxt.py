import os
import re
import pandas as pd
from ftfy import fix_text
from io import StringIO

raw_data_dir = "data/raw_data"
processed_data_dir = "data/processed_data"
os.makedirs(processed_data_dir, exist_ok=True)

def fix_vietnamese_text(text):
    if isinstance(text, str):
        return fix_text(text).strip()
    return text

def is_noise_line(line, filename):
    line_clean = line.strip()
    filename_base = os.path.splitext(filename)[0].lower()

    # Loại bỏ dòng chứa tên file (không phân biệt hoa thường)
    if filename_base in line_clean.lower():
        return True

    # Loại bỏ dòng rỗng hoặc chỉ ký tự đặc biệt, số, khoảng trắng
    if not line_clean or re.fullmatch(r'[\W_0-9\s]+', line_clean):
        return True

    # Loại bỏ dòng có trên 50% cột giống nhau (dòng phân nhóm, header phụ...)
    columns = line_clean.split(',')
    if len(columns) > 1:
        first_col = columns[0]
        repeated_ratio = sum(1 for c in columns if c == first_col) / len(columns)
        if repeated_ratio > 0.5:
            return True

    return False

def clean_data_from_file(file_path):
    filename = os.path.basename(file_path)
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']

    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                raw_lines = f.readlines()

            # Lọc dòng nhiễu, fix tiếng Việt
            cleaned_lines = [fix_vietnamese_text(line) 
                             for line in raw_lines 
                             if not is_noise_line(line, filename)]

            if len(cleaned_lines) < 2:
                print(f"[WARN] File {filename}: không có dữ liệu hợp lệ sau khi loại bỏ dòng nhiễu.")
                return None

            csv_content = "\n".join(cleaned_lines)
            df = pd.read_csv(StringIO(csv_content))

            # Fix tiếng Việt trong từng ô dataframe
            for col in df.columns:
                df[col] = df[col].apply(fix_vietnamese_text)

            # Loại bỏ dòng trùng và dòng toàn NaN
            df = df.drop_duplicates().dropna(how='all').reset_index(drop=True)

            if df.empty:
                print(f"[WARN] File {filename}: dữ liệu sau khi làm sạch rỗng.")
                return None

            return df

        except Exception as e:
            # Nếu lỗi encoding, thử encoding tiếp theo
            # Có thể ghi log lỗi để debug sau
            # print(f"[ERROR] Đọc file {filename} với encoding {enc} lỗi: {e}")
            continue

    print(f"[ERROR] File {filename}: Không đọc được với encoding chuẩn hoặc lỗi đọc file.")
    return None

def process_all_files(raw_dir, processed_dir):
    all_files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.csv')]
    total_files = len(all_files)
    processed_files = 0

    for filename in all_files:
        print(f"Đang xử lý file: {filename}")
        file_path = os.path.join(raw_dir, filename)
        cleaned_df = clean_data_from_file(file_path)
        if cleaned_df is not None:
            output_filename = os.path.splitext(filename)[0] + "_cleaned.csv"
            output_path = os.path.join(processed_dir, output_filename)
            cleaned_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Đã lưu file sạch: {output_path}")
            processed_files += 1
        else:
            print(f"Không tạo được dữ liệu sạch cho file: {filename}")

    print(f"Hoàn tất xử lý {processed_files}/{total_files} file CSV.")

if __name__ == "__main__":
    process_all_files(raw_data_dir, processed_data_dir)





