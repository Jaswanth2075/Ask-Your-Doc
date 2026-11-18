from document_processing.excel_loader import extract_excel
from document_processing.pdf_loader import extracted_pdf
from document_processing.text_cleaner import clean_text
from document_processing.txt_loader import extract_txt

def extracted_doc(file):

    extension = file.name.split(".")[-1].lower()

    if extension == "pdf":
        return extracted_pdf(file)

    elif extension == "txt":
        return extract_txt(file)

    elif extension in ["xlsx","xls"]:
        return extract_excel(file)

    else:
        return ValueError("Unsupported File Type")

    