import os
import json

input_file = '../data/languagedata_en.txt'
output_file = '../data/languagedata_vi.txt'
text_map_file = 'text_map.json'

if os.path.exists(text_map_file):
    with open(text_map_file, 'r', encoding='utf-8') as f:
        text_map = json.loads(f.read())
else:
    text_map = {}
    
with open(input_file, 'r', encoding='utf-16') as file:
    lines = file.readlines()
    
with open(output_file, 'w', encoding='utf-16') as output:
    for idx, line in enumerate(lines):
        print(f"Đang xử lý dòng {idx + 1}/{len(lines)}")
        
        parts = line.strip().split("\t")
        
        if len(parts) >= 6:
            text_to_translate = parts[5]
            translated_text = text_map.get(text_to_translate, text_to_translate)
            translated_text = translated_text.replace("&quot;", "\"")
            translated_text = translated_text.replace("&#39", "'")
            parts[5] = translated_text
        output.write('\t'.join(parts) + "\n")
print("File đã được dịch và lưu vào:", output_file)
