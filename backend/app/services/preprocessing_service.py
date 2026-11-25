from backend.app.core.schemas import PreprocessingRequest, PreprocessingResponse
from backend.app.utils.text_cleaner import clean_legal_text

class PreprocessingService:
    @staticmethod
    def process_clause(request: PreprocessingRequest) -> PreprocessingResponse:
        original = request.text
        processed, tokens, sentences, operations = clean_legal_text(
            text=original,
            remove_stopwords=request.remove_stopwords,
            lemmatize=request.lemmatize,
            preserve_legal_terms=request.preserve_legal_terms
        )
        
        orig_words = len(original.split())
        proc_words = len(processed.split())
        
        return PreprocessingResponse(
            original_text=original,
            processed_text=processed,
            original_word_count=orig_words,
            processed_word_count=proc_words,
            token_count=len(tokens),
            tokens=tokens,
            sentences=sentences,
            operations_applied=operations
        )
