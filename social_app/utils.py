import os
from django.conf import settings

def get_file_preview(file_path):

    try:
        abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if file_path.endswith('.pdf'):
            import PyPDF2
            with open(abs_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                first_page = reader.pages[0].extract_text() if len(reader.pages) > 0 else "No content"
                return first_page[:200] + "..."

        elif file_path.endswith('.docx'):
            from docx import Document
            doc = Document(abs_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text[:200] + "..."

        elif file_path.endswith(('.txt', '.csv')):
            with open(abs_path, 'r', encoding='utf-8') as text_file:
                text = text_file.read()
                return text[:200] + "..."

        else:
            return "Preview not available for this file type."
    except Exception as e:
        print(f"Error reading file: {e}")
        return "Unable to generate preview."