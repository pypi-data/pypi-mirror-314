from PIL import Image
import random
import platform

def resize_image(pil_image, new_width=None, new_height=None):
    # Get original width and height
    width, height = pil_image.size
    
    # Calculate the aspect ratio (width / height)
    aspect_ratio = width / height
    
    # If only width is specified, calculate the height
    if new_width:
        new_height = int(new_width / aspect_ratio)
    
    # If only height is specified, calculate the width
    elif new_height:
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image while maintaining the aspect ratio
    img_resized = pil_image.resize((new_width, new_height), Image.LANCZOS)
    
    # Return the resized image (PIL Image object)
    return img_resized

from PIL import Image, ImageDraw, ImageFont
import os

def get_max_font_size(draw, text, font_path, max_width, max_height, initial_font_size=36):
    """
    Get the maximum font size that allows the text to fit within the specified width and height.
    
    :param draw: ImageDraw object.
    :param text: The text string.
    :param font_path: Path to the .ttf font file.
    :param max_width: Maximum allowed width for the text.
    :param max_height: Maximum allowed height for the text.
    :param initial_font_size: Starting font size.
    
    :return: The best font size for the text to fit within the area.
    """
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    width = right - left
    height = bottom - top
    
    # Reduce font size until text fits within max_width and max_height
    while width > max_width or height > max_height:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        width = right - left
        height = bottom - top
        
        if font_size <= 5:  # Set a lower limit for font size
            break
    
    return font_size+15


def wrap_text(draw, text, font, max_width):
    """
    Wrap the text to fit within the specified width.
    
    :param draw: ImageDraw object.
    :param text: The text string.
    :param font: ImageFont object.
    :param max_width: Maximum allowed width for the text.
    
    :return: A list of wrapped lines of text.
    """
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
        width = right - left
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines
import os
import platform

import os
import platform

def is_english_font(font_name):
    """
    Heuristic check to determine if a font is likely an English font.
    This can be expanded to check for specific known English font names.
    """
    english_keywords = ['arial', 'times', 'tahoma', 'verdana', 'courier', 'georgia', 'calibri', 'segoe', 'helvetica']
    return any(keyword in font_name.lower() for keyword in english_keywords)

