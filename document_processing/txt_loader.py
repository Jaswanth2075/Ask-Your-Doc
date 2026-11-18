from document_processing.text_cleaner import clean_text
def extract_txt(file):
    return clean_text(file.read().decode("utf-8"))