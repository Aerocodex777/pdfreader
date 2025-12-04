# PDFReader - AI-Powered PDF Question Answering 📄💬

An intelligent document analysis system that lets you upload PDF files and ask natural language questions to get accurate answers extracted from your documents. Perfect for researchers, students, and professionals who need to quickly understand large documents.

## 🌟 Features

- **📤 Easy PDF Upload** - Drag-and-drop interface for hassle-free document uploads
- **🔍 Semantic Search** - AI understands your questions and finds relevant content
- **💡 Smart Chunking** - Intelligently splits documents into meaningful sections
- **🧠 RAG Architecture** - Retrieves relevant passages before generating answers
- **📊 Confidence Scores** - Transparent confidence metrics for each answer
- **🎨 Modern UI** - Beautiful, responsive interface for all devices
- **⚡ Fast Processing** - Quick inference and response generation
- **🔒 Privacy First** - All processing happens locally, your data stays private

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python web framework)
- **NLP Models**: 
  - Sentence Transformers (semantic similarity)
  - DistilBERT (question answering)
  - BERT-based extractive QA
- **PDF Processing**: PyPDF2, PyMuPDF
- **Vector Storage**: In-memory vectors (extensible to Pinecone/Weaviate)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive features and real-time updates
- **Fetch API**: Async communication with backend

### ML & Data
- **Transformers**: Hugging Face transformers library
- **Sentence Embeddings**: Sentence-BERT for semantic search
- **Vector Operations**: NumPy for efficient computation

## 📁 Project Structure

```
pdfreader/
└── ml-pdf-qa-app/
    ├── app.py                 # Main Flask application
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Environment variables (API keys)
    ├── .gitignore            # Git ignore rules
    ├── create_sample_pdf.py   # Script to generate test PDFs
    ├── sample.pdf            # Example PDF for testing
    ├── models/               # Pre-trained model files
    ├── src/                  # Source code modules
    │   ├── pdf_processor.py  # PDF extraction and chunking
    │   ├── embedder.py       # Semantic embedding generation
    │   └── qa_engine.py      # Question answering logic
    ├── uploads/              # User-uploaded PDF storage
    └── README.md             # Detailed project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aerocodex777/pdfreader.git
   cd pdfreader/ml-pdf-qa-app
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download ML models** (first run will auto-download)
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:5000`

## 💡 How It Works

### Architecture Overview

```
User Input (Question)
        ↓
    [Flask API]
        ↓
[PDF Embeddings Database]
        ↓
[Semantic Search] → Find relevant chunks
        ↓
[Context Assembly] → Build relevant passages
        ↓
[QA Model] → Generate answer
        ↓
    Response with confidence score
```

### Processing Pipeline

1. **PDF Upload & Processing**
   - Extract text from PDF
   - Split into overlapping chunks (256 tokens with 50% overlap)
   - Store chunk text and metadata

2. **Semantic Embedding**
   - Generate embeddings for all chunks using Sentence Transformers
   - Store embeddings for similarity search

3. **Question Processing**
   - Embed user's question
   - Calculate similarity with all chunk embeddings
   - Retrieve top-K most relevant chunks

4. **Answer Generation**
   - Concatenate relevant chunks as context
   - Pass to DistilBERT QA model
   - Extract answer span with confidence score

5. **Response Delivery**
   - Return answer with source chunks
   - Show confidence metrics
   - Include chunk references for verification

## 📊 API Endpoints

### GET `/`
Returns the main web interface.

### POST `/upload`
Upload and process a PDF file.

**Request:**
```
Content-Type: multipart/form-data
File: <PDF file>
```

**Response:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "chunks": 45,
  "message": "PDF processed successfully"
}
```

### POST `/ask`
Ask a question about the uploaded PDF.

**Request:**
```json
{
  "question": "What is the main topic?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "The main topic is...",
  "confidence": 0.92,
  "source_chunks": ["Chunk 1...", "Chunk 2..."],
  "processing_time": 0.34
}
```

### POST `/reset`
Clear current PDF and start fresh.

## 🎯 Use Cases

- **Research Papers**: Quickly find specific information in academic papers
- **Legal Documents**: Extract relevant clauses and information from contracts
- **Technical Manuals**: Get specific answers from product documentation
- **Reports**: Analyze business or scientific reports efficiently
- **Learning**: Enhanced study tool for textbooks and educational materials

## ⚙️ Configuration

Edit `app.py` or create `.env` file:

```
CHUNK_SIZE=256
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=5
MODEL_NAME=all-MiniLM-L6-v2
QA_MODEL=distilbert-base-uncased-distilled-squad
DEBUG=False
PORT=5000
```

## 📈 Performance Metrics

- **PDF Processing**: ~2-5 seconds for typical documents
- **Semantic Search**: <100ms for similarity calculation
- **QA Generation**: ~1-3 seconds per question
- **Memory Usage**: ~2-3GB with models loaded
- **Concurrent Users**: 5-10 on standard hardware

## 🔧 Troubleshooting

### Model Download Issues
```bash
# Pre-download models manually
python -m sentence_transformers.util download_all_models
```

### Memory Issues
- Reduce `CHUNK_SIZE` in configuration
- Use lighter models: `all-MiniLM-L6-v2` (recommended)
- Clear `uploads/` directory periodically

### PDF Upload Errors
- Ensure PDF is not corrupted
- Check file size (tested up to 50MB)
- Try converting to standard PDF format

### Slow Response Times
- Check available system RAM
- Reduce `TOP_K_RETRIEVAL` value
- Use CPU-optimized models

## 📦 Dependencies

See `requirements.txt` for complete list:
- Flask 2.3.3+
- sentence-transformers
- transformers
- torch
- PyPDF2
- numpy

## 🔐 Privacy & Security

✅ **No cloud storage** - All PDFs processed locally
✅ **No data transmission** - Everything stays on your machine
✅ **No tracking** - Complete privacy
✅ **Open source** - Audit the code yourself

## 🚀 Deployment

### Deploy to Heroku

1. Add `Procfile`:
   ```
   web: python app.py
   ```

2. Push to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy to AWS/Google Cloud
- Use Docker container (create Dockerfile)
- Configure environment variables
- Set up persistent storage for uploads

## 📚 Learning Resources

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [RAG Explained](https://www.promptingguide.ai/techniques/rag)
- [BERT QA Fine-tuning](https://huggingface.co/docs/transformers/tasks/question_answering)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Support for other document formats (Word, PowerPoint)
- Multi-document Q&A
- Fine-tuned models for domain-specific queries
- Caching and optimization
- UI/UX enhancements

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by **Aerocodex777**

For questions or suggestions, open an issue on GitHub!

---

**Repository**: [https://github.com/Aerocodex777/pdfreader](https://github.com/Aerocodex777/pdfreader)

**Key Features Summary:**
- 🔍 Semantic search with AI understanding
- 💬 Natural language questions and answers
- 📄 Multi-page PDF support
- 🧠 Machine learning powered
- 🎯 Accurate information extraction
- 🚀 Fast and efficient processing
