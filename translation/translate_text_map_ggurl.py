import time
import os
import json
import signal
import requests
from urllib.parse import quote

input_file = '../data/languagedata_en.txt'
text_map_file = 'text_map.json'

# Tải text_map nếu đã lưu trước đó
if os.path.exists(text_map_file):
    with open(text_map_file, 'r', encoding='utf-8') as f:
        text_map = json.loads(f.read())
else:
    text_map = {}

# Biến trạng thái
is_interrupted = False
def translate(text, lang1="en", lang2="vi"):
    # Mã hóa toàn bộ văn bản, bao gồm cả dấu hỏi và các ký tự đặc biệt
    escaped_str = quote(text)
    # Tạo URL cho Google Translate API
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={lang1}&tl={lang2}&dt=t&q={escaped_str}"

    # Gửi yêu cầu GET tới API
    response = requests.get(url)

    if response.status_code == 200:
        # Phân tích cú pháp JSON trả về từ API
        result = response.json()
        translated_text = ""
        for item in result[0]:
            translated_text += item[0]
        time.sleep(1)
        return translated_text
    else:
        exit(0)
        return "Error: Unable to translate"

def save_text_map():
    """Lưu text_map vào file JSON."""
    with open(text_map_file, 'w', encoding='utf-8') as f:
        json.dump(text_map, f, ensure_ascii=False)
    print("\nĐã lưu text_map.")


def signal_handler(sig, frame):
    """Xử lý tín hiệu hủy (Ctrl+C)."""
    global is_interrupted
    is_interrupted = True
    print("\nNhấn Ctrl+C lần nữa để thoát ngay hoặc chờ hoàn tất việc lưu.")
    save_text_map()
    exit(0)


# Gắn signal handler để xử lý Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
count = 0
try:
    with open(input_file, 'r', encoding='utf-16') as file:
        lines = file.readlines()

        for idx, line in enumerate(lines):
            if is_interrupted:
                break
            print(f"Đang xử lý dòng {idx + 1}/{len(lines)}")

            # Tách dòng theo tab để xử lý phần văn bản cần dịch
            parts = line.strip().split('\t')

            if len(parts) >= 6:  # Nếu có phần văn bản cần dịch (cột thứ 6)
                text_to_translate = parts[5]
                if text_to_translate != '"<null>"':
                    # Dịch văn bản
                    if text_to_translate in text_map:
                        translated_text = text_map[text_to_translate]
                    else:
                        count += 1
                        translated_text = translate(text_to_translate)
                        print(text_to_translate, "\n", translated_text)
                        text_map[text_to_translate] = text_to_translate
                    parts[5] = translated_text  # Gắn lại phần đã dịch vào phần tử thứ 6
            if (count + 1) % 100 == 0:
                count = 0
                save_text_map()
except Exception as e:
    print(f"\nĐã xảy ra lỗi: {e}")
finally:
    # Luôn lưu text_map khi kết thúc hoặc có lỗi
    save_text_map()
save_text_map()
