import os, errno
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.process.run import *
import argparse
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import random as rnd
import string
import sys
import random
from tqdm import tqdm
from data.process.string_generator import (
    create_strings_from_dict,
    create_strings_from_file,
    create_strings_from_wikipedia,
    create_strings_randomly,
)
from data.process.utils import load_dict, load_fonts
from data.process.data_generator import FakeTextDataGenerator
from multiprocessing import Pool
from data.process.word_generator import generate
from data.process.generate_data_convert import convert_txt
import numpy as np

# def hex_to_rgb(value):
#     value = value.lstrip('#')
#     lv = len(value)
#     return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
# def rgb_to_gray(im1):
#     im1 = np.array(im1, dtype=np.float32)
#     im1[...,0] = im1[...,0]*30.0
#     im1[...,1] = im1[...,1]*59.0
#     im1[...,2] = im1[...,2]*11.0
#     im1 = np.sum(im1, axis=2)
#     im1[...,:] = im1[...,:]/100.0
#     return im1

def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def word_generator(output_dir="", language='en', font_dir='fonts/en', font=False, use_wikipedia=False, length=1, count=5, input_file="",
         thread_count=1, name_format=0, extension='jpg', skew_angle=0, random_skew=False, blur=0,
         blur_if=True,contrast_if=False,reverse_if=False,noise_if=False, background=0,bk_path='', distorsion=0, distorsion_orientation=0, handwritten=False, width=-1, alignment=1,
         text_color="#FFFF00", orientation=0, space_width=1.0, character_spacing=0, margins=(5, 5, 5, 5), fit=False, output_mask=0, font_size=32):
    #text_color="#000000,#888888,#a8bb19"

    # Create the directory if it does not exist.
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    # lang_dict = load_dict(language)
    # Create font (path) list

    if font_dir:
        fonts = [
            os.path.join(font_dir, p)
            for p in os.listdir(font_dir)
            if os.path.splitext(p)[1] == ".ttf" or os.path.splitext(p)[1] == ".ttc" or os.path.splitext(p)[1] == ".TTF"
        ]
    elif font:
        if os.path.isfile(font):
            fonts = [font]
        else:
            sys.exit("Cannot open font")
    else:
        fonts = load_fonts(language)

    output_dir_new=output_dir
    for font in fonts:
        output_dir=output_dir_new+font.split("/")[-1].split(".")[0]+"/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Creating synthetic sentences (or word)
        strings = []

        if use_wikipedia:
            strings = create_strings_from_wikipedia(length, count, language)
        elif input_file != "":
            strings = create_strings_from_file(input_file, count)

        string_count = len(strings)

        p = Pool(thread_count)
        for _ in tqdm(
            p.imap_unordered(
                FakeTextDataGenerator.generate_from_tuple,
                zip(
                    [i for i in range(0, string_count)],
                    strings,
                    [font for _ in range(0, string_count)],
                    [output_dir] * string_count,
                    [font_size] * string_count,
                    [extension] * string_count,
                    [skew_angle] * string_count,
                    [random_skew] * string_count,
                    [blur] * string_count,
                    [blur_if] * string_count,
                    [contrast_if] * string_count,
                    [reverse_if] * string_count,
                    [noise_if] * string_count,
                    [background] * string_count,
                    [bk_path] * string_count,
                    [distorsion] * string_count,
                    [distorsion_orientation] * string_count,
                    [handwritten] * string_count,
                    [name_format] * string_count,
                    [width] * string_count,
                    [alignment] * string_count,
                    [text_color] * string_count,
                    [orientation] * string_count,
                    [space_width] * string_count,
                    [character_spacing] * string_count,
                    [margins] * string_count,
                    [fit] * string_count,
                    [output_mask] * string_count,
                ),
            ),
            total=count,
        ):
            pass
        p.terminate()

        if name_format == 2:
            # Create file with filename-to-label connections
            with open(
                os.path.join(output_dir, "labels.txt"), "w", encoding="utf8"
            ) as f:
                for i in range(string_count):
                    file_name = str(i) + "." + extension
                    f.write("{} {}\n".format(file_name, strings[i]))

