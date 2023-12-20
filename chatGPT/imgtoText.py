from PIL import Image
import pytesseract

# Path to the Tesseract executable (update with your path)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# Path to the image file
image_path = '/Users/MAC/Downloads/2023-03-05.jpg'

# Open the image file
img = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the extracted text
print("Extracted Text:")
print(text)
