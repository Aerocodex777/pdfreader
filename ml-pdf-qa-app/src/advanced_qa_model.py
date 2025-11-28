"""
Advanced QA Model using Semantic Search and Retrieval-Augmented Generation
This model provides more descriptive and accurate answers by finding relevant
passages using semantic similarity rather than just keyword matching.
"""

from sentence_transformers import SentenceTransformer, util
import torch
import re

class AdvancedQAModel:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.sentence_model = None
        self.document_embeddings = None
        self.document_chunks = []
        self.loaded = False

    def load_model(self):
        """Load the sentence transformer model for semantic search"""
        try:
            # Using a lightweight but effective model
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Semantic Search Model loaded successfully!")
            self.loaded = True
            return True
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            self.loaded = False
            return False

    def chunk_document(self, text, chunk_size=200, overlap=50):
        """
        Split document into overlapping chunks for better context preservation
        chunk_size: approximate number of words per chunk
        overlap: number of overlapping words between chunks
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            words = sentence.split()
            current_size += len(words)
            current_chunk.append(sentence)
            
            if current_size >= chunk_size:
                # Join chunk and save
                chunk_text = ' '.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)
                
                # Keep overlap - remove oldest sentences but keep recent ones
                overlap_size = 0
                new_chunk = []
                for sent in reversed(current_chunk):
                    overlap_size += len(sent.split())
                    new_chunk.insert(0, sent)
                    if overlap_size >= overlap:
                        break
                
                current_chunk = new_chunk
                current_size = overlap_size
        
        # Add remaining text as final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk).strip()
            if chunk_text:
                chunks.append(chunk_text)
        
        return chunks

    def index_document(self, text):
        """
        Process and index the document for semantic search
        """
        if not self.loaded:
            return False
        
        try:
            # Clean the text
            text = text.strip()
            if not text:
                return False
            
            # Split into meaningful chunks
            self.document_chunks = self.chunk_document(text, chunk_size=300, overlap=100)
            
            if not self.document_chunks:
                print("Warning: No chunks created from document")
                return False
            
            print(f"📚 Document indexed into {len(self.document_chunks)} chunks")
            
            # Encode all chunks
            self.document_embeddings = self.sentence_model.encode(
                self.document_chunks,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False

    def find_relevant_chunks(self, question, top_k=5):
        """
        Find the most relevant chunks using semantic similarity
        """
        if not self.loaded or self.document_embeddings is None:
            return []
        
        try:
            # Encode the question
            question_embedding = self.sentence_model.encode(question, convert_to_tensor=True)
            
            # Find similar chunks
            cos_scores = util.pytorch_cos_sim(question_embedding, self.document_embeddings)[0]
            top_results = torch.topk(cos_scores, k=min(top_k, len(self.document_chunks)))
            
            relevant_chunks = []
            for score, idx in zip(top_results[0], top_results[1]):
                chunk = self.document_chunks[int(idx)]
                confidence = float(score)
                relevant_chunks.append({
                    'text': chunk,
                    'confidence': confidence
                })
            
            return relevant_chunks
        except Exception as e:
            print(f"Error finding relevant chunks: {e}")
            return []

    def answer_question(self, question, context):
        """
        Generate a comprehensive answer by combining relevant chunks
        """
        if not self.loaded:
            return "Error: Model not loaded. Please load the model first."
        
        if not question or not context:
            return "Error: Both question and context are required."
        
        try:
            # Index the document if not already done
            if not self.document_chunks:
                success = self.index_document(context)
                if not success:
                    return "Error: Could not process the PDF. Please try uploading again."
            
            # Find relevant chunks
            relevant_chunks = self.find_relevant_chunks(question, top_k=5)
            
            if not relevant_chunks:
                return f"I couldn't find any information in the PDF related to: '{question}'. Please try a different question."
            
            # Build a comprehensive answer from relevant chunks
            answer = self._build_answer(question, relevant_chunks)
            
            return answer
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"

    def _build_answer(self, question, relevant_chunks):
        """
        Build a comprehensive answer from relevant chunks
        """
        if not relevant_chunks:
            return "No relevant information found."
        
        # Check if all chunks have low confidence
        avg_confidence = sum(c['confidence'] for c in relevant_chunks) / len(relevant_chunks)
        
        if avg_confidence < 0.3:
            return f"Found some information but confidence is low. The PDF may not contain clear information about: '{question}'"
        
        # Combine top chunks
        combined_context = "\n".join([chunk['text'] for chunk in relevant_chunks[:3]])
        
        # Use the question-answering pipeline if available
        try:
            from transformers import pipeline
            qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=-1
            )
            
            # Try to get a specific answer
            result = qa_pipeline(
                question=question,
                context=combined_context,
                max_answer_len=300,
                min_answer_len=20
            )
            
            answer = result['answer'].strip()
            score = result['score']
            
            if score > 0.5:
                return f"**Answer:** {answer}\n\n**Confidence:** {score:.1%}"
            else:
                # Fallback to chunk summary
                return self._summarize_chunks(question, relevant_chunks)
                
        except Exception as e:
            # Fallback: return best matching chunk with context
            return self._summarize_chunks(question, relevant_chunks)

    def _summarize_chunks(self, question, relevant_chunks):
        """
        Summarize relevant chunks into a descriptive answer
        """
        best_chunk = relevant_chunks[0]
        text = best_chunk['text']
        confidence = best_chunk['confidence']
        
        # Enhance with additional context
        answer_parts = [
            f"**Based on the PDF:**",
            f"\n{text[:500]}..." if len(text) > 500 else f"\n{text}",
            f"\n\n**Relevance Score:** {confidence:.1%}"
        ]
        
        if len(relevant_chunks) > 1:
            additional_context = " ".join([c['text'][:200] for c in relevant_chunks[1:3]])
            if additional_context:
                answer_parts.append(f"\n\n**Additional Context:**\n{additional_context}...")
        
        return "".join(answer_parts)
