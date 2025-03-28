import cv2

def hide_text(image_path, text_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Không đọc được ảnh!")
    
    with open(text_path, "r", encoding="utf-8") as f:
        text = "UTF8_STEG_HEADER" + f.read()   

    binary_str = ''.join(f"{byte:08b}" for byte in text.encode('utf-8', errors='replace'))
    binary_str += '1111111111111110'  
    
    required_pixels = len(binary_str) // 3 + 1
    available_pixels = img.shape[0] * img.shape[1]
    
    if required_pixels > available_pixels:
        raise ValueError(f"Ảnh quá nhỏ! Cần ít nhất {required_pixels} pixels, có {available_pixels}")

    data_index = 0
    for row in img:
        for pixel in row:
            for channel in [0, 1, 2]: 
                if data_index < len(binary_str):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(binary_str[data_index])
                    data_index += 1
            if data_index >= len(binary_str):
                break
        if data_index >= len(binary_str):
            break
    
    if not output_path.lower().endswith('.png'):
        output_path += '.png'
    cv2.imwrite(output_path, img)
    print(f"Đã giấu thành công vào {output_path}")

if __name__ == "__main__":
    image_path = input("Ảnh gốc: ").strip('"')
    text_path = input("File text cần giấu: ").strip('"')
    output_path = input("Ảnh đầu ra: ").strip('"')
    hide_text(image_path, text_path, output_path)