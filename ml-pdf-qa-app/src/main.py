from flask import Flask, request, jsonify, render_template
from pdf_processor import PDFProcessor
from advanced_qa_model import AdvancedQAModel
from config import Config
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

# Store the extracted text globally (for demo purposes)
extracted_text = ""

# Initialize Advanced QA model
print("Loading Advanced QA model with semantic search...")
qa_model = AdvancedQAModel(Config.MODEL_PATH)
model_loaded = qa_model.load_model()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global extracted_text
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File is not a PDF'}), 400
    
    try:
        # Save the uploaded PDF file
        upload_folder = Config.PDF_UPLOAD_FOLDER
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        
        # Extract text from the PDF
        pdf_processor = PDFProcessor(file_path)
        extracted_text = pdf_processor.extract_text()
        
        if not extracted_text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Index the document for semantic search
        indexing_success = qa_model.index_document(extracted_text)
        
        if not indexing_success:
            return jsonify({'error': 'Could not process PDF for Q&A'}), 400
        
        return jsonify({
            'message': 'File uploaded and indexed successfully!',
            'filename': file.filename,
            'text_length': len(extracted_text),
            'chunks': len(qa_model.document_chunks),
            'preview': extracted_text[:200] + '...'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global extracted_text
    
    if not model_loaded:
        return jsonify({'error': 'Model is still loading. Please try again in a moment.'}), 503
    
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not extracted_text:
            return jsonify({'error': 'No PDF uploaded. Please upload a PDF first'}), 400
        
        # Log for debugging
        print(f"\n� Question: {question}")
        print(f"📄 PDF has {len(qa_model.document_chunks)} chunks indexed")
        
        # Generate answer using the advanced QA model
        answer = qa_model.answer_question(question, extracted_text)
        
        print(f"✅ Answer generated\n")
        
        return jsonify({'question': question, 'answer': answer}), 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': f'Failed to answer question: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)