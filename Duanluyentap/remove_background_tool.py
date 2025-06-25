from PIL import Image

def remove_white_background(image_path, output_path):
    image = Image.open(image_path).convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        if item[0] >= 200 and item[1] >= 200 and item[2] >= 200:
            newData.append((255, 255, 255, 0))  # Làm trong suốt
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path, "PNG")
    print(f'✅ Đã xử lý và lưu: {output_path}')
if __name__ == '__main__':
    remove_white_background(
        'Duanluyentap/—Pngtree—cactus plant hot summer cool_3822338.png',   # ảnh xương rồng gốc
        'Duanluyentap/cactus_cleaned.png'   # ảnh đã xử lý
    )