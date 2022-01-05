import os
# import sys
# # sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append('/data/git/ocr-platform/seuic_dl/')
import cv2
import numpy as np
import random
from PIL import Image
import torchvision.transforms as transforms
import recognize_v1.data.process.distorsion as distorsion_generator
from math import *
# from shutil import copyfile
from common.common import to_json
from redis_help.redis_helper import RedisHelper
obj = RedisHelper()
import logging
         
def contrast_demo(img1, c, b):
    rows, cols = img1.shape
    blank = np.zeros([rows, cols], img1.dtype)
    dst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return dst

def add_gaussian_noise(image_in):
    temp_image = np.float64(np.copy(image_in))
    noise_sigma=25
    
    if len(temp_image.shape) == 2:
        h, w = temp_image.shape
        # 标准正态分布*noise_sigma
        noise = np.random.randn(h, w) * noise_sigma
        noisy_image = np.zeros(temp_image.shape, np.float64)
        noisy_image = temp_image + noise
    else:
        h, w, _ = temp_image.shape
        # 标准正态分布*noise_sigma
        noise = np.random.randn(h, w) * noise_sigma
        noisy_image = np.zeros(temp_image.shape, np.float64)
        noisy_image[:,:,0] = temp_image[:,:,0] + noise
        noisy_image[:,:,1] = temp_image[:,:,1] + noise
        noisy_image[:,:,2] = temp_image[:,:,2] + noise
    return noisy_image

def distorsion(img):
    # print('字体扭曲变形')
    distorsion_type=random.choice([1,2])
    distorsion_orientation=random.choice([0,1,2])
    if distorsion_type == 0:
        img = img  # Mind = blown
    elif distorsion_type == 1:
        img = distorsion_generator.sin(
            img,
            vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
            horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
    elif distorsion_type == 2:
        img = distorsion_generator.cos(
            img,
            vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
            horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
    else:
        img = distorsion_generator.random(
            img,
            vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
            horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
    return img
                                                                                                                          
def random_aug(img,aug_type,session_id):
    # print(img.shape) (38, 356)
    ######### Apply Border to image ############
    if aug_type == 1:
        bd_rnd_0=random.choice([0,1])
        if bd_rnd_0==0:
            color=random.randint(90,159)
            img = cv2.copyMakeBorder(img,random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10),cv2.BORDER_CONSTANT,value=[color,color,color])
        else:
            img = cv2.copyMakeBorder(img,random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10),cv2.BORDER_REPLICATE)
    ######### Apply gsblur to image ############
    elif aug_type == 2:
        if img.shape[1]>30:
            blur = random.choice([3,5])
            img=cv2.GaussianBlur(img,(blur,blur),0)
    ######### Apply gamma to image ############
    elif aug_type == 3:
        gamma = random.choice([0.95,1.05])
        img = np.power(img, gamma)
    ########## reverse the background color #########
    elif aug_type == 4:
        img = 255-img
    ######### Apply distorsion to image ############
    elif aug_type == 5:
        img=distorsion(img)
    ############### add gaussian noise ##############  
    elif aug_type == 6:
        if img.shape[1]>30:
            img=add_gaussian_noise(img)
    else:
        message='Please enter the correct type of data enhancement (data_aug)'
        obj.public(to_json(session_id=session_id, interface_type=4, status_type=3, data_type=1, message=message))
        return 
    return img


def text_generator(train_data_path='', data_aug=[],skew_angle=5,output_data_path='',session_id=777):
    try:
        '''
        0代表旋转，1代表边缘扩充，2代表模糊，3代表亮度，4代表反色, 5代表弯曲，6代表噪声
        '''
        txt_name='train_word.txt'
        if txt_name not in os.listdir(train_data_path):
            print('train_word.txt not in %s' % (train_data_path))
            message = 'train_word.txt not in %s' % (train_data_path)
            logging.error(message)
            obj.public(to_json(session_id=session_id, interface_type=4, status_type=1, data_type=1, message=message))
            return False
        txt_write=open(os.path.join(output_data_path,txt_name),'w')
        if 0 in data_aug:
            data_aug.remove(0)
            with open(os.path.join(train_data_path,txt_name), 'r')as f:
                line = f.readline()
                while line: 
                    print(line)  
                    line=line.strip()
                    img_name = line.split(' ')[0]
                    if img_name in os.listdir(train_data_path):
                        if img_name.endswith('jpg') or img_name.endswith('bmp') or img_name.endswith('png'):
                            i=0
                            for rotated_angle in range(-skew_angle,skew_angle):
                                img = cv2.imread(os.path.join(train_data_path, img_name), cv2.IMREAD_GRAYSCALE)
                                img = Image.fromarray(img)
                                img = transforms.ColorJitter(brightness=32.0 / 255, saturation=0.5)(img)
                                img = np.array(img)
                                for aug_type in data_aug:
                                    if_aug=random.choice([0,1,2])
                                    if if_aug==0:
                                        # print(aug_type)
                                        img = random_aug(img,aug_type,session_id)
                                # img = np.array(img)
                                height, width = img.shape[:2]
                                # 旋转后的尺寸
                                heightNew = int(width * fabs(sin(radians(rotated_angle))) + height * fabs(cos(radians(rotated_angle))))
                                widthNew = int(height * fabs(sin(radians(rotated_angle))) + width * fabs(cos(radians(rotated_angle))))
                                matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), rotated_angle, 1)
                                matRotation[0, 2] += (widthNew - width) / 2  
                                matRotation[1, 2] += (heightNew - height) / 2  
                                img = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

                                num_img=img_name.split('.')[0]+'_%d'%i+'.jpg'
                                label=line.split(' ')[1]
                                cv2.imwrite(os.path.join(output_data_path,num_img),img) 
                                txt_write.write(num_img+' '+label+'\n')  
                                i+=1
                    line = f.readline()
        else:
            with open(os.path.join(train_data_path,txt_name), 'r') as f:
                line = f.readline()
                while line: 
                    print(line)  
                    line=line.strip()
                    img_name = line.split(' ')[0]
                    i=0
                    # print('0')
                    if img_name in os.listdir(train_data_path):
                        # print(img_name)
                        if img_name.endswith('jpg') or img_name.endswith('bmp') or img_name.endswith('png'):
                            img = cv2.imread(os.path.join(train_data_path,img_name), cv2.IMREAD_GRAYSCALE)
                            # print('1')
                            img = Image.fromarray(img)
                            img = transforms.ColorJitter(brightness=32.0 / 255, saturation=0.5)(img)
                            img = np.array(img)
                            # print('2')
                            for aug_type in data_aug:
                                if_aug=random.choice([0,1,2])
                                if if_aug==0:
                                    img = random_aug(img,aug_type,session_id)
                                    # print('3')
                                # print('4')
                            num_img=img_name.split('.')[0]+'_%d'%i+'.jpg'
                            # print(num_img)
                            label=line.split(' ')[1]
                            cv2.imwrite(os.path.join(output_data_path,num_img),img) 
                            txt_write.write(num_img+' '+label+'\n')  
                            i+=1
                    line = f.readline()
        txt_write.close()
        return True
    except:
        print('error image:%s'%(line))
        message='error image:%s'%(line)
        logging.error(message)
        obj.public(to_json(session_id=session_id, interface_type=4, status_type=3, data_type=1, message=message))
        return False
    

if __name__=='__main__':
    
    text_generator(train_data_path='/data/git/ocr-platform/data/annotation_data/recognize/dataset/ocr_dataset_point/point_0928_add/',  data_aug=[0],session_id=777)
        
