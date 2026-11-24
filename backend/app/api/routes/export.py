import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.models import TrainingExperiment
from backend.app.services.export_service import export_service

router = APIRouter(prefix="/export", tags=["Exports"])

@router.get("/{export_type}")
def export_file(
    export_type: str,
    dataset_id: str = Query(None),
    experiment_id: str = Query(None),
    db: Session = Depends(get_db)
):
    try:
        if export_type == "original_csv":
            if not dataset_id:
                raise HTTPException(status_code=400, detail="dataset_id is required")
            path = export_service.export_clauses_csv(db, dataset_id, kind="original")
            return FileResponse(path, media_type="text/csv", filename=f"{dataset_id}_original_clauses.csv")

        elif export_type == "augmented_csv":
            if not dataset_id:
                raise HTTPException(status_code=400, detail="dataset_id is required")
            path = export_service.export_clauses_csv(db, dataset_id, kind="augmented")
            return FileResponse(path, media_type="text/csv", filename=f"{dataset_id}_augmented_clauses.csv")

        elif export_type == "accepted_csv":
            if not dataset_id:
                raise HTTPException(status_code=400, detail="dataset_id is required")
            path = export_service.export_clauses_csv(db, dataset_id, kind="accepted")
            return FileResponse(path, media_type="text/csv", filename=f"{dataset_id}_accepted_clauses.csv")

        elif export_type == "rejected_csv":
            if not dataset_id:
                raise HTTPException(status_code=400, detail="dataset_id is required")
            path = export_service.export_clauses_csv(db, dataset_id, kind="rejected")
            return FileResponse(path, media_type="text/csv", filename=f"{dataset_id}_rejected_clauses.csv")

        elif export_type == "dataset_json":
            if not dataset_id:
                raise HTTPException(status_code=400, detail="dataset_id is required")
            path = export_service.export_dataset_json(db, dataset_id)
            return FileResponse(path, media_type="application/json", filename=f"{dataset_id}_full_dataset.json")

        elif export_type == "evaluation_pdf":
            if not experiment_id:
                raise HTTPException(status_code=400, detail="experiment_id is required")
            path = export_service.generate_evaluation_report_pdf(db, experiment_id)
            return FileResponse(path, media_type="application/pdf", filename=f"{experiment_id}_evaluation_report.pdf")

        elif export_type == "classification_report_csv":
            if not experiment_id:
                raise HTTPException(status_code=400, detail="experiment_id is required")
            path = export_service.export_classification_report_csv(db, experiment_id)
            return FileResponse(path, media_type="text/csv", filename=f"{experiment_id}_classification_report.csv")

        elif export_type == "confusion_matrix_png":
            if not experiment_id:
                raise HTTPException(status_code=400, detail="experiment_id is required")
            path = export_service.generate_confusion_matrix_image(db, experiment_id)
            return FileResponse(path, media_type="image/png", filename=f"{experiment_id}_confusion_matrix.png")

        elif export_type == "trained_model":
            if not experiment_id:
                raise HTTPException(status_code=400, detail="experiment_id is required")
            exp = db.query(TrainingExperiment).filter(TrainingExperiment.id == experiment_id).first()
            if not exp or not exp.model_artifact_path or not os.path.exists(exp.model_artifact_path):
                raise HTTPException(status_code=404, detail="Model artifact file not found.")
            return FileResponse(
                exp.model_artifact_path,
                media_type="application/octet-stream",
                filename=os.path.basename(exp.model_artifact_path)
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported export type: {export_type}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
