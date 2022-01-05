
def text_generator_1(template,  data_aug=[],  bk_img='',  word_type='', data_quantity=[20000,2000],font_size=[20,100],  output_data_path='',skew_angle=5,session_id=777):
    '''
    根据用户输入的模板类型产生训练数据
    template ：字符的模板（初步有num,upper(大写字母),lower(小写字母),字符等，
    如用户输入  nnnsuunnn  
    u代表大写字母A-Z
    l代表小写字母a-z 
    n代表数字0-9
    a代表大小写字母A-Z a-z的混合
    b代表大写字母A-Z与数字0-9的混合
    c代表大小写字母A-Z a-z与数字0-9的混合
    s代表通用特殊符号：!@#$%^&*()-_+={[}]\\|":;?/>.<,~ 
    如果固定哪些字符用英文{}括起来(包含空格)，如果固定选择哪些字符用英文()括起来,英文逗号隔开
    例如：332-JK123 如果中间横杠-是固定的，其他字母随机则：nnn{-}uunnn 
                    如果JK字母也是固定的，则：nnn{-}{JK}nnn  生成如：258-JK557
                    如果首个数字是固定在3,6,8中选择的，则：{(3,6,8)}nn{-}{JK}nnn 生成如：385-JK207 637-JK500 801-JK912等等
    也可以选择默认0，1，2，3，4，5
    0：通用数字（'0123456789'）
    1：通用数字加上大写字母（'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'）
    2：通用数字加大小写字母加符号（'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$&%*+-:./<>@\\'）
    3：称重（'0123456789kgKG净含量重皮毛公斤,.：，/lb'）
    4：点阵日期（'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$&%*+-:./<>@\\'）
    5：镂空（'0123456789'）
    data_aug: 数据的增强方式（以英文逗号割开，0代表旋转，1代表边缘扩充，2代表模糊，3代表亮度，4代表反色, 5代表弯曲，6代表噪声。比如： [0,1] 代表选择了旋转和边缘扩充）
    bk_img  : 背景图片路径（多个背景图片文件夹路径或者单个图片路径，默认为通用背景图片路径）
    word_type：字体路径（多个字体文件夹路径或者单个字体路径，默认为通用字体路径）
    data_quantity：数据集大小[20000,2000]（不填默认训练集每个字体类型20000，验证集每个字体类型2000）
    skew_angle: 旋转角度，如果不设置旋转的数据增强方式，该参数可以忽略，可不填，如果设置旋转不修改旋转角度，默认为5

    参数：
    template ：字符的模板
    data_aug: 数据的增强方式
    bk_img  : 背景图片路径
    word_type：字体路径
    data_quantity：数据集大小
    output_data_path: 训练数据文件路径
    skew_angle: 旋转角度
    返回：
    无

    '''
    from data.batch_generate_folder import text_generator
    class_dict=text_generator(template,  data_aug,  bk_img,  word_type,  data_quantity,font_size, output_data_path,skew_angle)
    print(class_dict)

if __name__=='__main__':
    text_generator_1(template='nnn{-JK}{ }{(1,2,3)}nnn{公斤}',
                    data_aug=[0,1,2,3,4,5,6],  
                    bk_img='data/bk_picture/pictures_JD/',  
                    word_type='data/fonts/cn/',  
                    data_quantity=10, 
                    output_data_path='save_dataset/',
                    skew_angle=10)