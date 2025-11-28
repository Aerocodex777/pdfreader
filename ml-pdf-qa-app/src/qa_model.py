from transformers import pipeline
import re

class QAModel:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.qa_pipeline = None

    def load_model(self):
        """Load the pre-trained QA model from Hugging Face"""
        try:
            # Using distilbert-based QA model (lightweight and fast)
            self.qa_pipeline = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad",
                device=-1  # Use CPU (-1) or GPU (0) if available
            )
            print("✓ QA Model loaded successfully!")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False

    def find_relevant_passages(self, context, question, num_passages=3, passage_length=512):
        """
        Find the most relevant passages from context based on the question.
        Uses keyword matching and semantic similarity.
        """
        # Split context into sentences
        sentences = re.split(r'(?<=[.!?])\s+', context)
        
        # Filter out very short sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return context[:passage_length]
        
        # Extract keywords from question
        question_words = set(question.lower().split())
        # Remove common stop words
        stop_words = {'what', 'where', 'when', 'why', 'how', 'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'but', 'this', 'that', 'these', 'those', 'as', 'by'}
        question_words = question_words - stop_words
        
        # Score sentences based on keyword matches
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = sum(1 for word in question_words if word in sentence.lower())
            sentence_scores.append((i, sentence, score))
        
        # Sort by score (descending) and get top passages
        sentence_scores.sort(key=lambda x: x[2], reverse=True)
        top_sentences = sorted(sentence_scores[:num_passages], key=lambda x: x[0])  # Re-sort by original order
        
        # Combine top sentences into a passage
        passage = ' '.join([s[1] for s in top_sentences])
        
        # If passage is too long, truncate it
        if len(passage) > passage_length:
            passage = passage[:passage_length]
        
        # If no relevant passages found, use the first part of context
        if not passage.strip():
            passage = context[:passage_length]
        
        return passage

    def answer_question(self, question, context):
        """Generate an answer based on the question and the provided context"""
        if not self.qa_pipeline:
            return "Error: Model not loaded. Please load the model first."
        
        if not question or not context:
            return "Error: Both question and context are required."
        
        try:
            # Clean and validate context
            context = context.strip()
            if not context:
                return "Error: PDF content appears to be empty. Please upload a valid PDF."
            
            # Find relevant passages from the context
            relevant_passage = self.find_relevant_passages(context, question, num_passages=5, passage_length=512)
            
            if not relevant_passage or len(relevant_passage) < 20:
                return f"I could not find relevant information in the uploaded PDF to answer: '{question}'. Please try a different question or upload a different PDF."
            
            # Generate answer using the QA model
            result = self.qa_pipeline(
                question=question,
                context=relevant_passage,
                max_answer_len=150,
                min_answer_len=10
            )
            
            answer = result['answer'].strip()
            score = result['score']
            
            # Add confidence-based warnings
            if score < 0.3:
                confidence_note = "(Low confidence - this answer may not be accurate)"
                return f"Answer: {answer}\n\n{confidence_note}"
            elif score < 0.5:
                confidence_note = "(Medium confidence)"
                return f"Answer: {answer}\n{confidence_note} (Confidence: {score:.1%})"
            else:
                return f"Answer: {answer} (Confidence: {score:.1%})"
                
        except Exception as e:
            return f"Error generating answer: {str(e)}"
