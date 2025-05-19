import os
import pandas as pd
import numpy as np

raw_data_dir = "data/raw_data/UEBtuyensinh"
processed_data_dir = "data/processed_data"

if not os.path.exists(processed_data_dir):
    os.makedirs(processed_data_dir)

for filename in os.listdir(raw_data_dir):
    if filename.endswith(".csv"):
        print(f"Đang xử lý: {filename}")
        file_path = os.path.join(raw_data_dir, filename)
        
        # Đọc dữ liệu
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # Làm sạch dữ liệu

        # Bỏ dòng mà tất cả các giá trị đều giống nhau (dòng lặp lại tiêu đề)
        df = df[~df.apply(lambda row: row.nunique() == 1, axis=1)]

        # Thay "nan" (kiểu chuỗi) bằng np.nan
        df.replace("nan", np.nan, inplace=True)
        df.replace("NaN", np.nan, inplace=True)

        # Bỏ các dòng toàn bộ là NaN
        df.dropna(how='all', inplace=True)

        # Bỏ dòng trùng lặp
        df.drop_duplicates(inplace=True)

        # Làm sạch chuỗi văn bản
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()

        # Ghi dữ liệu sạch
        processed_path = os.path.join(processed_data_dir, filename)
        df.to_csv(processed_path, index=False, encoding='utf-8-sig')

print("✅ Đã làm sạch dữ liệu bảng và lưu vào thư mục processed_data.")


