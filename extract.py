import cv2

def extract_text(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Không đọc được ảnh!")

    binary_data = []
    delimiter = '1111111111111110'
    found_delimiter = False
    
    for row in img:
        for pixel in row:
            for channel in pixel[:3]:  
                binary_data.append(str(channel & 1))
                
                if len(binary_data) >= len(delimiter):
                    last_bits = ''.join(binary_data[-len(delimiter):])
                    if last_bits == delimiter:
                        found_delimiter = True
                        break

            if found_delimiter:
                break

        if found_delimiter:
            break
    
    if not found_delimiter:
        raise ValueError("Không tìm thấy dữ liệu ẩn!")


    binary_str = ''.join(binary_data[:-len(delimiter)])  
    padding = 8 - (len(binary_str) % 8)
    binary_str += '0' * padding if padding != 8 else ''

    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        byte_array.append(int(byte, 2))
    
    try:
        decoded_text = byte_array.decode('utf-8', errors='replace')
        if decoded_text.startswith("UTF8_STEG_HEADER"):
            final_text = decoded_text[len("UTF8_STEG_HEADER"):]
        else:
            final_text = decoded_text
    except Exception as e:
        raise ValueError(f"Lỗi giải mã: {str(e)}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    print(f"Đã giải mã thành công vào {output_path}")

if __name__ == "__main__":
    image_path = input("Ảnh chứa tin: ").strip('"')
    output_path = input("File text đầu ra: ").strip('"')
    extract_text(image_path, output_path)