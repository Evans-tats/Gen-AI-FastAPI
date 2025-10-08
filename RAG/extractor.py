from pypdf import PdfReader
def pdf_text_extractor(filepath :str) -> None:
    content = ""
    pdf_reader = pdf_reader(filepath)
    for page in pdf_reader:
        page_text = page.extract_text()
        if page_text:
            content += f"{page_text}\n\n"
    
    with open(filepath.replace("pdf", "txt"), "w", encoding="utf-8") as f:
        f.write(content)