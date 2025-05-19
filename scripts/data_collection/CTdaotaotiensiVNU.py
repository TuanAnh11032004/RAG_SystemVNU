import pandas as pd
import os

# URL chứa bảng HTML
url = "https://www.vnu.edu.vn/home/?C2456"

# Tạo thư mục lưu trữ nếu chưa tồn tại
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# Đọc tất cả các bảng từ URL
tables = pd.read_html(url)

# In số lượng bảng
print(f"Tìm thấy {len(tables)} bảng.")

# Lấy bảng đầu tiên
df = tables[1]
print(df)

# Lưu bảng vào file CSV trong thư mục data/data_raw
output_path = os.path.join(output_dir, "DaotaotiensiVNU.csv")
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Đã lưu bảng vào: {output_path}")