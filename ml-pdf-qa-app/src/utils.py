def validate_pdf_file(file_path):
    if not file_path.endswith('.pdf'):
        raise ValueError("File must be a PDF.")
    return True

def preprocess_text(text):
    """Advanced text preprocessing for better QA accuracy"""
    import re
    
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    # Normalize punctuation
    text = re.sub(r'([.!?])\s+', r'\1 ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def save_uploaded_file(uploaded_file, destination):
    with open(destination, 'wb') as f:
        f.write(uploaded_file.read())
    return destination

def highlight_answer_in_context(answer, context):
    """Find and highlight where the answer appears in the context"""
    import re
    
    # Create a regex pattern for flexible matching
    pattern = re.escape(answer)
    matches = re.finditer(pattern, context, re.IGNORECASE)
    
    return list(matches)
