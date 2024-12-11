from PIL import Image
import numpy as np

def create_mask(image):
    # Open the image using PIL
    
    # Convert the image to grayscale
    gray_image = image.convert("L")  # "L" mode for grayscale
    
    # Convert the grayscale image to a numpy array
    gray_array = np.array(gray_image)
    
    # Create a binary mask: pixels with value > 0 will be 255 (white), others 0 (black)
    mask_array = np.where(gray_array > 0, 255, 0).astype(np.uint8)
    
    # Convert the numpy array back to a PIL image
    mask = Image.fromarray(mask_array)
    
    return mask
