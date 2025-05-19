import pandas as pd
import os

# Đường dẫn file HTML hoặc URL của bạn
url = "https://vnu.edu.vn/ttsk/?C2228/N36574/Nam-2025:-dHQGHN-tuyen-sinh-hon-20.000-chi-tieu-dai-hoc-chinh-quy.htm"

# Đọc tất cả bảng từ trang
tables = pd.read_html(url)
print(f"Tìm thấy {len(tables)} bảng.")

# Chọn bảng đầu tiên (hoặc bảng bạn muốn)
df = tables[0]

# Đặt dòng đầu tiên làm header
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

print("Cột hiện có trong bảng:", df.columns.tolist())

# Hàm kiểm tra STT hợp lệ
def is_valid_stt(val):
    if pd.isna(val):
        return False
    val_str = str(val).strip()
    if val_str == "Tổng cộng":
        return True
    try:
        int(val_str)
        return True
    except:
        return False

# Lọc dòng có STT hợp lệ
df_clean = df[df['STT'].apply(is_valid_stt)].copy()

# Tạo thư mục lưu file nếu chưa tồn tại
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# Lưu file CSV
output_path = os.path.join(output_dir, "tuyensinhVNU.csv")
df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Đã lưu kết quả vào: {output_path}")



