import os
import random as rnd
import numpy as np
from PIL import Image, ImageFilter,ImageOps
from data.process import computer_text_generator, background_generator, distorsion_generator
import cv2

def contrast_demo(img1, c, b):
    rows, cols = img1.shape
    # print(img1.shape)
    blank = np.zeros([rows, cols], img1.dtype)
    dst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return dst


def gaussian_noise(img, mean, sigma):
    # print(img.size)
    img = img / 255
    noise = np.random.normal(mean, sigma, img.shape)
    gaussian_out = img + noise
    gaussian_out = np.clip(gaussian_out, 0, 1)
    gaussian_out = np.uint8(gaussian_out*255)

    return gaussian_out

import base64
try:
    from data.process import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """
        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        blur_if,
        contrast_if,
        reverse_if,
        noise_if,
        background_type,
        bk_img,
        distorsion,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        fit,
        output_mask,
        # meat_if
    ):

        image = None
        if rnd.random() < 0.2:
            margins = (0,0,0,0)#(random.choice(range(10)), random.choice(range(10)), random.choice(range(10)), random.choice(range(10)))
        else:
            margins = (rnd.choice(range(10)), rnd.choice(range(10)), rnd.choice(range(10)), rnd.choice(range(10)))

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom
        
        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image, mask = handwritten_text_generator.generate(text, text_color)
        else:
                # print(size)
                size = rnd.choice(range(size[0], size[1]))
                image, mask = computer_text_generator.generate(
                    text,
                    font,
                    text_color,
                    size,
                    orientation,
                    space_width,
                    character_spacing,
                    fit,
                )
                
        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)
        
        rotated_img = image.rotate(
        skewing_angle if not random_skew else random_angle, expand=1
        )
        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion and rotated_img.size[0]>200:
            distorsion_type = rnd.choice([0,1,2,3])
            # print(distorsion_type)
            if distorsion_type == 0:
                distorted_img = rotated_img  # Mind = blown
                distorted_mask = rotated_mask
            elif distorsion_type == 1:
                distorted_img, distorted_mask = distorsion_generator.sin(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            elif distorsion_type == 2:
                distorted_img, distorted_mask = distorsion_generator.cos(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            else:
                distorted_img, distorted_mask = distorsion_generator.random(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
        else:
            distorted_img = rotated_img  
            distorted_mask = rotated_mask
   
        ##################################
        # Resize image to desired format #
        ##################################
        # Horizontal text
        if orientation == 0:
            new_width = int(
                distorted_img.size[0]
                * (float(size - vertical_margin) / float(distorted_img.size[1]))
            )
            resized_img = distorted_img.resize(
                (new_width, size - vertical_margin), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize((new_width, size - vertical_margin))
            # print(horizontal_margin)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
            
        # Vertical text
        elif orientation == 1:
            new_height = int(
                float(distorted_img.size[1])
                * (float(size - horizontal_margin) / float(distorted_img.size[0]))
            )
            resized_img = distorted_img.resize(
                (size - horizontal_margin, new_height), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize(
                (size - horizontal_margin, new_height), Image.ANTIALIAS
            )
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        # background=rnd.choice([0,1,3])
        if bk_img!='':
            background_type=3
            bk_path=bk_img
        else:
            background_type = rnd.choice([0,1,3])
            bk_path='/data/git/ocr-platform/data/seuic_dl'+'/recognize/data/bk_picture/pictures/'
        if background_type == 0 and background_width>200:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.picture(
                background_height, background_width,bk_path
            )
        background_mask = Image.new("RGB", (background_width, background_height), (0, 0, 0))

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if alignment == 0 or width == -1:
            background_img.paste(resized_img, (margin_left, margin_top), resized_img)
            background_mask.paste(resized_mask, (margin_left, margin_top))
        elif alignment == 1:
            background_img.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (int(background_width / 2 - new_text_width / 2), margin_top),
            )
        elif alignment == 2:
            background_img.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (int(background_width / 2 - new_text_width / 2), margin_top),
            )
        else:
            background_img.paste(
                resized_img,
                (background_width - new_text_width - margin_right, margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (background_width - new_text_width - margin_right, margin_top),
            )

        ##################################
        # Apply contrast #
        ##################################
        if contrast_if and new_text_width>200:
            random_contrast=rnd.choice([True,False])
            if random_contrast:
                # print('######   1    #######')
                background_img=background_img.convert('L')
                background_img=np.array(background_img)
                # background_img = background_img[:]
                background_img = contrast_demo(background_img,c=1.6,b=3)
                # print('######   2    #######')
                # cv2.imwrite('background_img.jpg',background_img)
                background_img=Image.fromarray(background_img)
                # print('######   3    #######')
                background_mask=background_mask.convert('L')
                background_mask=np.array(background_mask)
                # background_mask = background_mask[:]
                background_mask = contrast_demo(background_mask,c=1.6,b=3)
                background_mask=Image.fromarray(background_mask)

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion:
            noise_if=False
        if noise_if and new_text_width>200:
            noise_rnd=rnd.choice([0,1])
            if noise_rnd==0:
                # background_img_=background_img.convert('RGB')
                # background_img_.save('image_before.jpg')
                background_img=background_img.convert('L')
                background_mask=background_mask.convert('L')
                background_img = np.array(background_img) 
                background_mask = np.array(background_mask) 
                background_img=gaussian_noise(background_img, 0, 0.001*background_img.shape[0]/2)
                background_mask=gaussian_noise(background_mask, 0, 0.001*background_mask.shape[0]/2)
                # cv2.imwrite('image.jpg',background_img)
                background_img=Image.fromarray(background_img)
                background_mask=Image.fromarray(background_mask)
                
        ##################################
        # Apply gaussian blur #
        ##################################
        if blur_if and new_text_width>200:
            random_blur=rnd.choice([True,False])
            gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        else:
            gaussian_filter = ImageFilter.GaussianBlur(
                radius=0
            )

        final_image = background_img.filter(gaussian_filter)
        final_mask = background_mask.filter(gaussian_filter)

        ##################################
        # Apply reverse #
        ##################################
        if reverse_if:
            random_reverse=rnd.choice([True,False,False,False,False])
            if random_reverse:
                final_image=final_image.convert('L')
                final_image = ImageOps.invert(final_image)
                final_mask=final_mask.convert('L')
                final_mask = ImageOps.invert(final_mask)
                
        #####################################
        # Generate name for resulting image #
        #####################################
        text = base64.b64encode(bytes(text, 'utf-8'))
        text = text.decode()
        text = text.replace('+', '-').replace('/', '_').replace('=', '')
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
            mask_name = "{}_{}_mask.png".format(str(index), text)
        elif name_format == 2:
            image_name = "{}.{}".format(str(index), extension)
            mask_name = "{}_mask.png".format(str(index))
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
        # dict = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        # val = image_name.split('_')[0]
        # index = dict.index(val) + 1
        # if index == 25 or index == 39 or index == 51 or index == 52 or index == 55 or index == 59 or index == 62:
        #     return
        # Save the image
        if out_dir is not None:
            final_image.convert("RGB").save(os.path.join(out_dir,  image_name))
            if output_mask == 1:
                final_mask.convert("RGB").save(os.path.join(out_dir, mask_name))
        else:
            if output_mask == 1:
                return final_image.convert("RGB"), final_mask.convert("RGB")
            return final_image.convert("RGB")


        
