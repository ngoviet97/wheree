from PIL import Image
import pytesseract

# Path to the Tesseract executable (update with your path)
# Use the command on terminal to find the path (only works for mac): which tesseract
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# Path to the image file
image_path = '~/path/file.jpg'

# Open the image file
img = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the extracted text
print("Extracted Text:")
print(text)