def get_default_font():
    system = platform.system().lower()

    if system == 'darwin':  # macOS
        # Check common system font directories
        font_dirs = [
            '/System/Library/Fonts',  # System fonts directory
            '/Library/Fonts',         # User fonts directory
            '/Network/Library/Fonts', # Network fonts directory (rare but possible)
        ]
        for font_dir in font_dirs:
            if os.path.isdir(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.lower().endswith('.ttf') or file.lower().endswith('.otf'):
                            if is_english_font(file):
                                return os.path.join(root, file)
        return None  # If no English font is found

    elif system == 'linux':  # Linux
        # Check common system font directories
        font_dirs = [
            '/usr/share/fonts',          # System fonts directory
            '/usr/local/share/fonts',    # Local fonts directory
        ]
        for font_dir in font_dirs:
            if os.path.isdir(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.lower().endswith('.ttf') or file.lower().endswith('.otf'):
                            if is_english_font(file):
                                return os.path.join(root, file)
        return None  # If no English font is found

    elif system == 'windows':  # Windows
        # Check the default fonts directory
        font_dir = 'C:/Windows/Fonts'
        if os.path.isdir(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith('.ttf') or file.lower().endswith('.otf'):
                        if is_english_font(file):
                            return os.path.join(root, file)
        return None  # If no English font is found

    else:
        return None  # Unsupported OS


def random_alignment(text_width, max_width,alignment):
    """
    Return a random alignment for the text.
    The possible alignments are: 'left', 'center', 'right'.
    The x-coordinate will be adjusted based on the selected alignment.
    
    :param text_width: Width of the text.
    :param max_width: Maximum width available for the text.
    
    :return: The x-coordinate for the text based on the selected alignment.
    """
    
    if alignment == 'left':
        return 0  # Left alignment
    elif alignment == 'center':
        return (max_width - text_width) // 2  # Center alignment
    elif alignment == 'right':
        return max_width - text_width  # Right alignment

def paste_title_subtitle_button(base_image: Image, bbox: tuple, title: str, subtitle: str, button_text: str, self_align):
    font_path: str = get_default_font()
    """
    Paste a title, subtitle, and action button inside a given bounding box on the base image,
    with specific area allocations:
    - 40% for the title at the top
    - 40% for the subtitle in the middle
    - 20% width for the action button on the left side
    Each text element will have its font size dynamically adjusted based on the available area.
    
    :param base_image: The base image (PIL Image).
    :param bbox: A tuple (x, y, w, h) representing the top-left corner and width/height of the bounding box.
    :param title: The title text to display.
    :param subtitle: The subtitle text to display.
    :param button_text: The text on the action button.
    :param font_path: Path to the .ttf font file (default is "arial.ttf").
    
    :return: The modified PIL Image with the title, subtitle, and button pasted inside the bounding box.
    """
    x, y, w, h = bbox
    draw = ImageDraw.Draw(base_image)

    # Check if the font file exists, and if not, use a fallback default font
    if not os.path.exists(font_path):
        print(f"Font file '{font_path}' not found. Using default font.")
        title_font_size = 20
        subtitle_font_size = 16
        button_font = ImageFont.load_default()
    else:
        try:
            # Dynamically determine font size based on box size
            title_font_size = get_max_font_size(draw, title, font_path, w, h * 0.4, 36)
            subtitle_font_size = get_max_font_size(draw, subtitle, font_path, w, h * 0.4, 24)
            button_font = ImageFont.truetype(font_path, 20)
        except IOError:
            print(f"Error loading font from {font_path}. Falling back to default font.")
            title_font_size = 20
            subtitle_font_size = 16
            button_font = ImageFont.load_default()

    # Load the fonts with the dynamically calculated sizes
    title_font = ImageFont.truetype(font_path, title_font_size)
    subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)

    # Calculate the boundaries for title, subtitle, and button
    title_height = h * 0.4  # 40% height for title
    subtitle_height = h * 0.4  # 40% height for subtitle
    button_width = w * 0.2  # 20% width for button
    button_height = 40  # Fixed height for action button

    # Define the vertical areas
    title_area_bottom = y + title_height  # Bottom of the title area
    subtitle_area_bottom = title_area_bottom + subtitle_height  # Bottom of the subtitle area
    button_area_bottom = subtitle_area_bottom + button_height  # Bottom of the button area

    # Ensure no overflow and adjust button if needed
    if button_area_bottom > y + h:
        button_area_bottom = y + h  # Prevent button from going out of bounds

    # Title: place text in the top 40% area
    title_x = x + 10  # Padding for title
    title_y = y + 10  # Padding for title
    title_lines = wrap_text(draw, title, title_font, w - 20)
    
        
    current_y = title_y
    if self_align=='left':
        alignment = random.choice(['right', 'center'])
    else:
        alignment = random.choice(['left', 'center'])
    for line in title_lines:
        # Calculate text width
        left, top, right, bottom = draw.textbbox((title_x, current_y), line, font=title_font)
        text_width = right - left
        
        # Randomly align the title
        title_x = x + random_alignment(text_width, w - 20,alignment=alignment)
        
        draw.text((title_x, current_y), line, font=title_font, fill="white")
        current_y += bottom - top + 5  # Adjust line spacing
    
    # Subtitle: place text in the middle 40% area
    subtitle_x = x + 10  # Padding for subtitle
    subtitle_y = title_area_bottom + 10  # Just below the title area
    subtitle_lines = wrap_text(draw, subtitle, subtitle_font, w - 20)
    
    current_y = subtitle_y
    for line in subtitle_lines:
        # Calculate text width
        left, top, right, bottom = draw.textbbox((subtitle_x, current_y), line, font=subtitle_font)
        text_width = right - left
        
        # Randomly align the subtitle
        subtitle_x = x + random_alignment(text_width, w - 20,alignment=alignment)
        
        draw.text((subtitle_x, current_y), line, font=subtitle_font, fill="gray")
        current_y += bottom - top + 5  # Adjust line spacing
    
    # Button: place text inside a 20% width box on the left side
    button_y = subtitle_area_bottom + (subtitle_height - button_height) // 2  # Center vertically in remaining area
    
    # Ensure button fits within the vertical space
    if button_y + button_height > y + h:
        button_y = y + h - button_height  # Adjust button to fit within bottom of the bounding box
    
    # Randomly align the button within the 20% width
    
    button_x = x + random_alignment(button_width, w - 20,alignment=alignment)
    
    # Draw the button (rectangle)
    draw.rectangle([button_x, button_y, button_x + button_width, button_y + button_height], fill="blue")
    
    # Button text: centered inside the button
    left, top, right, bottom = draw.textbbox((button_x, button_y), button_text, font=button_font)
    button_text_width = right - left
    button_text_height = bottom - top
    button_text_x = button_x + (button_width - button_text_width) // 2  # Center text horizontally
    button_text_y = button_y + (button_height - button_text_height) // 2  # Center text vertically
    
    draw.text((button_text_x, button_text_y), button_text, font=button_font, fill="white")

    return base_image,alignment


