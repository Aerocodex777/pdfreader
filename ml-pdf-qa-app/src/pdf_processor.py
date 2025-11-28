class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        from PyPDF2 import PdfReader
        import re

        text = ""
        try:
            with open(self.file_path, "rb") as file:
                reader = PdfReader(file)
                
                # Extract text from all pages
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                # Clean up the text
                text = self._clean_text(text)
                
        except Exception as e:
            print(f"Error reading PDF file: {e}")
        
        return text.strip()

    def _clean_text(self, text):
        """Clean and normalize extracted text"""
        # Remove excessive whitespace while preserving paragraph structure
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Remove excessive newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Remove extra spaces and tabs
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Preserve some structure by keeping line breaks for readability
        text = text.replace('. ', '.\n')  # Add newlines after sentences
        
        return text
