from PIL import Image
import re
import pytesseract


threshold = 128

def convert_to_black_and_white(image):

    grayscale_image = image.convert("L")

    # 將灰階像素值轉換為只有黑色和白色的像素值
    black_and_white_image = grayscale_image.point(lambda x: 0 if x < threshold else 255, "1")

    # 回傳轉換後的圖像
    return black_and_white_image

def menu_img(img):
    # img = Image.open(img_path)
    img = convert_to_black_and_white(img)

    #偵測圖片中的中文字
    text = pytesseract.image_to_string(img, lang='chi_tra')

    #去除奇怪的字元
    dish_list = re.sub(r'[^\w\s]|[0-9]|[\n\t\b]', '', text)
    # print(text)
    return dish_list
