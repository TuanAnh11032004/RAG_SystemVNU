import pandas as pd
import os
from ftfy import fix_text
import re

# Định nghĩa thư mục đầu vào và đầu ra
raw_data_dir = "data/raw_data"
processed_data_dir = "data/processed_data"

# Tạo thư mục processed_data nếu chưa tồn tại
os.makedirs(processed_data_dir, exist_ok=True)

# Hàm sửa lỗi mã hóa tiếng Việt
def fix_vietnamese_text(text):
    if isinstance(text, str):
        return fix_text(text).strip()
    return text

# Hàm làm sạch dữ liệu từ một file CSV
def clean_data_from_file(file_path):
    try:
        # Thử đọc file CSV bằng pandas với các mã hóa khác nhau
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        df = None
        for enc in encodings:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        
        if df is None:
            # Nếu không đọc được bằng pandas, thử đọc nội dung thô
            print(f"Không thể đọc file {file_path} bằng pandas, thử đọc nội dung thô...")
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        raw_data = file.read()
                    lines = raw_data.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        line = line.strip()
                        if line:
                            fixed_line = fix_vietnamese_text(line)
                            fixed_line = re.sub(r'^,|,$', '', fixed_line)
                            cleaned_lines.append(fixed_line)
                    
                    if len(cleaned_lines) < 2:
                        print(f"Không có dữ liệu hợp lệ trong file {file_path}")
                        return None
                    
                    # Tách dữ liệu thành bảng
                    data = []
                    headers = None
                    for idx, line in enumerate(cleaned_lines):
                        row = [fix_vietnamese_text(col.strip('"').strip()) for col in line.split(',')]
                        if idx == 0 and len(row) >= 2:
                            headers = row
                        elif headers:
                            while len(row) < len(headers):
                                row.append("")
                            data.append(row[:len(headers)])
                    
                    if not headers or not data:
                        print(f"Không tìm thấy bảng hợp lệ trong file {file_path}")
                        return None
                    
                    df = pd.DataFrame(data, columns=headers)
                    break
                except UnicodeDecodeError:
                    continue
        
        if df is None:
            print(f"Không thể đọc file {file_path} với bất kỳ mã hóa nào.")
            return None

        # Làm sạch dữ liệu trong DataFrame
        # Sửa lỗi mã hóa tiếng Việt cho tất cả cột
        for col in df.columns:
            df[col] = df[col].apply(fix_vietnamese_text)
        
        # Loại bỏ dòng trùng lặp
        df = df.drop_duplicates()
        
        # Loại bỏ dòng trống (nếu tất cả giá trị trong dòng đều trống)
        df = df.dropna(how='all')
        
        # Đặt lại chỉ số (index) cho DataFrame
        df = df.reset_index(drop=True)
        
        return df

    except Exception as e:
        print(f"Lỗi khi xử lý file {file_path}: {e}")
        return None

# Duyệt qua tất cả file trong thư mục raw_data
file_count = 0
processed_count = 0
for filename in os.listdir(raw_data_dir):
    if filename.endswith('.csv'):  # Chỉ xử lý file CSV
        file_path = os.path.join(raw_data_dir, filename)
        if os.path.isfile(file_path):  # Đảm bảo là file, không phải thư mục
            file_count += 1
            print(f"Đang xử lý file: {filename}")
            cleaned_df = clean_data_from_file(file_path)
            
            if cleaned_df is not None and not cleaned_df.empty:
                # Tạo tên file đầu ra
                output_filename = os.path.splitext(filename)[0] + "_cleaned.csv"
                output_path = os.path.join(processed_data_dir, output_filename)
                # Lưu dữ liệu sạch vào file CSV với mã hóa UTF-8 BOM để hiển thị đúng tiếng Việt trên Excel
                cleaned_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                processed_count += 1
                print(f"Đã lưu dữ liệu sạch vào: {output_path}")
            else:
                print(f"Không có dữ liệu sạch để lưu cho file: {filename}")

print(f"Hoàn tất quá trình làm sạch dữ liệu! Đã xử lý {processed_count}/{file_count} file CSV.")



