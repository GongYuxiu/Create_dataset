import random
from random import randint
import os
import numpy as np
import string
dict_num='0123456789'
dict_letter_up='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
dict_letter_lw='abcdefghijklmnopqrstuvwxyz'
dict_letter='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
dict_num_letter='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
dict_num_letter_all='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
dict_symbol='!@#$%^&*()-_+={[}]\\|":;?/>.<,~'
string_list={'u':dict_letter_up,'l':dict_letter_lw,'n':dict_num,'a':dict_letter,'b':dict_num_letter,'c':dict_num_letter_all,'s':dict_symbol}

def shuffle_word(in_path,out_path):
    out = open(out_path,'w')
    lines=[]
    infile= open(in_path, 'r')
    for line in infile:
        lines.append(line)
    random.shuffle(lines)
    for line in lines:
        out.write(line)
    infile.close()
    out.close()

def generate_long_words(txt_path, numbers=100000, dict = dict_num):
    dict3_len = len(dict)
    f = open(txt_path, 'w')
    for ind in range(numbers):
        str = ''
        rand = random.random()
        for text_ind in range(3):
            digit_len = randint(2,6)
            for ind_2 in range(digit_len):
                replicate_num = 1
                rand_1 = random.random()
                if rand_1 < 0.025:
                    replicate_num = 3
                dict_index = randint(0, dict3_len - 1)
                for ind_3 in range(replicate_num):
                    str += dict[dict_index]
            if rand < 0.1:
                # if text_ind != 3:
                    str += '   '
        f.write(str + '\n')
    f.close()

def generate_short_words(txt_path, numbers=100000, dict = dict_num):
    dict3_len = len(dict)
    f = open(txt_path, 'a+')
    for ind in range(numbers):
        str = ''
        rand = random.random()
        digit_len = randint(2,4)
        for ind_2 in range(digit_len):
            replicate_num = 1
            rand_1 = random.random()
            if rand_1 < 0.025:
                replicate_num = 3
            dict_index = randint(0, dict3_len - 1)
            for ind_3 in range(replicate_num):
                str += dict[dict_index]
        if rand < 0.1:
            # if text_ind != 3:
                str += '   '
        f.write(str + '\n')
    f.close()

def random_seq(choice_seq,count=3,repeatable=True):
    if repeatable:
        return [random.choice(choice_seq) for _ in range(count)]
    return random.sample(choice_seq,count)
def num_shuffle(count,repeatable=True):
    digits=random_seq(string.digits,count,repeatable=True)
    random.shuffle(digits)
    return ''.join(digits)
def uppercase_shuffle(count,repeatable=True):
    letters=random_seq(string.ascii_uppercase,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)
def lowercase_shuffle(count,repeatable=True):
    letters=random_seq(string.ascii_lowercase,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)
def letter_shuffle(count,repeatable=True):
    letters=random_seq(string.ascii_letters,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)
def num_letter_shuffle(count,repeatable=True):
    letters=random_seq(dict_num_letter,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)
def num_letter_all_shuffle(count,repeatable=True):
    letters=random_seq(dict_num_letter_all,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)
def symbol_shuffle(count,repeatable=True):
    letters=random_seq(dict_symbol,count,repeatable=True)
    random.shuffle(letters)
    return ''.join(letters)

