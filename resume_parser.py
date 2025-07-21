import docx2txt
from pdfminer.high_level import extract_text
import tempfile

def extract_resume_text(uploaded_file):
    try:
        if uploaded_file.name.endswith('.pdf'):
            return extract_text(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            # Save .docx temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            return docx2txt.process(tmp_path)
        else:
            return "❌ Unsupported file format"
    except Exception as e:
        return f"❌ Error: {e}"
