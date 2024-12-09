import os
from PIL import Image, ImageOps
import cv2

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
    return {
        "width": width,
        "height": height,
        "hex_data": hex_data,
        "x_offset": x,
        "y_offset": y,
    }

def process_video(file_path, invert=False, max_frames=20):
    cap = cv2.VideoCapture(file_path)
    frames = []
    frame_count = 0
    if not cap.isOpened():
        raise ValueError("Cannot open video file.")
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        result = converter(img, invert)
        frames.append(result)
        frame_count += 1
    cap.release()
    return frames

def generate_c_code_image(data):
    hex_data = data["hex_data"]
    return (
        f"const image picture[] = {{\n"
        f"    {{\n"
        f"        {data['width']}, {data['height']},\n"
        f"{hex_data}\n"
        f"    }}\n"
        f"}};\n\n"
        f"init {{\n"
        f"    cls_oled(OLED_BLACK);\n"
        f"    image_oled({data['x_offset']}, {data['y_offset']}, TRUE, TRUE, picture[0]);\n"
        f"}}"
    )

def generate_c_code_video(frames):
    frame_definitions = []
    for frame in frames:
        frame_def = f"    {{ {frame['width']}, {frame['height']},\n{frame['hex_data']} }}"
        frame_definitions.append(frame_def)
    video_array = "const image video[] = {\n" + ",\n".join(frame_definitions) + "\n};\n\n"
    track = ", ".join(str(i) for i in range(len(frames)))
    track_array = f"const int track[] = {{{track}}};\n\n"
    c_code = (
        "int frame;\n\n"
        "main\n"
        "{\n"
        "    play_video();\n"
        "}\n\n"
        "function play_video() {\n"
        "    vm_tctrl(10);\n"
        "    if(frame < sizeof(track)/sizeof(int)) combo_run(play)\n"
        "    else frame = 0;\n"
        "}\n\n"
        "combo play {\n"
        "    cls_oled(0);\n"
        "    image_oled(0, 0, TRUE, TRUE, video[track[frame]]);\n"
        "    wait(20);\n"
        "    frame++;\n"
        "}\n\n" +
        video_array +
        track_array
    )
    return c_code

def process_file(file_path, invert=False, max_frames=20):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".mp4", ".avi", ".mov", ".mkv", ".webm"]:
        print("Processing video...")
        frames = process_video(file_path, invert, max_frames)
        return generate_c_code_video(frames)
    else:
        print("Processing image...")
        img_data = converter(file_path, invert)
        return generate_c_code_image(img_data)
