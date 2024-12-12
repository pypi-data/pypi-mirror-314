from PIL import Image
import random
from .image_utils import resize_image,paste_title_subtitle_button


def paste_logo(base_image, logo):
    # Randomly choose whether to align the logo to the left or right
    align = random.choice(['left', 'right'])

    # Get base image size
    base_width, base_height = base_image.size
    
    logo=resize_image(logo,new_height=int(base_image.size[1]*0.10))
    # Get logo size
    logo_width, logo_height = logo.size

    if align == 'left':
        # Paste logo at the top-left corner (10px padding)
        base_image.paste(logo, (10, 10), logo)
        logo_postion=(10, 10)
    else:
        # Paste logo at the top-right corner (10px padding from the right)
        right_x = base_width - logo_width - 10
        base_image.paste(logo, (right_x, 10), logo)
        logo_postion=(right_x, 10)

    return base_image,logo_postion

def paste_product(base_image,product,title,subtitle,cta_text):
    align = random.choice(['left', 'right'])
    product=resize_image(product,new_width=random.choice(range(int(base_image.size[0]*.3),int(base_image.size[0]*.48))))
    product_size=product.size
    if align=='left':
        x=random.choice(range(10,int(base_image.size[0]*.5)-product.size[0]))
        y=random.choice(range(int(base_image.size[0]*.12),int(base_image.size[1]*.78)-product.size[1]))
        base_image.paste(product,(x,y),product)
        x_right=int(base_image.size[0]*.50)
        y_right=int(base_image.size[0]*.12)
        width=int(base_image.size[0]*.50)
        hight=int(base_image.size[0]*.7)
        product_postion=(x,y)
        base_image,text_align=paste_title_subtitle_button(base_image=base_image,bbox=[x_right,y_right,width,hight],title=title,subtitle=subtitle,button_text=cta_text,self_align=align)
    else:
        x=random.choice(range(int(base_image.size[0]*.5)+10,int(base_image.size[0])-product.size[0]))
        y=random.choice(range(int(base_image.size[0]*.12),int(base_image.size[1]*.78)-product.size[1]))
        base_image.paste(product,(x,y),product)
        x_right=10
        y_right=int(base_image.size[0]*.12)
        width=int(base_image.size[0]*.50)
        hight=int(base_image.size[0]*.7)
        product_postion=(x,y)
        base_image,text_align=paste_title_subtitle_button(base_image=base_image,bbox=[x_right,y_right,width,hight],title=title,subtitle=subtitle,button_text=cta_text,self_align=align)
    return base_image,product_postion,product_size,text_align