from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import glob
import numpy as np
import os
import cv2
import argparse

'''
1. 从文字库随机选择10个字符
2. 生成图片
3. 随机使用函数
'''

# 从文字库中随机选择n个字符
def sto_choice_from_info_str(info_str, quantity=10):
    start = random.randint(0, len(info_str)-11)
    end = start + 10
    random_word = info_str[start:end]
    return random_word

def random_word_color():
    # 目前是黑色,更改这个函数还会改变字的颜色
    font_color_choice = [[54,54,54],[54,54,54],[105,105,105]]
    font_color = random.choice(font_color_choice)
    noise = np.array([random.randint(0,10),random.randint(0,10),random.randint(0,10)])
    font_color = (np.array(font_color) + noise).tolist()
    return tuple(font_color)

# 生成一张图片
def create_an_image(bground_path, width, height):
    bground_list = os.listdir(bground_path)
    bground_choice = random.choice(bground_list)
    bground = Image.open(bground_path+bground_choice)
    x, y = random.randint(0,bground.size[0]-width), random.randint(0, bground.size[1]-height)
    bground = bground.crop((x, y, x+width, y+height))
    return bground

# 选取作用函数
def random_choice_in_process_func():
    pass

# 模糊函数
def darken_func(image):
    #.SMOOTH
    #.SMOOTH_MORE
    #.GaussianBlur(radius=2 or 1)
    # .MedianFilter(size=3)
    # 随机选取模糊参数
    filter_ = random.choice(
                            [ImageFilter.SMOOTH,
                            ImageFilter.SMOOTH_MORE,
                            ImageFilter.GaussianBlur(radius=1.3)]
                            )
    image = image.filter(filter_)

    return image


# 旋转函数
def rotate_func():
    pass

# 噪声函数
def random_noise_func():
    pass

# 字体拉伸函数
def stretching_func():
    pass

# 随机选取文字贴合起始的坐标, 根据背景的尺寸和字体的大小选择
def random_x_y(bground_size, font_size):
    width, height = bground_size
    # 为防止文字溢出图片，x，y要预留宽高
    x = random.randint(0, width-font_size*10)
    y = random.randint(0, int((height-font_size)/4))
    return x, y

def random_font_size():
    font_size = random.randint(24,27)
    return font_size

def random_font(font_path):
    font_list = os.listdir(font_path)
    random_font = random.choice(font_list)
    return font_path + random_font

def main(save_path, num, info_str):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # 随机选取10个字符
    random_word = sto_choice_from_info_str(info_str, 10)
    # 生成一张背景图片，已经剪裁好，宽高为32*280
    raw_image = create_an_image('./background/', 280, 32)

    # 随机选取字体大小
    font_size = random_font_size()
    # 随机选取字体
    font_name = random_font('./font/')

    # 随机选取字体颜色
    font_color = random_word_color()

    # 随机选取文字贴合的坐标 x,y
    draw_x, draw_y = random_x_y(raw_image.size, font_size)

    # 将文本贴到背景图片
    font = ImageFont.truetype(font_name, font_size)
    draw = ImageDraw.Draw(raw_image)
    draw.text((draw_x, draw_y), random_word, fill=font_color, font=font)

    # 随机选取作用函数和数量作用于图片
    raw_image = darken_func(raw_image)

    # 保存文本信息和对应图片名称
    raw_image.save(os.path.join(save_path, random_word+'_'+str(num)+'.png'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', '--i', type=str, default="./data/demo_input.txt",
                        help='input Chinese words list file path')
    parser.add_argument('--output', '--o', type=str, default="./out/train/",
                        help='output image files directory')
    parser.add_argument('--num', '--n', type=int, default=10,
                        help='number of output files')
    args = parser.parse_args()

    # open file
    file_name = args.input
    output_path = args.output
    total = args.num
    with open(file_name, 'r', encoding='utf-8') as input_file:
        info_list = [part.strip().replace('\t', '') for part in input_file.readlines()]
        info_str = ''.join(info_list)


    for num in range(0, total):
        main(output_path, num, info_str)
        if num % 1000 == 0:
            print('[%d/%d]'%(num,total))


