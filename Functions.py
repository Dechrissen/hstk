import pytesseract
from PIL import Image, ImageOps, ImageEnhance


def tweakImage(image_file):
    """
    Crops (removes top and bottom portions) and inverts contrast (into black
    text on white background) for a raw headline snap image.

    args
        image_file : the path to an image file

    returns
        cropped_image : a PIL Image object
    """

    image = Image.open(image_file)

    # remove the 'A' channel if the image has one
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        image = Image.merge('RGB', (r,g,b))

    # invert the contrast
    image = ImageOps.invert(image)
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(2)

    # get the dimensions of the image
    width, height = image.size

    # set the amount of top & bottom to trim off (20% here)
    trim = .2 * height

    # crop the image
    crop_region = (0, trim, width, (height - trim))
    cropped_image = image.crop(crop_region)

    # show the image for testing purposes
    #cropped_image.show()

    return cropped_image

def imageToText(tweaked_image):
    """
    Converts a tweaked headline snap image into text.

    args
        tweaked_image : a cropped and contrast-inverted headline snap

    returns
        cleaned_text : the headline snap as a string
    """

    # Windows only: set the location of the tesseract executable
    # this also needs to be present in your PATH (both Windows and Linux)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # set the config for the conversion (not sure what this does)
    config = ("--psm 6")

    # OCR
    text = pytesseract.image_to_string(tweaked_image, config=config, lang='eng')

    # clean the raw text from the OCR
    cleaned_text = text.replace('\n', ' ')

    return cleaned_text
