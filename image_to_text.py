"""Extracting Text from the image wihtin the first page of PDF file"""

from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from io import BytesIO

Image.MAX_IMAGE_PIXELS = None   # To work with large image files

pytesseract.pytesseract.tesseract_cmd = r'PATH_TO_TESSERACT_EXECUTABLE'

with open('PATH_TO_PDF_FILE_Containing_Image', 'rb') as f:
    pdf = PdfReader(f)
    page = pdf.pages[0]
    xObject = page['/Resources']['/XObject'].get_object()
    image_data = None

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            image_data = xObject[obj]._data
            break

if image_data:
    image = Image.open(BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    print(text)
else:
    print("No image found on the first page.")

