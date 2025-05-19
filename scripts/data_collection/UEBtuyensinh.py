import pandas as pd
import os

# URL chứa bảng HTML
url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-kinh-te-ha-noi-QHE.html"

# Tạo thư mục lưu trữ nếu chưa tồn tại
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

try:
    # Đọc tất cả các bảng từ URL
    tables = pd.read_html(url)
    print(f"🔍 Tìm thấy {len(tables)} bảng.")

    # Duyệt và xử lý các bảng 0 -> 3 (nếu có)
    for i in range(4):
        if i < len(tables):
            df = tables[i]
            print(f"\n📄 Bảng {i} (hiển thị 5 dòng đầu):")
            print(df.head())  # In 5 dòng đầu

            # Tạo tên file CSV
            filename = f"UEBtuyensinh_table{i}.csv"
            output_path = os.path.join(output_dir, filename)

            # Lưu bảng vào file CSV
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"✅ Đã lưu bảng {i} vào: {output_path}")
        else:
            print(f"⚠️ Không có bảng thứ {i} trong trang.")

except Exception as e:
    print(f"❌ Lỗi khi đọc bảng từ URL: {e}")
