import math
import os.path
from os.path import splitext
import sys

from PIL import Image
#import typer
#app = typer.Typer()

#@app.command()
# 裁剪空白透明区域
def crop_blank(file):
    with Image.open(file) as img:
        print(img.getbbox())
        img_cropped = img.crop(img.getbbox(alpha_only=False))
        img_cropped.save(splitext(file)[0] + "_cropped.png")

#@app.command()
# 透明化背景
def transparent_background(file):
    with Image.open(file) as img:
        img = img.convert("RGBA")
        data = img.getdata()
        newData = []
        (r, g, b) = img.getpixel((0, 0))
        for item in data:
            if item[0] == r and item[1] == g and item[2] == b:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(splitext(file)[0] + "_transparent.png")


# 合并图片
def combine_image(path):
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    _merge_images(files, os.path.join(path+"combine.png"))


def _merge_images(files, output, scale=1.0):
    # COLS = int(input("请输入合并列数："))
    # ROWS = int(input("请输入合并行数："))
    COLS = math.ceil(math.sqrt(len(files)))
    ROWS = math.ceil(len(files) / COLS)
    images = [Image.open(file) for file in files]
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    max_height = max(heights)
    new_img = Image.new('RGB', (max_width * COLS, max_height * ROWS))
    index = 0
    for j in range(ROWS):
        for i in range(COLS):
            if index >= len(images):
                break
            img = images[index]
            new_img.paste(img, (i * max_width, j * max_height))
            index += 1
    new_img = new_img.resize((int(new_img.size[0] * scale), int(new_img.size[1] * scale)))
    new_img.save(output)

def _getbbox(img,alpha_threshold=0.01):
    img = img.copy()
    width,height = img.size
    threshold = 255 * alpha_threshold
    # 遍历图像的每个像素
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if a < threshold:
                img.putpixel((x, y), (255, 255, 255, 0))  # 将透明度小于阈值的像素设置为完全透明

    # 获取图像的边界框（bounding box），去除透明度小于0.1的区域
    return img.getbbox()


# 切分图片
# reverse 逆序切分
def split_image(file, reverse=False):
    COLS = int(input("请输入切分列数："))
    ROWS = int(input("请输入切分行数："))
    results = []
    with Image.open(file) as img:
        width, height = img.size
        min_bbox = None

        for j in range(ROWS):
            for i in range(COLS):
                img_split = img.crop(
                    (i * width // COLS, j * height // ROWS, (i + 1) * width // COLS, (j + 1) * height // ROWS))
                if bbox := img_split.getbbox(): #_getbbox(img_split,0.1):
                    print(i,j,bbox)
                    if min_bbox is None:
                        min_bbox = bbox
                    else:
                        min_bbox = [min(min_bbox[0], bbox[0]), min(min_bbox[1], bbox[1]), max(min_bbox[2], bbox[2]), max(min_bbox[3], bbox[3])]
                    # img_split = img_split.transpose(Image.FLIP_LEFT_RIGHT) #镜像
                    if reverse:
                        results.insert(0, img_split)
                    else:
                        results.append(img_split)

    # 写文件
    # 创建子目录
    if not os.path.exists(splitext(file)[0]):
        os.makedirs(splitext(file)[0])
    index = 0
    for img in results:
        if min_bbox is not None:
            img = img.crop(min_bbox)
        img.save(splitext(file)[0] + "/" + f"{index}".zfill(2) +".png")
        index = index + 1

    # 打开文件夹
    os.system(f"start explorer {splitext(file)[0]}")


# 把git每一帧存为图片
def _gif_to_images(file,MAX_FRAME=32):
    import imageio
    images = imageio.mimread(file)
    image_path = file.split(".")[0]
    # 减少帧数，大致在9~16帧
    images = images[::math.ceil(len(images) / MAX_FRAME)]
    for i, image in enumerate(images):
        imageio.imwrite(splitext(file)[0] + f"_frame_{i}.png", image)

    # 合并图片
    files = [splitext(file)[0] + f"_frame_{i}.png" for i in range(len(images))]

    _merge_images(files, splitext(file)[0] + "_merged.png", 0.5)
    for f in files:
        os.remove(f)
    # 显示图像
    with Image.open(splitext(file)[0] + "_merged.png") as img:
        img.show()

# 把mp4存成图片
def _mp4_to_images(file, MAX_FRAME=32):
    import cv2
    cap = cv2.VideoCapture(file)
    image_path = file.split(".")[0]
    frame_count = 0
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        frame_count += 1
    frames = frames[::math.ceil(len(frames) / MAX_FRAME)]
    for frame_count, frame in enumerate(frames):
        cv2.imwrite(splitext(file)[0] + f"_frame_{frame_count}.png", frame)
    cap.release()

    # 合并图片
    files = [splitext(file)[0] + f"_frame_{i}.png" for i in range(frame_count)]
    _merge_images(files, splitext(file)[0] + "_merged.png", 0.5)
    for f in files:
        os.remove(f)
    # 显示图像
    with Image.open(splitext(file)[0] + "_merged.png") as img:
        img.show()

def video_to_images(file):
    if file.endswith(".gif"):
        _gif_to_images(file)
    elif file.endswith(".mp4"):
        _mp4_to_images(file)

def main():
    if len(sys.argv) < 2 or (not os.path.exists(sys.argv[1])):
        print("Usage: jimg <file>")
        sys.exit(1)

    # 显示处理选项
    process = [("裁剪空白区域", crop_blank), ("切分图片", split_image), ("合并图片", combine_image),
               ("mp4/gif等视频转图片集", video_to_images), ("透明化背景", transparent_background)]
    for i, (name, _) in enumerate(process):
        print(f"{i + 1}. {name}")
    choice = 0
    while True:
        choice = input("请选择操作：")
        if not (choice.isdigit() and int(choice) in range(1, len(process) + 1)):
            print("无效的选择")
        else:
            break
    print(f"你选择了 {process[int(choice) - 1][0]}")
    process[int(choice) - 1][1](sys.argv[1])
    print("处理完成")


if __name__ == "__main__":
    main()
