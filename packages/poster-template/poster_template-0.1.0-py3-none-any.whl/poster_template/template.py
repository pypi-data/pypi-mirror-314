from PIL import Image
from .coordiante import paste_logo,paste_product

def generate_template(product:Image.Image,logo:Image.Image,title:str,subtitle:str,cta_text:str)->Image.Image:
    base_image=Image.new(mode='RGB',size=(1024,1024),color=(0,0,0))
    base_image=paste_logo(base_image=base_image,logo=logo)
    base_image=paste_product(base_image=base_image,product=product,title=title,subtitle=subtitle,cta_text=cta_text)
    return base_image
