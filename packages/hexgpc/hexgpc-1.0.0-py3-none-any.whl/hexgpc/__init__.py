import os
from PIL import Image, ImageOps

def converter(file_path, invert=False, display_width=128, display_height=64):
    img = Image.open(file_path)
    img = img.convert("L")
    if invert:
        img = ImageOps.invert(img)
    img = img.resize((min(img.width, display_width), min(img.height, display_height)), Image.Resampling.LANCZOS)
    width, height = img.size
    x = (display_width - width) // 2
    y = (display_height - height) // 2
    img = img.convert("1", dither=Image.FLOYDSTEINBERG)
    pixels = list(img.getdata())
    hex_vals = []
    for i in range(0, len(pixels), 8):
        byte = 0
        for bit in range(8):
            if i + bit < len(pixels) and pixels[i + bit] == 0:
                byte |= 1 << (7 - bit)
        hex_vals.append(f"0x{byte:02X}")
    formatted = []
    for i in range(0, len(hex_vals), 16):
        line = ", ".join(hex_vals[i:i+16])
        formatted.append(f"        {line}")
    hex_data = ",\n".join(formatted)
    Form = (
        f"const image picture[] = {{\n"
        f"    {{\n"
        f"        {width}, {height},\n"
        f"{hex_data}\n"
        f"    }}\n"
        f"}};\n\n"
        f"init {{\n"
        f"    cls_oled(OLED_BLACK);\n"
        f"    image_oled({x}, {y}, TRUE, TRUE, picture[0]);\n"
        f"}}"
    )
    return Form
