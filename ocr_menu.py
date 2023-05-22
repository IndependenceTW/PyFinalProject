from PIL import Image
import re
import pytesseract


def menu_img(img):
    # img = Image.open(img_path)
    img = img.convert('L')
    text = pytesseract.image_to_string(img, lang='chi_tra')
    dish_list = re.sub(r'[^\w\s]|[0-9]|[\n\t\b]', '', text)
    # print(text)
    return dish_list
