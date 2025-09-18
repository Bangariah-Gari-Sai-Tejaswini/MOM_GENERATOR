from pypdf import PdfReader

def text_extractor(file):
    file.seek(0)  # Reset file pointer
    try:
        pdf = PdfReader(file, strict=False)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text if text else "No text found in PDF"
    except Exception as e:
        return f"Error reading PDF: {e}"
    
    