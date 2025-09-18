import numpy as np
from PIL import Image
import cv2
import os
import google.generativeai as genai

def extract_image(image_file):
    """
    Extract text from an uploaded image using Google Generative AI OCR
    """
    # Load image from uploaded file
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        return "Cannot read image. Please upload a valid image."

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale and threshold
    img_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image_btw = cv2.threshold(img_grey, 150, 255, cv2.THRESH_BINARY)

    # Convert to PIL Image
    final_image = Image.fromarray(image_btw)

    # Configure Google Generative AI
    key = os.getenv('GOOGLE_API_KEY')
    if not key:
        return "Google API key not found."
    genai.configure(api_key=key)

    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    prompt = '''You need to perform OCR as given image and extract the text from it.
    Give only the text as output, do not give any other explanation or description.'''

    # Extract text
    try:
        response = model.generate_content([prompt, final_image])
        output_text = response.text
        return output_text
    except Exception as e:
        return f"Error extracting text from image: {e}"
