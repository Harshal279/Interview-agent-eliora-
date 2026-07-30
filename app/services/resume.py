import pypdf 

reader = pypdf.PdfReader("resume.pdf")

for page in reader.pages:
    print(page.extract_text())