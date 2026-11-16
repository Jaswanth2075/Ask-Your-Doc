import fitz

def extracted_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")

    text = ""
    for page in document :
        text += page.get_text()

    return text