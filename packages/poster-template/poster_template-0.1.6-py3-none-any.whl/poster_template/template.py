from PIL import Image
from .coordiante import paste_logo,paste_product
from image_utils import resize_image


def generate_template(product:Image.Image,logo:Image.Image,title:str,subtitle:str,cta_text:str)->Image.Image:
    base_image=Image.new(mode='RGB',size=(1024,1024),color=(0,0,0))
    base_image,logo_postion=paste_logo(base_image=base_image,logo=logo)
    base_image,product_postion,product_size,text_align=paste_product(base_image=base_image,product=product,title=title,subtitle=subtitle,cta_text=cta_text)
    
    return base_image,{'logo_postion':logo_postion,'product_postion':product_postion,'product_size':product_size,'text_align':text_align}


def regenerate_template_new(base_image,product,logo,logo_postion,product_size,product_postion,product_align):
    base_image=base_image.resize((1024,1024))
    logo=resize_image(logo,new_height=int(base_image.size[1]*0.10))
    product=product.resize(product_size)
    base_image.paste(logo, logo_postion, logo)
    base_image.paste(product,product_postion,product)
    return base_image
