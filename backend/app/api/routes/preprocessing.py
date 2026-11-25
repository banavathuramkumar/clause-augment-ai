from fastapi import APIRouter, HTTPException
from app.core.schemas import PreprocessingRequest, PreprocessingResponse
from app.services.preprocessing_service import PreprocessingService

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

@router.post("/run", response_model=PreprocessingResponse)
def run_preprocessing(request: PreprocessingRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    return PreprocessingService.process_clause(request)