def generate_template_words(txt_path,numbers, dict_template):
    '''
    u代表大写字母A-Z
    l代表小写字母a-z 
    n代表数字0-9
    a代表大小写字母A-Z a-z的混合
    b代表大写字母A-Z与数字0-9的混合
    c代表大小写字母A-Z a-z与数字0-9的混合
    s代表通用特殊符号：!@#$%^&*()-_+={[}]\\|":;?/>.<,~ 
    如果固定哪些字符用英文{}括起来(包含空格)，如果固定选择哪些字符用英文()括起来,英文逗号隔开
    例如：332-JK123 如果中间横杠-是固定的，其他字母随机则：nnn{-}uunnn 
                    如果JK字母也是固定的，则：nnn{-}{JK}nnn 
                    如果首个数字是固定在3,6,8中选择的，则：{(3,6,8)}nn{-}{JK}nnn
    '''
    str_list={'u':uppercase_shuffle,'l':lowercase_shuffle,'n':num_shuffle,'a':letter_shuffle,'b':num_letter_shuffle,'c':num_letter_all_shuffle,'s':symbol_shuffle}
    
    f = open(txt_path, 'w')
    for ind in range(numbers):
        str=''
        start_word=''
        count=1
        par_if=False
        index=0
        class_dict=[]
        while index<(len(dict_template)):
            if dict_template[index] in str_list.keys() and par_if==False:
                if start_word!='' and dict_template[index]==start_word:
                    count+=1
                    if index==len(dict_template)-1:
                        str+=str_list[start_word](count)
                        class_dict.append([start_word])
                else:
                    if start_word!='':
                        str+=str_list[start_word](count)
                        class_dict.append([start_word])
                        count=1
                        start_word=dict_template[index]
                    else:
                        start_word=dict_template[index]
            else:
                if dict_template[index]=='{':
                    par_if=True
                    if start_word!='':
                        str+=str_list[start_word](count)
                        class_dict.append([start_word])
                        count=1
                if dict_template[index]!='{' and par_if:
                    if dict_template[index]=='}':
                        par_if=False
                        start_word=''
                    elif dict_template[index]=='(':
                        str_0=dict_template[index+1:].split(')')[0].split(',')
                        for str_1 in str_0:
                            class_dict.append(str_1)
                        str+=random.choice(str_0)
                        index+=(len(str_0)+len(str_0)-1+1)
                        par_if=False
                        if index+2<len(dict_template):
                            # start_word=dict_template[index+2]
                            count=1
                    else:
                        str+=dict_template[index]
                        class_dict.append(dict_template[index])
            index+=1
        # print(class_dict)
        f.write(str + '\n')
    f.close()
    class_dict_result = []
    seen = set()
    class_dict_result_string=''
    for x in class_dict:
        hsh = tuple(sorted(x))
        if hsh not in seen:
            class_dict_result.append(x)
            seen.add(hsh)
    for class_d in class_dict_result:
        if isinstance(class_d,list):
            class_dict_result_string+=string_list[class_d[0]]
        else:
            class_dict_result_string+=class_d
    # print(class_dict_result_string)
    # print("".join({}.fromkeys(class_dict_result_string).keys()).replace(" ",""))
    return "".join({}.fromkeys(class_dict_result_string).keys()).replace(" ","")

def generate(template = dict_num):
    if isinstance(template,int):
        if template==0:
            dict_string='0123456789'
        elif template==1:
            dict_string='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif template==2:
            dict_string='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$&%*+-:./<>@\\'
        train_path='data/texts/general_train_0.txt'
        train_path_out='data/texts/general_train.txt'
        valid_path='data/texts/general_valid_0.txt'
        valid_path_out='data/texts/general_valid.txt'
        generate_long_words(train_path, 100000, dict_string)
        generate_short_words(train_path, 100000, dict_string)
        generate_long_words(valid_path, 10000, dict_string)
        generate_short_words(valid_path, 10000, dict_string)
        shuffle_word(train_path,train_path_out)
        shuffle_word(valid_path,valid_path_out)
        return dict_string
    else:
        class_dict_result=generate_template_words('data/texts/general_train.txt',numbers=100000, dict_template = template)
        class_dict_result=generate_template_words('data/texts/general_valid.txt',numbers=10000, dict_template = template)
        return class_dict_result


if __name__ == '__main__':
    class_dict_result=generate(template=2)
    print(class_dict_result)
    class_dict_result=generate(template='nua{-}{(J,K)}nnn{ }{kg}')
    print(class_dict_result)
    # generate(dict='{(J,K)}{ }nnn')

