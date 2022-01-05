import random as rnd
import cv2
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

def generate(
    text, font, text_color, font_size, orientation, space_width, character_spacing, fit
):  
    # print('text, font, text_color, font_size, orientation, space_width, character_spacing, fit:',text, font, text_color, font_size, orientation, space_width, character_spacing, fit)
    if orientation == 0:
        return _generate_horizontal_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(
    text, font, text_color, font_size, space_width, character_spacing, fit
):
    image_font = ImageFont.truetype(font=font, size=font_size)
    space_width = int(image_font.getsize(" ")[0] * space_width)
    
    char_widths = [image_font.getsize(c)[0] if c != " " else space_width for c in text]
    

    AR_ttf=font.split("/")[-1]
    if AR_ttf=='AR_0123456.ttf':
        AR_add=6
    else:
        AR_add=0
    text_width = sum(char_widths) + character_spacing * (len(text) - 1)
    text_height = max([image_font.getsize(c)[1] for c in text])+AR_add
    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask, mode="RGB")
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]

    ##############################################################
    # c1, c2 = colors[0], colors[-1]
    # fill = (
    #     rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
    #     rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
    #     rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    # )
    #####################color choice###########################
    fill=rnd.choice(colors)
    # print(font)
   
    for i, c in enumerate(text):
            txt_img_draw.text(
                (int(sum(char_widths[0:i])*0.9) + i * character_spacing, 0+AR_add),
                c,
                fill=fill,
                font=image_font,
            )
            txt_mask_draw.text(
                (int(sum(char_widths[0:i])*0.9) + i * character_spacing, 0+AR_add),
                c,
                fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
                font=image_font,
            )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


def _generate_vertical_text(
    text, font, text_color, font_size, space_width, character_spacing, fit
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    for i, c in enumerate(text):
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=(i // (255 * 255), i // 255, i % 255),
            font=image_font,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


if __name__=="__main__":
    text='净重22.456kg'
    font='/data/git/ocr-platform/TextRecognitionDataGenerator-master/trdg/fonts/cn/SIMFANG.ttf'
    text_color='#7A7A7A,#D1C7BE'
    font_size=60
    orientation=0
    space_width=1.0
    character_spacing=6
    fit=True

    image, mask = generate(
    text, font, text_color, font_size, orientation, space_width, character_spacing, fit)
    image = image.convert("RGB")
    image.save('image.jpg')
    # mask = mask.convert("RGB")
    # mask.save('mask.jpg')
    