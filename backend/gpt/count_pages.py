import PyPDF2

def main():
    pdf_path = r"C:\Users\16196\Desktop\ai-cheat-sheet-builder-v2\backend\gpt\pdf\output.pdf"
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        page_count = len(reader.pages)
    print(f"The PDF has {page_count} pages.")

if __name__ == "__main__":
    main()