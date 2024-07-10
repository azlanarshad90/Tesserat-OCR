"""Extracting Text from the image wihtin the first page of PDF file"""

from PIL import Image
import pytesseract
from io import BytesIO
import fitz

Image.MAX_IMAGE_PIXELS = None   # To work with large image files

pytesseract.pytesseract.tesseract_cmd = r'PATH_TO_TESSERACT_EXECUTABLE'

def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    
    pdf_document = fitz.open(pdf_path)
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        
        image_list = page.get_images(full=True)
        
        for image_index, img_dict in enumerate(image_list):
            xref = img_dict[0]
            base_image = pdf_document.extract_image(xref)
            
            if base_image["colorspace"] == 1:
                image_bytes = base_image["image"]
                try:
                    pil_image = Image.open(BytesIO(image_bytes))
                    text = pytesseract.image_to_string(pil_image)
                    extracted_text += text + "\n"
                except pytesseract.TesseractError as e:
                    print(f"Tesseract OCR error on page {page_number + 1}, image {image_index + 1}: {e}")
                except Exception as e:
                    print(f"Error processing page {page_number + 1}, image {image_index + 1}: {e}")
    
    pdf_document.close()
    return extracted_text


pdf_path = 'PATH_TO_PDF_FILE_Containing_Images'
final_text = extract_text_from_pdf(pdf_path)

print("Extracted text:\n", final_text)
