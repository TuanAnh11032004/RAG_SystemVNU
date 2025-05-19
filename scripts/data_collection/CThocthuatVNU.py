import pandas as pd
import os

# URL chứa bảng HTML
url = "https://tuyensinh.vnu.edu.vn/index.php/Home/listnganh"

# Tạo thư mục lưu trữ nếu chưa tồn tại
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# Đọc tất cả các bảng từ URL
tables = pd.read_html(url)

# In số lượng bảng
print(f"Tìm thấy {len(tables)} bảng.")

# Lấy bảng đầu tiên
df = tables[0]
print(df)

# Lưu bảng vào file CSV trong thư mục data/data_raw
output_path = os.path.join(output_dir, "CThocthuatVNU.csv")
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Đã lưu bảng vào: {output_path}")