# Milestone 08: Milestone 1 - Architectural Foundation

## 1. Modular Directory Organization
The codebase adheres to a decoupled architecture separating presentation, API routing, domain services, ML pipelines, and algorithmic transformers:

- `backend/app/main.py`: Application entrypoint, CORS configuration, lifespan benchmark seeding, and router aggregation.
- `backend/app/config.py`: Centralized configuration managing environment variables, directories, thresholds, and keyword registries.
- `backend/app/core/`: Database engine (`database.py`), SQLAlchemy ORM entities (`models.py`), and Pydantic validation contracts (`schemas.py`).
- `backend/app/algorithms/`: Pure algorithmic implementations of text (EDA, sentence restructuring, Gemini) and tabular (SMOTE, noise, perturbation) transformers.
- `backend/app/services/`: Business logic bridging data persistence and machine learning orchestration (`dataset_service.py`, `preprocessing_service.py`, `augmentation_service.py`, `validation_service.py`, `training_service.py`).
- `backend/app/ml/`: Isolated machine learning experiment logic, custom feature transformers, classifiers, regressors, and evaluation metric calculators.