def text_generator(template,  data_aug,  bk_img,  word_type, data_quantity,font_size, output_data_path,skew_angle):
        train_path = output_data_path + 'train_word/'
        valid_path= output_data_path + 'valid_word/'
        if not os.path.exists(train_path):
            os.makedirs(train_path)
        if not os.path.exists(valid_path):
            os.makedirs(valid_path)
  
        if isinstance(template,str) or isinstance(template,int):
            class_dict=generate(template=template)
        else:
            print('Please enter the correct template')
            return 0

        if word_type=='':
            if is_contain_chinese(class_dict):
                print(class_dict)
                word_type='data/fonts/general_cn/'
            else:
                print(class_dict)
                word_type='data/fonts/general_en/'
    
        #gneral_Low contrast
        # rgb=(random.randint(int(255*0.65),int(255*0.8)), random.randint(int(255*0.65),int(255*0.8)), random.randint(int(255*0.65),int(255*0.8)))
        # text_c=rgb_to_hex(rgb)
        # # print(0.3*rgb[0]+0.59*rgb[1]+0.11*rgb[2]) #(165,204)
        # # print(text_c)
        # blur_if = False
        # background = 1 #random.choice([0,1,3])
        # main(length=25,count=200, distorsion=distorsion, text_color=text_c, character_spacing=character_spacing, font_dir='fonts/general_en/', background=background,  skew_angle=skew_angle, random_skew=random_skew, blur=1,thread_count=10,blur_if=blur_if,  margins=margins, fit=True,  input_file='texts/general_num_letter.txt', output_dir=train_path, format_=format_)
        # main(length=25,count=50, distorsion=distorsion, text_color=text_c, character_spacing=character_spacing, font_dir='fonts/general_en/', background=background,  skew_angle=skew_angle, random_skew=random_skew, blur=1,thread_count=10,blur_if=blur_if,  margins=margins, fit=True,  input_file='texts/general_valid.txt', output_dir=valid_path, format_=format_)
        '''
        data_aug:
        0代表旋转，1代表边缘扩充，2代表模糊，3代表亮度，4代表反色， 5代表弯曲， 6代表噪声
        '''
        character_spacing = random.choice(range(4,10))

        blur_if = False
        random_skew=False
        contrast_if=False
        distor_if=False
        reverse_if=False
        noise_if=False
        skew_angle=0
        if 0 in data_aug:
            random_skew=True
            skew_angle=skew_angle
        if 2 in data_aug:
            blur_if = True
        if 3 in data_aug:
            contrast_if=True
        if 4 in data_aug:
            reverse_if=True
        if 5 in data_aug:
            distor_if=True
        if 6 in data_aug:
            noise_if=True

        distorsion = distor_if
            
        if isinstance(data_quantity,int):
            data_size_train=int(data_quantity)
            data_size_valid=int(data_quantity//10)
            print(data_size_train)
            print(data_size_valid)
        elif isinstance(data_quantity,string):
            print('Please enter the correct format of data_size')

        word_generator(length=25,count=data_size_train, distorsion=distorsion, text_color="#282828", character_spacing=character_spacing, font_dir=word_type,bk_path=bk_img,  skew_angle=skew_angle, random_skew=random_skew, blur=1,thread_count=10,blur_if=blur_if,contrast_if=contrast_if,reverse_if=reverse_if,noise_if=noise_if, fit=True,  input_file='data/texts/general_train.txt', output_dir=train_path,font_size=font_size)
        word_generator(length=25,count=data_size_valid, distorsion=distorsion, text_color="#282828", character_spacing=character_spacing, font_dir=word_type, bk_path=bk_img, skew_angle=skew_angle, random_skew=random_skew, blur=1,thread_count=10,blur_if=blur_if,contrast_if=contrast_if,reverse_if=reverse_if,noise_if=noise_if, fit=True,  input_file='data/texts/general_valid.txt', output_dir=valid_path,font_size=font_size)
        print('########### 数据集图片已经生成完毕！ #################')
        convert_txt(output_data_path,class_dict)
        print('########### 数据集标签已经生成完毕！ #################')
        return class_dict

if __name__=='__main__':
    # class_dict=text_generator(template='nnn{-JK}{ }{(1,2,3)}nnn{ }{公斤}',  data_aug=[0,6], bk_img='',word_type='', data_quantity=[10000,5],font_size=[20,100], output_data_path='/data/git/ocr-platform/statistic/TextGenerator/TextGenerator/dataset/',skew_angle=10)
    pass