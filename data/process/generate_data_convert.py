import os
import base64

def convert(anno_txt_path,classes_string, type='train', no_space=True, is_base64=True):
    jpgs = os.listdir('%s/'%anno_txt_path)
    print('img total number:%d'%len(jpgs))
    if no_space:
        f_w = open('%s/%s_word.txt' % (anno_txt_path, type), 'w')
    else:
        f_w = open('%s/%s.txt'%(anno_txt_path,type), 'w')
    # jpgs = glob.glob('%s/*.jpg'%anno_txt_path)
    for jpg in jpgs:
        if not jpg.endswith('.jpg'):
            print(jpg)
            continue
        jpg = os.path.basename(jpg)
        words_b64 = jpg[0:jpg.rfind('_')]
        if is_base64:
            words_b64 = words_b64.replace('-', '+').replace('_', '/')
            words_b64 = words_b64 + '=='
            words_b64 = base64.b64decode(words_b64)
            words_b64 = words_b64.decode()
        words_b64 = words_b64.strip()
        if no_space:
            words_b64 = words_b64.replace(' ', '')
        anno = words_b64 + '\n'
        anno_new = ''
        not_found_char = False
        for char in anno:
            if char != '\n' and char not in classes_string:
                not_found_char = True
                break
            if char != '\n':
                anno_new = anno_new + ' ' + (str(classes_string.index(char) + 1))
            else:
                anno_new = anno_new + '\n'
        if not_found_char:
            continue
        f_w.write('%s/%s%s'%(anno_txt_path, jpg, anno_new))
    f_w.close()

def convert_txt(image_path,classes_string):
    image_list_train=os.listdir(image_path+'train_word/')
    for image_ in image_list_train:
        if image_.endswith('.txt'):
            pass
        else:
            print(image_path+'train_word/'+image_)
            convert(image_path+'train_word/'+image_,classes_string, type='train', no_space=True)
    image_list_valid=os.listdir(image_path+'valid_word/')
    for image_ in image_list_valid:
        if image_.endswith('.txt'):
            pass
        else:
            print(image_path+'valid_word/'+image_)
            convert(image_path+'valid_word/'+image_,classes_string, type='valid', no_space=True)

if __name__ == '__main__':
    image_path='/data/git/ocr-platform/statistic/TextGenerator/TextGenerator/dataset/'
    classes_string='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'
    convert_txt(image_path,classes_string)